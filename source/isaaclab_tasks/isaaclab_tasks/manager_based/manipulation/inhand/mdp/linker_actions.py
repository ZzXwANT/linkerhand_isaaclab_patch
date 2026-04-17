from __future__ import annotations

from collections.abc import Sequence

import torch

from isaaclab.envs.mdp.actions import joint_actions_to_limits
from isaaclab.envs.mdp.actions.actions_cfg import EMAJointPositionToLimitsActionCfg
from isaaclab.managers.action_manager import ActionTerm
from isaaclab.utils import configclass

from .linker_mimic import LinkerMimicJointDriver, LinkerMimicRule

__all__ = [
    "LinkerMimicEMAJointPositionToLimitsAction",
    "LinkerMimicEMAJointPositionToLimitsActionCfg",
]


class LinkerMimicEMAJointPositionToLimitsAction(joint_actions_to_limits.EMAJointPositionToLimitsAction):
    """EMA joint action with LinkerHand-specific mimic joints resolved in software."""

    cfg: "LinkerMimicEMAJointPositionToLimitsActionCfg"

    def __init__(self, cfg: "LinkerMimicEMAJointPositionToLimitsActionCfg", env):
        super().__init__(cfg, env)
        self._mimic_driver = LinkerMimicJointDriver(self._joint_names, cfg.mimic_rules)

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        if env_ids is None:
            super().reset(slice(None))
            self._prev_applied_actions[:] = self._asset.data.joint_pos[:, self._joint_ids]
            return

        super().reset(env_ids)
        self._prev_applied_actions[env_ids, :] = self._asset.data.joint_pos[env_ids][:, self._joint_ids]

    def process_actions(self, actions: torch.Tensor):
        joint_actions_to_limits.JointPositionToLimitsAction.process_actions(self, actions)
        self._mimic_driver.apply(self._processed_actions)

        ema_actions = self._alpha * self._processed_actions
        ema_actions += (1.0 - self._alpha) * self._prev_applied_actions
        self._processed_actions[:] = torch.clamp(
            ema_actions,
            self._asset.data.soft_joint_pos_limits[:, self._joint_ids, 0],
            self._asset.data.soft_joint_pos_limits[:, self._joint_ids, 1],
        )
        self._prev_applied_actions[:] = self._processed_actions[:]


@configclass
class LinkerMimicEMAJointPositionToLimitsActionCfg(EMAJointPositionToLimitsActionCfg):
    """Configuration for LinkerHand EMA joint action with software-side mimic rules."""

    class_type: type[ActionTerm] = LinkerMimicEMAJointPositionToLimitsAction
    mimic_rules: tuple[LinkerMimicRule, ...] = ()

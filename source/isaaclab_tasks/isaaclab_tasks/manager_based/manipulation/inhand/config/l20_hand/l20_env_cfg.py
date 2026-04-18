# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.noise import AdditiveGaussianNoiseCfg as Gnoise
from isaaclab.assets import RigidObjectCfg
import isaaclab.sim as sim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

import isaaclab_tasks.manager_based.manipulation.inhand.inhand_env_cfg as inhand_env_cfg
import isaaclab_tasks.manager_based.manipulation.inhand.mdp as mdp

##
# Pre-defined configs
##
from isaaclab_assets.robots.linker import L20_CFG

# Documented active joints for the L20 asset. The task still drives the full joint
# vector so the mimic targets stay addressable and can be overwritten in software.
L20_ACTIVE_JOINTS = [
    "thumb_cmc_yaw", "thumb_cmc_roll", "thumb_cmc_pitch", "thumb_mcp",
    "index_mcp_roll", "index_mcp_pitch", "index_pip",
    "middle_mcp_roll", "middle_mcp_pitch", "middle_pip",
    "ring_mcp_roll", "ring_mcp_pitch", "ring_pip",
    "pinky_mcp_roll", "pinky_mcp_pitch", "pinky_pip",
]

L20_MIMIC_RULES = (
    ("pinky_dip", "pinky_pip", 0.8917),
    ("ring_dip", "ring_pip", 0.8917),
    ("middle_dip", "middle_pip", 0.8917),
    ("index_dip", "index_pip", 0.8917),
    ("thumb_dip", "thumb_mcp", 1.1619),
)


@configclass
class L20KinematicObsGroupCfg(ObsGroup):
    """Observations for the L20 in-hand task."""

    # observation terms
    # -- robot terms
    joint_pos = ObsTerm(func=mdp.joint_pos_limit_normalized, noise=Gnoise(std=0.005))
    joint_vel = ObsTerm(func=mdp.joint_vel_rel, scale=0.2, noise=Gnoise(std=0.01))

    # -- object terms
    object_pos = ObsTerm(
        func=mdp.root_pos_w, noise=Gnoise(std=0.002), params={"asset_cfg": SceneEntityCfg("object")}
    )
    object_quat = ObsTerm(
        func=mdp.root_quat_w, params={"asset_cfg": SceneEntityCfg("object"), "make_quat_unique": False}
    )
    object_lin_vel = ObsTerm(
        func=mdp.root_lin_vel_w, noise=Gnoise(std=0.002), params={"asset_cfg": SceneEntityCfg("object")}
    )
    object_ang_vel = ObsTerm(
        func=mdp.root_ang_vel_w,
        scale=0.2,
        noise=Gnoise(std=0.002),
        params={"asset_cfg": SceneEntityCfg("object")},
    )

    # -- command terms
    goal_pose = ObsTerm(func=mdp.generated_commands, params={"command_name": "object_pose"})
    goal_quat_diff = ObsTerm(
        func=mdp.goal_quat_diff,
        params={"asset_cfg": SceneEntityCfg("object"), "command_name": "object_pose", "make_quat_unique": False},
    )

    # -- action terms
    last_action = ObsTerm(func=mdp.last_action)

    def __post_init__(self):
        self.enable_corruption = True
        self.concatenate_terms = True


@configclass
class L20ActionsCfg:
    # 新的mimic处理
    joint_pos = mdp.LinkerMimicEMAJointPositionToLimitsActionCfg(
        asset_name="robot",
        joint_names=[".*"],
        alpha=0.95,
        rescale_to_limits=True,
        mimic_rules=L20_MIMIC_RULES,
    )


@configclass
class L20CubeEnvCfg(inhand_env_cfg.InHandObjectEnvCfg):
    def __post_init__(self):
        # Override observations and actions BEFORE calling parent __post_init__
        self.observations.policy = L20KinematicObsGroupCfg()
        self.actions = L20ActionsCfg()
        
        # post init of parent
        super().__post_init__()

        # switch robot to L20 hand
        self.scene.robot = L20_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # Keep the currently working training setup for the mimic-enabled L20 asset.
        self.scene.clone_in_fabric = False
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/object",
            spawn=sim_utils.UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/DexCube/dex_cube_instanceable.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=sim_utils.RigidBodyPropertiesCfg(
                    kinematic_enabled=False,
                    disable_gravity=False,
                    enable_gyroscopic_forces=True,
                    solver_position_iteration_count=8,
                    solver_velocity_iteration_count=0,
                    sleep_threshold=0.005,
                    stabilization_threshold=0.0025,
                    max_depenetration_velocity=1000.0,
                ),
                mass_props=sim_utils.MassPropertiesCfg(density=200.0),
            ),
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=(0.0, -0.25, 0.55), rot=(1.0, 0.0, 0.0, 0.0)
            ),
        )

@configclass
class L20CubeEnvCfg_PLAY(L20CubeEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove termination due to timeouts
        self.terminations.time_out = None

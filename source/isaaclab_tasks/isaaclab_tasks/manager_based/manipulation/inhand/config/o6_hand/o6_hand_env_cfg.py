# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.manipulation.inhand.inhand_env_cfg as inhand_env_cfg

##
# Pre-defined configs
##
from isaaclab_assets.robots.linker import O6_HAND_CFG  # isort: skip


@configclass
class O6HandCubeEnvCfg(inhand_env_cfg.InHandObjectEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # switch robot to O6 hand
        self.scene.robot = O6_HAND_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # enable clone in fabric
        self.scene.clone_in_fabric = True


@configclass
class O6HandCubeEnvCfg_PLAY(O6HandCubeEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove termination due to timeouts
        self.terminations.time_out = None

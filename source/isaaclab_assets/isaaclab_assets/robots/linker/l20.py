# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration for the LinkerHand L20 dexterous hand.

The following configurations are available:

* :obj:`L20_CFG`: L20 hand with implicit actuator model.

Reference:

* https://www.linkerhand.com/

"""

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators.actuator_cfg import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

##
# Configuration
##

_ASSET_DIR = Path(__file__).resolve().parent

L20_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=str(_ASSET_DIR / "l20_right.usd"),
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            retain_accelerations=False,
            enable_gyroscopic_forces=False,
            angular_damping=0.01,
            max_linear_velocity=1000.0,
            max_angular_velocity=64 / 3.14159 * 180.0,
            max_depenetration_velocity=1000.0,
            max_contact_impulse=1e32,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
            sleep_threshold=0.005,
            stabilization_threshold=0.0005,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, -0.1, 0.5),
        rot=(0.5, 0.5, -0.5, 0.5),
        joint_pos={
            "thumb_cmc_yaw": 0.8,    # 往内收（靠近 cube）
            "thumb_cmc_roll": 1.0,  # 关键：翻到上面
            "thumb_cmc_pitch": 0.3,  # 向下压
            "thumb_mcp": 0.6,        # 弯曲，形成接触面
            "index_mcp_roll": 0.1,
            "index_mcp_pitch": 0.6,
            "index_pip": 0.6,
            "middle_mcp_roll": 0.1,
            "middle_mcp_pitch": 0.6,
            "middle_pip": 0.6,
            "ring_mcp_roll": 0.1,
            "ring_mcp_pitch": 0.6,
            "ring_pip": 0.6,
            "pinky_mcp_roll": 0.1,
            "pinky_mcp_pitch": 0.6,
            "pinky_pip": 0.6,
        },
    ),
    actuators={
        "fingers": ImplicitActuatorCfg(
            joint_names_expr=[".*"],
            effort_limit_sim=50.0,
            stiffness=400.0,
            damping=10.0,
            friction=0.1,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of LinkerHand L20 robot."""

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators.actuator_cfg import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

_ASSET_DIR = Path(__file__).resolve().parent

O6_HAND_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=str(_ASSET_DIR / "o6_hand.usd"),
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.5),
        joint_pos={
            "thumb_cmc_yaw": 0.0,
            "thumb_cmc_pitch": 0.0,
            "thumb_ip": 0.0,
            "index_mcp_pitch": 0.0,
            "middle_mcp_pitch": 0.0,
            "ring_mcp_pitch": 0.0,
            "pinky_mcp_pitch": 0.0,
            "index_dip": 0.0,
            "middle_dip": 0.0,
            "ring_dip": 0.0,
            "pinky_dip": 0.0,
        },
    ),
    actuators={
        "fingers": ImplicitActuatorCfg(
            joint_names_expr=["thumb_cmc_yaw", "thumb_cmc_pitch", "thumb_ip", "index_mcp_pitch", "middle_mcp_pitch", "ring_mcp_pitch", "pinky_mcp_pitch", "index_dip", "middle_dip", "ring_dip", "pinky_dip"],
            effort_limit=1.0,
            velocity_limit=200.0,
            stiffness=3.0,
            damping=0.1,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)

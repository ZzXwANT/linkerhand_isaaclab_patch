# LinkerHand IsaacLab In-Hand Patch Bundle

这份目录是把 LinkerHand 适配 IsaacLab `inhand` 任务时整理出来的补丁快照，不是完整 IsaacLab 仓库。

## 目录映射

将本目录下的 `source/` 内容按相对路径覆盖到完整 IsaacLab 仓库：

- `source/isaaclab_assets` -> `<IsaacLab>/source/isaaclab_assets`
- `source/isaaclab_tasks` -> `<IsaacLab>/source/isaaclab_tasks`

这次整理后的关键新增/调整点：

- `isaaclab_assets/isaaclab_assets/robots/linker/`
  - 统一维护 `L20_CFG`、`L20LITE_CFG`、`O6_HAND_CFG`
  - 三个机器人配置都改为仓库内相对 USD 路径
- `isaaclab_tasks/.../inhand/mdp/`
  - 新增 `linker_actions.py`
  - 新增 `linker_mimic.py`
  - `L20` 的 mimic 驱动现在放在任务侧，不再依赖额外的 IsaacLab core 补丁文件
- `isaaclab_tasks/.../inhand/config/o6_hand/`
  - 补齐 `__init__.py`
  - 补齐 `agents/__init__.py`
  - 修正 `O6` 的 task / agent / experiment 命名

## 资产放置规则

LinkerHand 资产目录固定为：

`<IsaacLab>/source/isaaclab_assets/isaaclab_assets/robots/linker/`

需要存在以下 USD 文件（通过isaaclab ignore mimic导入，Save as Flattened USD转为USD）：

- `l20_right.usd`
- `l20lite_no_mimic.usd`
- `o6_hand.usd`

当前这份快照里没有附带实际 USD 文件；如果你打包发布这套补丁，需要把这三份 USD 一起放到上面这个目录。

## 可用任务

保留原有命名：

- `Isaac-Repose-Cube-L20-v0`
- `Isaac-Repose-Cube-L20-Play-v0`
- `Isaac-Repose-Cube-L20Lite-v0`
- `Isaac-Repose-Cube-L20Lite-Play-v0`

本次补齐：

- `Isaac-Repose-Cube-O6-v0`
- `Isaac-Repose-Cube-O6-Play-v0`

## 训练与播放

建议使用 IsaacLab 官方 RSL-RL 入口，而不是本目录里的临时脚本。

训练示例：

```bash
./isaaclab.sh -p source/standalone/workflows/rsl_rl/train.py --task Isaac-Repose-Cube-L20-v0
./isaaclab.sh -p source/standalone/workflows/rsl_rl/train.py --task Isaac-Repose-Cube-L20Lite-v0
./isaaclab.sh -p source/standalone/workflows/rsl_rl/train.py --task Isaac-Repose-Cube-O6-v0
```

播放示例：

```bash
./isaaclab.sh -p source/standalone/workflows/rsl_rl/play.py --task Isaac-Repose-Cube-L20-Play-v0 --checkpoint <checkpoint_path>
./isaaclab.sh -p source/standalone/workflows/rsl_rl/play.py --task Isaac-Repose-Cube-L20Lite-Play-v0 --checkpoint <checkpoint_path>
./isaaclab.sh -p source/standalone/workflows/rsl_rl/play.py --task Isaac-Repose-Cube-O6-Play-v0 --checkpoint <checkpoint_path>
```

如果你在 Windows 环境运行完整 IsaacLab，把 `./isaaclab.sh` 替换为 `isaaclab.bat`。

## 当前状态

- `L20`
  - 已按当前实验参数保留
  - 使用任务侧 `LinkerMimicEMAJointPositionToLimitsActionCfg`
  - 你已有结论是放入完整 IsaacLab 后可以训练
- `L20Lite`
  - 已整理为显式 active joints 驱动
  - 保留当前实验参数与物块参数
  - 仍需要在完整 IsaacLab 中重新做 smoke test
- `O6`
  - 已补齐任务注册和 agent 命名
  - 仍需要在完整 IsaacLab 中重新做 smoke test

## 额外说明

- 原来放在 `source/isaaclab/` 下的 mimic/core patch 试验文件已经删除，避免和正式补丁混淆。
- `scrpts/` 目录保留为临时材料，不作为权威入口。
- 纯规则层的最小测试放在 `tests/test_linker_mimic.py`，用于验证 mimic 映射逻辑本身。

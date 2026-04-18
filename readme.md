# LinkerHand IsaacLab Patch

LinkerHand 在 IsaacLab 中的任务适配补丁仓库，当前聚焦 `manager_based/manipulation/inhand` 任务，覆盖 `L20`、`L20Lite`、`O6` 三套手型。

项目目标不是提供完整 IsaacLab 分叉，而是沉淀一组可复制到主 IsaacLab 工程中的资产配置、任务配置和手型专用驱动逻辑。

详细改动记录见 [CHANGELOG.md](CHANGELOG.md)。

## 项目内容

- LinkerHand 机器人配置导出
- `inhand` 任务下的 `L20` / `L20Lite` / `O6` 适配配置
- `L20` 所需的软件侧 mimic 动作层
- 最小规则测试与补丁说明

## 演示位置

### Demo Slot 1

> 在这里插入第一个 GIF 或视频，建议展示 `L20` 训练或 play 效果。

<!-- media-slot-1 -->
<!-- 示例：![L20 Demo](docs/media/l20_demo.gif) -->
<!-- 或者：<video src="docs/media/l20_demo.mp4" controls muted loop></video> -->

### Demo Slot 2

> 在这里插入第二个 GIF 或视频，建议展示 `L20Lite`、`O6` 或资产效果。

<!-- media-slot-2 -->
<!-- 示例：![O6 Demo](docs/media/o6_demo.gif) -->
<!-- 或者：<video src="docs/media/o6_demo.mp4" controls muted loop></video> -->

## 目录结构

- `source/isaaclab_assets`
  - LinkerHand 机器人配置与资产入口
- `source/isaaclab_tasks`
  - `inhand` 任务配置、注册入口和 Linker 专用动作层
- `tests`
  - 轻量规则测试
- `scrpts`
  - 当前保留的临时脚本材料，不作为长期权威入口

## 如何使用

将本仓库的 `source/` 内容按相对路径覆盖到完整 IsaacLab 仓库：

- `source/isaaclab_assets` -> `<IsaacLab>/source/isaaclab_assets`
- `source/isaaclab_tasks` -> `<IsaacLab>/source/isaaclab_tasks`

LinkerHand 资产目录固定为：

`<IsaacLab>/source/isaaclab_assets/isaaclab_assets/robots/linker/`

需要存在以下 USD 文件：

- `l20_right.usd`
- `l20lite_no_mimic.usd`
- `o6_hand.usd`

当前仓库不包含这三份 USD，本仓库只保存代码侧补丁。

## 任务列表

- `Isaac-Repose-Cube-L20-v0`
- `Isaac-Repose-Cube-L20-Play-v0`
- `Isaac-Repose-Cube-L20Lite-v0`
- `Isaac-Repose-Cube-L20Lite-Play-v0`
- `Isaac-Repose-Cube-O6-v0`
- `Isaac-Repose-Cube-O6-Play-v0`

## 训练与播放

建议直接使用 IsaacLab 官方 RSL-RL 入口。

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

Windows 环境下把 `./isaaclab.sh` 替换为 `isaaclab.bat`。

## 当前状态

- `L20`
  - 已保留当前实验参数
  - 使用任务侧 `LinkerMimicEMAJointPositionToLimitsActionCfg`
  - 已知放入完整 IsaacLab 后可训练
- `L20Lite`
  - 已整理为显式 active joints 驱动
  - 仍需要在完整 IsaacLab 中重新 smoke-test
- `O6`
  - 已补齐任务注册和 agent 命名
  - 仍需要在完整 IsaacLab 中重新 smoke-test

## 说明

- 旧的 `source/isaaclab/` mimic/core patch 试验文件已经移除
- LinkerHand 专用 mimic 逻辑现在位于任务侧
- 最小规则测试位于 `tests/test_linker_mimic.py`

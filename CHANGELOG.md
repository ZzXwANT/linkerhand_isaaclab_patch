# Changelog

## 2026-04-18

### Added

- 新增 LinkerHand 任务侧 mimic 适配层：
  - `linker_actions.py`
  - `linker_mimic.py`
- 新增 `O6` 的任务注册入口与 `agents/__init__.py`
- 新增 `tests/test_linker_mimic.py`
- 新增独立 `CHANGELOG.md`

### Changed

- 将 `L20` 的 mimic 处理从散落的 IsaacLab core patch 文件迁移到任务侧共享动作层
- 统一 `isaaclab_assets.robots.linker` 的导出接口，明确导出：
  - `L20_CFG`
  - `L20LITE_CFG`
  - `O6_HAND_CFG`
- 将 `L20`、`L20Lite`、`O6` 的 USD 路径统一改为仓库内相对路径
- 保留 `L20` 和 `L20Lite` 当前实验参数，并整理 `inhand` 下的配置结构
- 补齐 `inhand` 与 `config` 的导入链，确保任务注册能自动触发

### Removed

- 删除旧的试验性 core patch 文件：

  - `source/isaaclab/joint_actions_to_limits.py`
  - `source/isaaclab/joint_actions_to_limits_mimic.py`
  - `source/isaaclab/l20_mimic_driver.py`

### Notes

- 当前仓库仍不包含实际 USD 资产，只保存代码侧补丁
- `L20` 已知可训练，`L20Lite` 与 `O6` 仍需在完整 IsaacLab 中重新 smoke-test

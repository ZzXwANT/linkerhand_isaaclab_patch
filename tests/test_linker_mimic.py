from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HAS_TORCH = importlib.util.find_spec("torch") is not None

def _load_linker_mimic_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "source"
        / "isaaclab_tasks"
        / "isaaclab_tasks"
        / "manager_based"
        / "manipulation"
        / "inhand"
        / "mdp"
        / "linker_mimic.py"
    )
    spec = importlib.util.spec_from_file_location("linker_mimic", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(_HAS_TORCH, "torch is required to run the mimic tensor test")
class LinkerMimicJointDriverTest(unittest.TestCase):
    def test_mimic_joints_follow_driver_joints(self):
        import torch

        module = _load_linker_mimic_module()
        driver = module.LinkerMimicJointDriver(
            joint_names=("thumb_mcp", "thumb_dip", "index_pip", "index_dip"),
            rules=(
                ("thumb_dip", "thumb_mcp", 1.1619),
                ("index_dip", "index_pip", 0.8917),
            ),
        )
        actions = torch.tensor([[0.25, 0.0, -0.5, 0.0]], dtype=torch.float32)

        driver.apply(actions)

        self.assertAlmostEqual(actions[0, 1].item(), 0.25 * 1.1619, places=6)
        self.assertAlmostEqual(actions[0, 3].item(), -0.5 * 0.8917, places=6)


if __name__ == "__main__":
    unittest.main()

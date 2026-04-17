from __future__ import annotations

from collections.abc import Sequence

import torch

LinkerMimicRule = tuple[str, str, float]

__all__ = ["LinkerMimicJointDriver", "LinkerMimicRule"]


class LinkerMimicJointDriver:
    """Applies software-side mimic relationships on a joint command tensor."""

    def __init__(self, joint_names: Sequence[str], rules: Sequence[LinkerMimicRule]):
        self._joint_names = tuple(joint_names)
        self._joint_name_to_index = {name: index for index, name in enumerate(self._joint_names)}
        self._rules = self._resolve_rules(rules)

    @property
    def rules(self) -> tuple[tuple[int, int, float], ...]:
        return self._rules

    def apply(self, actions: torch.Tensor) -> torch.Tensor:
        for mimic_index, driver_index, multiplier in self._rules:
            actions[:, mimic_index] = actions[:, driver_index] * multiplier
        return actions

    def _resolve_rules(self, rules: Sequence[LinkerMimicRule]) -> tuple[tuple[int, int, float], ...]:
        resolved_rules: list[tuple[int, int, float]] = []
        for mimic_name, driver_name, multiplier in rules:
            missing_names = [
                joint_name
                for joint_name in (mimic_name, driver_name)
                if joint_name not in self._joint_name_to_index
            ]
            if missing_names:
                raise ValueError(
                    "Mimic rule references joints that are not part of the action term: "
                    f"{missing_names}. Available joints: {self._joint_names}."
                )
            resolved_rules.append(
                (
                    self._joint_name_to_index[mimic_name],
                    self._joint_name_to_index[driver_name],
                    float(multiplier),
                )
            )
        return tuple(resolved_rules)

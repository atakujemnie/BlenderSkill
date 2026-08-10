from __future__ import annotations

"""Canonical component placement normalization for asset-local execution."""

from math import isfinite
from typing import Any, Mapping

EXECUTOR_ID = "COMPONENT_TRANSFORM"
EXECUTOR_VERSION = "0.21.0"


def _number(value: Any, *, field: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field}_NUMBER_REQUIRED") from exc
    if not isfinite(out):
        raise ValueError(f"{field}_FINITE_REQUIRED")
    return out


def _vec3(value: Any, *, field: str, default: tuple[float, float, float]) -> list[float]:
    if value is None:
        return list(default)
    if isinstance(value, Mapping):
        return [
            _number(value.get("x", default[0]), field=f"{field}_X"),
            _number(value.get("y", default[1]), field=f"{field}_Y"),
            _number(value.get("z", default[2]), field=f"{field}_Z"),
        ]
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{field}_VEC3_REQUIRED")
    return [_number(item, field=field) for item in value]


def normalize(component: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve legacy placement fields into one explicit transform record."""
    blockers: list[dict[str, Any]] = []
    source = "IMPLICIT_ORIGIN"
    explicit = False
    transform = component.get("transform")
    try:
        if isinstance(transform, Mapping):
            location = _vec3(transform.get("location_mm"), field="LOCATION_MM", default=(0.0, 0.0, 0.0))
            rotation = _vec3(transform.get("rotation_deg"), field="ROTATION_DEG", default=(0.0, 0.0, 0.0))
            scale = _vec3(transform.get("scale"), field="SCALE", default=(1.0, 1.0, 1.0))
            coordinate_space = str(transform.get("coordinate_space") or "ASSET_LOCAL").upper()
            source = "TRANSFORM"
            explicit = True
        elif component.get("location_mm") is not None:
            location = _vec3(component.get("location_mm"), field="LOCATION_MM", default=(0.0, 0.0, 0.0))
            rotation = _vec3(component.get("rotation_deg"), field="ROTATION_DEG", default=(0.0, 0.0, 0.0))
            scale = [1.0, 1.0, 1.0]
            coordinate_space = "ASSET_LOCAL"
            source = "LEGACY_LOCATION_MM"
            explicit = True
        elif isinstance(component.get("center_offset"), Mapping):
            offset = component["center_offset"]
            location = _vec3(offset, field="CENTER_OFFSET", default=(0.0, 0.0, 0.0))
            rotation = [0.0, 0.0, 0.0]
            scale = [1.0, 1.0, 1.0]
            coordinate_space = "ASSET_LOCAL"
            source = "LEGACY_CENTER_OFFSET"
            explicit = True
        else:
            location = [0.0, 0.0, 0.0]
            rotation = [0.0, 0.0, 0.0]
            scale = [1.0, 1.0, 1.0]
            coordinate_space = "ASSET_LOCAL"
    except ValueError as exc:
        blockers.append({"reason": str(exc)})
        location = [0.0, 0.0, 0.0]
        rotation = [0.0, 0.0, 0.0]
        scale = [1.0, 1.0, 1.0]
        coordinate_space = "ASSET_LOCAL"

    if coordinate_space not in {"ASSET_LOCAL", "PARENT_LOCAL"}:
        blockers.append({"reason": "COMPONENT_COORDINATE_SPACE_INVALID", "actual": coordinate_space})
    if any(value == 0.0 for value in scale):
        blockers.append({"reason": "COMPONENT_SCALE_ZERO_FORBIDDEN"})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "executor_id": EXECUTOR_ID,
        "transform": {
            "location_mm": location,
            "rotation_deg": rotation,
            "scale": scale,
            "coordinate_space": coordinate_space,
            "explicit": explicit,
            "source": source,
        },
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "normalize"]

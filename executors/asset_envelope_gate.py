from __future__ import annotations

"""Validate component placement, extents and declared seams against the asset envelope."""

from math import isfinite
from typing import Any, Mapping

from executors.component_transform import normalize as normalize_transform
from executors.parameter_graph import resolve as resolve_parameters

EXECUTOR_ID = "ASSET_ENVELOPE_GATE"
EXECUTOR_VERSION = "0.21.0"


def _value(record: Any) -> float | None:
    if isinstance(record, Mapping):
        raw = record.get("value")
    else:
        raw = record
    if raw is None:
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if isfinite(value) else None


def _root(components: Mapping[str, Mapping[str, Any]]) -> tuple[str | None, Mapping[str, Any] | None]:
    roots = [(str(component_id), component) for component_id, component in components.items() if not component.get("parent")]
    if len(roots) != 1:
        return None, None
    return roots[0]


def _resolved_dimension(resolved: Mapping[str, Any], component_id: str, names: tuple[str, ...]) -> float | None:
    component = resolved.get(component_id, {})
    if not isinstance(component, Mapping):
        return None
    for name in names:
        raw = component.get(name)
        if isinstance(raw, Mapping) and raw.get("value") is not None:
            return _value(raw)
    return None


def _extent(resolved: Mapping[str, Any], component_id: str) -> tuple[float | None, float | None, float | None]:
    width = _resolved_dimension(resolved, component_id, ("width", "x"))
    depth = _resolved_dimension(resolved, component_id, ("depth", "band_depth", "profile_depth", "channel_depth_y", "y"))
    height = _resolved_dimension(resolved, component_id, ("height", "thickness", "profile_height", "recess_height", "z"))
    return width, depth, height


def validate(asset: Mapping[str, Any]) -> dict[str, Any]:
    components_raw = asset.get("components", {})
    if not isinstance(components_raw, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "COMPONENTS_MAPPING_REQUIRED"}],
        }
    components = {str(key): dict(value) for key, value in components_raw.items() if isinstance(value, Mapping)}
    root_id, root_component = _root(components)
    if root_id is None or root_component is None:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "EXACTLY_ONE_COMPONENT_ROOT_REQUIRED"}],
        }

    parameters = resolve_parameters({"components": components})
    if parameters.get("status") != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": list(parameters.get("blockers", [])),
        }
    resolved = parameters["resolved"]
    root_width, root_depth, root_height = _extent(resolved, root_id)
    if root_width is None or root_depth is None or root_height is None:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ROOT_ENVELOPE_DIMENSIONS_REQUIRED", "component_id": root_id}],
        }

    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    aabbs: dict[str, dict[str, list[float]]] = {}
    for component_id, component in components.items():
        transform = normalize_transform(component)
        if transform["status"] != "PASS":
            blockers.extend({"component_id": component_id, **item} for item in transform["blockers"])
            continue
        location = transform["transform"]["location_mm"]
        width, depth, height = _extent(resolved, component_id)
        if component_id == root_id:
            width, depth, height = root_width, root_depth, root_height
        if width is None or depth is None or height is None:
            warnings.append({"reason": "COMPONENT_EXTENT_NOT_FULLY_RESOLVED", "component_id": component_id})
            continue
        half = [width / 2.0, depth / 2.0, height / 2.0]
        minimum = [location[0] - half[0], location[1] - half[1], location[2]]
        maximum = [location[0] + half[0], location[1] + half[1], location[2] + height]
        aabbs[component_id] = {"min": minimum, "max": maximum}
        if component_id == root_id or bool(component.get("allow_outside_envelope", False)):
            continue
        tolerance = float(component.get("envelope_tolerance_mm", asset.get("envelope_tolerance_mm", 0.5)))
        if minimum[0] < -root_width / 2.0 - tolerance or maximum[0] > root_width / 2.0 + tolerance:
            blockers.append({"reason": "COMPONENT_OUTSIDE_ASSET_ENVELOPE_X", "component_id": component_id, "aabb": aabbs[component_id]})
        if minimum[1] < -root_depth / 2.0 - tolerance or maximum[1] > root_depth / 2.0 + tolerance:
            blockers.append({"reason": "COMPONENT_OUTSIDE_ASSET_ENVELOPE_Y", "component_id": component_id, "aabb": aabbs[component_id]})
        if minimum[2] < -tolerance or maximum[2] > root_height + tolerance:
            blockers.append({"reason": "COMPONENT_OUTSIDE_ASSET_ENVELOPE_Z", "component_id": component_id, "aabb": aabbs[component_id]})

    for raw in list(asset.get("seam_constraints", []) or []):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "SEAM_CONSTRAINT_INVALID"})
            continue
        a = str(raw.get("a") or "")
        b = str(raw.get("b") or "")
        axis = str(raw.get("axis") or "X").upper()
        expected = float(raw.get("expected_gap_mm", 0.0))
        tolerance = float(raw.get("tolerance_mm", 0.5))
        if a not in aabbs or b not in aabbs or axis not in {"X", "Y", "Z"}:
            blockers.append({"reason": "SEAM_CONSTRAINT_UNRESOLVED", "a": a, "b": b, "axis": axis})
            continue
        index = {"X": 0, "Y": 1, "Z": 2}[axis]
        first, second = aabbs[a], aabbs[b]
        gap_ab = second["min"][index] - first["max"][index]
        gap_ba = first["min"][index] - second["max"][index]
        measured = max(gap_ab, gap_ba)
        if abs(measured - expected) > tolerance:
            blockers.append(
                {
                    "reason": "SEAM_GAP_MISMATCH",
                    "a": a,
                    "b": b,
                    "axis": axis,
                    "expected_gap_mm": expected,
                    "measured_gap_mm": round(measured, 6),
                    "tolerance_mm": tolerance,
                }
            )

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "asset_id": asset.get("asset_id"),
        "root_component_id": root_id,
        "root_envelope_mm": [root_width, root_depth, root_height],
        "aabbs": aabbs,
        "blockers": blockers,
        "warnings": warnings,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "validate"]

from __future__ import annotations

"""Deterministic validation of one component against a compact scene snapshot."""

from math import isfinite
from typing import Any, Mapping

EXECUTOR_ID = "SCENE_COMPONENT_VALIDATION"
EXECUTOR_VERSION = "0.21.0"


def _vec3(value: Any) -> list[float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        return None
    try:
        values = [float(item) for item in value]
    except (TypeError, ValueError):
        return None
    return values if all(isfinite(item) for item in values) else None


def _location(record: Mapping[str, Any]) -> list[float] | None:
    transform = record.get("transform")
    if not isinstance(transform, Mapping):
        return None
    return _vec3(transform.get("location_mm"))


def _resolved_value(parameters: Mapping[str, Any], names: tuple[str, ...]) -> float | None:
    for name in names:
        raw = parameters.get(name)
        if isinstance(raw, Mapping) and raw.get("value") is not None:
            try:
                return float(raw["value"])
            except (TypeError, ValueError):
                return None
        if isinstance(raw, (int, float)):
            return float(raw)
    return None


def validate(task_pack: Mapping[str, Any], snapshot: Mapping[str, Any]) -> dict[str, Any]:
    component_id = str(task_pack.get("component_id") or "")
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if str(snapshot.get("asset_id") or "") != str(task_pack.get("asset_id") or ""):
        blockers.append({"reason": "SCENE_ASSET_MISMATCH"})
    if int(snapshot.get("asset_revision") or 0) != int(task_pack.get("asset_revision") or 0):
        blockers.append(
            {
                "reason": "SCENE_ASSET_REVISION_MISMATCH",
                "expected": int(task_pack.get("asset_revision") or 0),
                "actual": int(snapshot.get("asset_revision") or 0),
            }
        )
    try:
        scene_revision = int(snapshot.get("scene_revision") or 0)
    except (TypeError, ValueError):
        scene_revision = 0
    if scene_revision < 1:
        blockers.append({"reason": "SCENE_REVISION_REQUIRED"})

    objects = [
        dict(item)
        for item in list(snapshot.get("objects", []) or [])
        if isinstance(item, Mapping) and str(item.get("component_id") or "") == component_id
    ]
    if not objects:
        blockers.append({"reason": "SCENE_COMPONENT_OBJECT_REQUIRED", "component_id": component_id})

    component = task_pack.get("component")
    component = dict(component) if isinstance(component, Mapping) else {}
    transform = component.get("transform")
    transform = dict(transform) if isinstance(transform, Mapping) else {}
    expected_location = _vec3(transform.get("location_mm"))
    validation = task_pack.get("validation_contract")
    validation = dict(validation) if isinstance(validation, Mapping) else {}
    placement_tolerance = float(validation.get("placement_tolerance_mm", 0.5))
    if expected_location is not None and objects:
        measured_locations = [value for value in (_location(item) for item in objects) if value is not None]
        if not measured_locations:
            blockers.append({"reason": "SCENE_COMPONENT_LOCATION_REQUIRED", "component_id": component_id})
        else:
            closest = min(
                max(abs(measured[index] - expected_location[index]) for index in range(3))
                for measured in measured_locations
            )
            if closest > placement_tolerance:
                blockers.append(
                    {
                        "reason": "SCENE_COMPONENT_PLACEMENT_MISMATCH",
                        "component_id": component_id,
                        "expected_location_mm": expected_location,
                        "closest_max_axis_error_mm": round(closest, 6),
                        "tolerance_mm": placement_tolerance,
                    }
                )

    parameters = task_pack.get("resolved_parameters")
    parameters = dict(parameters) if isinstance(parameters, Mapping) else {}
    expected_dimensions = [
        _resolved_value(parameters, ("width", "x")),
        _resolved_value(parameters, ("depth", "band_depth", "profile_depth", "channel_depth_y", "y")),
        _resolved_value(parameters, ("height", "thickness", "profile_height", "recess_height", "z")),
    ]
    require_dimensions = bool(validation.get("require_dimensions_match", False))
    single_mesh = [item for item in objects if str(item.get("object_type") or "").upper() == "MESH"]
    if require_dimensions:
        if any(value is None for value in expected_dimensions):
            blockers.append({"reason": "EXPECTED_COMPONENT_DIMENSIONS_UNRESOLVED", "component_id": component_id})
        elif len(single_mesh) != 1:
            blockers.append(
                {
                    "reason": "SINGLE_MESH_DIMENSION_PROOF_REQUIRED",
                    "component_id": component_id,
                    "mesh_object_count": len(single_mesh),
                }
            )
        else:
            measured = _vec3(single_mesh[0].get("dimensions_mm"))
            if measured is None:
                blockers.append({"reason": "SCENE_OBJECT_DIMENSIONS_REQUIRED", "component_id": component_id})
            else:
                tolerance = float(validation.get("dimension_tolerance_mm", 0.5))
                errors = [abs(measured[index] - float(expected_dimensions[index])) for index in range(3)]
                if max(errors) > tolerance:
                    blockers.append(
                        {
                            "reason": "SCENE_COMPONENT_DIMENSIONS_MISMATCH",
                            "component_id": component_id,
                            "expected_dimensions_mm": [float(value) for value in expected_dimensions],
                            "actual_dimensions_mm": measured,
                            "axis_errors_mm": errors,
                            "tolerance_mm": tolerance,
                        }
                    )
    elif len(single_mesh) == 1 and all(value is not None for value in expected_dimensions):
        warnings.append({"reason": "DIMENSION_MATCH_NOT_REQUIRED", "component_id": component_id})

    required_material_resources = {
        str(binding.get("resource_id") or "")
        for binding in dict(task_pack.get("resolved_design_bindings", {}) or {}).values()
        if isinstance(binding, Mapping)
        and str(binding.get("resource_type") or binding.get("resolved", {}).get("type") or "").upper() == "MATERIAL"
        and str(binding.get("resource_id") or "")
    }
    if required_material_resources and objects and bool(validation.get("require_material_resources", True)):
        observed = {
            str(material_id)
            for item in objects
            for material_id in list(item.get("material_ids", []) or [])
        }
        missing = sorted(required_material_resources - observed)
        if missing:
            blockers.append({"reason": "SCENE_REQUIRED_MATERIALS_MISSING", "resource_ids": missing})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "asset_id": task_pack.get("asset_id"),
        "asset_revision": task_pack.get("asset_revision"),
        "component_id": component_id,
        "scene_revision": scene_revision,
        "snapshot_hash": snapshot.get("snapshot_hash"),
        "object_count": len(objects),
        "blockers": blockers,
        "warnings": warnings,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "validate"]

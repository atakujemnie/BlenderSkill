from __future__ import annotations

"""Fail closed when a recipe cannot represent the component it claims to build."""

from typing import Any, Mapping

EXECUTOR_ID = "REPRESENTATION_CONTRACT_GATE"
EXECUTOR_VERSION = "0.22.0"

_DEFAULT_REQUIREMENTS: dict[str, set[str]] = {
    "PROFILE_PRISM": {"PROFILE_PRISM"},
    "TACTILE_GRID_PANEL": {"ARRAY", "INSTANCE"},
    "SLOTTED_GRATE_PLATE": {"ARRAY", "BOOLEAN_CUT"},
    "RECESSED_CHANNEL": {"BOOLEAN_CUT"},
    "RECESSED_HOUSING": {"BOOLEAN_CUT"},
    "EMISSIVE_STRIP": {"ASSIGN_BINDING"},
    "SENSOR_LENS": {"CYLINDER"},
    "SENSOR_RING": {"RING"},
    "FASTENER": {"CYLINDER"},
    "ROUNDED_SLOT": {"CAPSULE_PRISM"},
}


def _ops(recipe: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [dict(item) for item in list(recipe.get("operations", []) or []) if isinstance(item, Mapping)]


def _feature_ids(operation: Mapping[str, Any]) -> set[str]:
    values: set[str] = set()
    if operation.get("feature_id") not in (None, ""):
        values.add(str(operation.get("feature_id")))
    values.update(str(value) for value in list(operation.get("feature_ids", []) or []) if str(value))
    return values


def validate(task_pack: Mapping[str, Any], recipe: Mapping[str, Any]) -> dict[str, Any]:
    component = task_pack.get("component")
    if not isinstance(component, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_PACK_COMPONENT_REQUIRED"}],
        }

    component_id = str(task_pack.get("component_id") or component.get("id") or "")
    recipe_component_id = str(recipe.get("component_id") or "")
    blockers: list[dict[str, Any]] = []
    if recipe_component_id != component_id:
        blockers.append(
            {
                "reason": "RECIPE_COMPONENT_MISMATCH",
                "expected": component_id,
                "actual": recipe_component_id,
            }
        )

    operations = _ops(recipe)
    op_types = {str(item.get("op") or "").upper() for item in operations}
    shape_class = str(component.get("shape_class") or "").upper()
    contract = component.get("representation_contract")
    if contract is not None and not isinstance(contract, Mapping):
        blockers.append({"reason": "REPRESENTATION_CONTRACT_MAPPING_REQUIRED"})
        contract = {}
    contract = dict(contract or {})

    required_any_groups: list[set[str]] = []
    default = _DEFAULT_REQUIREMENTS.get(shape_class)
    if default:
        required_any_groups.append(default)
    for raw in list(contract.get("required_any_operations", []) or []):
        if isinstance(raw, (list, tuple, set)):
            required_any_groups.append({str(value).upper() for value in raw})
    required_all = {str(value).upper() for value in list(contract.get("required_operations", []) or [])}
    forbidden = {str(value).upper() for value in list(contract.get("forbidden_operations", []) or [])}

    for group in required_any_groups:
        if group and not (op_types & group):
            blockers.append(
                {
                    "reason": "REPRESENTATION_REQUIRED_OPERATION_MISSING",
                    "shape_class": shape_class,
                    "required_any": sorted(group),
                    "actual": sorted(op_types),
                }
            )
    missing_all = sorted(required_all - op_types)
    if missing_all:
        blockers.append(
            {
                "reason": "REPRESENTATION_REQUIRED_OPERATIONS_MISSING",
                "required": missing_all,
                "actual": sorted(op_types),
            }
        )
    present_forbidden = sorted(forbidden & op_types)
    if present_forbidden:
        blockers.append({"reason": "REPRESENTATION_FORBIDDEN_OPERATION_USED", "operations": present_forbidden})

    required_features = {str(value) for value in list(contract.get("required_feature_ids", []) or [])}
    actual_features = {feature_id for item in operations for feature_id in _feature_ids(item)}
    missing_features = sorted(required_features - actual_features)
    if missing_features:
        blockers.append({"reason": "REPRESENTATION_REQUIRED_FEATURES_MISSING", "feature_ids": missing_features})

    minimum_repeat = contract.get("minimum_repeat_count")
    if minimum_repeat is not None:
        repeat_count = 0
        for item in operations:
            op = str(item.get("op") or "").upper()
            if op == "ARRAY":
                repeat_count = max(repeat_count, int(item.get("count", 1)))
            elif op == "INSTANCE":
                repeat_count += 1
        if repeat_count < int(minimum_repeat):
            blockers.append(
                {
                    "reason": "REPRESENTATION_REPEAT_COUNT_TOO_LOW",
                    "minimum": int(minimum_repeat),
                    "actual": repeat_count,
                }
            )

    minimum_geometry_outputs = contract.get("minimum_geometry_outputs")
    if minimum_geometry_outputs is not None:
        geometry_types = {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM", "CYLINDER", "RING", "CAPSULE_PRISM", "INSTANCE"}
        geometry_outputs = sum(1 for item in operations if str(item.get("op") or "").upper() in geometry_types)
        if geometry_outputs < int(minimum_geometry_outputs):
            blockers.append(
                {
                    "reason": "REPRESENTATION_GEOMETRY_OUTPUT_COUNT_TOO_LOW",
                    "minimum": int(minimum_geometry_outputs),
                    "actual": geometry_outputs,
                }
            )

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "component_id": component_id,
        "shape_class": shape_class,
        "operation_types": sorted(op_types),
        "feature_ids": sorted(actual_features),
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "validate"]

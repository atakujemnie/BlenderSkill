from __future__ import annotations

"""Authorize one component recipe before Blender mutation and inject canonical placement."""

from copy import deepcopy
from typing import Any, Mapping

from executors.feature_contract_gate import validate as validate_features
from executors.hard_surface_recipe import validate as validate_recipe
from executors.representation_contract_gate import validate as validate_representation

EXECUTOR_ID = "COMPONENT_EXECUTION_GATE"
EXECUTOR_VERSION = "0.22.0"


def _feature_validation_enabled(task_pack: Mapping[str, Any]) -> bool:
    component = task_pack.get("component")
    if not isinstance(component, Mapping):
        return False
    return bool(component.get("feature_contract_required", False) or component.get("feature_contract"))


def authorize(task_pack: Mapping[str, Any], recipe: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    component_id = str(task_pack.get("component_id") or "")
    allowed = {str(value) for value in list(task_pack.get("allowed_to_modify", []) or [])}
    if component_id not in allowed:
        blockers.append({"reason": "TASK_COMPONENT_NOT_MUTABLE", "component_id": component_id})
    if str(recipe.get("component_id") or "") != component_id:
        blockers.append(
            {
                "reason": "RECIPE_COMPONENT_MISMATCH",
                "expected": component_id,
                "actual": str(recipe.get("component_id") or ""),
            }
        )

    recipe_verdict = validate_recipe(recipe)
    if recipe_verdict.get("status") != "PASS":
        blockers.extend(recipe_verdict.get("blockers", []))
    representation = validate_representation(task_pack, recipe)
    if representation.get("status") != "PASS":
        blockers.extend(representation.get("blockers", []))
    feature = validate_features(task_pack, recipe, None) if _feature_validation_enabled(task_pack) else None
    if isinstance(feature, Mapping) and feature.get("status") != "PASS":
        blockers.extend(feature.get("blockers", []))

    component = task_pack.get("component")
    transform = component.get("transform") if isinstance(component, Mapping) else None
    if not isinstance(transform, Mapping):
        blockers.append({"reason": "CANONICAL_COMPONENT_TRANSFORM_REQUIRED"})
    elif bool(component.get("placement_required", False)) and not bool(transform.get("explicit", False)):
        blockers.append({"reason": "EXPLICIT_COMPONENT_PLACEMENT_REQUIRED", "component_id": component_id})

    if blockers:
        return {
            "status": "BLOCKED",
            "executor_id": EXECUTOR_ID,
            "component_id": component_id,
            "feature_contract": feature,
            "blockers": blockers,
        }

    prepared = deepcopy(dict(recipe))
    prepared["component_transform"] = {
        "location_mm": list(transform.get("location_mm", [0.0, 0.0, 0.0])),
        "rotation_deg": list(transform.get("rotation_deg", [0.0, 0.0, 0.0])),
        "scale": list(transform.get("scale", [1.0, 1.0, 1.0])),
        "coordinate_space": str(transform.get("coordinate_space") or "ASSET_LOCAL"),
    }
    origin = component.get("origin") if isinstance(component, Mapping) else None
    prepared["component_origin"] = dict(origin) if isinstance(origin, Mapping) else {"type": "CENTER"}
    prepared["task_pack_asset_revision"] = task_pack.get("asset_revision")
    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "component_id": component_id,
        "recipe": prepared,
        "representation": representation,
        "feature_contract": feature,
        "blockers": [],
    }


def execute(task_pack: Mapping[str, Any], recipe: Mapping[str, Any], *, collection_name: str | None = None) -> dict[str, Any]:
    authorized = authorize(task_pack, recipe)
    if authorized["status"] != "PASS":
        return authorized
    from executors.blender_design_resource_adapter import apply_bindings
    from executors.blender_hard_surface_builder import execute as execute_blender_recipe

    result = execute_blender_recipe(authorized["recipe"], collection_name=collection_name)
    if result.get("status") != "PASS":
        return {
            **result,
            "execution_gate": EXECUTOR_ID,
            "representation_status": authorized["representation"]["status"],
        }
    materials = apply_bindings(task_pack, list(result.get("created_objects", []) or []))
    if materials.get("status") != "PASS":
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "component_id": authorized["component_id"],
            "build_result": result,
            "blockers": materials.get("blockers", []),
        }
    return {
        **result,
        "execution_gate": EXECUTOR_ID,
        "representation_status": authorized["representation"]["status"],
        "feature_contract_status": authorized["feature_contract"].get("status") if isinstance(authorized.get("feature_contract"), Mapping) else None,
        "materialization": materials,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "authorize", "execute"]

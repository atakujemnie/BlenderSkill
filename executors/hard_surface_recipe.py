from __future__ import annotations

"""Validate a compact deterministic recipe for manufactured hard-surface parts.

The recipe is an intermediate representation between LLM planning and Blender
mutation. Agents select primitives/operations and parameters; a Blender adapter
executes the approved recipe. This keeps repetitive geometry out of prompts.
"""

from typing import Any, Mapping

EXECUTOR_ID = "HARD_SURFACE_RECIPE"
EXECUTOR_VERSION = "0.1.0"

OPERATIONS = {
    "BOX",
    "ROUNDED_BOX",
    "WEDGE",
    "PROFILE_PRISM",
    "BOOLEAN_CUT",
    "BOOLEAN_UNION",
    "BEVEL",
    "MIRROR",
    "ARRAY",
    "INSTANCE",
    "ASSIGN_BINDING",
    "ANCHOR",
}
GEOMETRY_OPERATIONS = {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM"}
REFERENCE_OPERATIONS = {"BOOLEAN_CUT", "BOOLEAN_UNION", "MIRROR", "ARRAY", "INSTANCE"}


def validate(recipe: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    component_id = str(recipe.get("component_id") or "")
    if not component_id:
        blockers.append({"reason": "COMPONENT_ID_REQUIRED"})

    operations = list(recipe.get("operations", []) or [])
    if not operations:
        blockers.append({"reason": "RECIPE_OPERATIONS_REQUIRED"})

    output_ids: set[str] = set()
    op_ids: set[str] = set()
    for index, raw in enumerate(operations):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "OPERATION_INVALID", "index": index})
            continue
        op = dict(raw)
        op_id = str(op.get("id") or "")
        op_type = str(op.get("op") or "").upper()
        if not op_id:
            blockers.append({"reason": "OPERATION_ID_REQUIRED", "index": index})
        elif op_id in op_ids:
            blockers.append({"reason": "DUPLICATE_OPERATION_ID", "operation_id": op_id})
        op_ids.add(op_id)
        if op_type not in OPERATIONS:
            blockers.append({"reason": "OPERATION_TYPE_INVALID", "operation_id": op_id, "op": op_type})
            continue

        if op_type in GEOMETRY_OPERATIONS:
            output_id = str(op.get("output") or "")
            if not output_id:
                blockers.append({"reason": "GEOMETRY_OUTPUT_REQUIRED", "operation_id": op_id})
            elif output_id in output_ids:
                blockers.append({"reason": "DUPLICATE_GEOMETRY_OUTPUT", "output": output_id})
            output_ids.add(output_id)
            dimensions = op.get("dimensions")
            if op_type in {"BOX", "ROUNDED_BOX", "WEDGE"} and not isinstance(dimensions, Mapping):
                blockers.append({"reason": "DIMENSIONS_REQUIRED", "operation_id": op_id})
            if op_type == "PROFILE_PRISM" and not op.get("profile"):
                blockers.append({"reason": "PROFILE_REQUIRED", "operation_id": op_id})

        if op_type in REFERENCE_OPERATIONS:
            source = str(op.get("source") or "")
            if not source:
                blockers.append({"reason": "SOURCE_REQUIRED", "operation_id": op_id})
            elif source not in output_ids and not bool(op.get("external_source", False)):
                blockers.append({"reason": "SOURCE_NOT_AVAILABLE_YET", "operation_id": op_id, "source": source})

        if op_type in {"BOOLEAN_CUT", "BOOLEAN_UNION"}:
            target = str(op.get("target") or "")
            cutter = str(op.get("cutter") or "")
            if target not in output_ids:
                blockers.append({"reason": "BOOLEAN_TARGET_NOT_AVAILABLE", "operation_id": op_id, "target": target})
            if cutter not in output_ids:
                blockers.append({"reason": "BOOLEAN_CUTTER_NOT_AVAILABLE", "operation_id": op_id, "cutter": cutter})

        if op_type == "BEVEL":
            target = str(op.get("target") or "")
            if target not in output_ids:
                blockers.append({"reason": "BEVEL_TARGET_NOT_AVAILABLE", "operation_id": op_id, "target": target})
            width = op.get("width")
            if width is None:
                blockers.append({"reason": "BEVEL_WIDTH_REQUIRED", "operation_id": op_id})

        if op_type == "ASSIGN_BINDING":
            if not op.get("target") or not op.get("binding_id"):
                blockers.append({"reason": "BINDING_TARGET_AND_ID_REQUIRED", "operation_id": op_id})

        if op_type == "ANCHOR":
            if not op.get("anchor_id") or not op.get("target"):
                blockers.append({"reason": "ANCHOR_TARGET_REQUIRED", "operation_id": op_id})

    final_outputs = list(recipe.get("final_outputs", []) or [])
    if not final_outputs:
        warnings.append({"reason": "FINAL_OUTPUTS_NOT_DECLARED"})
    for output in final_outputs:
        if str(output) not in output_ids:
            blockers.append({"reason": "FINAL_OUTPUT_UNKNOWN", "output": str(output)})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "component_id": component_id,
        "operation_count": len(operations),
        "geometry_output_count": len(output_ids),
        "blockers": blockers,
        "warnings": warnings,
    }


def compact_summary(recipe: Mapping[str, Any]) -> dict[str, Any]:
    """Return a prompt-safe summary instead of echoing the full recipe."""
    operations = list(recipe.get("operations", []) or [])
    counts: dict[str, int] = {}
    for raw in operations:
        if isinstance(raw, Mapping):
            op = str(raw.get("op") or "UNKNOWN").upper()
            counts[op] = counts.get(op, 0) + 1
    return {
        "component_id": recipe.get("component_id"),
        "operation_count": len(operations),
        "operation_types": counts,
        "final_outputs": list(recipe.get("final_outputs", []) or []),
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "OPERATIONS", "compact_summary", "validate"]

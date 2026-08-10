from __future__ import annotations

"""Pure-Python orchestration for one asset/component production iteration."""

from typing import Any, Mapping

from executors.asset_state_runtime import validate_asset
from executors.component_task_pack import build as build_task_pack
from executors.design_binding_resolver import resolve as resolve_bindings
from executors.parameter_graph import resolve as resolve_parameters

EXECUTOR_ID = "ASSET_PRODUCTION_ORCHESTRATOR"
EXECUTOR_VERSION = "0.1.0"


def prepare_component_task(spec: Mapping[str, Any]) -> dict[str, Any]:
    asset = spec.get("asset")
    if not isinstance(asset, Mapping):
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "ASSET_REQUIRED"}]}

    state = validate_asset(asset)
    if state["status"] != "PASS":
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "failed_stage": "ASSET_STATE",
            "blockers": state["blockers"],
        }

    parameters = resolve_parameters({"components": asset.get("components", {})})
    if parameters["status"] != "PASS":
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "failed_stage": "PARAMETER_GRAPH",
            "blockers": parameters["blockers"],
        }

    binding_spec = {
        "resources": spec.get("design_resources", {}),
        "bindings": asset.get("bindings", {}),
    }
    bindings = resolve_bindings(binding_spec)
    if bindings["status"] != "PASS":
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "failed_stage": "DESIGN_BINDINGS",
            "blockers": bindings["blockers"],
        }

    task = build_task_pack(
        {
            "asset": asset,
            "component_id": spec.get("component_id"),
            "include_descendants": bool(spec.get("include_descendants", False)),
            "task_kind": spec.get("task_kind", "BUILD"),
            "max_input_tokens": spec.get("max_input_tokens", 8000),
            "resolved_parameters": parameters["resolved"],
            "resolved_bindings": bindings["resolved_bindings"],
            "reference_evidence": spec.get("reference_evidence", []),
        }
    )
    if task["status"] != "PASS":
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "failed_stage": "TASK_PACK",
            "blockers": task["blockers"],
            "metrics": task.get("metrics", {}),
        }

    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "asset_id": asset.get("asset_id"),
        "asset_revision": asset.get("revision"),
        "component_id": spec.get("component_id"),
        "task_pack": task["task_pack"],
        "metrics": {
            **task["metrics"],
            "resolved_parameter_count": parameters["parameter_count"],
            "resolved_binding_count": len(bindings["resolved_bindings"]),
            "design_deviation_count": len(bindings["deviations"]),
        },
        "design_deviations": bindings["deviations"],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "prepare_component_task"]

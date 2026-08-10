from __future__ import annotations

"""Pure-Python orchestration for one asset/component production iteration."""

from typing import Any, Mapping

from executors.asset_state_runtime import validate_asset
from executors.component_task_pack import build as build_task_pack
from executors.design_binding_resolver import resolve as resolve_bindings
from executors.parameter_graph import resolve as resolve_parameters
from executors.reference_evidence_registry import query as query_reference_evidence

EXECUTOR_ID = "ASSET_PRODUCTION_ORCHESTRATOR"
EXECUTOR_VERSION = "0.22.0"


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

    reference_evidence = [
        dict(item)
        for item in list(spec.get("reference_evidence", []) or [])
        if isinstance(item, Mapping)
    ]
    registry = spec.get("reference_evidence_registry")
    if registry is not None:
        if not isinstance(registry, Mapping):
            return {
                "status": "FAIL",
                "executor_id": EXECUTOR_ID,
                "failed_stage": "REFERENCE_EVIDENCE",
                "blockers": [{"reason": "REFERENCE_EVIDENCE_REGISTRY_MAPPING_REQUIRED"}],
            }
        queried = query_reference_evidence(
            registry,
            component_id=str(spec.get("component_id") or ""),
            feature_ids=[str(value) for value in list(spec.get("reference_feature_ids", []) or [])],
            views=[str(value) for value in list(spec.get("reference_views", []) or [])],
            include_inspiration=bool(spec.get("include_inspiration_reference", False)),
        )
        if queried["status"] != "PASS":
            return {
                "status": "FAIL",
                "executor_id": EXECUTOR_ID,
                "failed_stage": "REFERENCE_EVIDENCE",
                "blockers": queried.get("blockers", []),
            }
        reference_evidence.extend(queried["evidence"])

    deduplicated_evidence: list[dict[str, Any]] = []
    seen_evidence: set[str] = set()
    for item in reference_evidence:
        identity = str(item.get("evidence_id") or item.get("artifact_id") or item.get("reference_id") or "")
        if identity and identity in seen_evidence:
            continue
        if identity:
            seen_evidence.add(identity)
        deduplicated_evidence.append(item)

    task_spec = {
        "asset": asset,
        "component_id": spec.get("component_id"),
        "include_descendants": bool(spec.get("include_descendants", False)),
        "task_kind": spec.get("task_kind", "BUILD"),
        "resolved_parameters": parameters["resolved"],
        "resolved_bindings": bindings["resolved_bindings"],
        "reference_evidence": deduplicated_evidence,
    }
    if spec.get("reference_artifacts") is not None:
        task_spec["reference_artifacts"] = spec.get("reference_artifacts")
        task_spec["reference_artifact_root"] = spec.get("reference_artifact_root")
    if spec.get("max_input_tokens") is not None:
        task_spec["max_input_tokens"] = int(spec["max_input_tokens"])

    task = build_task_pack(task_spec)
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
            "reference_registry_evidence_count": len(deduplicated_evidence),
        },
        "design_deviations": bindings["deviations"],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "prepare_component_task"]

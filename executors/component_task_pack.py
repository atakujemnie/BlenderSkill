from __future__ import annotations

"""Build the smallest deterministic task pack needed for one component mutation."""

import json
from typing import Any, Mapping

EXECUTOR_ID = "COMPONENT_TASK_PACK"
EXECUTOR_VERSION = "0.1.0"
DEFAULT_BUILD_TOKEN_BUDGET = 8000
DEFAULT_REPAIR_TOKEN_BUDGET = 4000


def _components(asset: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = asset.get("components", {})
    if isinstance(raw, Mapping):
        return {str(k): dict(v) for k, v in raw.items() if isinstance(v, Mapping)}
    out: dict[str, dict[str, Any]] = {}
    for item in list(raw or []):
        if isinstance(item, Mapping) and item.get("id"):
            out[str(item["id"])] = dict(item)
    return out


def _descendants(components: Mapping[str, Mapping[str, Any]], root: str) -> set[str]:
    found = {root}
    changed = True
    while changed:
        changed = False
        for component_id, component in components.items():
            if str(component.get("parent") or "") in found and component_id not in found:
                found.add(component_id)
                changed = True
    return found


def _estimate_tokens(value: Any) -> int:
    # Deterministic conservative estimator for routing/budgeting. It deliberately
    # avoids a model-specific tokenizer dependency inside BlenderSkill.
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return max(1, (len(text) + 3) // 4)


def build(spec: Mapping[str, Any]) -> dict[str, Any]:
    asset = spec.get("asset")
    if not isinstance(asset, Mapping):
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "ASSET_REQUIRED"}]}
    component_id = str(spec.get("component_id") or "")
    components = _components(asset)
    if component_id not in components:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "COMPONENT_NOT_FOUND", "component_id": component_id}],
        }

    include_descendants = bool(spec.get("include_descendants", False))
    mutable = _descendants(components, component_id) if include_descendants else {component_id}
    read_only = sorted(set(components) - mutable)
    component = components[component_id]

    resolved_parameters = spec.get("resolved_parameters", {})
    component_parameters = {}
    if isinstance(resolved_parameters, Mapping):
        component_parameters = dict(resolved_parameters.get(component_id, {}) or {})

    resolved_bindings = spec.get("resolved_bindings", {})
    binding_ids = list(component.get("binding_ids", []) or [])
    component_bindings = {}
    if isinstance(resolved_bindings, Mapping):
        component_bindings = {
            binding_id: resolved_bindings[binding_id]
            for binding_id in binding_ids
            if binding_id in resolved_bindings
        }

    open_corrections = [
        dict(item)
        for item in list(asset.get("corrections", []) or [])
        if isinstance(item, Mapping)
        and str(item.get("component_id") or "") in mutable
        and str(item.get("status", "OPEN")).upper() == "OPEN"
    ]

    relation_ids = set(component.get("assembly_relation_ids", []) or [])
    relations = [
        dict(item)
        for item in list(asset.get("assembly_relations", []) or [])
        if isinstance(item, Mapping)
        and (
            str(item.get("id") or item.get("relation_id") or "") in relation_ids
            or str(item.get("a") or "").split(".", 1)[0] in mutable
            or str(item.get("b") or "").split(".", 1)[0] in mutable
        )
    ]

    references = []
    for item in list(spec.get("reference_evidence", []) or []):
        if not isinstance(item, Mapping):
            continue
        target = str(item.get("component_id") or component_id)
        if target in mutable:
            references.append(
                {
                    key: item.get(key)
                    for key in ("reference_id", "component_id", "view", "roi", "artifact_id", "authority")
                    if item.get(key) is not None
                }
            )

    task_kind = str(spec.get("task_kind", "BUILD")).upper()
    token_budget = int(
        spec.get(
            "max_input_tokens",
            DEFAULT_REPAIR_TOKEN_BUDGET if task_kind == "REPAIR" else DEFAULT_BUILD_TOKEN_BUDGET,
        )
    )

    task_pack = {
        "schema_version": 1,
        "asset_id": asset.get("asset_id"),
        "asset_revision": asset.get("revision"),
        "stage": asset.get("stage"),
        "task_kind": task_kind,
        "component_id": component_id,
        "component": {
            "id": component_id,
            "parent": component.get("parent"),
            "state": component.get("state"),
            "origin": component.get("origin"),
            "anchors": component.get("anchors", {}),
            "shape_class": component.get("shape_class"),
            "construction_recipe": component.get("construction_recipe"),
        },
        "allowed_to_modify": sorted(mutable),
        "read_only": read_only,
        "resolved_parameters": component_parameters,
        "resolved_design_bindings": component_bindings,
        "open_corrections": open_corrections,
        "assembly_relations": relations,
        "reference_evidence": references,
        "validation_contract": component.get("validation", {}),
    }

    estimated = _estimate_tokens(task_pack)
    blockers: list[dict[str, Any]] = []
    if estimated > token_budget:
        blockers.append(
            {
                "reason": "COMPONENT_TASK_TOKEN_BUDGET_EXCEEDED",
                "estimated_tokens": estimated,
                "maximum": token_budget,
            }
        )
    if spec.get("include_full_asset") or spec.get("include_full_history") or spec.get("include_full_library"):
        blockers.append({"reason": "BULK_CONTEXT_FORBIDDEN_IN_COMPONENT_TASK"})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "task_pack": task_pack,
        "metrics": {
            "estimated_input_tokens": estimated,
            "token_budget": token_budget,
            "mutable_component_count": len(mutable),
            "read_only_component_count": len(read_only),
            "correction_count": len(open_corrections),
            "reference_evidence_count": len(references),
        },
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "build"]

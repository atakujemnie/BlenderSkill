from __future__ import annotations

"""Build the smallest deterministic task pack needed for one component mutation."""

import json
from typing import Any, Mapping

from executors.component_transform import normalize as normalize_transform
from executors.reference_evidence_materializer import materialize as materialize_reference_evidence

EXECUTOR_ID = "COMPONENT_TASK_PACK"
EXECUTOR_VERSION = "0.22.0"
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

    transform = normalize_transform(component)
    if transform["status"] != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": transform["blockers"],
        }

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
                    for key in (
                        "evidence_id",
                        "reference_id",
                        "component_id",
                        "view",
                        "authority",
                        "feature_ids",
                        "roi",
                        "artifact_id",
                        "registration_id",
                    )
                    if item.get(key) is not None
                }
            )

    reference_attachments: list[dict[str, Any]] = []
    artifact_catalog = spec.get("reference_artifacts")
    if isinstance(artifact_catalog, Mapping) and references:
        materialized = materialize_reference_evidence(
            references,
            artifact_catalog,
            allowed_root=spec.get("reference_artifact_root"),
        )
        if materialized["status"] != "PASS":
            return {
                "status": "FAIL",
                "validator_id": EXECUTOR_ID,
                "blockers": materialized["blockers"],
            }
        reference_attachments = materialized["attachments"]

    task_kind = str(spec.get("task_kind", "BUILD")).upper()
    token_budget = int(
        spec.get(
            "max_input_tokens",
            DEFAULT_REPAIR_TOKEN_BUDGET if task_kind == "REPAIR" else DEFAULT_BUILD_TOKEN_BUDGET,
        )
    )

    feature_contract = component.get("feature_contract", {})
    visual_feature_map = component.get("visual_feature_map", {})
    qa_views = component.get("qa_views", [])
    edge_profiles = component.get("edge_profiles", {})

    task_pack = {
        "schema_version": 3,
        "asset_id": asset.get("asset_id"),
        "asset_revision": asset.get("revision"),
        "stage": asset.get("stage"),
        "task_kind": task_kind,
        "component_id": component_id,
        "component": {
            "id": component_id,
            "parent": component.get("parent"),
            "state": component.get("state"),
            "acceptance_level": component.get("acceptance_level"),
            "origin": component.get("origin"),
            "anchors": component.get("anchors", {}),
            "shape_class": component.get("shape_class"),
            "construction_recipe": component.get("construction_recipe"),
            "transform": transform["transform"],
            "placement_required": bool(component.get("placement_required", False)),
            "representation_contract": component.get("representation_contract", {}),
            "feature_contract_required": bool(
                component.get("feature_contract_required", asset.get("enforce_feature_contracts", False))
            ),
            "feature_contract": feature_contract,
            "visual_feature_map": visual_feature_map,
            "qa_views": qa_views,
            "edge_profiles": edge_profiles,
        },
        "allowed_to_modify": sorted(mutable),
        "read_only": read_only,
        "resolved_parameters": component_parameters,
        "resolved_design_bindings": component_bindings,
        "open_corrections": open_corrections,
        "assembly_relations": relations,
        "reference_evidence": references,
        "reference_attachments": reference_attachments,
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
            "reference_attachment_count": len(reference_attachments),
            "feature_contract_present": bool(feature_contract),
            "qa_view_count": len(list(qa_views or [])) if isinstance(qa_views, (list, tuple)) else len(dict(qa_views or {})),
            "placement_explicit": bool(transform["transform"]["explicit"]),
        },
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "build"]

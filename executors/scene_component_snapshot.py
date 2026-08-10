from __future__ import annotations

"""Compact, deterministic scene/component snapshots and structural diffs."""

import hashlib
import json
from typing import Any, Mapping

EXECUTOR_ID = "SCENE_COMPONENT_SNAPSHOT"
EXECUTOR_VERSION = "0.22.0"
SCHEMA_VERSION = 2
ALLOWED_OBJECT_FIELDS = (
    "object_id",
    "component_id",
    "object_type",
    "parent_id",
    "transform",
    "dimensions_mm",
    "mesh_metrics",
    "evaluated_mesh_metrics",
    "material_ids",
    "modifier_stack",
    "binding_ids",
    "anchor_ids",
    "feature_ids",
    "feature_proofs",
    "visibility",
)
VOLATILE_FIELDS = {"selected", "active", "viewport_color", "session_uid", "runtime_pointer"}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _estimate_tokens(value: Any) -> int:
    return max(1, (len(_canonical(value)) + 3) // 4)


def _normalize_object(raw: Mapping[str, Any]) -> dict[str, Any]:
    item: dict[str, Any] = {}
    for key in ALLOWED_OBJECT_FIELDS:
        if key in raw and raw.get(key) is not None:
            item[key] = raw.get(key)
    item["object_id"] = str(item.get("object_id") or raw.get("name") or "")
    item["component_id"] = str(item.get("component_id") or "")
    item["object_type"] = str(item.get("object_type") or raw.get("type") or "UNKNOWN").upper()
    for list_field in ("material_ids", "binding_ids", "anchor_ids", "feature_ids"):
        if list_field in item:
            item[list_field] = sorted({str(value) for value in list(item.get(list_field) or []) if str(value)})
    if "modifier_stack" in item:
        item["modifier_stack"] = [
            {
                key: modifier.get(key)
                for key in ("name", "type", "enabled", "settings_hash")
                if modifier.get(key) is not None
            }
            for modifier in list(item.get("modifier_stack") or [])
            if isinstance(modifier, Mapping)
        ]
    if "feature_proofs" in item:
        normalized_proofs = [dict(proof) for proof in list(item.get("feature_proofs") or []) if isinstance(proof, Mapping)]
        normalized_proofs.sort(
            key=lambda proof: (
                str(proof.get("feature_id") or ""),
                str(proof.get("proof_type") or ""),
                str(proof.get("operation_id") or ""),
            )
        )
        item["feature_proofs"] = normalized_proofs
    item["object_hash"] = _hash({key: value for key, value in item.items() if key != "object_hash"})
    return item


def build(report: Mapping[str, Any], *, component_ids: list[str] | None = None) -> dict[str, Any]:
    objects_raw = report.get("objects", [])
    if not isinstance(objects_raw, list):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "SCENE_OBJECT_LIST_REQUIRED"}],
        }
    wanted = {str(value) for value in (component_ids or [])}
    objects: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in objects_raw:
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "SCENE_OBJECT_RECORD_INVALID"})
            continue
        normalized = _normalize_object(raw)
        object_id = normalized["object_id"]
        if not object_id:
            blockers.append({"reason": "SCENE_OBJECT_ID_REQUIRED"})
            continue
        if object_id in seen:
            blockers.append({"reason": "SCENE_OBJECT_ID_DUPLICATE", "object_id": object_id})
            continue
        seen.add(object_id)
        if wanted and normalized["component_id"] not in wanted:
            continue
        objects.append(normalized)
    objects.sort(key=lambda item: (item.get("component_id", ""), item["object_id"]))

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": report.get("asset_id"),
        "asset_revision": report.get("asset_revision"),
        "scene_revision": report.get("scene_revision"),
        "component_scope": sorted(wanted),
        "objects": objects,
    }
    snapshot["snapshot_hash"] = _hash(snapshot)
    estimated = _estimate_tokens(snapshot)
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "snapshot": snapshot,
        "metrics": {
            "object_count": len(objects),
            "estimated_tokens": estimated,
            "component_count": len({item["component_id"] for item in objects if item.get("component_id")}),
            "feature_proof_count": sum(len(list(item.get("feature_proofs", []) or [])) for item in objects),
        },
        "blockers": blockers,
    }


def diff(previous: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, Any]:
    if previous.get("asset_id") and current.get("asset_id") and previous.get("asset_id") != current.get("asset_id"):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "SNAPSHOT_ASSET_MISMATCH"}],
        }
    before = {
        str(item.get("object_id")): dict(item)
        for item in list(previous.get("objects", []) or [])
        if isinstance(item, Mapping) and item.get("object_id")
    }
    after = {
        str(item.get("object_id")): dict(item)
        for item in list(current.get("objects", []) or [])
        if isinstance(item, Mapping) and item.get("object_id")
    }
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed: list[dict[str, Any]] = []
    for object_id in sorted(set(before) & set(after)):
        if before[object_id].get("object_hash") == after[object_id].get("object_hash"):
            continue
        fields: dict[str, dict[str, Any]] = {}
        keys = sorted((set(before[object_id]) | set(after[object_id])) - {"object_hash"})
        for key in keys:
            if before[object_id].get(key) != after[object_id].get(key):
                fields[key] = {"before": before[object_id].get(key), "after": after[object_id].get(key)}
        changed.append({"object_id": object_id, "fields": fields})
    payload = {
        "added": added,
        "removed": removed,
        "changed": changed,
        "changed_object_count": len(added) + len(removed) + len(changed),
    }
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "diff": payload,
        "diff_hash": _hash(payload),
        "estimated_tokens": _estimate_tokens(payload),
        "blockers": [],
    }


def assert_mutation_scope(
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    allowed_to_modify: list[str],
) -> dict[str, Any]:
    result = diff(previous, current)
    if result["status"] != "PASS":
        return result
    allowed = {str(value) for value in allowed_to_modify}
    before = {
        str(item.get("object_id")): str(item.get("component_id") or "")
        for item in list(previous.get("objects", []) or [])
        if isinstance(item, Mapping)
    }
    after = {
        str(item.get("object_id")): str(item.get("component_id") or "")
        for item in list(current.get("objects", []) or [])
        if isinstance(item, Mapping)
    }
    violations: list[dict[str, Any]] = []
    changed_ids = (
        set(result["diff"]["added"])
        | set(result["diff"]["removed"])
        | {item["object_id"] for item in result["diff"]["changed"]}
    )
    for object_id in sorted(changed_ids):
        component_id = after.get(object_id) or before.get(object_id) or ""
        if component_id not in allowed:
            violations.append(
                {
                    "reason": "MUTATION_SCOPE_VIOLATION",
                    "object_id": object_id,
                    "component_id": component_id,
                }
            )
    return {
        "status": "PASS" if not violations else "FAIL",
        "validator_id": EXECUTOR_ID,
        "allowed_to_modify": sorted(allowed),
        "diff": result["diff"],
        "blockers": violations,
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "assert_mutation_scope",
    "build",
    "diff",
]

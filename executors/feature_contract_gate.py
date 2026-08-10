from __future__ import annotations

"""Validate reference-critical feature completeness against recipe + scene proof.

v0.22 turns the existing FEATURE_CONTRACT / VISUAL_FEATURE_MAP guidance into an
executable gate. A component may have correct outer dimensions and still be
wrong because a camera ring, fastener, recess, repeated slot or edge treatment
is missing. MUST features therefore require explicit ownership and machine-
readable proof instead of being inferred from a successful executor call.
"""

from math import isfinite
from typing import Any, Mapping

EXECUTOR_ID = "FEATURE_CONTRACT_GATE"
EXECUTOR_VERSION = "0.22.0"
PRIORITIES = {"MUST", "SHOULD", "OPTIONAL"}


def _as_records(component: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw_contract = component.get("feature_contract")
    if raw_contract is None:
        return []
    if isinstance(raw_contract, Mapping):
        raw_features = raw_contract.get("features", raw_contract)
        if isinstance(raw_features, Mapping):
            records: list[dict[str, Any]] = []
            for feature_id, raw in raw_features.items():
                if isinstance(raw, Mapping):
                    records.append({"feature_id": str(feature_id), **dict(raw)})
            return records
        if isinstance(raw_features, list):
            return [dict(item) for item in raw_features if isinstance(item, Mapping)]
        return []
    if isinstance(raw_contract, list):
        return [dict(item) for item in raw_contract if isinstance(item, Mapping)]
    return []


def _operation_feature_ids(operation: Mapping[str, Any]) -> set[str]:
    values: set[str] = set()
    if operation.get("feature_id") not in (None, ""):
        values.add(str(operation.get("feature_id")))
    values.update(str(value) for value in list(operation.get("feature_ids", []) or []) if str(value))
    return values


def _recipe_operations(recipe: Mapping[str, Any], feature_id: str) -> list[dict[str, Any]]:
    return [
        dict(item)
        for item in list(recipe.get("operations", []) or [])
        if isinstance(item, Mapping) and feature_id in _operation_feature_ids(item)
    ]


def _snapshot_proofs(snapshot: Mapping[str, Any], component_id: str, feature_id: str) -> tuple[list[dict[str, Any]], int]:
    proofs: list[dict[str, Any]] = []
    object_count = 0
    for raw in list(snapshot.get("objects", []) or []):
        if not isinstance(raw, Mapping) or str(raw.get("component_id") or "") != component_id:
            continue
        feature_ids = {str(value) for value in list(raw.get("feature_ids", []) or [])}
        if feature_id in feature_ids:
            object_count += 1
        for proof in list(raw.get("feature_proofs", []) or []):
            if isinstance(proof, Mapping) and str(proof.get("feature_id") or "") == feature_id:
                proofs.append(dict(proof))
    return proofs, object_count


def _declared_count(operations: list[Mapping[str, Any]]) -> int:
    array_counts = [int(item.get("count", 1)) for item in operations if str(item.get("op") or "").upper() == "ARRAY"]
    if array_counts:
        return max(array_counts)
    instances = sum(1 for item in operations if str(item.get("op") or "").upper() == "INSTANCE")
    geometry = sum(
        1
        for item in operations
        if str(item.get("op") or "").upper()
        in {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM", "CYLINDER", "RING", "CAPSULE_PRISM"}
    )
    if instances:
        return max(1, geometry) + instances
    return geometry or len(operations)


def _metric_values(proofs: list[Mapping[str, Any]], metric: str) -> list[float]:
    values: list[float] = []
    for proof in proofs:
        candidates: list[Any] = []
        if metric in proof:
            candidates.append(proof.get(metric))
        metrics = proof.get("metrics")
        if isinstance(metrics, Mapping) and metric in metrics:
            candidates.append(metrics.get(metric))
        for raw in candidates:
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            if isfinite(value):
                values.append(value)
    return values


def _measurement_matches(values: list[float], spec: Any) -> bool:
    if not values:
        return False
    if isinstance(spec, (int, float)):
        target = float(spec)
        return any(abs(value - target) <= 1e-6 for value in values)
    if not isinstance(spec, Mapping):
        return False
    if spec.get("value") is not None:
        target = float(spec["value"])
        tolerance = float(spec.get("tolerance", spec.get("tolerance_mm", 0.0)))
        if not any(abs(value - target) <= tolerance for value in values):
            return False
    if spec.get("min") is not None and not any(value >= float(spec["min"]) for value in values):
        return False
    if spec.get("max") is not None and not any(value <= float(spec["max"]) for value in values):
        return False
    return True


def validate(task_pack: Mapping[str, Any], recipe: Mapping[str, Any], snapshot: Mapping[str, Any] | None = None) -> dict[str, Any]:
    component_raw = task_pack.get("component")
    component = dict(component_raw) if isinstance(component_raw, Mapping) else {}
    component_id = str(task_pack.get("component_id") or component.get("id") or "")
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []

    raw_contract = component.get("feature_contract")
    if raw_contract is not None and not isinstance(raw_contract, (Mapping, list)):
        blockers.append({"reason": "FEATURE_CONTRACT_MAPPING_OR_LIST_REQUIRED", "component_id": component_id})
        features: list[dict[str, Any]] = []
    else:
        features = _as_records(component)

    if bool(component.get("feature_contract_required", False)) and not features:
        blockers.append({"reason": "FEATURE_CONTRACT_REQUIRED", "component_id": component_id})

    seen: set[str] = set()
    must_total = 0
    must_passed = 0
    for feature in features:
        feature_id = str(feature.get("feature_id") or feature.get("id") or "")
        priority = str(feature.get("priority", "MUST")).upper()
        feature_blockers: list[dict[str, Any]] = []
        if not feature_id:
            feature_blockers.append({"reason": "FEATURE_ID_REQUIRED"})
        elif feature_id in seen:
            feature_blockers.append({"reason": "FEATURE_ID_DUPLICATE", "feature_id": feature_id})
        seen.add(feature_id)
        if priority not in PRIORITIES:
            feature_blockers.append({"reason": "FEATURE_PRIORITY_INVALID", "feature_id": feature_id, "priority": priority})

        owner = str(feature.get("owner_component_id") or component_id)
        if owner != component_id:
            feature_blockers.append(
                {
                    "reason": "FEATURE_OWNER_COMPONENT_MISMATCH",
                    "feature_id": feature_id,
                    "expected": component_id,
                    "actual": owner,
                }
            )

        operations = _recipe_operations(recipe, feature_id) if feature_id else []
        op_types = {str(item.get("op") or "").upper() for item in operations}
        required_ops = {str(value).upper() for value in list(feature.get("required_operations", []) or [])}
        forbidden_ops = {str(value).upper() for value in list(feature.get("forbidden_operations", []) or [])}
        missing_ops = sorted(required_ops - op_types)
        if missing_ops:
            feature_blockers.append(
                {
                    "reason": "FEATURE_REQUIRED_OPERATIONS_MISSING",
                    "feature_id": feature_id,
                    "required": missing_ops,
                    "actual": sorted(op_types),
                }
            )
        used_forbidden = sorted(forbidden_ops & op_types)
        if used_forbidden:
            feature_blockers.append(
                {"reason": "FEATURE_FORBIDDEN_OPERATION_USED", "feature_id": feature_id, "operations": used_forbidden}
            )

        expected_count = feature.get("expected_count")
        minimum_count = feature.get("minimum_count")
        declared_count = _declared_count(operations)
        if expected_count is not None and declared_count != int(expected_count):
            feature_blockers.append(
                {
                    "reason": "FEATURE_COUNT_MISMATCH",
                    "feature_id": feature_id,
                    "expected": int(expected_count),
                    "actual": declared_count,
                }
            )
        if minimum_count is not None and declared_count < int(minimum_count):
            feature_blockers.append(
                {
                    "reason": "FEATURE_COUNT_TOO_LOW",
                    "feature_id": feature_id,
                    "minimum": int(minimum_count),
                    "actual": declared_count,
                }
            )

        requires_evidence = bool(feature.get("requires_reference_evidence", feature.get("visual_required", False)))
        evidence_ids = [str(value) for value in list(feature.get("evidence_ids", []) or []) if str(value)]
        if requires_evidence and not evidence_ids:
            feature_blockers.append({"reason": "FEATURE_REFERENCE_EVIDENCE_REQUIRED", "feature_id": feature_id})

        proofs: list[dict[str, Any]] = []
        object_count = 0
        if snapshot is not None and feature_id:
            proofs, object_count = _snapshot_proofs(snapshot, component_id, feature_id)
        require_scene_proof = bool(feature.get("require_scene_proof", priority == "MUST"))
        if require_scene_proof and snapshot is not None and not proofs and object_count == 0:
            feature_blockers.append({"reason": "FEATURE_SCENE_PROOF_REQUIRED", "feature_id": feature_id})

        proof_types = {str(item.get("proof_type") or "").upper() for item in proofs}
        required_proof_types = {str(value).upper() for value in list(feature.get("required_proof_types", []) or [])}
        missing_proof_types = sorted(required_proof_types - proof_types)
        if snapshot is not None and missing_proof_types:
            feature_blockers.append(
                {
                    "reason": "FEATURE_PROOF_TYPE_MISSING",
                    "feature_id": feature_id,
                    "required": missing_proof_types,
                    "actual": sorted(proof_types),
                }
            )

        measurements = feature.get("expected_measurements", {})
        if isinstance(measurements, Mapping) and snapshot is not None:
            for metric, expected in measurements.items():
                values = _metric_values(proofs, str(metric))
                if not _measurement_matches(values, expected):
                    feature_blockers.append(
                        {
                            "reason": "FEATURE_MEASUREMENT_MISMATCH",
                            "feature_id": feature_id,
                            "metric": str(metric),
                            "expected": expected,
                            "actual_values": values,
                        }
                    )

        feature_status = "PASS" if not feature_blockers else "FAIL"
        if priority == "MUST":
            must_total += 1
            if feature_status == "PASS":
                must_passed += 1
            else:
                blockers.extend(feature_blockers)
        elif feature_blockers:
            warnings.extend(feature_blockers)

        results.append(
            {
                "feature_id": feature_id,
                "priority": priority,
                "status": feature_status,
                "operation_types": sorted(op_types),
                "declared_count": declared_count,
                "proof_types": sorted(proof_types),
                "scene_object_count": object_count,
                "blockers": feature_blockers,
            }
        )

    coverage = 1.0 if must_total == 0 else must_passed / must_total
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "asset_id": task_pack.get("asset_id"),
        "asset_revision": task_pack.get("asset_revision"),
        "component_id": component_id,
        "scene_revision": snapshot.get("scene_revision") if isinstance(snapshot, Mapping) else None,
        "must_feature_count": must_total,
        "must_feature_passed": must_passed,
        "must_feature_coverage": round(coverage, 6),
        "feature_results": results,
        "blockers": blockers,
        "warnings": warnings,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "PRIORITIES", "validate"]

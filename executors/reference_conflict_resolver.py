from __future__ import annotations

"""Deterministic per-property reference conflict arbitration for v0.11."""

from typing import Any, Mapping

EXECUTOR_ID = "REFERENCE_CONFLICT_RESOLVER"
EXECUTOR_VERSION = "0.1.0"
DEFAULT_AUTHORITY = {
    "EXPLICIT_DIMENSION": 100,
    "EXPLICIT_TEXT_SPEC": 95,
    "DETAIL_ORTHO": 90,
    "ORTHOGRAPHIC": 85,
    "DETAIL_PERSPECTIVE": 75,
    "HERO_PERSPECTIVE": 65,
    "PIXEL_INFERENCE": 55,
    "GENERIC_STYLE_INFERENCE": 30,
}


def _candidate_score(candidate: Mapping[str, Any], authority: Mapping[str, int]) -> tuple[int, float]:
    kind = str(candidate.get("authority_kind", candidate.get("evidence_kind", ""))).upper()
    rank = int(candidate.get("authority_rank", authority.get(kind, 0)))
    confidence = float(candidate.get("confidence", 0.0) or 0.0)
    return rank, confidence


def resolve(conflict: Mapping[str, Any], *, authority_policy: Mapping[str, int] | None = None) -> dict[str, Any]:
    authority = dict(DEFAULT_AUTHORITY)
    if authority_policy:
        authority.update({str(k).upper(): int(v) for k, v in authority_policy.items()})
    property_id = str(conflict.get("property_id", "UNKNOWN"))
    candidates = [dict(x) for x in list(conflict.get("candidates", []))]
    blockers: list[dict[str, Any]] = []
    if len(candidates) < 2:
        blockers.append({"reason": "AT_LEAST_TWO_CANDIDATES_REQUIRED"})
    for i, candidate in enumerate(candidates):
        if not candidate.get("source_reference_id"):
            blockers.append({"reason": "SOURCE_REFERENCE_REQUIRED", "candidate": i})
        if "value" not in candidate and "value_range" not in candidate:
            blockers.append({"reason": "VALUE_REQUIRED", "candidate": i})
        if not candidate.get("authority_kind") and "authority_rank" not in candidate:
            blockers.append({"reason": "AUTHORITY_REQUIRED", "candidate": i})
    if blockers:
        return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "property_id": property_id, "resolution_class": "UNRESOLVED", "blockers": blockers}
    ranked = sorted(enumerate(candidates), key=lambda item: (_candidate_score(item[1], authority), -item[0]), reverse=True)
    best_idx, best = ranked[0]
    best_score = _candidate_score(best, authority)
    tied = [(idx, candidate) for idx, candidate in ranked if _candidate_score(candidate, authority) == best_score]
    if len(tied) > 1:
        canonical_values = {repr(candidate.get("value", candidate.get("value_range"))) for _, candidate in tied}
        if len(canonical_values) > 1:
            return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "property_id": property_id, "resolution_class": "UNRESOLVED_EQUAL_AUTHORITY", "blockers": [{"reason": "EQUAL_AUTHORITY_CONFLICT", "candidate_indices": [idx for idx, _ in tied]}]}
    decision_id = str(conflict.get("decision_id") or f"conflict:{property_id}:{best.get('source_reference_id')}:{best_idx}")
    rejected = []
    for idx, candidate in enumerate(candidates):
        if idx == best_idx:
            continue
        rejected.append({"candidate_index": idx, "source_reference_id": candidate.get("source_reference_id"), "value": candidate.get("value", candidate.get("value_range")), "authority": _candidate_score(candidate, authority)})
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "executor_version": EXECUTOR_VERSION, "property_id": property_id, "resolution_class": "RESOLVED_AUTHORITY", "decision_id": decision_id, "selected_candidate_index": best_idx, "selected_value": best.get("value", best.get("value_range")), "selected_source_reference_id": best.get("source_reference_id"), "selected_view": best.get("view"), "selected_authority": best_score, "rejected": rejected, "averaging_used": False, "blockers": []}


def validate_decision(decision: Mapping[str, Any]) -> dict[str, Any]:
    blockers = []
    if str(decision.get("status", "")).upper() != "PASS":
        blockers.append({"reason": "DECISION_NOT_PASS"})
    if str(decision.get("validator_id", "")).upper() != EXECUTOR_ID:
        blockers.append({"reason": "NONCANONICAL_VALIDATOR"})
    for key in ("property_id", "decision_id", "selected_source_reference_id"):
        if not decision.get(key):
            blockers.append({"reason": f"{key.upper()}_REQUIRED"})
    if decision.get("averaging_used"):
        blockers.append({"reason": "UNJUSTIFIED_AVERAGING_FORBIDDEN"})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "blockers": blockers}

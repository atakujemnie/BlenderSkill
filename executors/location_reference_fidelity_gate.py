from __future__ import annotations

from typing import Any, Iterable

DEFAULT_LIMITS = {
    "layout_anchor_error_mm": 100.0,
    "orientation_error_deg": 5.0,
    "hero_scale_error_pct": 3.0,
    "composition_score_min": 0.85,
}


def evaluate_location_reference_fidelity(metrics: dict[str, Any], must_owners: Iterable[dict[str, Any]], limits: dict[str, float] | None = None) -> dict[str, Any]:
    policy = dict(DEFAULT_LIMITS)
    if limits:
        policy.update(limits)
    blockers: list[dict[str, Any]] = []
    for key in ("layout_anchor_error_mm", "orientation_error_deg", "hero_scale_error_pct"):
        value = float(metrics.get(key, float("inf")))
        if value > float(policy[key]):
            blockers.append({"code": "METRIC_OVER_LIMIT", "metric": key, "value": value, "limit": policy[key]})
    score = float(metrics.get("composition_score", 0.0))
    if score < float(policy["composition_score_min"]):
        blockers.append({"code": "COMPOSITION_SCORE_LOW", "value": score, "limit": policy["composition_score_min"]})
    for owner in must_owners:
        if owner.get("importance", "MUST") == "MUST" and owner.get("status") != "PASS":
            blockers.append({"code": "MUST_OWNER_NOT_PASS", "owner_id": owner.get("owner_id")})
    return {"validator_id": "LOCATION_REFERENCE_FIDELITY_GATE", "status": "PASS" if not blockers else "FAIL", "limits": policy, "blockers": blockers}

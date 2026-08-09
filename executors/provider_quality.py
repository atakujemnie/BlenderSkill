from __future__ import annotations

"""Quality/suitability ranking independent from discovery and capability probing."""

from typing import Any, Mapping, Sequence

EXECUTOR_ID = "PROVIDER_QUALITY_SELECT"
EXECUTOR_VERSION = "0.18.0"
TIER = {"A": 4, "B": 3, "C": 2, "D": 1, "UNRATED": 0}
MIN_TIER = {"HERO": "A", "MID": "B", "BACKGROUND": "C", "BLOCKOUT": "D"}


def select(candidates: Sequence[Mapping[str, Any]], usage_class: str) -> dict[str, Any]:
    usage = str(usage_class or "MID").upper()
    minimum = MIN_TIER.get(usage, "B")
    eligible = []
    rejected = []
    for raw in candidates:
        c = dict(raw)
        probe_state = str(c.get("probe_state") or c.get("runtime_probe_status") or c.get("runtime_status") or c.get("status") or "PROBE_REQUIRED").upper()
        tier = str(c.get("quality_tier", "UNRATED")).upper()
        if probe_state != "PASS" and str(c.get("source_kind")) != "READY_ASSET_SOURCE":
            rejected.append({"provider_id": c.get("provider_id"), "reason": "RUNTIME_NOT_PASS", "probe_state": probe_state, "quality_state": "UNRATED"})
            continue
        if tier not in TIER or TIER[tier] < TIER[minimum]:
            rejected.append({"provider_id": c.get("provider_id"), "reason": "QUALITY_TIER_TOO_LOW", "tier": tier, "minimum": minimum, "quality_state": "REJECTED"})
            continue
        c["quality_state"] = "PASS"
        eligible.append(c)
    eligible.sort(key=lambda c: (TIER.get(str(c.get("quality_tier", "UNRATED")).upper(), 0), float(c.get("quality_score", 0.0))), reverse=True)
    chosen = eligible[0] if eligible else None
    return {
        "status": "PASS" if chosen else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "usage_class": usage,
        "minimum_quality_tier": minimum,
        "selected_provider_id": chosen.get("provider_id") if chosen else None,
        "selected_quality_tier": chosen.get("quality_tier") if chosen else None,
        "eligible_provider_ids": [c.get("provider_id") for c in eligible],
        "rejected": rejected,
    }

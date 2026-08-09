from __future__ import annotations

"""Deterministic scatter planner over pre-sampled candidate points."""

import hashlib, math
from typing import Any, Mapping

EXECUTOR_ID = "VEGETATION_SCATTER"; EXECUTOR_VERSION = "0.1.0"


def _score(seed: int, candidate_id: str, weight: float) -> float:
    digest = hashlib.sha256(f"{seed}:{candidate_id}".encode("utf-8")).digest(); u = int.from_bytes(digest[:8], "big") / float(2**64 - 1)
    return u * max(0.0, min(1.0, weight))


def _distance(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    return math.sqrt(sum((float(a[k]) - float(b[k])) ** 2 for k in ("x", "y", "z")))


def plan(spec: Mapping[str, Any]) -> dict[str, Any]:
    seed = spec.get("seed")
    if not isinstance(seed, int): return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "INTEGER_SEED_REQUIRED"}]}
    target_count = int(spec.get("target_count", 0) or 0); min_required = int(spec.get("min_required", target_count) or 0); min_spacing = max(0.0, float(spec.get("min_spacing_m", 0.0) or 0.0)); max_slope = float(spec.get("max_slope_deg", 90.0)); min_weight = float(spec.get("min_biome_weight", 0.0))
    candidates = []; rejected: list[dict[str, Any]] = []
    for raw in spec.get("candidates", []) or []:
        c = dict(raw); cid = str(c.get("id", ""))
        if not cid: rejected.append({"id": None, "reason": "CANDIDATE_ID_REQUIRED"}); continue
        if bool(c.get("excluded", False)): rejected.append({"id": cid, "reason": "EXCLUDED"}); continue
        if float(c.get("slope_deg", 0.0)) > max_slope: rejected.append({"id": cid, "reason": "SLOPE"}); continue
        weight = float(c.get("biome_weight", 1.0))
        if weight < min_weight: rejected.append({"id": cid, "reason": "BIOME_WEIGHT"}); continue
        c["_score"] = _score(seed, cid, weight); candidates.append(c)
    candidates.sort(key=lambda c: (-c["_score"], str(c["id"]))); selected: list[dict[str, Any]] = []
    for c in candidates:
        if target_count and len(selected) >= target_count: rejected.append({"id": c["id"], "reason": "TARGET_REACHED"}); continue
        if any(_distance(c, s) < min_spacing for s in selected): rejected.append({"id": c["id"], "reason": "MIN_SPACING"}); continue
        selected.append({k: v for k, v in c.items() if k != "_score"})
    signature_src = "|".join(str(c["id"]) for c in selected); signature = hashlib.sha256(f"{seed}:{signature_src}".encode("utf-8")).hexdigest(); blockers = []
    if len(selected) < min_required: blockers.append({"reason": "INSUFFICIENT_VALID_PLACEMENTS", "required": min_required, "actual": len(selected)})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "seed": seed, "selected": selected, "selected_count": len(selected), "rejected": rejected, "placement_signature": signature, "blockers": blockers}

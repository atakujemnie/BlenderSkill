from __future__ import annotations

from typing import Any, Iterable

RELATIONS = {
    "INSIDE_ZONE",
    "AGAINST_SURFACE",
    "CENTERED_ON",
    "ALIGNS_WITH",
    "FACES_TARGET",
    "ABOVE",
    "BEHIND",
    "ADJACENT",
    "CLEARANCE",
    "CONTAINS",
    "PAIRED_WITH",
}


def evaluate_spatial_relations(relations: Iterable[dict[str, Any]]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    checked = 0
    for rel in relations:
        checked += 1
        rid = str(rel.get("relation_id", f"rel_{checked}"))
        kind = rel.get("relation")
        if kind not in RELATIONS:
            blockers.append({"code": "INVALID_RELATION", "relation_id": rid, "relation": kind})
            continue
        if not rel.get("a") or not rel.get("b"):
            blockers.append({"code": "MISSING_ENDPOINT", "relation_id": rid})
            continue
        if bool(rel.get("must", True)) and rel.get("satisfied") is not True:
            blockers.append({"code": "MUST_RELATION_UNSATISFIED", "relation_id": rid, "relation": kind})
    return {
        "validator_id": "SPATIAL_RELATION_GATE",
        "status": "PASS" if not blockers else "FAIL",
        "checked": checked,
        "blockers": blockers,
    }

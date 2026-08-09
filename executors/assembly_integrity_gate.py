from __future__ import annotations

"""Validate semantic relations between separately authored assembly parts.

Blender-side adapters measure gaps/contact/interpenetration. This executor owns
acceptance semantics so local helpers cannot redefine a junction after seeing it.
"""

from typing import Any, Mapping

EXECUTOR_ID = "ASSEMBLY_INTEGRITY_GATE"
EXECUTOR_VERSION = "0.1.0"

RELATION_TYPES = {"BUTT_JOINT", "SHADOW_GAP", "RECESSED_INSERT", "OVERLAP_ALLOWED",
                  "FLUSH_MATE", "CLEARANCE", "EMBEDDED", "WELDED", "FREE"}
DEFAULTS: dict[str, dict[str, Any]] = {
    "BUTT_JOINT": {"max_penetration_area_mm2": 1.0, "max_gap_mm": 2.0},
    "SHADOW_GAP": {"max_penetration_area_mm2": 1.0, "min_gap_mm": 0.1},
    "FLUSH_MATE": {"max_penetration_area_mm2": 1.0, "max_gap_mm": 1.0},
    "CLEARANCE": {"max_penetration_area_mm2": 0.0, "min_gap_mm": 0.1},
    "RECESSED_INSERT": {"min_embedding_depth_mm": 0.1},
    "EMBEDDED": {"min_embedding_depth_mm": 0.1},
    "WELDED": {"min_contact_area_mm2": 0.1},
    "OVERLAP_ALLOWED": {}, "FREE": {},
}


def _num(m: Mapping[str, Any], key: str) -> float | None:
    try:
        return None if m.get(key) is None else float(m[key])
    except (TypeError, ValueError):
        return None


def _relation(raw: Mapping[str, Any]) -> dict[str, Any]:
    rid = str(raw.get("relation_id", "UNKNOWN"))
    rtype = str(raw.get("relation_type", raw.get("type", "FREE"))).upper()
    importance = str(raw.get("importance", "MUST")).upper()
    metrics = dict(raw.get("metrics", {}))
    constraints = {**DEFAULTS.get(rtype, {}), **dict(raw.get("constraints", {}))}
    blockers: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, ok: bool, **detail: Any) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", **detail})
        if not ok: blockers.append({"reason": name, **detail})

    check("RELATION_TYPE_KNOWN", rtype in RELATION_TYPES, relation_type=rtype)
    check("RELATION_PARTS_REQUIRED", bool(raw.get("a")) and bool(raw.get("b")), a=raw.get("a"), b=raw.get("b"))
    pen_area = _num(metrics, "penetration_area_mm2")
    pen_volume = _num(metrics, "penetration_volume_mm3")
    min_gap = _num(metrics, "min_gap_mm")
    mean_gap = _num(metrics, "mean_gap_mm")
    contact = _num(metrics, "contact_area_mm2")
    embed = _num(metrics, "embedding_depth_mm")

    if "max_penetration_area_mm2" in constraints:
        lim = float(constraints["max_penetration_area_mm2"])
        check("PENETRATION_AREA_LIMIT", pen_area is not None and pen_area <= lim, actual=pen_area, limit=lim)
    if "max_penetration_volume_mm3" in constraints:
        lim = float(constraints["max_penetration_volume_mm3"])
        check("PENETRATION_VOLUME_LIMIT", pen_volume is not None and pen_volume <= lim, actual=pen_volume, limit=lim)
    if "min_gap_mm" in constraints:
        lim = float(constraints["min_gap_mm"])
        check("MIN_GAP", min_gap is not None and min_gap >= lim, actual=min_gap, limit=lim)
    if "max_gap_mm" in constraints:
        lim = float(constraints["max_gap_mm"])
        candidate = mean_gap if mean_gap is not None else min_gap
        check("MAX_GAP", candidate is not None and candidate <= lim, actual=candidate, limit=lim)
    if "min_contact_area_mm2" in constraints:
        lim = float(constraints["min_contact_area_mm2"])
        check("MIN_CONTACT_AREA", contact is not None and contact >= lim, actual=contact, limit=lim)
    if "min_embedding_depth_mm" in constraints:
        lim = float(constraints["min_embedding_depth_mm"])
        check("MIN_EMBEDDING_DEPTH", embed is not None and embed >= lim, actual=embed, limit=lim)
    if "max_embedding_depth_mm" in constraints:
        lim = float(constraints["max_embedding_depth_mm"])
        check("MAX_EMBEDDING_DEPTH", embed is not None and embed <= lim, actual=embed, limit=lim)

    if rtype in {"BUTT_JOINT", "SHADOW_GAP", "FLUSH_MATE", "CLEARANCE"}:
        check("UNINTENDED_INTERPENETRATION_FORBIDDEN",
              (pen_area or 0.0) <= float(constraints.get("max_penetration_area_mm2", 0.0)))

    return {"relation_id": rid, "relation_type": rtype, "importance": importance,
            "a": raw.get("a"), "b": raw.get("b"),
            "status": "PASS" if not blockers else "FAIL",
            "checks": checks, "blockers": blockers}


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    relations = [_relation(dict(r)) for r in report.get("relations", [])]
    if not relations and not bool(report.get("allow_empty", False)):
        return {"status": "FAIL", "validator_id": EXECUTOR_ID,
                "evidence_kind": "ASSEMBLY_INTEGRITY",
                "provenance_id": report.get("provenance_id") or "assembly_integrity:EMPTY",
                "relations": [], "failed_must": ["RELATION_CONTRACT_REQUIRED"],
                "blockers": [{"reason": "RELATION_CONTRACT_REQUIRED"}]}
    failed = [r["relation_id"] for r in relations if r["status"] != "PASS" and r["importance"] == "MUST"]
    blockers = [b for r in relations if r["status"] != "PASS" and r["importance"] == "MUST" for b in r["blockers"]]
    return {"status": "PASS" if not failed else "FAIL", "validator_id": EXECUTOR_ID,
            "evidence_kind": "ASSEMBLY_INTEGRITY",
            "provenance_id": report.get("provenance_id") or f"assembly_integrity:{report.get('assembly_revision', 'UNKNOWN')}",
            "assembly_revision": report.get("assembly_revision"), "relations": relations,
            "failed_must": failed, "blockers": blockers}


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "RELATION_TYPES", "evaluate"]

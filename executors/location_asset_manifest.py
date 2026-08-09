from __future__ import annotations

from typing import Any, Iterable

FINAL_STATES = {"ACCEPTED", "INSTANCED"}
ALLOWED_STATES = {"MISSING", "PROXY", "BUILDING", "BUILT_UNVERIFIED", "ACCEPTED", "INSTANCED", "BLOCKED", "FAIL"}


def evaluate_asset_manifest(entries: Iterable[dict[str, Any]], *, final: bool = False) -> dict[str, Any]:
    rows = list(entries)
    blockers: list[dict[str, Any]] = []
    ids: set[str] = set()
    counts = {state: 0 for state in ALLOWED_STATES}
    required_total = 0
    required_final = 0
    hero_required = 0
    hero_final = 0

    for row in rows:
        asset_id = str(row.get("asset_id", "")).strip()
        state = str(row.get("state", "MISSING"))
        required = bool(row.get("required", True))
        tier = str(row.get("tier", "MID")).upper()
        if not asset_id or asset_id in ids:
            blockers.append({"code": "INVALID_ASSET_ID", "asset_id": asset_id})
        ids.add(asset_id)
        if state not in ALLOWED_STATES:
            blockers.append({"code": "INVALID_STATE", "asset_id": asset_id, "state": state})
            continue
        counts[state] += 1
        if required:
            required_total += 1
            if state in FINAL_STATES:
                required_final += 1
            elif final:
                blockers.append({"code": "REQUIRED_NOT_FINAL", "asset_id": asset_id, "state": state})
            if tier == "HERO":
                hero_required += 1
                if state in FINAL_STATES:
                    hero_final += 1
                elif final:
                    blockers.append({"code": "HERO_NOT_FINAL", "asset_id": asset_id, "state": state})
        if final and state == "PROXY":
            blockers.append({"code": "PROXY_IN_FINAL_LOCATION", "asset_id": asset_id})

    coverage = 1.0 if required_total == 0 else required_final / required_total
    hero_coverage = 1.0 if hero_required == 0 else hero_final / hero_required
    return {
        "validator_id": "LOCATION_ASSET_MANIFEST",
        "status": "PASS" if not blockers else "FAIL",
        "required_coverage": round(coverage, 6),
        "hero_coverage": round(hero_coverage, 6),
        "counts": counts,
        "blockers": blockers,
    }

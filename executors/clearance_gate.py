from __future__ import annotations

from typing import Any, Iterable


def evaluate_clearances(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    checked = 0
    for row in records:
        checked += 1
        cid = str(row.get("clearance_id", f"clearance_{checked}"))
        required = float(row.get("required_mm", 0.0))
        measured = float(row.get("measured_mm", -1.0))
        if required < 0 or measured < 0:
            blockers.append({"code": "INVALID_CLEARANCE", "clearance_id": cid})
            continue
        if measured + 1e-9 < required:
            blockers.append({
                "code": "CLEARANCE_VIOLATION",
                "clearance_id": cid,
                "required_mm": required,
                "measured_mm": measured,
            })
        if float(row.get("penetration_mm", 0.0)) > float(row.get("max_penetration_mm", 0.0)):
            blockers.append({"code": "UNINTENDED_PENETRATION", "clearance_id": cid})
    return {
        "validator_id": "LOCATION_CLEARANCE_GATE",
        "status": "PASS" if not blockers else "FAIL",
        "checked": checked,
        "blockers": blockers,
    }

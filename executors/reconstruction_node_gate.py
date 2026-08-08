from __future__ import annotations

"""Proof-bearing acceptance gate for one Reconstruction Shape Node."""

from typing import Any, Mapping

EXECUTOR_ID = "RECONSTRUCTION_NODE_GATE"
EXECUTOR_VERSION = "0.1.0"

PASS = "PASS"
NOT_REQUIRED = "NOT_REQUIRED"


def _record_status(value: Any, *, strict: bool = True) -> tuple[str, str | None]:
    if value is None:
        return "UNVERIFIED", "MISSING_RECORD"
    if isinstance(value, str):
        status = value.upper()
        if status == NOT_REQUIRED:
            return PASS, None
        if status == PASS and strict:
            return "UNVERIFIED", "EVIDENCE_RECORD_REQUIRED"
        return status, None
    if not isinstance(value, Mapping):
        return "UNVERIFIED", "INVALID_RECORD"
    status = str(value.get("status", "UNVERIFIED")).upper()
    if status == NOT_REQUIRED:
        return PASS, None
    if status != PASS:
        return status, None
    if strict:
        if not value.get("evidence_kind"):
            return "UNVERIFIED", "EVIDENCE_KIND_REQUIRED"
        if not value.get("provenance_id"):
            return "UNVERIFIED", "PROVENANCE_REQUIRED"
    return PASS, None


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    strict = bool(report.get("strict_evidence", True))
    node_id = str(report.get("node_id", "UNKNOWN"))
    blockers: list[dict[str, str]] = []

    parent = str(report.get("parent_status", PASS)).upper()
    if parent != PASS:
        blockers.append({"owner": "parent", "status": parent, "reason": "PARENT_NOT_ACCEPTED"})

    dependencies = dict(report.get("dependencies", {}))
    for dep_id, dep_status in sorted(dependencies.items()):
        status = str(dep_status.get("status", dep_status) if isinstance(dep_status, Mapping) else dep_status).upper()
        if status != "ACCEPTED" and status != PASS:
            blockers.append({"owner": f"dependency:{dep_id}", "status": status, "reason": "DEPENDENCY_NOT_ACCEPTED"})

    required_single = {
        "isolation": report.get("isolation"),
        "numeric_constraints": report.get("numeric_constraints"),
        "regression": report.get("regression"),
    }
    if report.get("section_contract") is not None:
        required_single["section_contract"] = report.get("section_contract")

    for owner, value in required_single.items():
        status, reason = _record_status(value, strict=strict)
        if status != PASS:
            blockers.append({"owner": owner, "status": status, "reason": reason or "REQUIRED_CHECK_NOT_PASS"})

    views = dict(report.get("views", {}))
    required_views = [str(v) for v in report.get("required_views", views.keys())]
    for view in required_views:
        status, reason = _record_status(views.get(view), strict=strict)
        if status != PASS:
            blockers.append({"owner": f"view:{view}", "status": status, "reason": reason or "REQUIRED_VIEW_NOT_PASS"})

    deviations = list(report.get("deviations", []))
    for dev in deviations:
        severity = str(dev.get("severity", "SOFT")).upper()
        status = str(dev.get("status", "OPEN")).upper()
        if severity in {"HARD", "MUST", "CANONICAL"} and status not in {"RESOLVED", "ACCEPTED_BY_AUTHORITY"}:
            blockers.append({"owner": f"deviation:{dev.get('id','UNKNOWN')}", "status": status, "reason": "UNRESOLVED_HARD_DEVIATION"})
        if status == "ACCEPTED_BY_AUTHORITY" and (not dev.get("authority_source") or not dev.get("authority_record_id")):
            blockers.append({"owner": f"deviation:{dev.get('id','UNKNOWN')}", "status": "UNVERIFIED", "reason": "AUTHORITY_PROVENANCE_REQUIRED"})

    status = "ACCEPTED" if not blockers else "FAIL"
    if blockers and all(b["status"] in {"UNVERIFIED", "NOT_EVALUATED"} for b in blockers):
        status = "UNVERIFIED"
    if any(b["reason"] in {"PARENT_NOT_ACCEPTED", "DEPENDENCY_NOT_ACCEPTED"} for b in blockers):
        status = "BLOCKED"

    return {
        "status": status,
        "node_id": node_id,
        "graph_revision": report.get("graph_revision"),
        "node_revision": report.get("node_revision"),
        "accepted": status == "ACCEPTED",
        "children_unlocked": status == "ACCEPTED",
        "blockers": blockers,
    }

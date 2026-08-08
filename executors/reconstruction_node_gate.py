from __future__ import annotations

"""Proof-bearing acceptance gate for one Reconstruction Shape Node.

v0.11 adds per-view evidence contracts, derived-parameter provenance and
execution-authorization linkage.
"""

from typing import Any, Mapping

EXECUTOR_ID = "RECONSTRUCTION_NODE_GATE"
EXECUTOR_VERSION = "0.3.0"
PASS = "PASS"; NOT_REQUIRED = "NOT_REQUIRED"
REFERENCE_DERIVED_EVIDENCE = {"REGISTERED_OVERLAY", "SILHOUETTE_DIFF", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "PERSPECTIVE_INSPECTION", "LANDMARK_PROJECTION", "PART_BOUNDARY_VALIDATION", "TRIM_PATH_VALIDATION", "JUNCTION_VALIDATION", "EDGE_FAMILY_VALIDATION", "MATERIAL_APPEARANCE_VALIDATION", "DERIVED_PARAMETER_FIT"}
PROJECTED_EVIDENCE = {"REGISTERED_OVERLAY", "SILHOUETTE_DIFF", "FEATURE_ROI", "LOCAL_FEATURE_ROI", "LANDMARK_PROJECTION", "PART_BOUNDARY_VALIDATION", "TRIM_PATH_VALIDATION", "JUNCTION_VALIDATION"}
CANONICAL_VIEW_VALIDATORS = {"REFERENCE_OVERLAY_VALIDATE", "APPEARANCE_REFERENCE_VALIDATE"}
CANONICAL_OWNER_VALIDATORS = {"QA_SCENE_ISOLATE", "REFERENCE_MEASURE", "REFERENCE_OVERLAY_VALIDATE", "APPEARANCE_REFERENCE_VALIDATE", "SECTION_LOFT_HARD_SURFACE", "LAYER_STACK_VALIDATE", "MESH_VALIDATE", "REFERENCE_CONFLICT_RESOLVER", "RECONSTRUCTION_NODE_GATE"}


def _record_status(value: Any, *, strict: bool = True, require_view_validator: bool = False, allowed_evidence: set[str] | None = None) -> tuple[str, str | None]:
    if value is None: return "UNVERIFIED", "MISSING_RECORD"
    if isinstance(value, str):
        status = value.upper()
        if status == NOT_REQUIRED: return PASS, None
        if status == PASS and strict: return "UNVERIFIED", "EVIDENCE_RECORD_REQUIRED"
        return status, None
    if not isinstance(value, Mapping): return "UNVERIFIED", "INVALID_RECORD"
    status = str(value.get("status", "UNVERIFIED")).upper()
    if status == NOT_REQUIRED: return PASS, None
    if status != PASS: return status, None
    if not strict: return PASS, None
    evidence = str(value.get("evidence_kind", "")).upper()
    if not evidence: return "UNVERIFIED", "EVIDENCE_KIND_REQUIRED"
    if allowed_evidence is not None and evidence not in allowed_evidence: return "UNVERIFIED", f"VIEW_EVIDENCE_KIND_NOT_ALLOWED:{evidence}"
    provenance = value.get("provenance_id") or value.get("artifact_id") or value.get("report_id")
    if not provenance: return "UNVERIFIED", "PROVENANCE_REQUIRED"
    validator = str(value.get("validator_id", "")).upper()
    if not validator: return "UNVERIFIED", "VALIDATOR_ID_REQUIRED"
    if require_view_validator:
        if validator not in CANONICAL_VIEW_VALIDATORS: return "UNVERIFIED", "CANONICAL_REFERENCE_VIEW_VALIDATOR_REQUIRED"
    elif validator not in CANONICAL_OWNER_VALIDATORS: return "UNVERIFIED", "CANONICAL_VALIDATOR_REQUIRED"
    if evidence in REFERENCE_DERIVED_EVIDENCE and not (value.get("source_reference_ids") or value.get("source_reference_id")): return "UNVERIFIED", "SOURCE_REFERENCE_REQUIRED"
    if evidence in PROJECTED_EVIDENCE and not value.get("registration_id"): return "UNVERIFIED", "REGISTRATION_ID_REQUIRED"
    return PASS, None


def _view_contract(report: Mapping[str, Any], view: str) -> set[str] | None:
    contracts = report.get("view_contracts", {})
    if not isinstance(contracts, Mapping): return None
    cfg = contracts.get(view)
    if not isinstance(cfg, Mapping): return None
    kinds = cfg.get("allowed_evidence_kinds") or cfg.get("required_evidence_kinds")
    if not kinds: return None
    if isinstance(kinds, str): return {kinds.upper()}
    return {str(x).upper() for x in kinds}


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    strict = bool(report.get("strict_evidence", True)); node_id = str(report.get("node_id", "UNKNOWN")); blockers: list[dict[str, str]] = []
    parent = str(report.get("parent_status", PASS)).upper()
    if parent != PASS: blockers.append({"owner": "parent", "status": parent, "reason": "PARENT_NOT_ACCEPTED"})
    dependencies = dict(report.get("dependencies", {}))
    for dep_id, dep_status in sorted(dependencies.items()):
        status = str(dep_status.get("status", dep_status) if isinstance(dep_status, Mapping) else dep_status).upper()
        if status not in {"ACCEPTED", PASS}: blockers.append({"owner": f"dependency:{dep_id}", "status": status, "reason": "DEPENDENCY_NOT_ACCEPTED"})
    if report.get("authorization") is not None:
        auth = report.get("authorization")
        if not isinstance(auth, Mapping) or str(auth.get("validator_id", "")).upper() != "EXECUTION_AUTHORIZATION_GATE": blockers.append({"owner": "authorization", "status": "UNVERIFIED", "reason": "CANONICAL_EXECUTION_AUTHORIZATION_REQUIRED"})
        elif str(auth.get("status", "")).upper() != PASS: blockers.append({"owner": "authorization", "status": "FAIL", "reason": "EXECUTION_AUTHORIZATION_NOT_PASS"})
    required_single = {"isolation": report.get("isolation"), "numeric_constraints": report.get("numeric_constraints"), "regression": report.get("regression")}
    if report.get("section_contract") is not None: required_single["section_contract"] = report.get("section_contract")
    for owner, value in required_single.items():
        status, reason = _record_status(value, strict=strict)
        if status != PASS: blockers.append({"owner": owner, "status": status, "reason": reason or "REQUIRED_CHECK_NOT_PASS"})
    views = dict(report.get("views", {})); required_views = [str(v) for v in report.get("required_views", views.keys())]
    for view in required_views:
        status, reason = _record_status(views.get(view), strict=strict, require_view_validator=True, allowed_evidence=_view_contract(report, view))
        if status != PASS: blockers.append({"owner": f"view:{view}", "status": status, "reason": reason or "REQUIRED_VIEW_NOT_PASS"})
    for item in list(report.get("derived_parameters", [])):
        if not isinstance(item, Mapping): blockers.append({"owner": "derived_parameter", "status": "UNVERIFIED", "reason": "INVALID_DERIVED_PARAMETER_RECORD"}); continue
        param_id = str(item.get("id", "UNKNOWN")); required = ["value", "method", "source_reference_id", "confidence", "provenance_id"]; missing = [key for key in required if item.get(key) is None]
        if missing: blockers.append({"owner": f"derived_parameter:{param_id}", "status": "UNVERIFIED", "reason": "DERIVED_PARAMETER_PROVENANCE_MISSING:" + ",".join(missing)})
        if item.get("conflict_decision_required") and not item.get("conflict_decision_id"): blockers.append({"owner": f"derived_parameter:{param_id}", "status": "UNVERIFIED", "reason": "CONFLICT_DECISION_REQUIRED"})
    for dev in list(report.get("deviations", [])):
        severity = str(dev.get("severity", "SOFT")).upper(); status = str(dev.get("status", "OPEN")).upper(); owner = f"deviation:{dev.get('id', 'UNKNOWN')}"
        if severity in {"HARD", "MUST", "CANONICAL"} and status not in {"RESOLVED", "ACCEPTED_BY_AUTHORITY"}: blockers.append({"owner": owner, "status": status, "reason": "UNRESOLVED_HARD_DEVIATION"})
        if status == "ACCEPTED_BY_AUTHORITY" and (not dev.get("authority_source") or not dev.get("authority_record_id")): blockers.append({"owner": owner, "status": "UNVERIFIED", "reason": "AUTHORITY_PROVENANCE_REQUIRED"})
    status = "ACCEPTED" if not blockers else "FAIL"
    if blockers and all(b["status"] in {"UNVERIFIED", "NOT_EVALUATED"} for b in blockers): status = "UNVERIFIED"
    if any(b["reason"] in {"PARENT_NOT_ACCEPTED", "DEPENDENCY_NOT_ACCEPTED", "EXECUTION_AUTHORIZATION_NOT_PASS"} for b in blockers): status = "BLOCKED"
    return {"status": status, "node_id": node_id, "graph_revision": report.get("graph_revision"), "node_revision": report.get("node_revision"), "accepted": status == "ACCEPTED", "children_unlocked": status == "ACCEPTED", "blockers": blockers, "strict_reference_anchoring": strict, "canonical_view_validators": sorted(CANONICAL_VIEW_VALIDATORS)}

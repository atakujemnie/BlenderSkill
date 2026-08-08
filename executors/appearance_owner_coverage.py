from __future__ import annotations

"""Validate Appearance Contract coverage and report namespace integrity."""

from typing import Any, Mapping

EXECUTOR_ID = "APPEARANCE_OWNER_COVERAGE"
EXECUTOR_VERSION = "0.1.0"
PASS_LIKE = {"PASS", "NOT_REQUIRED"}


def evaluate(contract: Mapping[str, Any], report: Mapping[str, Any]) -> dict[str, Any]:
    owners = [dict(x) for x in list(contract.get("owners", []))]
    expected = {str(owner.get("owner_id")) for owner in owners if str(owner.get("importance", "MUST")).upper() == "MUST"}
    expected.discard("None")
    blockers: list[dict[str, Any]] = []
    shape_nodes = report.get("shape_nodes")
    appearance = report.get("appearance_owners")
    evidence = report.get("evidence")
    if not isinstance(shape_nodes, Mapping):
        blockers.append({"reason": "SHAPE_NODE_NAMESPACE_REQUIRED"}); shape_nodes = {}
    if not isinstance(appearance, Mapping):
        blockers.append({"reason": "APPEARANCE_OWNER_NAMESPACE_REQUIRED"}); appearance = {}
    if not isinstance(evidence, Mapping):
        blockers.append({"reason": "EVIDENCE_NAMESPACE_REQUIRED"})
    overlap = sorted(set(shape_nodes) & set(appearance))
    if overlap:
        blockers.append({"reason": "NAMESPACE_COLLISION", "ids": overlap})
    accounted = set(); failed = []; unverified = []
    for owner_id in sorted(expected):
        rec = appearance.get(owner_id)
        if not isinstance(rec, Mapping):
            continue
        accounted.add(owner_id)
        status = str(rec.get("status", "UNVERIFIED")).upper()
        if status == "FAIL": failed.append(owner_id)
        elif status not in PASS_LIKE: unverified.append(owner_id)
    missing = sorted(expected - accounted)
    if missing: blockers.append({"reason": "MUST_OWNER_MISSING", "ids": missing})
    if failed: blockers.append({"reason": "MUST_OWNER_FAIL", "ids": failed})
    if unverified: blockers.append({"reason": "MUST_OWNER_UNVERIFIED", "ids": unverified})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "contract_revision": contract.get("revision"), "expected_must": len(expected), "accounted_must": len(accounted), "missing_must": missing, "failed_must": failed, "unverified_must": unverified, "coverage": (len(accounted) / len(expected)) if expected else 1.0, "blockers": blockers}

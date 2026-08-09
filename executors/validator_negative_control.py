from __future__ import annotations

"""Prove that an acceptance validator can reject known-broken fixtures."""

from typing import Any, Mapping

EXECUTOR_ID = "VALIDATOR_NEGATIVE_CONTROL"
EXECUTOR_VERSION = "0.1.0"


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    validator_id = str(report.get("validator_id_under_test", "UNKNOWN"))
    positives = list(report.get("positive_controls", []))
    negatives = list(report.get("negative_controls", []))
    blockers: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []

    if not positives:
        blockers.append({"reason": "POSITIVE_CONTROL_REQUIRED"})
    if not negatives:
        blockers.append({"reason": "NEGATIVE_CONTROL_REQUIRED"})

    for raw in positives:
        case = dict(raw)
        actual = str(case.get("actual_status", case.get("status", "UNVERIFIED"))).upper()
        expected = str(case.get("expected_status", "PASS")).upper()
        ok = actual == expected
        cases.append({"case_id": case.get("case_id"), "class": "POSITIVE", "actual": actual,
                      "expected": expected, "status": "PASS" if ok else "FAIL"})
        if not ok:
            blockers.append({"reason": "POSITIVE_CONTROL_MISMATCH", "case_id": case.get("case_id"),
                             "actual": actual, "expected": expected})

    for raw in negatives:
        case = dict(raw)
        actual = str(case.get("actual_status", case.get("status", "UNVERIFIED"))).upper()
        expected = str(case.get("expected_status", "FAIL")).upper()
        ok = actual == expected
        cases.append({"case_id": case.get("case_id"), "class": "NEGATIVE", "actual": actual,
                      "expected": expected, "status": "PASS" if ok else "FAIL"})
        if not ok:
            blockers.append({"reason": "NEGATIVE_CONTROL_DID_NOT_BITE", "case_id": case.get("case_id"),
                             "actual": actual, "expected": expected})

    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID,
            "evidence_kind": "VALIDATOR_NEGATIVE_CONTROL",
            "provenance_id": report.get("provenance_id") or f"validator_control:{validator_id}",
            "validator_id_under_test": validator_id, "cases": cases, "blockers": blockers}


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "evaluate"]

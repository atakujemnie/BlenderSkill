from __future__ import annotations

"""Non-compensating final geometry-integrity aggregate before fidelity/runtime."""

from typing import Any, Mapping

EXECUTOR_ID = "GEOMETRIC_INTEGRITY_GATE"
EXECUTOR_VERSION = "0.1.0"
PASS = "PASS"


def _status(value: Any) -> str:
    if isinstance(value, Mapping):
        return str(value.get("status", "UNVERIFIED")).upper()
    return str(value or "UNVERIFIED").upper()


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []

    def require(owner: str, record: Any, validator: str | None = None) -> None:
        st = _status(record)
        if st != PASS:
            blockers.append({"owner": owner, "status": st, "reason": "REQUIRED_INTEGRITY_RECORD_NOT_PASS"})
            return
        if not isinstance(record, Mapping):
            blockers.append({"owner": owner, "status": "UNVERIFIED", "reason": "INTEGRITY_EVIDENCE_RECORD_REQUIRED"})
            return
        if validator and str(record.get("validator_id", "")).upper() != validator:
            blockers.append({"owner": owner, "status": "UNVERIFIED", "reason": f"VALIDATOR_REQUIRED:{validator}"})
        if not (record.get("provenance_id") or record.get("artifact_id") or record.get("report_id")):
            blockers.append({"owner": owner, "status": "UNVERIFIED", "reason": "PROVENANCE_REQUIRED"})

    mutations = list(report.get("mutation_postconditions", []))
    if not mutations and not bool(report.get("allow_no_mutations", False)):
        blockers.append({"owner": "mutation_postconditions", "status": "UNVERIFIED", "reason": "MUTATION_POSTCONDITIONS_REQUIRED"})
    for i, rec in enumerate(mutations):
        require(f"mutation:{i}", rec, "MUTATION_POSTCONDITION_GATE")

    require("assembly_integrity", report.get("assembly_integrity"), "ASSEMBLY_INTEGRITY_GATE")

    topology = list(report.get("topology_records", []))
    if not topology:
        blockers.append({"owner": "topology", "status": "UNVERIFIED", "reason": "TOPOLOGY_RECORD_REQUIRED"})
    for i, rec in enumerate(topology):
        require(f"topology:{i}", rec, "MESH_VALIDATE")

    controls = list(report.get("validator_controls", []))
    required_control_ids = {str(x) for x in report.get("required_validator_controls", [])}
    seen_controls = set()
    for i, rec in enumerate(controls):
        require(f"validator_control:{i}", rec, "VALIDATOR_NEGATIVE_CONTROL")
        if isinstance(rec, Mapping):
            seen_controls.add(str(rec.get("validator_id_under_test", "")))
    for missing in sorted(required_control_ids - seen_controls):
        blockers.append({"owner": f"validator_control:{missing}", "status": "UNVERIFIED",
                         "reason": "REQUIRED_NEGATIVE_CONTROL_MISSING"})

    stale = list(report.get("stale_evidence_ids", []))
    if stale:
        blockers.append({"owner": "evidence_freshness", "status": "FAIL",
                         "reason": "STALE_EVIDENCE_REFERENCED", "evidence_ids": stale})
    unresolved = list(report.get("unresolved_relation_ids", []))
    if unresolved:
        blockers.append({"owner": "assembly_relations", "status": "FAIL",
                         "reason": "UNRESOLVED_ASSEMBLY_RELATIONS", "relation_ids": unresolved})

    return {"status": PASS if not blockers else "FAIL", "validator_id": EXECUTOR_ID,
            "evidence_kind": "GEOMETRIC_INTEGRITY_GATE",
            "provenance_id": report.get("provenance_id") or f"geometric_integrity:{report.get('asset_revision', 'UNKNOWN')}",
            "asset_revision": report.get("asset_revision"), "blockers": blockers,
            "can_enter_fidelity_gate": not blockers}


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "evaluate"]

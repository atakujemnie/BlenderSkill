from __future__ import annotations

"""Pure-Python state-transition and checkpoint validator for reconstruction."""

from copy import deepcopy
from typing import Any, Mapping

EXECUTOR_ID = "NODE_STATE_STORE"
EXECUTOR_VERSION = "0.2.0"

CANONICAL_STATES = {
    "DECLARED", "CONSTRAINED", "READY_TO_BUILD", "BUILT_UNVERIFIED",
    "ACCEPTED", "UNVERIFIED", "FAIL", "BLOCKED", "DIRTY", "SUPERSEDED",
}
ALLOWED_TRANSITIONS = {
    "DECLARED": {"CONSTRAINED", "BLOCKED", "SUPERSEDED"},
    "CONSTRAINED": {"READY_TO_BUILD", "BLOCKED", "SUPERSEDED"},
    "READY_TO_BUILD": {"BUILT_UNVERIFIED", "BLOCKED", "SUPERSEDED"},
    "BUILT_UNVERIFIED": {"ACCEPTED", "UNVERIFIED", "FAIL", "BLOCKED", "SUPERSEDED"},
    "ACCEPTED": {"DIRTY", "SUPERSEDED"},
    "UNVERIFIED": {"CONSTRAINED", "READY_TO_BUILD", "BLOCKED", "SUPERSEDED"},
    "FAIL": {"CONSTRAINED", "READY_TO_BUILD", "BLOCKED", "SUPERSEDED"},
    "BLOCKED": {"CONSTRAINED", "READY_TO_BUILD", "SUPERSEDED"},
    "DIRTY": {"CONSTRAINED", "READY_TO_BUILD", "BLOCKED", "SUPERSEDED"},
    "SUPERSEDED": set(),
}


def _proof_ok(record: Any, validator_id: str) -> bool:
    return (
        isinstance(record, Mapping)
        and str(record.get("status", "")).upper() in {"PASS", "ACCEPTED"}
        and str(record.get("validator_id", "")).upper() == validator_id
        and bool(record.get("provenance_id") or record.get("authorization_id") or record.get("artifact_id"))
    )


def validate_transition(old_state: str, new_state: str, *, evidence: Mapping[str, Any] | None = None) -> dict[str, Any]:
    old_state = old_state.upper()
    new_state = new_state.upper()
    blockers: list[dict[str, str]] = []
    if old_state not in CANONICAL_STATES:
        blockers.append({"reason": "INVALID_OLD_STATE", "state": old_state})
    if new_state not in CANONICAL_STATES:
        blockers.append({"reason": "INVALID_NEW_STATE", "state": new_state})
    if not blockers and new_state not in ALLOWED_TRANSITIONS[old_state]:
        blockers.append({"reason": "ILLEGAL_TRANSITION", "transition": f"{old_state}->{new_state}"})
    if not blockers and new_state == "READY_TO_BUILD" and not _proof_ok(evidence, "EXECUTION_AUTHORIZATION_GATE"):
        blockers.append({"reason": "EXECUTION_AUTHORIZATION_REQUIRED"})
    if not blockers and new_state == "BUILT_UNVERIFIED":
        if not _proof_ok(evidence, "LOCAL_BUILDER"):
            blockers.append({"reason": "MUTATION_ARTIFACT_REQUIRED"})
        else:
            post = evidence.get("mutation_postcondition") if isinstance(evidence, Mapping) else None
            if not _proof_ok(post, "MUTATION_POSTCONDITION_GATE"):
                blockers.append({"reason": "MUTATION_POSTCONDITION_REQUIRED"})
    if not blockers and new_state == "ACCEPTED" and not _proof_ok(evidence, "RECONSTRUCTION_NODE_GATE"):
        blockers.append({"reason": "CANONICAL_NODE_GATE_REQUIRED"})
    if not blockers and new_state == "DIRTY" and (
        not isinstance(evidence, Mapping) or not (evidence.get("change_id") or evidence.get("dirty_reason"))
    ):
        blockers.append({"reason": "DIRTY_REASON_REQUIRED"})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID,
            "old_state": old_state, "new_state": new_state, "blockers": blockers,
            "can_transition": not blockers}


def validate_checkpoint(checkpoint: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    if not checkpoint.get("asset_id"): blockers.append({"reason": "ASSET_ID_REQUIRED"})
    if not checkpoint.get("graph_revision"): blockers.append({"reason": "GRAPH_REVISION_REQUIRED"})
    if not checkpoint.get("state_revision"): blockers.append({"reason": "STATE_REVISION_REQUIRED"})
    shape_nodes = checkpoint.get("shape_nodes")
    appearance_owners = checkpoint.get("appearance_owners")
    evidence = checkpoint.get("evidence")
    if not isinstance(shape_nodes, Mapping): blockers.append({"reason": "SHAPE_NODE_NAMESPACE_REQUIRED"})
    if not isinstance(appearance_owners, Mapping): blockers.append({"reason": "APPEARANCE_OWNER_NAMESPACE_REQUIRED"})
    if not isinstance(evidence, Mapping): blockers.append({"reason": "EVIDENCE_NAMESPACE_REQUIRED"})
    if isinstance(shape_nodes, Mapping):
        for node_id, node in shape_nodes.items():
            state = str(node.get("state", "DECLARED")).upper() if isinstance(node, Mapping) else "INVALID"
            if state not in CANONICAL_STATES:
                blockers.append({"reason": "INVALID_NODE_STATE", "node_id": str(node_id), "state": state})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID,
            "asset_id": checkpoint.get("asset_id"), "graph_revision": checkpoint.get("graph_revision"),
            "state_revision": checkpoint.get("state_revision"), "blockers": blockers}


def apply_transition(checkpoint: Mapping[str, Any], node_id: str, new_state: str,
                     *, evidence: Mapping[str, Any] | None = None) -> dict[str, Any]:
    cp = deepcopy(dict(checkpoint))
    shape_nodes = cp.setdefault("shape_nodes", {})
    if node_id not in shape_nodes:
        raise KeyError(f"unknown node_id: {node_id}")
    node = dict(shape_nodes[node_id])
    old_state = str(node.get("state", "DECLARED")).upper()
    verdict = validate_transition(old_state, new_state, evidence=evidence)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "checkpoint": cp, "transition": verdict}
    node["state"] = new_state.upper()
    if evidence:
        node["last_transition_provenance"] = (
            evidence.get("provenance_id") or evidence.get("authorization_id") or evidence.get("artifact_id")
        )
    shape_nodes[node_id] = node
    history = list(cp.get("history", []))
    history.append({"node_id": node_id, "from": old_state, "to": new_state.upper(),
                    "provenance": node.get("last_transition_provenance")})
    cp["history"] = history
    return {"status": "PASS", "checkpoint": cp, "transition": verdict}

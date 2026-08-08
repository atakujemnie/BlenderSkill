from __future__ import annotations

"""Hard execution-authorization gate for Reconstruction Shape Nodes.

v0.11 closes the v0.10 loophole exposed by the Lafar Street Lamp benchmark:
a structurally valid Shape Graph could report ``ready_nodes=[]`` while an
asset-local builder still mutated every RDL in one run.

This executor does not build geometry. It decides whether a requested mutation
is authorized and emits a proof-bearing authorization record.
"""

from typing import Any, Mapping

EXECUTOR_ID = "EXECUTION_AUTHORIZATION_GATE"
EXECUTOR_VERSION = "0.1.0"

PASS = "PASS"
FAIL = "FAIL"
RDLS = {f"RDL{i}": i for i in range(6)}
MUTATION_ACTIONS = {"BUILD", "REPAIR"}
_ALLOWED_SOURCE_STATES = {
    "BUILD": {"CONSTRAINED"},
    "REPAIR": {"DIRTY", "FAIL", "UNVERIFIED"},
}


def _nodes(spec: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = spec.get("nodes", {})
    if isinstance(raw, Mapping):
        return {str(k): dict(v) for k, v in raw.items()}
    out: dict[str, dict[str, Any]] = {}
    for item in list(raw or []):
        node = dict(item)
        node_id = str(node.get("id", ""))
        if not node_id or node_id in out:
            raise ValueError("DUPLICATE_OR_EMPTY_NODE_ID")
        out[node_id] = node
    return out


def _refs(node: Mapping[str, Any], key: str) -> list[str]:
    value = node.get(key, [])
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(x) for x in value]


def _required_ancestors(nodes: Mapping[str, Mapping[str, Any]], node: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    parent = node.get("parent")
    if parent and node.get("require_parent_accepted", True):
        refs.append(str(parent))
    refs.extend(_refs(node, "depends_on"))
    return sorted(set(refs))


def _prior_stage_blockers(nodes: Mapping[str, Mapping[str, Any]], node_rdl: str) -> list[dict[str, str]]:
    if node_rdl not in RDLS:
        return [{"node_id": "UNKNOWN", "status": "INVALID_RDL"}]
    target = RDLS[node_rdl]
    if target <= 0:
        return []
    blockers: list[dict[str, str]] = []
    for node_id, other in sorted(nodes.items()):
        rdl = str(other.get("rdl", ""))
        if rdl not in RDLS or RDLS[rdl] >= target:
            continue
        if str(other.get("importance", "MUST")).upper() != "MUST":
            continue
        state = str(other.get("state", "DECLARED")).upper()
        if state != "ACCEPTED":
            blockers.append({"node_id": node_id, "status": state})
    return blockers


def issue_authorization(spec: Mapping[str, Any], node_id: str, *, node_revision: str, action: str = "BUILD", authorization_id: str | None = None) -> dict[str, Any]:
    """Evaluate whether a node may transition to READY_TO_BUILD."""
    action = action.upper()
    if action not in MUTATION_ACTIONS:
        raise ValueError(f"action must be one of {sorted(MUTATION_ACTIONS)}")

    nodes = _nodes(spec)
    node_id = str(node_id)
    node = nodes.get(node_id)
    blockers: list[dict[str, Any]] = []

    if node is None:
        blockers.append({"reason": "NODE_MISSING", "node_id": node_id})
    else:
        state = str(node.get("state", "DECLARED")).upper()
        allowed = _ALLOWED_SOURCE_STATES[action]
        if state not in allowed:
            blockers.append({"reason": "SOURCE_STATE_NOT_AUTHORIZABLE", "state": state, "allowed": sorted(allowed)})
        if not node.get("validation"):
            blockers.append({"reason": "VALIDATION_CONTRACT_MISSING"})
        if str(node.get("level", "")) != "G0" and not node.get("shape_class"):
            blockers.append({"reason": "SHAPE_CLASS_MISSING"})
        for ref in _required_ancestors(nodes, node):
            if ref not in nodes:
                blockers.append({"reason": "DEPENDENCY_MISSING", "dependency": ref})
                continue
            dep_state = str(nodes[ref].get("state", "DECLARED")).upper()
            if dep_state != "ACCEPTED":
                blockers.append({"reason": "DEPENDENCY_NOT_ACCEPTED", "dependency": ref, "status": dep_state})
        for item in _prior_stage_blockers(nodes, str(node.get("rdl", ""))):
            blockers.append({"reason": "PRIOR_RDL_BARRIER_NOT_ACCEPTED", **item})

    status = PASS if not blockers else FAIL
    auth_id = authorization_id or f"auth:{spec.get('graph_revision','UNKNOWN')}:{node_id}:{node_revision}:{action}"
    return {
        "status": status,
        "authorization_id": auth_id,
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "graph_revision": spec.get("graph_revision"),
        "node_id": node_id,
        "node_revision": node_revision,
        "action": action,
        "transition": "CONSTRAINED_OR_REPAIRABLE->READY_TO_BUILD",
        "blockers": blockers,
        "can_transition_ready": status == PASS,
    }


def can_mutate(spec: Mapping[str, Any], node_id: str, authorization: Mapping[str, Any] | None, *, action: str = "BUILD") -> dict[str, Any]:
    """Return PASS only when production geometry mutation is legal."""
    action = action.upper()
    nodes = _nodes(spec)
    node_id = str(node_id)
    node = nodes.get(node_id)
    blockers: list[dict[str, Any]] = []

    if node is None:
        blockers.append({"reason": "NODE_MISSING"})
    else:
        state = str(node.get("state", "DECLARED")).upper()
        if state != "READY_TO_BUILD":
            blockers.append({"reason": "NODE_NOT_READY_TO_BUILD", "state": state})
        for ref in _required_ancestors(nodes, node):
            dep_state = str(nodes.get(ref, {}).get("state", "DECLARED")).upper()
            if dep_state != "ACCEPTED":
                blockers.append({"reason": "DEPENDENCY_NOT_ACCEPTED", "dependency": ref, "status": dep_state})
        for item in _prior_stage_blockers(nodes, str(node.get("rdl", ""))):
            blockers.append({"reason": "PRIOR_RDL_BARRIER_NOT_ACCEPTED", **item})

    if not isinstance(authorization, Mapping):
        blockers.append({"reason": "AUTHORIZATION_RECORD_REQUIRED"})
    else:
        if str(authorization.get("status", "")).upper() != PASS:
            blockers.append({"reason": "AUTHORIZATION_NOT_PASS"})
        if str(authorization.get("validator_id", "")).upper() != EXECUTOR_ID:
            blockers.append({"reason": "NONCANONICAL_AUTHORIZATION_VALIDATOR"})
        if str(authorization.get("node_id", "")) != node_id:
            blockers.append({"reason": "AUTHORIZATION_NODE_MISMATCH"})
        if authorization.get("graph_revision") != spec.get("graph_revision"):
            blockers.append({"reason": "AUTHORIZATION_GRAPH_REVISION_MISMATCH"})
        if str(authorization.get("action", "")).upper() != action:
            blockers.append({"reason": "AUTHORIZATION_ACTION_MISMATCH"})
        if not authorization.get("authorization_id"):
            blockers.append({"reason": "AUTHORIZATION_ID_REQUIRED"})
        if not authorization.get("node_revision"):
            blockers.append({"reason": "NODE_REVISION_REQUIRED"})

    status = PASS if not blockers else FAIL
    return {"status": status, "validator_id": EXECUTOR_ID, "graph_revision": spec.get("graph_revision"), "node_id": node_id, "action": action, "can_mutate_geometry": status == PASS, "blockers": blockers}

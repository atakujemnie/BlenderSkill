from __future__ import annotations

"""Pure-Python validator and readiness planner for Reconstruction Shape Graphs."""

from collections import deque
from typing import Any, Mapping

EXECUTOR_ID = "SHAPE_GRAPH"
EXECUTOR_VERSION = "0.1.0"

LEVELS = {f"G{i}": i for i in range(6)}
RDLS = {f"RDL{i}": i for i in range(6)}
CANONICAL_STATES = {
    "DECLARED", "CONSTRAINED", "READY_TO_BUILD", "BUILT_UNVERIFIED",
    "ACCEPTED", "FAIL", "BLOCKED", "DIRTY", "SUPERSEDED",
}


def _nodes(spec: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = spec.get("nodes", {})
    if isinstance(raw, Mapping):
        out = {str(k): dict(v) for k, v in raw.items()}
        for node_id, node in out.items():
            node.setdefault("id", node_id)
        return out
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


def _detect_cycle(nodes: Mapping[str, Mapping[str, Any]]) -> list[str] | None:
    edges: dict[str, set[str]] = {node_id: set() for node_id in nodes}
    indegree = {node_id: 0 for node_id in nodes}
    for node_id, node in nodes.items():
        refs = set(_refs(node, "depends_on"))
        parent = node.get("parent")
        if parent:
            refs.add(str(parent))
        for ref in refs:
            if ref in nodes and ref != node_id and node_id not in edges[ref]:
                edges[ref].add(node_id)
                indegree[node_id] += 1
    q = deque(sorted(k for k, d in indegree.items() if d == 0))
    visited = 0
    while q:
        current = q.popleft()
        visited += 1
        for nxt in sorted(edges[current]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    if visited == len(nodes):
        return None
    return sorted(k for k, d in indegree.items() if d > 0)


def validate(spec: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    try:
        nodes = _nodes(spec)
    except ValueError as exc:
        return {"status": "FAIL", "errors": [{"id": str(exc)}], "warnings": []}

    root = str(spec.get("root", ""))
    if not root or root not in nodes:
        errors.append({"id": "ROOT_MISSING", "root": root})

    for node_id, node in nodes.items():
        level = str(node.get("level", ""))
        rdl = str(node.get("rdl", ""))
        state = str(node.get("state", "DECLARED")).upper()
        if level not in LEVELS:
            errors.append({"id": "INVALID_LEVEL", "node": node_id, "value": level})
        if rdl not in RDLS:
            errors.append({"id": "INVALID_RDL", "node": node_id, "value": rdl})
        if level in LEVELS and rdl in RDLS and LEVELS[level] != RDLS[rdl] and not node.get("allow_level_rdl_mismatch", False):
            errors.append({"id": "LEVEL_RDL_MISMATCH", "node": node_id, "level": level, "rdl": rdl})
        if state not in CANONICAL_STATES:
            errors.append({"id": "INVALID_STATE", "node": node_id, "value": state})
        parent = node.get("parent")
        if parent is not None and str(parent) not in nodes:
            errors.append({"id": "PARENT_MISSING", "node": node_id, "parent": str(parent)})
        for dep in _refs(node, "depends_on"):
            if dep not in nodes:
                errors.append({"id": "DEPENDENCY_MISSING", "node": node_id, "dependency": dep})
            elif level in LEVELS:
                dep_rdl = str(nodes[dep].get("rdl", ""))
                if dep_rdl in RDLS and RDLS[dep_rdl] > RDLS.get(rdl, 99) and not node.get("allow_future_dependency", False):
                    errors.append({"id": "FUTURE_LEVEL_DEPENDENCY", "node": node_id, "dependency": dep})
        if level != "G0" and not node.get("shape_class"):
            errors.append({"id": "SHAPE_CLASS_MISSING", "node": node_id})
        if str(node.get("importance", "MUST")).upper() == "MUST" and not node.get("validation"):
            errors.append({"id": "VALIDATION_CONTRACT_MISSING", "node": node_id})

    cycle = _detect_cycle(nodes)
    if cycle:
        errors.append({"id": "GRAPH_CYCLE", "nodes": cycle})

    ready: list[str] = []
    blocked: list[dict[str, Any]] = []
    if not cycle:
        for node_id, node in sorted(nodes.items()):
            state = str(node.get("state", "DECLARED")).upper()
            if state not in {"CONSTRAINED", "READY_TO_BUILD", "DIRTY", "FAIL"}:
                continue
            required: list[str] = []
            parent = node.get("parent")
            if parent and node.get("require_parent_accepted", True):
                required.append(str(parent))
            required.extend(_refs(node, "depends_on"))
            not_accepted = [ref for ref in required if ref in nodes and str(nodes[ref].get("state", "DECLARED")).upper() != "ACCEPTED"]
            if not_accepted:
                blocked.append({"node": node_id, "reason": "DEPENDENCY_NOT_ACCEPTED", "dependencies": sorted(set(not_accepted))})
            else:
                ready.append(node_id)

    return {
        "status": "FAIL" if errors else "PASS",
        "graph_revision": spec.get("graph_revision"),
        "root": root,
        "node_count": len(nodes),
        "ready_nodes": ready,
        "blocked_nodes": blocked,
        "errors": errors,
        "warnings": warnings,
    }


def evaluate_stage_barrier(spec: Mapping[str, Any], rdl: str) -> dict[str, Any]:
    if rdl not in RDLS:
        raise ValueError(f"rdl must be one of {sorted(RDLS)}")
    nodes = _nodes(spec)
    target = RDLS[rdl]
    required = []
    accepted = []
    blockers = []
    for node_id, node in sorted(nodes.items()):
        node_rdl = str(node.get("rdl", ""))
        if node_rdl not in RDLS or RDLS[node_rdl] > target:
            continue
        if str(node.get("importance", "MUST")).upper() != "MUST":
            continue
        required.append(node_id)
        state = str(node.get("state", "DECLARED")).upper()
        if state == "ACCEPTED":
            accepted.append(node_id)
        else:
            blockers.append({"node_id": node_id, "status": state})
    return {
        "status": "PASS" if not blockers else "FAIL",
        "rdl": rdl,
        "graph_revision": spec.get("graph_revision"),
        "required_nodes": required,
        "accepted_nodes": accepted,
        "blockers": blockers,
        "can_advance": not blockers,
    }

from __future__ import annotations

"""Propagate repair invalidation through Shape/Appearance/Evidence namespaces."""

from copy import deepcopy
from typing import Any, Mapping
import re

EXECUTOR_ID = "DEPENDENCY_INVALIDATOR"
EXECUTOR_VERSION = "0.1.0"


def _bump(value: Any) -> str:
    text = str(value or "rev_000")
    m = re.match(r"^(.*?)(\d+)$", text)
    if not m:
        return text + "_001"
    prefix, digits = m.groups()
    return f"{prefix}{int(digits) + 1:0{len(digits)}d}"


def _reverse_edges(graph: Mapping[str, Any]) -> dict[str, set[str]]:
    nodes = dict(graph.get("nodes", {}))
    rev = {str(n): set() for n in nodes}
    for nid, raw in nodes.items():
        node = dict(raw)
        parent = node.get("parent")
        if parent in rev:
            rev[str(parent)].add(str(nid))
        for dep in node.get("depends_on", []):
            if dep in rev:
                rev[str(dep)].add(str(nid))
    return rev


def _closure(rev: Mapping[str, set[str]], seeds: set[str]) -> set[str]:
    out = set(seeds)
    stack = list(seeds)
    while stack:
        cur = stack.pop()
        for nxt in rev.get(cur, set()):
            if nxt not in out:
                out.add(nxt)
                stack.append(nxt)
    return out


def invalidate(graph: Mapping[str, Any], checkpoint: Mapping[str, Any], changed_nodes,
               appearance_contract: Mapping[str, Any] | None = None,
               *, change_id: str = "change:UNKNOWN") -> dict[str, Any]:
    cp = deepcopy(dict(checkpoint))
    nodes = cp.setdefault("shape_nodes", {})
    seeds = {str(n) for n in changed_nodes}
    unknown = sorted(n for n in seeds if n not in nodes)
    if unknown:
        return {"status": "FAIL", "validator_id": EXECUTOR_ID,
                "blockers": [{"reason": "UNKNOWN_CHANGED_NODE", "nodes": unknown}],
                "checkpoint": cp}

    affected = _closure(_reverse_edges(graph), seeds)
    dirty, blocked = [], []
    for nid in sorted(affected):
        rec = dict(nodes[nid])
        rec["node_revision"] = _bump(rec.get("node_revision"))
        rec["invalidated_by"] = change_id
        old = str(rec.get("state", "DECLARED")).upper()
        if nid in seeds or old in {"ACCEPTED", "BUILT_UNVERIFIED", "UNVERIFIED", "FAIL", "DIRTY"}:
            rec["state"] = "DIRTY"
            dirty.append(nid)
        elif old != "SUPERSEDED":
            rec["state"] = "BLOCKED"
            blocked.append(nid)
        nodes[nid] = rec

    invalid_owners = []
    owners = cp.setdefault("appearance_owners", {})
    contract_owners = [] if appearance_contract is None else list(appearance_contract.get("owners", []))
    host_map = {str(o.get("owner_id")): {str(x) for x in o.get("hosts", [])} for o in contract_owners}
    for owner_id, raw in list(owners.items()):
        hosts = host_map.get(str(owner_id), {str(x) for x in dict(raw).get("hosts", [])})
        if hosts & affected:
            rec = dict(raw)
            rec["status"] = "UNVERIFIED"
            rec["invalidated_by"] = change_id
            owners[owner_id] = rec
            invalid_owners.append(str(owner_id))

    superseded = []
    evidence = cp.setdefault("evidence", {})
    for eid, raw in list(evidence.items()):
        if not isinstance(raw, Mapping):
            continue
        rec = dict(raw)
        node_id = str(rec.get("node_id", ""))
        owner_id = str(rec.get("owner_id", ""))
        hosts = {str(x) for x in rec.get("hosts", [])}
        if node_id in affected or owner_id in invalid_owners or bool(hosts & affected):
            rec["status"] = "SUPERSEDED"
            rec["superseded_by"] = change_id
            evidence[eid] = rec
            superseded.append(str(eid))

    history = list(cp.get("history", []))
    history.append({"action": "DEPENDENCY_INVALIDATION", "change_id": change_id,
                    "seed_nodes": sorted(seeds), "affected_nodes": sorted(affected)})
    cp["history"] = history
    cp["state_revision"] = _bump(cp.get("state_revision"))

    return {"status": "PASS", "validator_id": EXECUTOR_ID,
            "provenance_id": f"dependency_invalidation:{change_id}",
            "change_id": change_id, "affected_nodes": sorted(affected),
            "dirty_nodes": dirty, "blocked_nodes": blocked,
            "invalidated_appearance_owners": sorted(invalid_owners),
            "superseded_evidence": sorted(superseded), "checkpoint": cp, "blockers": []}


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "invalidate"]

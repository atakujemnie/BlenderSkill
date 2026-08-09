from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

VALID_KINDS = {"LOCATION", "ZONE", "SYSTEM", "ASSET", "INSTANCE"}
VALID_STATES = {"MISSING", "PROXY", "BUILDING", "BUILT_UNVERIFIED", "ACCEPTED", "INSTANCED", "BLOCKED", "FAIL"}

@dataclass(frozen=True)
class GraphIssue:
    code: str
    node_id: str
    detail: str


def validate_location_scene_graph(nodes: Iterable[dict[str, Any]]) -> dict[str, Any]:
    items = list(nodes)
    by_id: dict[str, dict[str, Any]] = {}
    issues: list[GraphIssue] = []
    for node in items:
        node_id = str(node.get("id", "")).strip()
        if not node_id:
            issues.append(GraphIssue("MISSING_ID", "<unknown>", "node id is required"))
            continue
        if node_id in by_id:
            issues.append(GraphIssue("DUPLICATE_ID", node_id, "node ids must be unique"))
            continue
        by_id[node_id] = node
        if node.get("kind") not in VALID_KINDS:
            issues.append(GraphIssue("INVALID_KIND", node_id, f"kind={node.get('kind')!r}"))
        if node.get("state", "MISSING") not in VALID_STATES:
            issues.append(GraphIssue("INVALID_STATE", node_id, f"state={node.get('state')!r}"))

    roots = [n for n in items if n.get("kind") == "LOCATION"]
    if len(roots) != 1:
        issues.append(GraphIssue("LOCATION_ROOT_COUNT", "<graph>", f"expected 1 LOCATION root, got {len(roots)}"))

    for node_id, node in by_id.items():
        parent = node.get("parent")
        if node.get("kind") == "LOCATION":
            if parent not in (None, ""):
                issues.append(GraphIssue("LOCATION_HAS_PARENT", node_id, str(parent)))
            continue
        if not parent or parent not in by_id:
            issues.append(GraphIssue("MISSING_PARENT", node_id, str(parent)))

    for node_id in by_id:
        seen: set[str] = set()
        cur = node_id
        while cur in by_id:
            if cur in seen:
                issues.append(GraphIssue("PARENT_CYCLE", node_id, f"cycle through {cur}"))
                break
            seen.add(cur)
            parent = by_id[cur].get("parent")
            if not parent:
                break
            cur = str(parent)

    return {
        "validator_id": "LOCATION_SCENE_GRAPH",
        "status": "PASS" if not issues else "FAIL",
        "node_count": len(items),
        "issues": [issue.__dict__ for issue in issues],
    }

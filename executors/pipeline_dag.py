from __future__ import annotations

"""Pure-Python dependency planner for incremental asset pipelines.

The planner computes the downstream closure of explicitly changed/dirty stages.
It does not execute Blender or project-specific stage callables.
"""

from collections import defaultdict, deque
from typing import Iterable, Mapping


def _normalized_graph(dependencies: Mapping[str, Iterable[str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    all_nodes: set[str] = set()
    for stage, deps in dependencies.items():
        stage = str(stage)
        d = {str(x) for x in deps}
        graph[stage] = d
        all_nodes.add(stage)
        all_nodes.update(d)
    for node in all_nodes:
        graph.setdefault(node, set())
    return graph


def topological_order(dependencies: Mapping[str, Iterable[str]]) -> list[str]:
    graph = _normalized_graph(dependencies)
    indegree = {node: len(deps) for node, deps in graph.items()}
    downstream: dict[str, set[str]] = defaultdict(set)
    for node, deps in graph.items():
        for dep in deps:
            downstream[dep].add(node)

    q = deque(sorted(node for node, deg in indegree.items() if deg == 0))
    order: list[str] = []
    while q:
        node = q.popleft()
        order.append(node)
        for child in sorted(downstream[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                q.append(child)

    if len(order) != len(graph):
        cyclic = sorted(node for node, deg in indegree.items() if deg > 0)
        raise ValueError(f"PIPELINE_DAG_CYCLE: {cyclic}")
    return order


def downstream_closure(
    dependencies: Mapping[str, Iterable[str]],
    changed: Iterable[str],
) -> set[str]:
    graph = _normalized_graph(dependencies)
    downstream: dict[str, set[str]] = defaultdict(set)
    for node, deps in graph.items():
        for dep in deps:
            downstream[dep].add(node)

    dirty = {str(x) for x in changed}
    unknown = sorted(dirty - set(graph))
    if unknown:
        raise KeyError(f"UNKNOWN_PIPELINE_STAGE: {unknown}")

    q = deque(sorted(dirty))
    while q:
        node = q.popleft()
        for child in sorted(downstream[node]):
            if child not in dirty:
                dirty.add(child)
                q.append(child)
    return dirty


def plan_execution(
    dependencies: Mapping[str, Iterable[str]],
    *,
    changed: Iterable[str] = (),
    explicitly_dirty: Iterable[str] = (),
    accepted_clean: Iterable[str] = (),
) -> dict:
    """Return deterministic execute/reuse order.

    `changed` and `explicitly_dirty` propagate downstream. `accepted_clean` is
    informational: if a stage becomes dirty through dependency closure it must
    execute even if it was previously accepted.
    """
    graph = _normalized_graph(dependencies)
    order = topological_order(graph)
    roots = {str(x) for x in changed} | {str(x) for x in explicitly_dirty}
    dirty = downstream_closure(graph, roots) if roots else set()
    clean = {str(x) for x in accepted_clean}

    execute = [stage for stage in order if stage in dirty]
    reuse = [stage for stage in order if stage in clean and stage not in dirty]
    blocked_reuse = sorted(clean & dirty)

    return {
        "status": "PASS",
        "changed_or_explicit_dirty": sorted(roots),
        "execute": execute,
        "reuse": reuse,
        "previously_clean_but_invalidated": blocked_reuse,
        "stage_count": len(order),
        "execute_count": len(execute),
        "reuse_count": len(reuse),
    }


DEFAULT_HARD_SURFACE_DAG = {
    "BUILD_GEOMETRY": (),
    "UV_CONTRACT": ("BUILD_GEOMETRY",),
    "DECAL_ASSET": (),
    "BAKE_BASECOLOR": ("UV_CONTRACT",),
    "BAKE_NORMAL": ("BUILD_GEOMETRY", "UV_CONTRACT"),
    "BAKE_AO": ("BUILD_GEOMETRY", "UV_CONTRACT"),
    "BAKE_ROUGHNESS": ("UV_CONTRACT",),
    "BAKE_METALLIC": ("UV_CONTRACT",),
    "BAKE_EMISSIVE": ("UV_CONTRACT",),
    "RUNTIME_MATERIAL": (
        "BAKE_BASECOLOR",
        "BAKE_NORMAL",
        "BAKE_AO",
        "BAKE_ROUGHNESS",
        "BAKE_METALLIC",
        "BAKE_EMISSIVE",
    ),
    "PACKAGE_EXPORT": ("BUILD_GEOMETRY", "RUNTIME_MATERIAL", "DECAL_ASSET"),
    "EXPORT_ROUNDTRIP": ("PACKAGE_EXPORT",),
    "CATALOG_REGISTER": ("PACKAGE_EXPORT",),
    "ENGINE_SMOKE_TEST": ("EXPORT_ROUNDTRIP", "CATALOG_REGISTER"),
    "COMPLETION_GATE": ("ENGINE_SMOKE_TEST",),
}

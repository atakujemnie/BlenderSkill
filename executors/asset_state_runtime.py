from __future__ import annotations

"""Persistent, copy-on-write asset/component production state.

This module deliberately contains no Blender dependency. It is the canonical
external authoring state used to prepare scoped Blender tasks and preserve human
corrections between agent runs.
"""

from copy import deepcopy
from typing import Any, Mapping

EXECUTOR_ID = "ASSET_STATE_RUNTIME"
EXECUTOR_VERSION = "0.1.0"

ASSET_STAGES = (
    "BRIEF",
    "REFERENCE_ANALYSIS",
    "RECONSTRUCTION_MANIFEST",
    "BLOCKOUT",
    "STRUCTURAL_GEOMETRY",
    "DETAILS",
    "MATERIALS",
    "GAME_READY",
    "FIDELITY_AUDIT",
    "APPROVED",
)
COMPONENT_STATES = {
    "DECLARED",
    "CONSTRAINED",
    "READY_TO_BUILD",
    "BUILT_UNVERIFIED",
    "ACCEPTED",
    "UNVERIFIED",
    "FAIL",
    "BLOCKED",
    "DIRTY",
    "SUPERSEDED",
}
CORRECTION_PRIORITIES = {"SOFT", "HARD", "CANONICAL"}
CORRECTION_STATUSES = {"OPEN", "RESOLVED", "REJECTED", "SUPERSEDED"}


def _components(asset: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = asset.get("components", {})
    if isinstance(raw, Mapping):
        return {str(k): dict(v) for k, v in raw.items()}
    out: dict[str, dict[str, Any]] = {}
    for item in list(raw or []):
        node = dict(item)
        node_id = str(node.get("id") or "")
        if not node_id or node_id in out:
            raise ValueError("DUPLICATE_OR_EMPTY_COMPONENT_ID")
        out[node_id] = node
    return out


def _detect_parent_cycle(components: Mapping[str, Mapping[str, Any]]) -> list[str] | None:
    for start in components:
        seen: list[str] = []
        current: str | None = start
        while current:
            if current in seen:
                idx = seen.index(current)
                return seen[idx:] + [current]
            seen.append(current)
            parent = components.get(current, {}).get("parent")
            current = str(parent) if parent else None
    return None


def validate_asset(asset: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    if not str(asset.get("asset_id") or "").strip():
        blockers.append({"reason": "ASSET_ID_REQUIRED"})

    try:
        revision = int(asset.get("revision", 0))
        if revision < 1:
            blockers.append({"reason": "REVISION_MUST_BE_POSITIVE", "actual": revision})
    except (TypeError, ValueError):
        revision = 0
        blockers.append({"reason": "REVISION_INVALID"})

    stage = str(asset.get("stage", "")).upper()
    if stage not in ASSET_STAGES:
        blockers.append({"reason": "ASSET_STAGE_INVALID", "stage": stage})

    try:
        components = _components(asset)
    except ValueError as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": str(exc)}],
            "warnings": [],
        }

    if not components:
        blockers.append({"reason": "COMPONENT_TREE_REQUIRED"})

    roots: list[str] = []
    for component_id, component in components.items():
        state = str(component.get("state", "DECLARED")).upper()
        if state not in COMPONENT_STATES:
            blockers.append(
                {"reason": "COMPONENT_STATE_INVALID", "component_id": component_id, "state": state}
            )
        parent = component.get("parent")
        if parent:
            if str(parent) not in components:
                blockers.append(
                    {"reason": "COMPONENT_PARENT_MISSING", "component_id": component_id, "parent": str(parent)}
                )
        else:
            roots.append(component_id)

        anchors = component.get("anchors", {})
        if anchors is not None and not isinstance(anchors, Mapping):
            blockers.append({"reason": "ANCHORS_MUST_BE_MAPPING", "component_id": component_id})

        dimensions = component.get("dimensions", {})
        if dimensions is not None and not isinstance(dimensions, Mapping):
            blockers.append({"reason": "DIMENSIONS_MUST_BE_MAPPING", "component_id": component_id})

    if len(roots) != 1:
        blockers.append({"reason": "EXACTLY_ONE_COMPONENT_ROOT_REQUIRED", "roots": sorted(roots)})

    cycle = _detect_parent_cycle(components)
    if cycle:
        blockers.append({"reason": "COMPONENT_PARENT_CYCLE", "path": cycle})

    correction_ids: set[str] = set()
    for raw in list(asset.get("corrections", []) or []):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "CORRECTION_INVALID_RECORD"})
            continue
        correction = dict(raw)
        correction_id = str(correction.get("id") or "")
        if not correction_id:
            blockers.append({"reason": "CORRECTION_ID_REQUIRED"})
        elif correction_id in correction_ids:
            blockers.append({"reason": "DUPLICATE_CORRECTION_ID", "correction_id": correction_id})
        correction_ids.add(correction_id)

        target = str(correction.get("component_id") or "")
        if target not in components:
            blockers.append(
                {"reason": "CORRECTION_COMPONENT_MISSING", "correction_id": correction_id, "component_id": target}
            )
        priority = str(correction.get("priority", "HARD")).upper()
        if priority not in CORRECTION_PRIORITIES:
            blockers.append(
                {"reason": "CORRECTION_PRIORITY_INVALID", "correction_id": correction_id, "priority": priority}
            )
        status = str(correction.get("status", "OPEN")).upper()
        if status not in CORRECTION_STATUSES:
            blockers.append(
                {"reason": "CORRECTION_STATUS_INVALID", "correction_id": correction_id, "status": status}
            )
        if status == "RESOLVED" and correction.get("resolved_in_revision") is None:
            warnings.append(
                {"reason": "RESOLVED_CORRECTION_REVISION_MISSING", "correction_id": correction_id}
            )

    relations = list(asset.get("assembly_relations", []) or [])
    relation_ids: set[str] = set()
    for raw in relations:
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "ASSEMBLY_RELATION_INVALID_RECORD"})
            continue
        relation_id = str(raw.get("id") or raw.get("relation_id") or "")
        if not relation_id:
            blockers.append({"reason": "ASSEMBLY_RELATION_ID_REQUIRED"})
        elif relation_id in relation_ids:
            blockers.append({"reason": "DUPLICATE_ASSEMBLY_RELATION_ID", "relation_id": relation_id})
        relation_ids.add(relation_id)
        for side in ("a", "b"):
            endpoint = str(raw.get(side) or "")
            if "." not in endpoint:
                blockers.append(
                    {"reason": "ASSEMBLY_ENDPOINT_INVALID", "relation_id": relation_id, "side": side, "value": endpoint}
                )
                continue
            component_id, anchor_id = endpoint.split(".", 1)
            component = components.get(component_id)
            if component is None:
                blockers.append(
                    {"reason": "ASSEMBLY_COMPONENT_MISSING", "relation_id": relation_id, "component_id": component_id}
                )
            elif anchor_id not in dict(component.get("anchors", {})):
                blockers.append(
                    {
                        "reason": "ASSEMBLY_ANCHOR_MISSING",
                        "relation_id": relation_id,
                        "component_id": component_id,
                        "anchor_id": anchor_id,
                    }
                )

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "asset_id": asset.get("asset_id"),
        "revision": revision,
        "stage": stage,
        "component_count": len(components),
        "root_component_id": roots[0] if len(roots) == 1 else None,
        "open_corrections": sum(
            1 for item in list(asset.get("corrections", []) or [])
            if isinstance(item, Mapping) and str(item.get("status", "OPEN")).upper() == "OPEN"
        ),
        "blockers": blockers,
        "warnings": warnings,
    }


def _bump_revision(asset: dict[str, Any], event: Mapping[str, Any]) -> None:
    asset["revision"] = int(asset.get("revision", 0)) + 1
    history = list(asset.get("history", []) or [])
    history.append({"revision": asset["revision"], **dict(event)})
    asset["history"] = history


def add_correction(asset: Mapping[str, Any], correction: Mapping[str, Any]) -> dict[str, Any]:
    verdict = validate_asset(asset)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": verdict["blockers"]}

    cp = deepcopy(dict(asset))
    item = dict(correction)
    item["id"] = str(item.get("id") or "")
    item["component_id"] = str(item.get("component_id") or "")
    item["priority"] = str(item.get("priority", "HARD")).upper()
    item["status"] = str(item.get("status", "OPEN")).upper()
    existing = {str(c.get("id")) for c in list(cp.get("corrections", []) or []) if isinstance(c, Mapping)}

    blockers: list[dict[str, Any]] = []
    if not item["id"]:
        blockers.append({"reason": "CORRECTION_ID_REQUIRED"})
    if item["id"] in existing:
        blockers.append({"reason": "DUPLICATE_CORRECTION_ID", "correction_id": item["id"]})
    components = _components(cp)
    if item["component_id"] not in components:
        blockers.append({"reason": "CORRECTION_COMPONENT_MISSING", "component_id": item["component_id"]})
    if item["priority"] not in CORRECTION_PRIORITIES:
        blockers.append({"reason": "CORRECTION_PRIORITY_INVALID", "priority": item["priority"]})
    if item["status"] != "OPEN":
        blockers.append({"reason": "NEW_CORRECTION_MUST_BE_OPEN", "status": item["status"]})
    if blockers:
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": blockers}

    corrections = list(cp.get("corrections", []) or [])
    corrections.append(item)
    cp["corrections"] = corrections
    component = dict(components[item["component_id"]])
    if component.get("state") == "ACCEPTED":
        component["state"] = "DIRTY"
    components[item["component_id"]] = component
    cp["components"] = components
    _bump_revision(cp, {"event": "CORRECTION_ADDED", "correction_id": item["id"], "component_id": item["component_id"]})
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "asset": cp, "revision": cp["revision"]}


def resolve_correction(
    asset: Mapping[str, Any], correction_id: str, *, resolution: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    cp = deepcopy(dict(asset))
    corrections = list(cp.get("corrections", []) or [])
    found = False
    for index, raw in enumerate(corrections):
        if not isinstance(raw, Mapping) or str(raw.get("id")) != str(correction_id):
            continue
        item = dict(raw)
        if str(item.get("status", "OPEN")).upper() != "OPEN":
            return {
                "status": "FAIL",
                "validator_id": EXECUTOR_ID,
                "blockers": [{"reason": "CORRECTION_NOT_OPEN", "correction_id": correction_id}],
            }
        item["status"] = "RESOLVED"
        item["resolution"] = dict(resolution or {})
        corrections[index] = item
        found = True
        break
    if not found:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "CORRECTION_NOT_FOUND", "correction_id": correction_id}],
        }
    cp["corrections"] = corrections
    _bump_revision(cp, {"event": "CORRECTION_RESOLVED", "correction_id": correction_id})
    for index, raw in enumerate(cp["corrections"]):
        if isinstance(raw, Mapping) and str(raw.get("id")) == str(correction_id):
            item = dict(raw)
            item["resolved_in_revision"] = cp["revision"]
            cp["corrections"][index] = item
            break
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "asset": cp, "revision": cp["revision"]}


def advance_stage(asset: Mapping[str, Any], new_stage: str) -> dict[str, Any]:
    target = str(new_stage).upper()
    current = str(asset.get("stage", "")).upper()
    if current not in ASSET_STAGES or target not in ASSET_STAGES:
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "ASSET_STAGE_INVALID"}]}
    if ASSET_STAGES.index(target) != ASSET_STAGES.index(current) + 1:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "NON_SEQUENTIAL_STAGE_ADVANCE", "from": current, "to": target}],
        }
    hard_open = [
        str(item.get("id"))
        for item in list(asset.get("corrections", []) or [])
        if isinstance(item, Mapping)
        and str(item.get("status", "OPEN")).upper() == "OPEN"
        and str(item.get("priority", "HARD")).upper() in {"HARD", "CANONICAL"}
    ]
    if hard_open:
        return {
            "status": "BLOCKED",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "OPEN_HARD_CORRECTIONS", "correction_ids": sorted(hard_open)}],
        }
    cp = deepcopy(dict(asset))
    cp["stage"] = target
    _bump_revision(cp, {"event": "STAGE_ADVANCED", "from": current, "to": target})
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "asset": cp, "revision": cp["revision"]}


__all__ = [
    "ASSET_STAGES",
    "COMPONENT_STATES",
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "add_correction",
    "advance_stage",
    "resolve_correction",
    "validate_asset",
]

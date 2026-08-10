from __future__ import annotations

"""Deterministic authorization for component production tasks.

The caller requests authorization; this executor owns the PASS/BLOCKED decision
from persisted state. v0.22 permits an already ACCEPTED component to be reopened
for the next production stage; acceptance_level prevents a structural acceptance
from being mistaken for final completion.
"""

from typing import Any, Mapping

from executors.asset_state_runtime import ASSET_STAGES

EXECUTOR_ID = "ASSET_EXECUTION_AUTHORIZATION_GATE"
EXECUTOR_VERSION = "0.22.0"

_AUTHORIZABLE_STATES = {"CONSTRAINED", "DIRTY", "UNVERIFIED", "FAIL", "ACCEPTED"}


def evaluate(asset: Mapping[str, Any], component_id: str) -> dict[str, Any]:
    components = asset.get("components", {})
    if not isinstance(components, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "validator_version": EXECUTOR_VERSION,
            "source": "SYSTEM",
            "blockers": [{"reason": "COMPONENTS_MAPPING_REQUIRED"}],
        }

    component_id = str(component_id)
    component = components.get(component_id)
    if not isinstance(component, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "validator_version": EXECUTOR_VERSION,
            "source": "SYSTEM",
            "blockers": [{"reason": "COMPONENT_NOT_FOUND", "component_id": component_id}],
        }

    blockers: list[dict[str, Any]] = []
    stage = str(asset.get("stage") or "").upper()
    if stage not in ASSET_STAGES:
        blockers.append({"reason": "ASSET_STAGE_INVALID", "stage": stage})
    elif ASSET_STAGES.index(stage) < ASSET_STAGES.index("BLOCKOUT"):
        blockers.append({"reason": "ASSET_STAGE_NOT_BUILDABLE", "stage": stage, "minimum": "BLOCKOUT"})

    state = str(component.get("state") or "DECLARED").upper()
    if state not in _AUTHORIZABLE_STATES:
        blockers.append({"reason": "COMPONENT_STATE_NOT_AUTHORIZABLE", "state": state})

    dependencies = [str(value) for value in list(component.get("depends_on", []) or [])]
    incomplete = [
        dependency_id
        for dependency_id in dependencies
        if not isinstance(components.get(dependency_id), Mapping)
        or str(components[dependency_id].get("state") or "").upper() != "ACCEPTED"
    ]
    if incomplete:
        blockers.append({"reason": "COMPONENT_DEPENDENCY_NOT_ACCEPTED", "component_ids": sorted(incomplete)})

    open_hard: list[str] = []
    for raw in list(asset.get("corrections", []) or []):
        if not isinstance(raw, Mapping):
            continue
        if str(raw.get("component_id") or "") != component_id:
            continue
        if str(raw.get("status", "OPEN")).upper() != "OPEN":
            continue
        if str(raw.get("priority", "HARD")).upper() in {"HARD", "CANONICAL"}:
            open_hard.append(str(raw.get("id") or ""))
    if open_hard:
        blockers.append({"reason": "OPEN_HARD_COMPONENT_CORRECTIONS", "correction_ids": sorted(open_hard)})

    return {
        "status": "PASS" if not blockers else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "validator_version": EXECUTOR_VERSION,
        "source": "SYSTEM",
        "asset_id": asset.get("asset_id"),
        "asset_revision": int(asset.get("revision", 0)),
        "component_id": component_id,
        "asset_stage": stage,
        "component_state": state,
        "component_acceptance_level": component.get("acceptance_level"),
        "dependencies": dependencies,
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "evaluate"]

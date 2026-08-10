from __future__ import annotations

"""Build a compact UI view model for the asset production studio."""

from collections import Counter
from typing import Any, Mapping

from executors.asset_state_runtime import ASSET_STAGES, validate_asset
from executors.production_task_lifecycle import TASK_STATUSES

EXECUTOR_ID = "ASSET_STUDIO_VIEW_MODEL"
EXECUTOR_VERSION = "0.1.0"


def _components(asset: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw = asset.get("components", {})
    if isinstance(raw, Mapping):
        return {str(key): dict(value) for key, value in raw.items() if isinstance(value, Mapping)}
    return {
        str(item["id"]): dict(item)
        for item in list(raw or [])
        if isinstance(item, Mapping) and item.get("id")
    }


def build(
    asset: Mapping[str, Any],
    *,
    tasks: Mapping[str, Mapping[str, Any]] | None = None,
    selected_component_id: str | None = None,
    scene_snapshot: Mapping[str, Any] | None = None,
    design_impacts: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    validation = validate_asset(asset)
    if validation["status"] != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": validation["blockers"],
        }
    task_map = {str(key): dict(value) for key, value in (tasks or {}).items() if isinstance(value, Mapping)}
    components = _components(asset)
    selected = str(selected_component_id or next(iter(components), ""))
    if selected and selected not in components:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "STUDIO_COMPONENT_NOT_FOUND", "component_id": selected}],
        }

    open_corrections = [
        dict(item)
        for item in list(asset.get("corrections", []) or [])
        if isinstance(item, Mapping) and str(item.get("status", "OPEN")).upper() == "OPEN"
    ]
    tasks_by_component: dict[str, list[dict[str, Any]]] = {}
    for task in task_map.values():
        tasks_by_component.setdefault(str(task.get("component_id") or ""), []).append(task)
    for values in tasks_by_component.values():
        values.sort(key=lambda item: (int(item.get("priority", 100)), str(item.get("task_id"))))

    component_rows: list[dict[str, Any]] = []
    for component_id, component in components.items():
        corrections = [item for item in open_corrections if str(item.get("component_id") or "") == component_id]
        component_tasks = tasks_by_component.get(component_id, [])
        component_rows.append(
            {
                "component_id": component_id,
                "parent": component.get("parent"),
                "state": component.get("state"),
                "shape_class": component.get("shape_class"),
                "binding_count": len(list(component.get("binding_ids", []) or [])),
                "open_correction_count": len(corrections),
                "task_statuses": [str(task.get("status") or "") for task in component_tasks],
            }
        )
    component_rows.sort(key=lambda row: (str(row.get("parent") or ""), row["component_id"]))

    current_stage = str(asset.get("stage") or "BRIEF").upper()
    stage_index = ASSET_STAGES.index(current_stage)
    stages = [
        {
            "stage": stage,
            "state": "DONE" if index < stage_index else "CURRENT" if index == stage_index else "PENDING",
        }
        for index, stage in enumerate(ASSET_STAGES)
    ]
    task_counts = Counter(str(task.get("status") or "UNKNOWN").upper() for task in task_map.values())
    for status in TASK_STATUSES:
        task_counts.setdefault(status, 0)

    selected_component = components.get(selected, {})
    selected_corrections = [
        item for item in open_corrections if str(item.get("component_id") or "") == selected
    ]
    selected_tasks = tasks_by_component.get(selected, [])
    scene_objects = []
    if isinstance(scene_snapshot, Mapping):
        scene_objects = [
            dict(item)
            for item in list(scene_snapshot.get("objects", []) or [])
            if isinstance(item, Mapping) and str(item.get("component_id") or "") == selected
        ]

    view_model = {
        "schema_version": 1,
        "asset": {
            "asset_id": asset.get("asset_id"),
            "name": asset.get("name"),
            "revision": asset.get("revision"),
            "stage": current_stage,
            "progress": stage_index / max(1, len(ASSET_STAGES) - 1),
            "design_system_ids": list(asset.get("design_system_ids", []) or []),
            "global_dimensions_mm": dict(asset.get("global_dimensions_mm", {}) or {}),
        },
        "stages": stages,
        "components": component_rows,
        "task_summary": dict(sorted(task_counts.items())),
        "selected_component_id": selected,
        "inspector": {
            "component": selected_component,
            "open_corrections": selected_corrections,
            "tasks": selected_tasks,
            "scene_objects": scene_objects,
        },
        "design_impacts": [dict(item) for item in list(design_impacts or []) if isinstance(item, Mapping)],
        "scene_snapshot_hash": scene_snapshot.get("snapshot_hash") if isinstance(scene_snapshot, Mapping) else None,
    }
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "view_model": view_model,
        "blockers": [],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "build"]

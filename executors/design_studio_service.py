from __future__ import annotations

"""Operational listing and mutation service for shared design-system resources."""

import json
from pathlib import Path
from typing import Any, Mapping

from executors.design_system_repository import impact_report
from executors.design_system_repository import initialize as initialize_resource
from executors.design_system_repository import load as load_resource
from executors.design_system_repository import save as save_resource

EXECUTOR_ID = "DESIGN_STUDIO_SERVICE"
EXECUTOR_VERSION = "0.20.0"


def _root(root: str | Path) -> Path:
    return Path(root).expanduser().resolve() / "design_systems"


def list_design_systems(root: str | Path) -> dict[str, Any]:
    directory = _root(root)
    systems: list[dict[str, Any]] = []
    if not directory.is_dir():
        return {"status": "PASS", "executor_id": EXECUTOR_ID, "design_systems": [], "count": 0}
    for system_dir in sorted(directory.iterdir(), key=lambda path: path.name):
        resources_dir = system_dir / "resources"
        if not system_dir.is_dir() or not resources_dir.is_dir():
            continue
        resources = [path.name for path in resources_dir.iterdir() if path.is_dir() and (path / "resource.json").is_file()]
        systems.append(
            {
                "design_system_id": system_dir.name,
                "resource_count": len(resources),
                "resource_ids": sorted(resources),
            }
        )
    return {"status": "PASS", "executor_id": EXECUTOR_ID, "design_systems": systems, "count": len(systems)}


def list_resources(root: str | Path, *, design_system_id: str | None = None) -> dict[str, Any]:
    directory = _root(root)
    resources: list[dict[str, Any]] = []
    if not directory.is_dir():
        return {"status": "PASS", "executor_id": EXECUTOR_ID, "resources": [], "count": 0}
    systems = [directory / design_system_id] if design_system_id else sorted(directory.iterdir(), key=lambda path: path.name)
    for system_dir in systems:
        resources_dir = system_dir / "resources"
        if not resources_dir.is_dir():
            continue
        for resource_dir in sorted(resources_dir.iterdir(), key=lambda path: path.name):
            current = resource_dir / "resource.json"
            if not current.is_file():
                continue
            try:
                payload = json.loads(current.read_text(encoding="utf-8"))
            except Exception as exc:
                resources.append(
                    {
                        "design_system_id": system_dir.name,
                        "resource_id": resource_dir.name,
                        "status": "INVALID",
                        "error": str(exc),
                    }
                )
                continue
            usage = impact_report(root, system_dir.name, resource_dir.name)
            resources.append(
                {
                    "status": "PASS",
                    "design_system_id": system_dir.name,
                    "resource_id": payload.get("resource_id"),
                    "kind": payload.get("kind"),
                    "version": payload.get("version"),
                    "revision": payload.get("revision"),
                    "locked": bool(payload.get("locked", False)),
                    "payload": payload.get("payload", {}),
                    "affected_asset_count": usage.get("affected_asset_count", 0) if usage.get("status") == "PASS" else 0,
                }
            )
    return {"status": "PASS", "executor_id": EXECUTOR_ID, "resources": resources, "count": len(resources)}


def get_resource(root: str | Path, design_system_id: str, resource_id: str) -> dict[str, Any]:
    loaded = load_resource(root, design_system_id, resource_id)
    if loaded.get("status") != "PASS":
        return loaded
    impact = impact_report(root, design_system_id, resource_id)
    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "resource": loaded["resource"],
        "impact": impact if impact.get("status") == "PASS" else None,
        "blockers": [],
    }


def upsert_resource(
    root: str | Path,
    resource: Mapping[str, Any],
    *,
    expected_revision: int,
) -> dict[str, Any]:
    if int(expected_revision) == 0:
        created = initialize_resource(root, resource)
        return {
            **created,
            "executor_id": EXECUTOR_ID,
            "revision": int(resource.get("revision", 1)) if created.get("status") == "PASS" else None,
        }
    design_system_id = str(resource.get("design_system_id") or "")
    resource_id = str(resource.get("resource_id") or "")
    loaded = load_resource(root, design_system_id, resource_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_revision = int(loaded["resource"].get("revision", 0))
    if current_revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "executor_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "RESOURCE_REVISION_CONFLICT",
                    "expected": int(expected_revision),
                    "actual": current_revision,
                }
            ],
        }
    payload = dict(resource)
    payload["revision"] = current_revision + 1
    saved = save_resource(root, payload, expected_revision=current_revision)
    return {**saved, "executor_id": EXECUTOR_ID}


def resource_impact(root: str | Path, design_system_id: str, resource_id: str) -> dict[str, Any]:
    result = impact_report(root, design_system_id, resource_id)
    return {**result, "executor_id": EXECUTOR_ID}


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "get_resource",
    "list_design_systems",
    "list_resources",
    "resource_impact",
    "upsert_resource",
]

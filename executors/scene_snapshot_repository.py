from __future__ import annotations

"""Filesystem persistence for compact scene/component snapshots."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from executors.scene_component_snapshot import build as build_snapshot

EXECUTOR_ID = "SCENE_SNAPSHOT_REPOSITORY"
EXECUTOR_VERSION = "0.20.0"
SCHEMA_VERSION = 1


def _safe_id(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError("ASSET_ID_PATH_UNSAFE")
    return raw


def snapshot_dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id) / "scene_snapshots"


def validate_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    asset_id = str(snapshot.get("asset_id") or "").strip()
    if not asset_id:
        blockers.append({"reason": "SNAPSHOT_ASSET_ID_REQUIRED"})
    try:
        scene_revision = int(snapshot.get("scene_revision", 0))
    except (TypeError, ValueError):
        scene_revision = -1
    if scene_revision < 1:
        blockers.append({"reason": "SCENE_REVISION_POSITIVE_REQUIRED"})

    objects = snapshot.get("objects")
    if not isinstance(objects, list):
        blockers.append({"reason": "SNAPSHOT_OBJECT_LIST_REQUIRED"})
    else:
        rebuilt = build_snapshot(
            {
                "asset_id": snapshot.get("asset_id"),
                "asset_revision": snapshot.get("asset_revision"),
                "scene_revision": snapshot.get("scene_revision"),
                "objects": objects,
            },
            component_ids=[str(value) for value in list(snapshot.get("component_scope", []) or [])],
        )
        if rebuilt["status"] != "PASS":
            blockers.extend(rebuilt.get("blockers", []))
        elif snapshot.get("snapshot_hash") and rebuilt["snapshot"]["snapshot_hash"] != snapshot.get("snapshot_hash"):
            blockers.append(
                {
                    "reason": "SNAPSHOT_HASH_MISMATCH",
                    "declared": snapshot.get("snapshot_hash"),
                    "actual": rebuilt["snapshot"]["snapshot_hash"],
                }
            )
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "scene_revision": scene_revision,
        "blockers": blockers,
    }


def publish(root: str | Path, snapshot: Mapping[str, Any]) -> dict[str, Any]:
    verdict = validate_snapshot(snapshot)
    if verdict["status"] != "PASS":
        return verdict
    path = snapshot_dir(root, str(snapshot["asset_id"]))
    path.mkdir(parents=True, exist_ok=True)
    current = path / "current.json"
    revisions = path / "revisions"
    revisions.mkdir(exist_ok=True)

    scene_revision = int(snapshot["scene_revision"])
    if current.is_file():
        existing = json.loads(current.read_text(encoding="utf-8"))
        previous = int(existing.get("scene_revision", 0))
        if scene_revision <= previous:
            return {
                "status": "FAIL",
                "validator_id": EXECUTOR_ID,
                "blockers": [
                    {
                        "reason": "SCENE_REVISION_NOT_MONOTONIC",
                        "previous": previous,
                        "new": scene_revision,
                    }
                ],
            }

    payload = dict(snapshot)
    payload.setdefault("schema_version", SCHEMA_VERSION)
    revision_path = revisions / f"s{scene_revision:06d}.json"
    if revision_path.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "SCENE_REVISION_ALREADY_EXISTS", "scene_revision": scene_revision}],
        }
    _atomic_write(current, payload)
    _atomic_write(revision_path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "asset_id": payload.get("asset_id"),
        "scene_revision": scene_revision,
        "snapshot_hash": payload.get("snapshot_hash"),
        "path": str(current),
    }


def load(root: str | Path, asset_id: str, scene_revision: int | None = None) -> dict[str, Any]:
    path = snapshot_dir(root, asset_id)
    source = path / "current.json" if scene_revision is None else path / "revisions" / f"s{int(scene_revision):06d}.json"
    if not source.is_file():
        return {
            "status": "NOT_FOUND",
            "validator_id": EXECUTOR_ID,
            "snapshot": None,
            "blockers": [{"reason": "SCENE_SNAPSHOT_NOT_FOUND", "path": str(source)}],
        }
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "snapshot": None,
            "blockers": [{"reason": "SCENE_SNAPSHOT_INVALID_JSON", "error": str(exc)}],
        }
    verdict = validate_snapshot(payload)
    return {
        "status": verdict["status"],
        "validator_id": EXECUTOR_ID,
        "snapshot": payload,
        "path": str(source),
        "blockers": verdict["blockers"],
    }


def list_revisions(root: str | Path, asset_id: str) -> dict[str, Any]:
    revisions = snapshot_dir(root, asset_id) / "revisions"
    if not revisions.is_dir():
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "scene_revisions": []}
    values = [
        int(path.stem[1:])
        for path in sorted(revisions.glob("s*.json"))
        if path.stem[1:].isdigit()
    ]
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "scene_revisions": values}


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temporary = Path(handle.name)
    os.replace(temporary, path)


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "list_revisions",
    "load",
    "publish",
    "snapshot_dir",
    "validate_snapshot",
]

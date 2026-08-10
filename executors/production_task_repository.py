from __future__ import annotations

"""Filesystem persistence for asset-scoped production task queues."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from executors.production_task_lifecycle import validate_task

EXECUTOR_ID = "PRODUCTION_TASK_REPOSITORY"
EXECUTOR_VERSION = "0.1.0"
SCHEMA_VERSION = 1


def _safe_id(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError("ASSET_ID_PATH_UNSAFE")
    return raw


def queue_dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id) / "production_tasks"


def _validate_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    if not str(payload.get("asset_id") or "").strip():
        blockers.append({"reason": "TASK_QUEUE_ASSET_ID_REQUIRED"})
    try:
        queue_revision = int(payload.get("queue_revision", 0))
    except (TypeError, ValueError):
        queue_revision = -1
    if queue_revision < 1:
        blockers.append({"reason": "TASK_QUEUE_REVISION_POSITIVE_REQUIRED"})
    tasks = payload.get("tasks", {})
    if not isinstance(tasks, Mapping):
        blockers.append({"reason": "TASK_QUEUE_MAPPING_REQUIRED"})
    else:
        for task_id, raw in tasks.items():
            if not isinstance(raw, Mapping):
                blockers.append({"reason": "TASK_QUEUE_RECORD_INVALID", "task_id": str(task_id)})
                continue
            if str(raw.get("task_id") or "") != str(task_id):
                blockers.append({"reason": "TASK_QUEUE_ID_MISMATCH", "task_id": str(task_id)})
            verdict = validate_task(raw)
            blockers.extend({"task_id": str(task_id), **item} for item in verdict["blockers"])
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
    }


def initialize(root: str | Path, asset_id: str, tasks: Mapping[str, Mapping[str, Any]] | None = None) -> dict[str, Any]:
    path = queue_dir(root, asset_id)
    current = path / "tasks.json"
    if current.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_QUEUE_ALREADY_EXISTS", "path": str(current)}],
        }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "queue_revision": 1,
        "tasks": {str(task_id): dict(task) for task_id, task in (tasks or {}).items()},
    }
    verdict = _validate_payload(payload)
    if verdict["status"] != "PASS":
        return verdict
    path.mkdir(parents=True, exist_ok=False)
    (path / "revisions").mkdir()
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "path": str(current),
        "queue": payload,
    }


def load(root: str | Path, asset_id: str, revision: int | None = None) -> dict[str, Any]:
    path = queue_dir(root, asset_id)
    source = path / "tasks.json" if revision is None else path / "revisions" / f"r{int(revision):06d}.json"
    if not source.is_file():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_QUEUE_NOT_FOUND", "path": str(source)}],
        }
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_QUEUE_INVALID_JSON", "error": str(exc)}],
        }
    verdict = _validate_payload(payload)
    return {
        "status": verdict["status"],
        "validator_id": EXECUTOR_ID,
        "path": str(source),
        "queue": payload,
        "blockers": verdict["blockers"],
    }


def save(
    root: str | Path,
    asset_id: str,
    tasks: Mapping[str, Mapping[str, Any]],
    *,
    expected_queue_revision: int,
) -> dict[str, Any]:
    current = load(root, asset_id)
    if current["status"] != "PASS":
        return current
    previous_revision = int(current["queue"]["queue_revision"])
    if previous_revision != int(expected_queue_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "TASK_QUEUE_REVISION_CONFLICT",
                    "expected": int(expected_queue_revision),
                    "actual": previous_revision,
                }
            ],
        }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "queue_revision": previous_revision + 1,
        "tasks": {str(task_id): dict(task) for task_id, task in tasks.items()},
    }
    verdict = _validate_payload(payload)
    if verdict["status"] != "PASS":
        return verdict
    path = queue_dir(root, asset_id)
    _atomic_write(path / "tasks.json", payload)
    _write_revision(path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "queue_revision": payload["queue_revision"],
        "task_count": len(payload["tasks"]),
    }


def upsert_task(
    root: str | Path,
    asset_id: str,
    task: Mapping[str, Any],
    *,
    expected_queue_revision: int,
) -> dict[str, Any]:
    verdict = validate_task(task)
    if verdict["status"] != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": verdict["blockers"],
        }
    loaded = load(root, asset_id)
    if loaded["status"] != "PASS":
        return loaded
    tasks = {str(task_id): dict(value) for task_id, value in loaded["queue"]["tasks"].items()}
    tasks[str(task["task_id"])] = dict(task)
    return save(
        root,
        asset_id,
        tasks,
        expected_queue_revision=expected_queue_revision,
    )


def list_revisions(root: str | Path, asset_id: str) -> dict[str, Any]:
    revisions_dir = queue_dir(root, asset_id) / "revisions"
    if not revisions_dir.is_dir():
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": []}
    revisions = [
        int(path.stem[1:])
        for path in sorted(revisions_dir.glob("r*.json"))
        if path.stem[1:].isdigit()
    ]
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": revisions}


def _write_revision(path: Path, payload: Mapping[str, Any]) -> None:
    revision = int(payload["queue_revision"])
    target = path / "revisions" / f"r{revision:06d}.json"
    if target.exists():
        raise FileExistsError(f"TASK_QUEUE_REVISION_ALREADY_EXISTS:{revision}")
    _atomic_write(target, payload)


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temporary = Path(handle.name)
    os.replace(temporary, path)


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "initialize",
    "list_revisions",
    "load",
    "queue_dir",
    "save",
    "upsert_task",
]

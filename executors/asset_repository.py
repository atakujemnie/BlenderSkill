from __future__ import annotations

"""Filesystem persistence for canonical asset production state.

The repository stores one current JSON state plus immutable revision snapshots.
It is intentionally independent from Blender and LLM providers.
"""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from executors.asset_state_runtime import validate_asset

EXECUTOR_ID = "ASSET_REPOSITORY"
EXECUTOR_VERSION = "0.1.0"
SCHEMA_VERSION = 1


def _safe_id(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError("ASSET_ID_PATH_UNSAFE")
    return raw


def asset_dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id)


def initialize(root: str | Path, asset: Mapping[str, Any]) -> dict[str, Any]:
    verdict = validate_asset(asset)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": verdict["blockers"]}
    path = asset_dir(root, str(asset["asset_id"]))
    current = path / "asset.json"
    if current.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ASSET_ALREADY_EXISTS", "path": str(current)}],
        }
    path.mkdir(parents=True, exist_ok=False)
    (path / "revisions").mkdir()
    payload = dict(asset)
    payload.setdefault("schema_version", SCHEMA_VERSION)
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "path": str(current), "asset": payload}


def load(root: str | Path, asset_id: str, revision: int | None = None) -> dict[str, Any]:
    path = asset_dir(root, asset_id)
    source = path / "asset.json" if revision is None else path / "revisions" / f"r{int(revision):06d}.json"
    if not source.is_file():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ASSET_STATE_NOT_FOUND", "path": str(source)}],
        }
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ASSET_STATE_INVALID_JSON", "error": str(exc)}],
        }
    verdict = validate_asset(payload)
    return {
        "status": "PASS" if verdict["status"] == "PASS" else "FAIL",
        "validator_id": EXECUTOR_ID,
        "path": str(source),
        "asset": payload,
        "validation": verdict,
        "blockers": verdict["blockers"],
    }


def save(
    root: str | Path,
    asset: Mapping[str, Any],
    *,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    verdict = validate_asset(asset)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": verdict["blockers"]}
    path = asset_dir(root, str(asset["asset_id"]))
    current = path / "asset.json"
    if not current.is_file():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ASSET_NOT_INITIALIZED", "path": str(current)}],
        }
    existing = json.loads(current.read_text(encoding="utf-8"))
    existing_revision = int(existing.get("revision", 0))
    if expected_revision is not None and existing_revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "ASSET_REVISION_CONFLICT",
                    "expected": int(expected_revision),
                    "actual": existing_revision,
                }
            ],
        }
    new_revision = int(asset.get("revision", 0))
    if new_revision <= existing_revision:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "ASSET_REVISION_NOT_MONOTONIC",
                    "previous": existing_revision,
                    "new": new_revision,
                }
            ],
        }
    payload = dict(asset)
    payload.setdefault("schema_version", SCHEMA_VERSION)
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "path": str(current), "revision": new_revision}


def list_revisions(root: str | Path, asset_id: str) -> dict[str, Any]:
    revisions_dir = asset_dir(root, asset_id) / "revisions"
    if not revisions_dir.is_dir():
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": []}
    revisions = [int(path.stem[1:]) for path in sorted(revisions_dir.glob("r*.json")) if path.stem[1:].isdigit()]
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": revisions}


def _write_revision(path: Path, payload: Mapping[str, Any]) -> None:
    revision = int(payload.get("revision", 0))
    target = path / "revisions" / f"r{revision:06d}.json"
    if target.exists():
        raise FileExistsError(f"REVISION_SNAPSHOT_ALREADY_EXISTS:{revision}")
    _atomic_write(target, payload)


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "asset_dir", "initialize", "list_revisions", "load", "save"]

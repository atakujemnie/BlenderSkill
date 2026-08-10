from __future__ import annotations

"""Revisioned persistence for independent asset-level visual fidelity reviews."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

EXECUTOR_ID = "FIDELITY_REVIEW_REPOSITORY"
EXECUTOR_VERSION = "0.22.0"
SCHEMA_VERSION = 1


def _safe_id(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError("ASSET_ID_PATH_UNSAFE")
    return raw


def review_dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id) / "fidelity_reviews"


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")
        temp_name = handle.name
    os.replace(temp_name, path)


def initialize(root: str | Path, asset_id: str) -> dict[str, Any]:
    path = review_dir(root, asset_id)
    current = path / "review.json"
    if current.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "FIDELITY_REVIEW_REPOSITORY_ALREADY_EXISTS", "path": str(current)}],
        }
    path.mkdir(parents=True, exist_ok=False)
    (path / "revisions").mkdir()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "revision": 0,
        "review": None,
    }
    _atomic_write(current, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": 0, "path": str(current)}


def load(root: str | Path, asset_id: str, revision: int | None = None) -> dict[str, Any]:
    path = review_dir(root, asset_id)
    target = path / "review.json" if revision is None else path / "revisions" / f"r{int(revision):06d}.json"
    if not target.is_file():
        return {
            "status": "NOT_FOUND",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "FIDELITY_REVIEW_NOT_FOUND", "path": str(target)}],
        }
    payload = json.loads(target.read_text(encoding="utf-8"))
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "revision": int(payload.get("revision", 0)),
        "review": payload.get("review"),
        "record": payload,
    }


def publish(
    root: str | Path,
    asset_id: str,
    review: Mapping[str, Any],
    *,
    expected_revision: int,
) -> dict[str, Any]:
    loaded = load(root, asset_id)
    if loaded.get("status") == "NOT_FOUND":
        initialized = initialize(root, asset_id)
        if initialized.get("status") != "PASS":
            return initialized
        current_revision = 0
    elif loaded.get("status") == "PASS":
        current_revision = int(loaded.get("revision", 0))
    else:
        return loaded
    if current_revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "FIDELITY_REVIEW_REVISION_CONFLICT",
                    "expected": int(expected_revision),
                    "actual": current_revision,
                }
            ],
        }
    new_revision = current_revision + 1
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "revision": new_revision,
        "review": dict(review),
    }
    path = review_dir(root, asset_id)
    _atomic_write(path / "review.json", payload)
    _atomic_write(path / "revisions" / f"r{new_revision:06d}.json", payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "revision": new_revision,
        "review": dict(review),
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "initialize", "load", "publish", "review_dir"]

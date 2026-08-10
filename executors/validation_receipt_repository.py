from __future__ import annotations

"""Persist trusted validator receipts outside worker-supplied task results."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

EXECUTOR_ID = "VALIDATION_RECEIPT_REPOSITORY"
EXECUTOR_VERSION = "0.21.0"
SCHEMA_VERSION = 1


def _safe_id(value: Any, *, field: str) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError(f"{field}_PATH_UNSAFE")
    return raw


def _dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id, field="ASSET_ID") / "validation_receipts"


def _current(root: str | Path, asset_id: str) -> Path:
    return _dir(root, asset_id) / "receipts.json"


def validate_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    required = ("receipt_id", "validator_id", "validator_version", "asset_id", "asset_revision", "component_id", "scene_revision", "status")
    missing = [field for field in required if receipt.get(field) in (None, "")]
    if missing:
        blockers.append({"reason": "VALIDATION_RECEIPT_FIELDS_REQUIRED", "fields": missing})
    if str(receipt.get("status") or "").upper() not in {"PASS", "FAIL", "BLOCKED"}:
        blockers.append({"reason": "VALIDATION_RECEIPT_STATUS_INVALID"})
    try:
        if int(receipt.get("asset_revision", 0)) < 1:
            blockers.append({"reason": "VALIDATION_RECEIPT_ASSET_REVISION_INVALID"})
        if int(receipt.get("scene_revision", 0)) < 1:
            blockers.append({"reason": "VALIDATION_RECEIPT_SCENE_REVISION_INVALID"})
    except (TypeError, ValueError):
        blockers.append({"reason": "VALIDATION_RECEIPT_REVISION_INTEGER_REQUIRED"})
    if str(receipt.get("source") or "SYSTEM").upper() != "SYSTEM":
        blockers.append({"reason": "VALIDATION_RECEIPT_SOURCE_MUST_BE_SYSTEM"})
    return {"status": "PASS" if not blockers else "FAIL", "validator_id": EXECUTOR_ID, "blockers": blockers}


def initialize(root: str | Path, asset_id: str) -> dict[str, Any]:
    path = _current(root, asset_id)
    if path.exists():
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": load(root, asset_id)["revision"]}
    directory = path.parent
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "revisions").mkdir(exist_ok=True)
    payload = {"schema_version": SCHEMA_VERSION, "asset_id": asset_id, "revision": 1, "receipts": []}
    _atomic_write(path, payload)
    _write_revision(directory, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": 1}


def load(root: str | Path, asset_id: str) -> dict[str, Any]:
    path = _current(root, asset_id)
    if not path.is_file():
        return {"status": "NOT_FOUND", "validator_id": EXECUTOR_ID, "revision": 0, "receipts": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "revision": int(payload.get("revision", 0)),
        "receipts": [dict(item) for item in list(payload.get("receipts", []) or []) if isinstance(item, Mapping)],
    }


def publish(root: str | Path, asset_id: str, receipt: Mapping[str, Any], *, expected_revision: int | None = None) -> dict[str, Any]:
    verdict = validate_receipt(receipt)
    if verdict["status"] != "PASS":
        return verdict
    if str(receipt.get("asset_id")) != str(asset_id):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "VALIDATION_RECEIPT_ASSET_MISMATCH"}],
        }
    current = load(root, asset_id)
    if current["status"] == "NOT_FOUND":
        initialize(root, asset_id)
        current = load(root, asset_id)
    revision = int(current["revision"])
    if expected_revision is not None and revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "VALIDATION_RECEIPT_REVISION_CONFLICT", "expected": int(expected_revision), "actual": revision}],
        }
    receipts = [dict(item) for item in current["receipts"]]
    receipt_id = str(receipt["receipt_id"])
    if any(str(item.get("receipt_id")) == receipt_id for item in receipts):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "VALIDATION_RECEIPT_ID_IMMUTABLE", "receipt_id": receipt_id}],
        }
    normalized = dict(receipt)
    normalized["source"] = "SYSTEM"
    normalized["status"] = str(normalized["status"]).upper()
    receipts.append(normalized)
    receipts.sort(key=lambda item: str(item.get("receipt_id")))
    payload = {"schema_version": SCHEMA_VERSION, "asset_id": asset_id, "revision": revision + 1, "receipts": receipts}
    directory = _dir(root, asset_id)
    _atomic_write(_current(root, asset_id), payload)
    _write_revision(directory, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": revision + 1, "receipt": normalized}


def query(
    root: str | Path,
    asset_id: str,
    *,
    component_id: str,
    asset_revision: int,
    scene_revision: int | None = None,
    validator_ids: list[str] | None = None,
) -> dict[str, Any]:
    current = load(root, asset_id)
    if current["status"] == "NOT_FOUND":
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": 0, "receipts": []}
    required = {str(value) for value in list(validator_ids or [])}
    receipts = []
    for item in current["receipts"]:
        if str(item.get("component_id")) != str(component_id):
            continue
        if int(item.get("asset_revision", 0)) != int(asset_revision):
            continue
        if scene_revision is not None and int(item.get("scene_revision", 0)) != int(scene_revision):
            continue
        if required and str(item.get("validator_id")) not in required:
            continue
        receipts.append(dict(item))
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revision": current["revision"], "receipts": receipts}


def _write_revision(directory: Path, payload: Mapping[str, Any]) -> None:
    target = directory / "revisions" / f"r{int(payload['revision']):06d}.json"
    if target.exists():
        raise FileExistsError(f"VALIDATION_RECEIPT_REVISION_EXISTS:{payload['revision']}")
    _atomic_write(target, payload)


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temp = Path(handle.name)
    os.replace(temp, path)


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "initialize", "load", "publish", "query", "validate_receipt"]

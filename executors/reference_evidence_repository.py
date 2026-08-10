from __future__ import annotations

"""Revisioned persistence for asset-scoped reference evidence registries."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

from executors.reference_evidence_registry import validate

EXECUTOR_ID = "REFERENCE_EVIDENCE_REPOSITORY"
EXECUTOR_VERSION = "0.20.0-dev"
SCHEMA_VERSION = 1


def _safe_id(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError("ASSET_ID_PATH_UNSAFE")
    return raw


def evidence_dir(root: str | Path, asset_id: str) -> Path:
    return Path(root).expanduser().resolve() / "assets" / _safe_id(asset_id) / "reference_evidence"


def initialize(root: str | Path, asset_id: str, registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload_registry = dict(registry or {"evidence": []})
    verdict = validate(payload_registry)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": verdict["blockers"]}
    path = evidence_dir(root, asset_id)
    current = path / "evidence.json"
    if current.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "REFERENCE_EVIDENCE_ALREADY_EXISTS", "path": str(current)}],
        }
    path.mkdir(parents=True, exist_ok=False)
    (path / "revisions").mkdir()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "revision": 1,
        "evidence": list(payload_registry.get("evidence", []) or []),
    }
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "registry": payload, "path": str(current)}


def load(root: str | Path, asset_id: str, revision: int | None = None) -> dict[str, Any]:
    path = evidence_dir(root, asset_id)
    source = path / "evidence.json" if revision is None else path / "revisions" / f"r{int(revision):06d}.json"
    if not source.is_file():
        return {
            "status": "NOT_FOUND",
            "validator_id": EXECUTOR_ID,
            "registry": None,
            "blockers": [{"reason": "REFERENCE_EVIDENCE_NOT_FOUND", "path": str(source)}],
        }
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "registry": None,
            "blockers": [{"reason": "REFERENCE_EVIDENCE_INVALID_JSON", "error": str(exc)}],
        }
    verdict = validate(payload)
    blockers = list(verdict.get("blockers", []))
    if str(payload.get("asset_id") or "") != str(asset_id):
        blockers.append({"reason": "REFERENCE_EVIDENCE_ASSET_ID_MISMATCH"})
    try:
        payload_revision = int(payload.get("revision", 0))
    except (TypeError, ValueError):
        payload_revision = 0
    if payload_revision < 1:
        blockers.append({"reason": "REFERENCE_EVIDENCE_REVISION_POSITIVE_REQUIRED"})
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "registry": payload,
        "path": str(source),
        "blockers": blockers,
    }


def save(
    root: str | Path,
    asset_id: str,
    registry: Mapping[str, Any],
    *,
    expected_revision: int,
) -> dict[str, Any]:
    current = load(root, asset_id)
    if current["status"] != "PASS":
        return current
    previous_revision = int(current["registry"]["revision"])
    if previous_revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "REFERENCE_EVIDENCE_REVISION_CONFLICT",
                    "expected": int(expected_revision),
                    "actual": previous_revision,
                }
            ],
        }
    payload_registry = {"evidence": list(registry.get("evidence", []) or [])}
    verdict = validate(payload_registry)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "validator_id": EXECUTOR_ID, "blockers": verdict["blockers"]}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "asset_id": str(asset_id),
        "revision": previous_revision + 1,
        "evidence": payload_registry["evidence"],
    }
    path = evidence_dir(root, asset_id)
    _atomic_write(path / "evidence.json", payload)
    _write_revision(path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "revision": payload["revision"],
        "evidence_count": len(payload["evidence"]),
    }


def upsert(
    root: str | Path,
    asset_id: str,
    evidence: Mapping[str, Any],
    *,
    expected_revision: int,
) -> dict[str, Any]:
    loaded = load(root, asset_id)
    if loaded["status"] != "PASS":
        return loaded
    evidence_id = str(evidence.get("evidence_id") or "")
    if not evidence_id:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "EVIDENCE_ID_REQUIRED"}],
        }
    records = [dict(item) for item in list(loaded["registry"].get("evidence", []) or []) if isinstance(item, Mapping)]
    replaced = False
    for index, record in enumerate(records):
        if str(record.get("evidence_id") or "") == evidence_id:
            records[index] = dict(evidence)
            replaced = True
            break
    if not replaced:
        records.append(dict(evidence))
    records.sort(key=lambda item: str(item.get("evidence_id") or ""))
    return save(root, asset_id, {"evidence": records}, expected_revision=expected_revision)


def remove(
    root: str | Path,
    asset_id: str,
    evidence_id: str,
    *,
    expected_revision: int,
) -> dict[str, Any]:
    loaded = load(root, asset_id)
    if loaded["status"] != "PASS":
        return loaded
    records = [dict(item) for item in list(loaded["registry"].get("evidence", []) or []) if isinstance(item, Mapping)]
    filtered = [record for record in records if str(record.get("evidence_id") or "") != str(evidence_id)]
    if len(filtered) == len(records):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "REFERENCE_EVIDENCE_ID_NOT_FOUND", "evidence_id": str(evidence_id)}],
        }
    return save(root, asset_id, {"evidence": filtered}, expected_revision=expected_revision)


def list_revisions(root: str | Path, asset_id: str) -> dict[str, Any]:
    revisions = evidence_dir(root, asset_id) / "revisions"
    if not revisions.is_dir():
        return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": []}
    values = [
        int(path.stem[1:])
        for path in sorted(revisions.glob("r*.json"))
        if path.stem[1:].isdigit()
    ]
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "revisions": values}


def _write_revision(path: Path, payload: Mapping[str, Any]) -> None:
    revision = int(payload["revision"])
    target = path / "revisions" / f"r{revision:06d}.json"
    if target.exists():
        raise FileExistsError(f"REFERENCE_EVIDENCE_REVISION_ALREADY_EXISTS:{revision}")
    _atomic_write(target, payload)


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temporary = Path(handle.name)
    os.replace(temporary, path)


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "evidence_dir",
    "initialize",
    "list_revisions",
    "load",
    "remove",
    "save",
    "upsert",
]

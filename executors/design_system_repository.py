from __future__ import annotations

"""Versioned design-system resource repository with reverse-usage tracking."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping

EXECUTOR_ID = "DESIGN_SYSTEM_REPOSITORY"
EXECUTOR_VERSION = "0.1.0"
SCHEMA_VERSION = 1
RESOURCE_KINDS = {
    "MATERIAL",
    "TEXTURE_SET",
    "TRIM_PROFILE",
    "EDGE_PROFILE",
    "LED_PROFILE",
    "DETAIL_MODULE",
    "DECAL",
    "FASTENER",
    "GEOMETRY_MODULE",
    "NODE_GROUP",
}


def _safe_id(value: Any, *, field: str) -> str:
    raw = str(value or "").strip()
    if not raw or any(part in raw for part in ("/", "\\", "..")):
        raise ValueError(f"{field}_PATH_UNSAFE")
    return raw


def _resource_dir(root: str | Path, design_system_id: str, resource_id: str) -> Path:
    return (
        Path(root).expanduser().resolve()
        / "design_systems"
        / _safe_id(design_system_id, field="DESIGN_SYSTEM_ID")
        / "resources"
        / _safe_id(resource_id, field="RESOURCE_ID")
    )


def validate_resource(resource: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    design_system_id = str(resource.get("design_system_id") or "").strip()
    resource_id = str(resource.get("resource_id") or "").strip()
    kind = str(resource.get("kind") or "").upper()
    version = str(resource.get("version") or "").strip()
    try:
        revision = int(resource.get("revision", 0))
    except (TypeError, ValueError):
        revision = -1

    if not design_system_id:
        blockers.append({"reason": "DESIGN_SYSTEM_ID_REQUIRED"})
    if not resource_id:
        blockers.append({"reason": "RESOURCE_ID_REQUIRED"})
    if kind not in RESOURCE_KINDS:
        blockers.append({"reason": "RESOURCE_KIND_INVALID", "kind": kind})
    if not version:
        blockers.append({"reason": "RESOURCE_VERSION_REQUIRED"})
    if revision < 1:
        blockers.append({"reason": "RESOURCE_REVISION_POSITIVE_REQUIRED"})
    payload = resource.get("payload")
    if not isinstance(payload, Mapping):
        blockers.append({"reason": "RESOURCE_PAYLOAD_MAPPING_REQUIRED"})

    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
    }


def initialize(root: str | Path, resource: Mapping[str, Any]) -> dict[str, Any]:
    verdict = validate_resource(resource)
    if verdict["status"] != "PASS":
        return verdict
    path = _resource_dir(root, str(resource["design_system_id"]), str(resource["resource_id"]))
    current = path / "resource.json"
    if current.exists():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "RESOURCE_ALREADY_EXISTS", "path": str(current)}],
        }
    path.mkdir(parents=True, exist_ok=False)
    (path / "revisions").mkdir()
    payload = dict(resource)
    payload.setdefault("schema_version", SCHEMA_VERSION)
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "path": str(current),
        "resource": payload,
    }


def load(
    root: str | Path,
    design_system_id: str,
    resource_id: str,
    revision: int | None = None,
) -> dict[str, Any]:
    path = _resource_dir(root, design_system_id, resource_id)
    source = path / "resource.json" if revision is None else path / "revisions" / f"r{int(revision):06d}.json"
    if not source.is_file():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "RESOURCE_NOT_FOUND", "path": str(source)}],
        }
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "RESOURCE_INVALID_JSON", "error": str(exc)}],
        }
    verdict = validate_resource(payload)
    return {
        "status": verdict["status"],
        "validator_id": EXECUTOR_ID,
        "path": str(source),
        "resource": payload,
        "blockers": verdict["blockers"],
    }


def save(
    root: str | Path,
    resource: Mapping[str, Any],
    *,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    verdict = validate_resource(resource)
    if verdict["status"] != "PASS":
        return verdict
    path = _resource_dir(root, str(resource["design_system_id"]), str(resource["resource_id"]))
    current = path / "resource.json"
    if not current.is_file():
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "RESOURCE_NOT_INITIALIZED", "path": str(current)}],
        }
    existing = json.loads(current.read_text(encoding="utf-8"))
    previous_revision = int(existing.get("revision", 0))
    if expected_revision is not None and previous_revision != int(expected_revision):
        return {
            "status": "CONFLICT",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "RESOURCE_REVISION_CONFLICT",
                    "expected": int(expected_revision),
                    "actual": previous_revision,
                }
            ],
        }
    new_revision = int(resource.get("revision", 0))
    if new_revision <= previous_revision:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "RESOURCE_REVISION_NOT_MONOTONIC",
                    "previous": previous_revision,
                    "new": new_revision,
                }
            ],
        }
    payload = dict(resource)
    payload.setdefault("schema_version", SCHEMA_VERSION)
    _atomic_write(current, payload)
    _write_revision(path, payload)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "revision": new_revision,
        "version": payload.get("version"),
        "resource_id": payload.get("resource_id"),
    }


def resolve_binding(root: str | Path, binding: Mapping[str, Any]) -> dict[str, Any]:
    design_system_id = str(binding.get("design_system_id") or "")
    resource_id = str(binding.get("resource_id") or "")
    revision = binding.get("resource_revision")
    loaded = load(root, design_system_id, resource_id, int(revision) if revision is not None else None)
    if loaded["status"] != "PASS":
        return loaded
    resource = loaded["resource"]
    requested_version = binding.get("resource_version")
    if requested_version is not None and str(requested_version) != str(resource.get("version")):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [
                {
                    "reason": "RESOURCE_VERSION_MISMATCH",
                    "requested": str(requested_version),
                    "resolved": str(resource.get("version")),
                }
            ],
        }
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "binding_id": binding.get("binding_id"),
        "resource": resource,
        "locked": bool(resource.get("locked", False)),
    }


def record_usage(root: str | Path, usage: Mapping[str, Any]) -> dict[str, Any]:
    required = ("design_system_id", "resource_id", "asset_id", "component_id", "binding_id")
    missing = [field for field in required if not str(usage.get(field) or "").strip()]
    if missing:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "USAGE_FIELDS_REQUIRED", "fields": missing}],
        }
    resource = load(root, str(usage["design_system_id"]), str(usage["resource_id"]))
    if resource["status"] != "PASS":
        return resource
    index_path = (
        Path(root).expanduser().resolve()
        / "design_systems"
        / _safe_id(usage["design_system_id"], field="DESIGN_SYSTEM_ID")
        / "usage_index.json"
    )
    index = _load_index(index_path)
    resource_id = str(usage["resource_id"])
    records = list(index.setdefault("resources", {}).setdefault(resource_id, []))
    normalized = {
        "asset_id": str(usage["asset_id"]),
        "component_id": str(usage["component_id"]),
        "binding_id": str(usage["binding_id"]),
        "resource_revision": int(usage.get("resource_revision") or resource["resource"]["revision"]),
        "resource_version": str(usage.get("resource_version") or resource["resource"]["version"]),
    }
    identity = (normalized["asset_id"], normalized["component_id"], normalized["binding_id"])
    records = [
        record
        for record in records
        if (str(record.get("asset_id")), str(record.get("component_id")), str(record.get("binding_id"))) != identity
    ]
    records.append(normalized)
    records.sort(key=lambda record: (record["asset_id"], record["component_id"], record["binding_id"]))
    index["resources"][resource_id] = records
    _atomic_write(index_path, index)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "resource_id": resource_id,
        "usage_count": len(records),
    }


def reverse_usage(root: str | Path, design_system_id: str, resource_id: str) -> dict[str, Any]:
    index_path = (
        Path(root).expanduser().resolve()
        / "design_systems"
        / _safe_id(design_system_id, field="DESIGN_SYSTEM_ID")
        / "usage_index.json"
    )
    index = _load_index(index_path)
    usages = list(index.get("resources", {}).get(resource_id, []) or [])
    assets = sorted({str(item.get("asset_id")) for item in usages if item.get("asset_id")})
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "design_system_id": design_system_id,
        "resource_id": resource_id,
        "usage_count": len(usages),
        "asset_count": len(assets),
        "assets": assets,
        "usages": usages,
    }


def impact_report(root: str | Path, design_system_id: str, resource_id: str) -> dict[str, Any]:
    current = load(root, design_system_id, resource_id)
    if current["status"] != "PASS":
        return current
    usage = reverse_usage(root, design_system_id, resource_id)
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "resource_id": resource_id,
        "current_revision": current["resource"]["revision"],
        "current_version": current["resource"]["version"],
        "locked": bool(current["resource"].get("locked", False)),
        "affected_asset_count": usage["asset_count"],
        "affected_assets": usage["assets"],
        "affected_bindings": usage["usages"],
    }


def _load_index(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"schema_version": SCHEMA_VERSION, "resources": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("DESIGN_USAGE_INDEX_INVALID")
    payload.setdefault("schema_version", SCHEMA_VERSION)
    payload.setdefault("resources", {})
    return payload


def _write_revision(path: Path, payload: Mapping[str, Any]) -> None:
    revision = int(payload.get("revision", 0))
    target = path / "revisions" / f"r{revision:06d}.json"
    if target.exists():
        raise FileExistsError(f"RESOURCE_REVISION_ALREADY_EXISTS:{revision}")
    _atomic_write(target, payload)


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(serialized)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "RESOURCE_KINDS",
    "impact_report",
    "initialize",
    "load",
    "record_usage",
    "resolve_binding",
    "reverse_usage",
    "save",
    "validate_resource",
]

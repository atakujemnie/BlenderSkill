from __future__ import annotations

"""Hash-deduplicated promotion of logos, textures, decals and reusable source files."""

from pathlib import Path
from typing import Any, Mapping
import hashlib
import json
import shutil

EXECUTOR_ID = "DESIGN_SYSTEM_RESOURCE_REGISTRY"
EXECUTOR_VERSION = "0.16.0"

CATEGORY_DIR = {
    "MATERIAL": "materials",
    "TEXTURE": "materials",
    "BRANDING": "branding",
    "DECAL": "decals",
    "COMPONENT": "components",
    "PROFILE": "profiles",
    "NODEGROUP": "nodegroups",
    "REFERENCE": "references",
}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def promote(spec: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    root = Path(str(spec.get("design_system_path") or "")).expanduser()
    source = Path(str(spec.get("source_path") or "")).expanduser()
    resource_id = str(spec.get("resource_id") or "").strip()
    category = str(spec.get("category") or "").upper()

    if not root.is_dir():
        blockers.append({"reason": "DESIGN_SYSTEM_PATH_MISSING", "path": str(root)})
    if not source.is_file():
        blockers.append({"reason": "SOURCE_FILE_MISSING", "path": str(source)})
    if not resource_id:
        blockers.append({"reason": "RESOURCE_ID_REQUIRED"})
    if category not in CATEGORY_DIR:
        blockers.append({"reason": "INVALID_CATEGORY", "category": category})
    if blockers:
        return {"validator_id": EXECUTOR_ID, "status": "BLOCKED", "blockers": blockers}

    target_dir = root / CATEGORY_DIR[category]
    target_dir.mkdir(parents=True, exist_ok=True)
    registry_path = root / "sources.json"
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"validator_id": EXECUTOR_ID, "status": "BLOCKED", "blockers": [{"reason": "SOURCES_REGISTRY_INVALID", "error": str(exc)}]}
    else:
        registry = {"schema_version": "1.0", "sources": []}

    entries = list(registry.get("sources", []) or [])
    digest = _sha256(source)
    same_hash = next((entry for entry in entries if entry.get("sha256") == digest and entry.get("category") == category), None)
    same_id = next((entry for entry in entries if entry.get("resource_id") == resource_id), None)

    if same_id and same_id.get("sha256") != digest:
        return {
            "validator_id": EXECUTOR_ID,
            "status": "FAIL",
            "blockers": [{"reason": "RESOURCE_ID_HASH_CONFLICT", "resource_id": resource_id}],
        }

    if same_hash:
        return {
            "validator_id": EXECUTOR_ID,
            "executor_version": EXECUTOR_VERSION,
            "status": "REUSED",
            "resource_id": same_hash.get("resource_id"),
            "sha256": digest,
            "path": same_hash.get("canonical_path"),
            "blockers": [],
        }

    suffix = source.suffix.lower()
    target = target_dir / f"{resource_id}{suffix}"
    if target.exists() and _sha256(target) != digest:
        return {
            "validator_id": EXECUTOR_ID,
            "status": "FAIL",
            "blockers": [{"reason": "TARGET_PATH_HASH_CONFLICT", "path": str(target)}],
        }

    if not target.exists():
        shutil.copy2(source, target)

    entry = {
        "resource_id": resource_id,
        "category": category,
        "sha256": digest,
        "canonical_path": str(target),
        "source_path": str(source),
        "provenance": spec.get("provenance") or {},
        "license": spec.get("license") or "PROJECT_OWNED_OR_UNSPECIFIED",
    }
    entries.append(entry)
    registry["sources"] = entries
    registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "status": "PROMOTED",
        "resource_id": resource_id,
        "sha256": digest,
        "path": str(target),
        "blockers": [],
    }

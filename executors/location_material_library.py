from __future__ import annotations

"""Resolve or bootstrap a persistent material-language library for one location."""

from pathlib import Path
from typing import Any, Mapping
import json
import re

EXECUTOR_ID = "LOCATION_MATERIAL_LIBRARY"
EXECUTOR_VERSION = "0.14.0"
SUBDIRS = ("textures", "atlases", "masks", "references", "previews", "source")


def _slug(value: Any) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "").strip()).strip("._-")
    if not text:
        raise ValueError("LOCATION_ID_REQUIRED")
    return text


def resolve(spec: Mapping[str, Any]) -> dict[str, Any]:
    try:
        location_id = _slug(spec.get("location_id"))
    except ValueError:
        return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "LOCATION_ID_REQUIRED"}]}

    root = spec.get("material_library_root")
    game_root = spec.get("game_asset_root")
    if root:
        library = Path(str(root)).expanduser() / location_id
    elif game_root:
        library = Path(str(game_root)).expanduser() / "Materials" / "Locations" / location_id
    else:
        return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "MATERIAL_OR_GAME_ASSET_ROOT_REQUIRED"}]}

    create = bool(spec.get("create_if_missing", False))
    existed = library.is_dir()
    if not existed and create:
        library.mkdir(parents=True, exist_ok=True)
        for name in SUBDIRS:
            (library / name).mkdir(exist_ok=True)

    blockers: list[dict[str, Any]] = []
    if not library.is_dir():
        blockers.append({"reason": "LOCATION_MATERIAL_LIBRARY_MISSING", "path": str(library)})

    manifest = library / "material_language.json"
    if library.is_dir() and create and not manifest.exists():
        manifest.write_text(json.dumps({
            "schema_version": "1.0",
            "location_id": location_id,
            "library_version": 1,
            "material_families": {},
            "surface_rules": {},
            "texture_sets": {},
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    data: dict[str, Any] = {}
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            blockers.append({"reason": "MATERIAL_LANGUAGE_MANIFEST_INVALID", "error": str(exc)})
    elif library.is_dir():
        blockers.append({"reason": "MATERIAL_LANGUAGE_MANIFEST_MISSING", "path": str(manifest)})

    return {
        "status": "READY" if not blockers else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "location_id": location_id,
        "path": str(library),
        "manifest_path": str(manifest),
        "paths": {name: str(library / name) for name in SUBDIRS},
        "created": bool(create and not existed and library.is_dir()),
        "reused_existing": existed,
        "material_family_count": len(data.get("material_families", {}) or {}),
        "texture_set_count": len(data.get("texture_sets", {}) or {}),
        "blockers": blockers,
    }

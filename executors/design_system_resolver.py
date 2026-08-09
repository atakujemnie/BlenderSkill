from __future__ import annotations

"""Resolve or bootstrap the persistent source-side design system for a location."""

from pathlib import Path
from typing import Any, Mapping
import json
import re

EXECUTOR_ID = "LOCATION_DESIGN_SYSTEM_RESOLVE"
EXECUTOR_VERSION = "0.16.0"
SCHEMA_VERSION = "1.0"

SUBDIRS = (
    "materials",
    "branding",
    "components",
    "decals",
    "profiles",
    "nodegroups",
    "references",
    "previews",
    "families",
    "organizations",
)


def _slug(value: Any, reason: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "").strip()).strip("._-")
    if not text:
        raise ValueError(reason)
    return text


def _starter_markdown(location_id: str) -> str:
    return f"""# {location_id} Location Design System\n\nStatus: BOOTSTRAPPED — populate from canonical references before claiming DESIGN_SYSTEM_READY.\n\n## Authority and inheritance\n\n- location_id: `{location_id}`\n- parent design system: none declared\n- organization/faction overrides live under `organizations/`\n- asset-family overrides live under `families/`\n\n## Design tokens\n\nDocument canonical palette, scale/grid, proportions and recurring dimensions.\n\n## Shape, edge and detail language\n\nDocument silhouettes, transitions, edge families, seam/gap language and forbidden forms.\n\n## Material language\n\nReference approved material IDs and the persistent runtime material library. Do not create per-asset replacements for existing families.\n\n## Branding and graphics\n\nRegister source logos, symbols, wordmarks, signage icons, decals and placement rules.\n\n## Reusable components\n\nRegister shared panels, fasteners, utility modules, trim profiles, emitters and other repeated geometry.\n\n## Lighting and emissive language\n\nDocument color/intensity/placement roles and forbidden decorative misuse.\n\n## Weathering and environmental response\n\nDocument dirt, wetness, wear, maintenance state and location-specific surface response.\n\n## Asset-family rules\n\nLink family-specific overrides under `families/`.\n\n## Provenance\n\nAll promoted resources require source/provenance records in `sources.json`.\n"""


def resolve(spec: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    try:
        location_id = _slug(spec.get("location_id"), "LOCATION_ID_REQUIRED")
    except ValueError as exc:
        return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "blockers": [{"reason": str(exc)}]}

    root_value = spec.get("design_system_root")
    project_root_value = spec.get("project_root")
    if root_value:
        base_root = Path(str(root_value)).expanduser()
    elif project_root_value:
        base_root = Path(str(project_root_value)).expanduser() / "Blender" / "DesignSystems"
    else:
        return {
            "status": "BLOCKED",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "DESIGN_SYSTEM_OR_PROJECT_ROOT_REQUIRED"}],
        }

    location_root = base_root / location_id
    existed = location_root.is_dir()
    create = bool(spec.get("create_if_missing", False))
    created = False

    if not existed and create:
        location_root.mkdir(parents=True, exist_ok=True)
        for name in SUBDIRS:
            (location_root / name).mkdir(exist_ok=True)
        created = True

    if not location_root.is_dir():
        blockers.append({"reason": "LOCATION_DESIGN_SYSTEM_MISSING", "path": str(location_root)})

    md_path = location_root / "LOCATION_DESIGN_SYSTEM.md"
    manifest_path = location_root / "design_system.json"
    sources_path = location_root / "sources.json"
    library_manifest_path = location_root / "asset_library_manifest.json"
    asset_library_path = location_root / f"{location_id.upper()}_ASSET_LIBRARY.blend"

    if location_root.is_dir() and create:
        if not md_path.exists():
            md_path.write_text(_starter_markdown(location_id), encoding="utf-8")
        if not sources_path.exists():
            sources_path.write_text(json.dumps({
                "schema_version": SCHEMA_VERSION,
                "location_id": location_id,
                "sources": [],
            }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if not library_manifest_path.exists():
            library_manifest_path.write_text(json.dumps({
                "schema_version": SCHEMA_VERSION,
                "location_id": location_id,
                "blender_asset_library": str(asset_library_path),
                "materials": [],
                "components": [],
                "nodegroups": [],
                "profiles": [],
                "decals": [],
                "branding": [],
            }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if not manifest_path.exists():
            runtime_material_path = spec.get("material_library_path")
            if not runtime_material_path and spec.get("game_asset_root"):
                runtime_material_path = str(Path(str(spec["game_asset_root"])) / "Materials" / "Locations" / location_id)
            manifest_path.write_text(json.dumps({
                "schema_version": SCHEMA_VERSION,
                "location_id": location_id,
                "design_system_version": 1,
                "status": "BOOTSTRAPPED",
                "extends": None,
                "locked_tokens": [],
                "design_tokens": {},
                "shape_language": {},
                "edge_language": {},
                "detail_language": {},
                "material_families": {},
                "branding": {"applicable": False, "assets": {}},
                "component_families": {},
                "lighting": {},
                "weathering": {},
                "resource_paths": {
                    "source_root": str(location_root),
                    "material_library": runtime_material_path,
                    "asset_library_blend": str(asset_library_path),
                    **{name: str(location_root / name) for name in SUBDIRS},
                },
            }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for required, reason in (
        (md_path, "DESIGN_SYSTEM_MARKDOWN_MISSING"),
        (manifest_path, "DESIGN_SYSTEM_MANIFEST_MISSING"),
        (sources_path, "DESIGN_SYSTEM_SOURCES_MISSING"),
        (library_manifest_path, "ASSET_LIBRARY_MANIFEST_MISSING"),
    ):
        if location_root.is_dir() and not required.exists():
            blockers.append({"reason": reason, "path": str(required)})

    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            blockers.append({"reason": "DESIGN_SYSTEM_MANIFEST_INVALID", "error": str(exc)})

    organization_id = spec.get("organization_id")
    organization_path = None
    if organization_id and location_root.is_dir():
        try:
            org = _slug(organization_id, "ORGANIZATION_ID_INVALID")
            organization_path = location_root / "organizations" / org
            if create:
                organization_path.mkdir(parents=True, exist_ok=True)
        except ValueError as exc:
            blockers.append({"reason": str(exc)})

    status = "BLOCKED" if blockers else ("BOOTSTRAPPED" if created else "READY")
    return {
        "status": status,
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "location_id": location_id,
        "path": str(location_root),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "sources_path": str(sources_path),
        "asset_library_manifest_path": str(library_manifest_path),
        "asset_library_blend_path": str(asset_library_path),
        "organization_path": str(organization_path) if organization_path else None,
        "paths": {name: str(location_root / name) for name in SUBDIRS},
        "material_library_path": (manifest.get("resource_paths") or {}).get("material_library"),
        "created": created,
        "reused_existing": existed,
        "design_system_status": manifest.get("status"),
        "blockers": blockers,
    }

from __future__ import annotations

from typing import Any, Mapping

EXECUTOR_ID = "LOCATION_DESIGN_SYSTEM_MANIFEST"
EXECUTOR_VERSION = "0.16.0"

REQUIRED_TOP_LEVEL = (
    "schema_version",
    "location_id",
    "design_system_version",
    "status",
    "design_tokens",
    "shape_language",
    "edge_language",
    "detail_language",
    "material_families",
    "branding",
    "component_families",
    "lighting",
    "weathering",
    "resource_paths",
)


def evaluate(manifest: Mapping[str, Any], *, final: bool = False) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    missing = [key for key in REQUIRED_TOP_LEVEL if key not in manifest]
    if missing:
        blockers.append({"reason": "MISSING_REQUIRED_KEYS", "keys": missing})

    if not str(manifest.get("location_id") or "").strip():
        blockers.append({"reason": "LOCATION_ID_REQUIRED"})

    version = manifest.get("design_system_version")
    if not isinstance(version, int) or version < 1:
        blockers.append({"reason": "INVALID_DESIGN_SYSTEM_VERSION", "value": version})

    resources = manifest.get("resource_paths")
    if not isinstance(resources, Mapping):
        blockers.append({"reason": "RESOURCE_PATHS_INVALID"})
    else:
        for key in ("source_root", "material_library", "asset_library_blend"):
            if not resources.get(key):
                blockers.append({"reason": "RESOURCE_PATH_REQUIRED", "key": key})

    if final:
        if str(manifest.get("status") or "").upper() not in {"READY", "APPROVED"}:
            blockers.append({"reason": "DESIGN_SYSTEM_NOT_READY", "status": manifest.get("status")})
        for key in ("design_tokens", "shape_language", "edge_language", "material_families", "lighting", "weathering"):
            value = manifest.get(key)
            if not isinstance(value, Mapping) or not value:
                blockers.append({"reason": "DOMAIN_EMPTY", "domain": key})
        branding = manifest.get("branding")
        if isinstance(branding, Mapping) and branding.get("applicable"):
            assets = branding.get("assets")
            if not isinstance(assets, Mapping) or not assets:
                blockers.append({"reason": "BRANDING_APPLICABLE_BUT_EMPTY"})

    return {
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "status": "PASS" if not blockers else "FAIL",
        "final": final,
        "blockers": blockers,
    }

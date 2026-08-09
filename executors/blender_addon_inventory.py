from __future__ import annotations

"""Read-only Blender runtime discovery.

Discovery may inspect Blender preferences, addon_utils metadata and already-loaded
modules, but MUST NOT import or execute an undiscovered provider.
"""

from typing import Any
import sys

EXECUTOR_ID = "BLENDER_RUNTIME_ADDON_DISCOVERY"
EXECUTOR_VERSION = "0.18.0"


def _version_text(value: Any) -> str:
    if isinstance(value, (tuple, list)):
        return ".".join(str(int(x)) for x in value)
    return str(value or "UNKNOWN")


def _metadata_from_module(module: Any) -> dict[str, Any]:
    info = dict(getattr(module, "bl_info", {}) or {})
    return {
        "display_name": str(info.get("name") or getattr(module, "__name__", "")),
        "version": _version_text(info.get("version") or getattr(module, "__version__", None)),
        "metadata": {
            "description": info.get("description"),
            "category": info.get("category"),
            "blender": _version_text(info.get("blender")) if info.get("blender") else None,
        },
    }


def collect_runtime_inventory() -> dict[str, Any]:
    try:
        import bpy  # type: ignore
        import addon_utils  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"status": "BLOCKED", "validator_id": EXECUTOR_ID, "blockers": [{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}]}

    blender_version = _version_text(getattr(bpy.app, "version", None))
    try:
        enabled_ids = {str(item.module) for item in bpy.context.preferences.addons}
    except Exception:
        enabled_ids = set()

    discovered: dict[str, dict[str, Any]] = {}
    try:
        modules = list(addon_utils.modules(refresh=False))
    except TypeError:
        modules = list(addon_utils.modules())
    except Exception:
        modules = []

    for module in modules:
        module_name = str(getattr(module, "__name__", ""))
        if not module_name:
            continue
        meta = _metadata_from_module(module)
        discovered[module_name] = {"module_name": module_name, "display_name": meta["display_name"], "version": meta["version"], "enabled": module_name in enabled_ids, "discovered": True, "metadata": meta["metadata"]}

    for module_name in sorted(enabled_ids):
        if module_name in discovered:
            discovered[module_name]["enabled"] = True
            continue
        module = sys.modules.get(module_name)
        if module is not None:
            meta = _metadata_from_module(module)
            display_name, version, metadata = meta["display_name"], meta["version"], meta["metadata"]
        else:
            display_name = module_name.rsplit(".", 1)[-1]
            version = "UNKNOWN"
            metadata = {"metadata_partial": True, "discovery_policy": "NO_IMPORT"}
        discovered[module_name] = {"module_name": module_name, "display_name": display_name, "version": version, "enabled": True, "discovered": True, "metadata": metadata}

    asset_libraries: list[dict[str, Any]] = []
    try:
        for library in getattr(bpy.context.preferences.filepaths, "asset_libraries", []):
            asset_libraries.append({"name": str(getattr(library, "name", "Asset Library")), "path": str(getattr(library, "path", "")), "import_method": str(getattr(library, "import_method", "UNKNOWN"))})
    except Exception:
        pass

    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "blender_version": blender_version,
        "addons": sorted(discovered.values(), key=lambda x: (not x["enabled"], x["display_name"].lower())),
        "asset_libraries": asset_libraries,
        "builtins": [{"provider_id": "builtin_geometry_nodes", "display_name": "Blender Geometry Nodes", "version": blender_version, "domains": ["GEOMETRY_NODES", "PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"], "runtime_probe_status": "PROBE_REQUIRED"}],
        "blockers": [],
    }

from __future__ import annotations

"""Normalize read-only Blender discovery through the canonical provider registry."""

from hashlib import sha1
from typing import Any, Mapping
import re

from executors.provider_contracts import SourceKind, normalize_provider_record
from executors.provider_registry import match_provider

EXECUTOR_ID = "INSTALLED_PROVIDER_DISCOVERY"
EXECUTOR_VERSION = "0.18.0"


def _norm(value: Any) -> str:
    text = str(value or "").lower().replace("_", " ").replace("-", " ").replace(".", " ")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _version(value: Any) -> str:
    if isinstance(value, (tuple, list)):
        return ".".join(str(int(x)) for x in value)
    return str(value or "UNKNOWN")


def _addon_provider(addon: Mapping[str, Any]) -> dict[str, Any]:
    module_name = str(addon.get("module_name") or addon.get("module") or "")
    display_name = str(addon.get("display_name") or addon.get("name") or module_name)
    provider_id, definition = match_provider(module_name, display_name)
    if definition:
        classified = True
        source_kind = str(definition["source_kind"])
        domains = list(definition.get("domains") or [])
    else:
        classified = False
        provider_id = "addon:" + (_norm(module_name or display_name).replace(" ", "_") or "unknown")
        source_kind = SourceKind.UNKNOWN.value
        domains = []
    return normalize_provider_record({
        "provider_id": provider_id,
        "display_name": display_name,
        "module_name": module_name,
        "version": _version(addon.get("version")),
        "source_kind": source_kind,
        "domains": domains,
        "enabled": bool(addon.get("enabled", False)),
        "discovered": bool(addon.get("discovered", True)),
        "classification_known": classified,
        "runtime_probe_status": str(addon.get("runtime_probe_status") or "PROBE_REQUIRED"),
        "metadata": dict(addon.get("metadata") or {}),
    })


def build_inventory(raw: Mapping[str, Any]) -> dict[str, Any]:
    providers: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for addon in raw.get("addons", []) or []:
        item = _addon_provider(addon)
        existing = by_id.get(item["provider_id"])
        if existing:
            if item["enabled"] and not existing["enabled"]:
                existing.update(item)
            continue
        by_id[item["provider_id"]] = item
        providers.append(item)

    for library in raw.get("asset_libraries", []) or []:
        path = str(library.get("path") or "")
        name = str(library.get("name") or path or "Asset Library")
        digest = sha1(path.encode("utf-8")).hexdigest()[:10] if path else "no_path"
        provider_id = "asset_library:" + (_norm(name).replace(" ", "_") or "unnamed") + ":" + digest
        providers.append(normalize_provider_record({"provider_id": provider_id, "display_name": name, "module_name": "", "version": "N/A", "source_kind": "READY_ASSET_SOURCE", "domains": list(library.get("domains") or []), "enabled": True, "discovered": True, "classification_known": True, "runtime_probe_status": "NOT_APPLICABLE", "path": path}))

    builtins = list(raw.get("builtins", []) or []) or [{"provider_id": "builtin_geometry_nodes", "display_name": "Blender Geometry Nodes", "version": raw.get("blender_version", "UNKNOWN"), "domains": ["GEOMETRY_NODES", "PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"], "runtime_probe_status": "PROBE_REQUIRED"}]
    for builtin in builtins:
        providers.append(normalize_provider_record({"provider_id": str(builtin.get("provider_id") or "builtin_unknown"), "display_name": str(builtin.get("display_name") or builtin.get("provider_id") or "Blender Built-in"), "module_name": "bpy", "version": _version(builtin.get("version") or raw.get("blender_version")), "source_kind": "BUILTIN_BACKEND", "domains": list(builtin.get("domains") or []), "enabled": True, "discovered": True, "classification_known": True, "runtime_probe_status": str(builtin.get("runtime_probe_status") or "PROBE_REQUIRED") }))

    counts: dict[str, int] = {kind.value: 0 for kind in SourceKind}
    for provider in providers:
        counts[provider["source_kind"]] = counts.get(provider["source_kind"], 0) + 1
    providers.sort(key=lambda x: (x["source_kind"], x["provider_id"]))
    return {"status": "PASS", "validator_id": EXECUTOR_ID, "blender_version": str(raw.get("blender_version") or "UNKNOWN"), "providers": providers, "summary": {"ready_asset_sources_count": counts["READY_ASSET_SOURCE"], "procedural_generators_count": counts["PROCEDURAL_GENERATOR"], "external_generators_count": counts["EXTERNAL_GENERATOR"], "utilities_count": counts["UTILITY"], "builtin_backends_count": counts["BUILTIN_BACKEND"], "unknown_count": counts["UNKNOWN"]}}


def provider_ids(inventory: Mapping[str, Any]) -> set[str]:
    return {str(p.get("provider_id")) for p in inventory.get("providers", []) or []}

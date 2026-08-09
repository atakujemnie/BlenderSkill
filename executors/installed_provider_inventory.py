from __future__ import annotations

"""Normalize Blender runtime discovery into explicit provider/source buckets."""

from typing import Any, Iterable, Mapping
import re

EXECUTOR_ID = "INSTALLED_PROVIDER_DISCOVERY"
EXECUTOR_VERSION = "0.17.0"

SOURCE_KINDS = {
    "READY_ASSET_SOURCE",
    "PROCEDURAL_GENERATOR",
    "EXTERNAL_GENERATOR",
    "UTILITY",
    "BUILTIN_BACKEND",
}

_PROVIDER_RULES = (
    {
        "provider_id": "sapling_tree_gen",
        "aliases": ("sapling", "sapling tree gen", "add curve sapling"),
        "source_kind": "PROCEDURAL_GENERATOR",
        "domains": ("TREE", "WOODY_PLANT"),
    },
    {
        "provider_id": "ivygen",
        "aliases": ("ivygen", "ivy gen", "add curve ivygen"),
        "source_kind": "PROCEDURAL_GENERATOR",
        "domains": ("VINE", "SURFACE_GROWTH"),
    },
    {
        "provider_id": "ant_landscape",
        "aliases": ("a n t landscape", "ant landscape", "antlandscape", "ant landscape add on"),
        "source_kind": "PROCEDURAL_GENERATOR",
        "domains": ("TERRAIN",),
    },
    {
        "provider_id": "sverchok",
        "aliases": ("sverchok",),
        "source_kind": "PROCEDURAL_GENERATOR",
        "domains": ("PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"),
    },
    {
        "provider_id": "meshy",
        "aliases": ("meshy", "meshy official plugin"),
        "source_kind": "EXTERNAL_GENERATOR",
        "domains": ("EXTERNAL_3D_GENERATION",),
    },
    {
        "provider_id": "mpfb",
        "aliases": ("mpfb", "makehuman for blender", "makehuman"),
        "source_kind": "PROCEDURAL_GENERATOR",
        "domains": ("CHARACTER",),
    },
    {
        "provider_id": "geo_nodes_guide",
        "aliases": ("geo nodes guide", "geometry nodes guide", "geonodesguide"),
        "source_kind": "UTILITY",
        "domains": ("GEOMETRY_NODES",),
    },
    {
        "provider_id": "mcp",
        "aliases": ("mcp", "blender mcp"),
        "source_kind": "UTILITY",
        "domains": ("INTEGRATION",),
        "exact_short_aliases": ("mcp",),
    },
)


def _norm(value: Any) -> str:
    text = str(value or "").lower().replace("_", " ").replace("-", " ").replace(".", " ")
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _version(value: Any) -> str:
    if isinstance(value, (tuple, list)):
        return ".".join(str(int(x)) for x in value)
    return str(value or "UNKNOWN")


def _match_rule(module_name: str, display_name: str) -> Mapping[str, Any] | None:
    haystacks = {_norm(module_name), _norm(display_name), _norm(f"{module_name} {display_name}")}
    for rule in _PROVIDER_RULES:
        exact_short = {_norm(x) for x in rule.get("exact_short_aliases", ())}
        for alias in rule["aliases"]:
            needle = _norm(alias)
            if not needle:
                continue
            if needle in exact_short:
                if any(h == needle for h in haystacks):
                    return rule
            elif any(needle in h for h in haystacks):
                return rule
    return None


def _addon_provider(addon: Mapping[str, Any]) -> dict[str, Any]:
    module_name = str(addon.get("module_name") or addon.get("module") or "")
    display_name = str(addon.get("display_name") or addon.get("name") or module_name)
    rule = _match_rule(module_name, display_name)
    if rule:
        provider_id = rule["provider_id"]
        source_kind = rule["source_kind"]
        domains = list(rule["domains"])
        classified = True
    else:
        provider_id = "addon:" + (_norm(module_name or display_name).replace(" ", "_") or "unknown")
        source_kind = "UTILITY"
        domains = []
        classified = False
    return {
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
    }


def build_inventory(raw: Mapping[str, Any]) -> dict[str, Any]:
    providers: list[dict[str, Any]] = []
    seen: set[str] = set()

    for addon in raw.get("addons", []) or []:
        item = _addon_provider(addon)
        key = item["provider_id"]
        if key in seen:
            # Prefer enabled evidence when duplicate discovery surfaces expose the same provider.
            existing = next(x for x in providers if x["provider_id"] == key)
            if item["enabled"] and not existing["enabled"]:
                existing.update(item)
            continue
        seen.add(key)
        providers.append(item)

    for library in raw.get("asset_libraries", []) or []:
        path = str(library.get("path") or "")
        name = str(library.get("name") or path or "Asset Library")
        provider_id = "asset_library:" + (_norm(name).replace(" ", "_") or "unnamed")
        providers.append({
            "provider_id": provider_id,
            "display_name": name,
            "module_name": "",
            "version": "N/A",
            "source_kind": "READY_ASSET_SOURCE",
            "domains": list(library.get("domains") or []),
            "enabled": True,
            "discovered": True,
            "classification_known": True,
            "runtime_probe_status": "DISCOVERED",
            "path": path,
        })

    builtins = list(raw.get("builtins", []) or [])
    if not builtins:
        builtins = [{
            "provider_id": "builtin_geometry_nodes",
            "display_name": "Blender Geometry Nodes",
            "version": raw.get("blender_version", "UNKNOWN"),
            "domains": ["GEOMETRY_NODES", "PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"],
        }]
    for builtin in builtins:
        providers.append({
            "provider_id": str(builtin.get("provider_id") or "builtin_unknown"),
            "display_name": str(builtin.get("display_name") or builtin.get("provider_id") or "Blender Built-in"),
            "module_name": "bpy",
            "version": _version(builtin.get("version") or raw.get("blender_version")),
            "source_kind": "BUILTIN_BACKEND",
            "domains": list(builtin.get("domains") or []),
            "enabled": True,
            "discovered": True,
            "classification_known": True,
            "runtime_probe_status": str(builtin.get("runtime_probe_status") or "PASS"),
        })

    counts = {kind: 0 for kind in SOURCE_KINDS}
    for provider in providers:
        kind = provider["source_kind"]
        counts[kind] = counts.get(kind, 0) + 1

    providers.sort(key=lambda x: (x["source_kind"], x["provider_id"]))
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "blender_version": str(raw.get("blender_version") or "UNKNOWN"),
        "providers": providers,
        "summary": {
            "ready_asset_sources_count": counts["READY_ASSET_SOURCE"],
            "procedural_generators_count": counts["PROCEDURAL_GENERATOR"],
            "external_generators_count": counts["EXTERNAL_GENERATOR"],
            "utilities_count": counts["UTILITY"],
            "builtin_backends_count": counts["BUILTIN_BACKEND"],
        },
    }


def provider_ids(inventory: Mapping[str, Any]) -> set[str]:
    return {str(p.get("provider_id")) for p in inventory.get("providers", []) or []}

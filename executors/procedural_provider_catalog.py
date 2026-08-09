from __future__ import annotations

"""Curated v0.13 external-provider facts.

These are discovery hints, not runtime truth. Every executable third-party provider
still goes through PROCEDURAL_GENERATOR_PROVIDER against the actual Blender session.
"""

from copy import deepcopy

CATALOG_AS_OF = "2026-08-09"

_CATALOG = {
    "builtin_geometry_nodes": {"provider_id": "builtin_geometry_nodes", "provider_version": "5.1.x", "execution_type": "GEOMETRY_NODES", "blender_min": "5.1.0", "blender_max": "5.1.99", "supports_seed": True, "probe_required": True, "license": "GPL-compatible Blender runtime", "role": "PRIMARY_RUNTIME_BACKEND"},
    "nodetopython": {"provider_id": "nodetopython", "provider_version": "4.1.1", "execution_type": "DIRECT_PYTHON", "blender_min": "4.2.0", "blender_max": "5.1.99", "supports_seed": True, "probe_required": True, "license": "GPL-3.0", "role": "NODEGRAPH_COMPILER"},
    "geonodes": {"provider_id": "geonodes", "provider_version": "un-pinned", "execution_type": "DIRECT_PYTHON", "blender_min": "5.1.0", "blender_max": "5.1.99", "supports_seed": True, "probe_required": True, "license": "DISCOVER_AT_PROBE", "role": "PYTHON_GEOMETRY_NODES_AUTHORING"},
    "sapling_tree_gen": {"provider_id": "sapling_tree_gen", "provider_version": "extension", "execution_type": "BPY_OPERATOR", "blender_min": "4.2.0", "supports_seed": True, "probe_required": True, "license": "GPL-compatible extension", "role": "OPTIONAL_TREE_BACKEND"},
    "ivygen": {"provider_id": "ivygen", "provider_version": "extension", "execution_type": "BPY_OPERATOR", "blender_min": "4.2.0", "supports_seed": True, "probe_required": True, "license": "GPL-compatible extension", "role": "OPTIONAL_SURFACE_GROWTH_BACKEND"},
    "ant_landscape": {"provider_id": "ant_landscape", "provider_version": "extension", "execution_type": "BPY_OPERATOR", "blender_min": "4.2.0", "supports_seed": True, "probe_required": True, "license": "GPL-compatible extension", "role": "OPTIONAL_TERRAIN_BACKEND"},
    "archimesh": {"provider_id": "archimesh", "provider_version": "extension", "execution_type": "BPY_OPERATOR", "blender_min": "4.2.0", "supports_seed": True, "probe_required": True, "license": "GPL-compatible extension", "role": "OPTIONAL_ARCHITECTURAL_BLOCKOUT"},
    "sverchok": {"provider_id": "sverchok", "provider_version": "un-pinned", "execution_type": "DIRECT_PYTHON", "blender_min": "5.1.0", "blender_max": "5.1.99", "supports_seed": True, "probe_required": True, "license": "GPL-3.0", "role": "OPTIONAL_PARAMETRIC_BACKEND"},
    "engon_botaniq": {"provider_id": "engon_botaniq", "provider_version": "1.9.x", "execution_type": "BPY_OPERATOR", "blender_min": "4.2.0", "supports_seed": True, "probe_required": True, "license": "GPL-3.0 code; asset-pack license separate", "role": "OPTIONAL_ASSET_SCATTER_BACKEND"},
    "the_grove": {"provider_id": "the_grove", "provider_version": "2.2", "execution_type": "DIRECT_PYTHON", "blender_min": "4.2.0", "blender_max": "4.4.99", "supports_seed": True, "probe_required": True, "license": "COMMERCIAL/PROPRIETARY", "role": "VERSION_BLOCKED_TREE_BACKEND"},
    "procfunc": {"provider_id": "procfunc", "provider_version": "0.x", "execution_type": "SOURCE_ONLY", "blender_min": "4.2.0", "blender_max": "4.2.99", "supports_seed": True, "probe_required": False, "license": "BSD-3-Clause", "role": "SOURCE_PATTERN_ONLY"},
    "blenderproc": {"provider_id": "blenderproc", "provider_version": "2.8.0", "execution_type": "SOURCE_ONLY", "blender_min": "4.2.1", "blender_max": "4.2.99", "supports_seed": True, "probe_required": False, "license": "GPL-3.0", "role": "SOURCE_PATTERN_OR_EXTERNAL_WORKER"},
    "infinigen": {"provider_id": "infinigen", "provider_version": "un-pinned", "execution_type": "SOURCE_ONLY", "blender_min": "0", "supports_seed": True, "probe_required": False, "license": "BSD-3-Clause", "role": "ALGORITHM_REFERENCE"},
}


def get(provider_id: str) -> dict:
    return deepcopy(_CATALOG[provider_id])


def all_providers() -> dict[str, dict]:
    return deepcopy(_CATALOG)

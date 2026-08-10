from __future__ import annotations

import sys
from typing import Any, Iterable


def result(provider_id: str, state: str, *, capabilities: Iterable[str] = (), cleanup_state: str = "NOT_APPLICABLE", warnings: list[dict[str, Any]] | None = None, blockers: list[dict[str, Any]] | None = None, provider_version: str = "UNKNOWN", blender_version: str = "UNKNOWN", side_effects_detected: bool = False) -> dict[str, Any]:
    return {
        "provider_id": provider_id,
        "probe_state": state,
        "blender_version": blender_version,
        "provider_version": provider_version,
        "capabilities": list(capabilities),
        "cleanup_state": cleanup_state,
        "side_effects_detected": side_effects_detected,
        "warnings": warnings or [],
        "blockers": blockers or [],
    }


def blender_version(bpy: Any) -> str:
    return ".".join(str(x) for x in getattr(bpy.app, "version", ())) or "UNKNOWN"


def provider_version(provider: dict[str, Any]) -> str:
    return str(provider.get("version") or provider.get("provider_version") or "UNKNOWN")


def module_loaded(patterns: Iterable[str]) -> bool:
    normalized = tuple(str(p).lower() for p in patterns)
    return any(any(pattern in name.lower() for pattern in normalized) for name in sys.modules)


def resolve_operator(bpy: Any, dotted: str) -> Any | None:
    current = bpy.ops
    try:
        for part in dotted.split("."):
            current = getattr(current, part)
        return current
    except Exception:
        return None


def snapshot_ids(bpy: Any) -> tuple[set[str], set[str], set[str], set[str]]:
    return (
        set(bpy.data.objects.keys()),
        set(bpy.data.meshes.keys()),
        set(bpy.data.curves.keys()),
        set(bpy.data.node_groups.keys()),
    )


def remove_new_ids(bpy: Any, before: tuple[set[str], set[str], set[str], set[str]]) -> bool:
    before_objects, before_meshes, before_curves, before_groups = before
    try:
        for item in list(bpy.data.objects):
            if item.name not in before_objects:
                bpy.data.objects.remove(item, do_unlink=True)
        for item in list(bpy.data.node_groups):
            if item.name not in before_groups:
                bpy.data.node_groups.remove(item, do_unlink=True)
        for item in list(bpy.data.meshes):
            if item.name not in before_meshes:
                bpy.data.meshes.remove(item, do_unlink=True)
        for item in list(bpy.data.curves):
            if item.name not in before_curves:
                bpy.data.curves.remove(item, do_unlink=True)
    except Exception:
        return False
    return snapshot_ids(bpy) == before

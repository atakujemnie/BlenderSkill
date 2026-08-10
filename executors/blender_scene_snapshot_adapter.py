from __future__ import annotations

"""Measure Blender objects into compact SCENE_COMPONENT_SNAPSHOT records.

The adapter is read-only. It imports bpy only at execution time and emits the
stable metadata consumed by the external Studio runtime instead of serializing
the Blender scene or datablocks.
"""

import hashlib
import json
from typing import Any

from executors.scene_component_snapshot import build as build_snapshot

EXECUTOR_ID = "BLENDER_SCENE_SNAPSHOT_ADAPTER"
EXECUTOR_VERSION = "0.20.0"
M_TO_MM = 1000.0
MM_DIGITS = 3


def _bpy():
    import bpy

    return bpy


def _round(value: Any, digits: int = 6) -> float:
    return round(float(value), digits)


def _vector(values: Any, *, scale: float = 1.0, digits: int = 6) -> list[float]:
    return [_round(float(value) * scale, digits) for value in values]


def _mm_vector(values: Any) -> list[float]:
    return _vector(values, scale=M_TO_MM, digits=MM_DIGITS)


def _hash_settings(value: Any) -> str:
    serialized = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def _modifier_settings(modifier: Any) -> dict[str, Any]:
    kind = str(modifier.type).upper()
    settings: dict[str, Any] = {}
    if kind == "BEVEL":
        settings = {
            "width_mm": _round(float(modifier.width) * M_TO_MM, MM_DIGITS),
            "segments": int(modifier.segments),
            "limit_method": str(modifier.limit_method),
        }
    elif kind == "MIRROR":
        settings = {"use_axis": [bool(value) for value in modifier.use_axis]}
    elif kind == "ARRAY":
        settings = {
            "count": int(modifier.count),
            "constant_offset_mm": _mm_vector(modifier.constant_offset_displace),
            "use_relative_offset": bool(modifier.use_relative_offset),
            "use_constant_offset": bool(modifier.use_constant_offset),
        }
    elif kind == "BOOLEAN":
        settings = {
            "operation": str(modifier.operation),
            "solver": str(modifier.solver),
            "object": modifier.object.name if modifier.object is not None else None,
        }
    else:
        settings = {"type": kind}
    return settings


def _binding_ids(obj: Any) -> list[str]:
    values: set[str] = set()
    single = obj.get("blenderskill_binding_id")
    if single:
        values.add(str(single))
    multiple = obj.get("blenderskill_binding_ids")
    if isinstance(multiple, (list, tuple)):
        values.update(str(value) for value in multiple if value)
    return sorted(values)


def _anchor_ids(obj: Any) -> list[str]:
    values: set[str] = set()
    multiple = obj.get("blenderskill_anchor_ids")
    if isinstance(multiple, (list, tuple)):
        values.update(str(value) for value in multiple if value)
    prefix = "blenderskill_anchor_"
    for key in obj.keys():
        if str(key).startswith(prefix):
            values.add(str(key)[len(prefix) :])
    return sorted(values)


def _mesh_metrics(obj: Any) -> dict[str, int]:
    if obj.type != "MESH" or obj.data is None:
        return {}
    mesh = obj.data
    try:
        mesh.calc_loop_triangles()
        triangles = len(mesh.loop_triangles)
    except Exception:
        triangles = sum(max(0, len(polygon.vertices) - 2) for polygon in mesh.polygons)
    return {
        "vertices": len(mesh.vertices),
        "edges": len(mesh.edges),
        "polygons": len(mesh.polygons),
        "triangles": int(triangles),
    }


def measure_object(obj: Any) -> dict[str, Any]:
    component_id = str(obj.get("blenderskill_component_id") or "")
    world = obj.matrix_world
    location = world.translation
    rotation = world.to_euler("XYZ")
    scale = world.to_scale()
    modifier_stack = []
    for modifier in obj.modifiers:
        settings = _modifier_settings(modifier)
        modifier_stack.append(
            {
                "name": str(modifier.name),
                "type": str(modifier.type).upper(),
                "enabled": bool(modifier.show_viewport),
                "settings_hash": _hash_settings(settings),
            }
        )
    material_ids = [str(slot.material.name) for slot in obj.material_slots if slot.material is not None]
    parent_id = obj.parent.name if obj.parent is not None else None
    return {
        "object_id": str(obj.name),
        "component_id": component_id,
        "object_type": str(obj.type).upper(),
        "parent_id": parent_id,
        "transform": {
            "location_mm": _mm_vector(location),
            "rotation_rad": _vector(rotation),
            "scale": _vector(scale),
        },
        "dimensions_mm": _mm_vector(obj.dimensions),
        "mesh_metrics": _mesh_metrics(obj),
        "material_ids": sorted(material_ids),
        "modifier_stack": modifier_stack,
        "binding_ids": _binding_ids(obj),
        "anchor_ids": _anchor_ids(obj),
        "visibility": {
            "hide_viewport": bool(obj.hide_viewport),
            "hide_render": bool(obj.hide_render),
        },
    }


def collect(
    *,
    asset_id: str,
    asset_revision: int,
    scene_revision: int,
    component_ids: list[str] | None = None,
    collection_name: str | None = None,
) -> dict[str, Any]:
    bpy = _bpy()
    wanted = {str(value) for value in list(component_ids or [])}
    if collection_name:
        collection = bpy.data.collections.get(str(collection_name))
        if collection is None:
            return {
                "status": "FAIL",
                "executor_id": EXECUTOR_ID,
                "blockers": [{"reason": "BLENDER_COLLECTION_NOT_FOUND", "collection": str(collection_name)}],
            }
        objects = list(collection.all_objects)
    else:
        objects = list(bpy.context.scene.objects)

    records: list[dict[str, Any]] = []
    for obj in sorted(objects, key=lambda item: item.name):
        component_id = str(obj.get("blenderskill_component_id") or "")
        if not component_id:
            continue
        if wanted and component_id not in wanted:
            continue
        records.append(measure_object(obj))

    built = build_snapshot(
        {
            "asset_id": str(asset_id),
            "asset_revision": int(asset_revision),
            "scene_revision": int(scene_revision),
            "objects": records,
        },
        component_ids=sorted(wanted) if wanted else None,
    )
    return {
        **built,
        "executor_id": EXECUTOR_ID,
        "source": "BLENDER_5_1_DATA_API",
        "collection": collection_name,
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "collect",
    "measure_object",
]

from __future__ import annotations

"""Blender 5.1 adapter for HARD_SURFACE_RECIPE.

All recipe values use millimetres at the contract boundary. The adapter uses the
Blender data API for primitive creation and only creates named datablocks owned
by the requested component. It deliberately returns compact evidence instead of
scene dumps.
"""

from math import radians
from typing import Any, Mapping

from executors.hard_surface_recipe import validate as validate_recipe

EXECUTOR_ID = "BLENDER_HARD_SURFACE_BUILDER"
EXECUTOR_VERSION = "0.1.0"
MM = 0.001


def _bpy():
    import bpy

    return bpy


def _vec3(raw: Any, *, default=(0.0, 0.0, 0.0)) -> tuple[float, float, float]:
    if raw is None:
        return tuple(float(x) for x in default)
    if not isinstance(raw, (list, tuple)) or len(raw) != 3:
        raise ValueError("VEC3_REQUIRED")
    return tuple(float(x) for x in raw)


def _box_mesh(name: str, dimensions_mm: Mapping[str, Any]):
    bpy = _bpy()
    sx = float(dimensions_mm.get("x", dimensions_mm.get("width", 0.0))) * MM
    sy = float(dimensions_mm.get("y", dimensions_mm.get("depth", 0.0))) * MM
    sz = float(dimensions_mm.get("z", dimensions_mm.get("height", dimensions_mm.get("thickness", 0.0)))) * MM
    if min(sx, sy, sz) <= 0:
        raise ValueError("POSITIVE_BOX_DIMENSIONS_REQUIRED")
    x, y, z = sx / 2.0, sy / 2.0, sz / 2.0
    verts = [
        (-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
        (-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z),
    ]
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7),
    ]
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def _wedge_mesh(name: str, dimensions_mm: Mapping[str, Any], top_offset_mm: float = 0.0):
    bpy = _bpy()
    sx = float(dimensions_mm.get("x", dimensions_mm.get("width", 0.0))) * MM
    sy = float(dimensions_mm.get("y", dimensions_mm.get("depth", 0.0))) * MM
    sz = float(dimensions_mm.get("z", dimensions_mm.get("height", 0.0))) * MM
    if min(sx, sy, sz) <= 0:
        raise ValueError("POSITIVE_WEDGE_DIMENSIONS_REQUIRED")
    x, y, z = sx / 2.0, sy / 2.0, sz / 2.0
    offset = float(top_offset_mm) * MM
    verts = [
        (-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
        (-x, -y + offset, z), (x, -y + offset, z), (x, y + offset, z), (-x, y + offset, z),
    ]
    faces = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7),
    ]
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def _profile_prism_mesh(name: str, profile: Any, length_mm: float, axis: str = "X"):
    bpy = _bpy()
    if not isinstance(profile, (list, tuple)) or len(profile) < 3:
        raise ValueError("PROFILE_REQUIRES_AT_LEAST_THREE_POINTS")
    points = []
    for point in profile:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError("PROFILE_POINT_2D_REQUIRED")
        points.append((float(point[0]) * MM, float(point[1]) * MM))
    half = float(length_mm) * MM / 2.0
    if half <= 0:
        raise ValueError("POSITIVE_PROFILE_LENGTH_REQUIRED")
    axis = str(axis).upper()
    if axis not in {"X", "Y", "Z"}:
        raise ValueError("PROFILE_PRISM_AXIS_INVALID")

    def vertex(p, t):
        a, b = p
        if axis == "X":
            return (t, a, b)
        if axis == "Y":
            return (a, t, b)
        return (a, b, t)

    n = len(points)
    verts = [vertex(p, -half) for p in points] + [vertex(p, half) for p in points]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return mesh


def _create_object(collection, component_id: str, output_id: str, mesh, raw: Mapping[str, Any]):
    bpy = _bpy()
    name = f"BS_{component_id}_{output_id}"
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    loc = _vec3(raw.get("location_mm"))
    obj.location = tuple(v * MM for v in loc)
    rot = _vec3(raw.get("rotation_deg"))
    obj.rotation_euler = tuple(radians(v) for v in rot)
    obj["blenderskill_component_id"] = component_id
    obj["blenderskill_output_id"] = output_id
    return obj


def execute(recipe: Mapping[str, Any], *, collection_name: str | None = None) -> dict[str, Any]:
    verdict = validate_recipe(recipe)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": verdict["blockers"]}

    bpy = _bpy()
    component_id = str(recipe["component_id"])
    collection_name = collection_name or f"BS_{component_id}"
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)

    outputs: dict[str, Any] = {}
    created_objects: list[str] = []
    created_meshes: list[str] = []
    modifiers: list[dict[str, str]] = []
    anchors: dict[str, dict[str, Any]] = {}

    for raw in recipe.get("operations", []):
        op = dict(raw)
        op_type = str(op["op"]).upper()
        op_id = str(op["id"])

        if op_type in {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM"}:
            output_id = str(op["output"])
            if op_type in {"BOX", "ROUNDED_BOX"}:
                mesh = _box_mesh(f"BS_{component_id}_{output_id}", dict(op["dimensions"]))
            elif op_type == "WEDGE":
                mesh = _wedge_mesh(
                    f"BS_{component_id}_{output_id}",
                    dict(op["dimensions"]),
                    float(op.get("top_offset_mm", 0.0)),
                )
            else:
                mesh = _profile_prism_mesh(
                    f"BS_{component_id}_{output_id}",
                    op["profile"],
                    float(op["length_mm"]),
                    str(op.get("axis", "X")),
                )
            obj = _create_object(collection, component_id, output_id, mesh, op)
            outputs[output_id] = obj
            created_objects.append(obj.name)
            created_meshes.append(mesh.name)
            if op_type == "ROUNDED_BOX":
                width_mm = float(op.get("bevel_mm", 0.0))
                if width_mm > 0:
                    mod = obj.modifiers.new(name=f"BS_{op_id}_BEVEL", type="BEVEL")
                    mod.width = width_mm * MM
                    mod.segments = int(op.get("bevel_segments", 3))
                    modifiers.append({"object": obj.name, "modifier": mod.name, "type": "BEVEL"})
            continue

        if op_type == "BEVEL":
            target = outputs[str(op["target"])]
            mod = target.modifiers.new(name=f"BS_{op_id}_BEVEL", type="BEVEL")
            mod.width = float(op["width"]) * MM
            mod.segments = int(op.get("segments", 3))
            modifiers.append({"object": target.name, "modifier": mod.name, "type": "BEVEL"})
            continue

        if op_type in {"BOOLEAN_CUT", "BOOLEAN_UNION"}:
            target = outputs[str(op["target"])]
            cutter = outputs[str(op["cutter"])]
            mod = target.modifiers.new(name=f"BS_{op_id}_BOOL", type="BOOLEAN")
            mod.operation = "DIFFERENCE" if op_type == "BOOLEAN_CUT" else "UNION"
            mod.solver = "EXACT"
            mod.object = cutter
            cutter.hide_render = True
            cutter.hide_set(True)
            modifiers.append({"object": target.name, "modifier": mod.name, "type": mod.type})
            continue

        if op_type == "MIRROR":
            target = outputs[str(op["source"])]
            mod = target.modifiers.new(name=f"BS_{op_id}_MIRROR", type="MIRROR")
            axes = str(op.get("axes", "X")).upper()
            mod.use_axis[0] = "X" in axes
            mod.use_axis[1] = "Y" in axes
            mod.use_axis[2] = "Z" in axes
            modifiers.append({"object": target.name, "modifier": mod.name, "type": mod.type})
            continue

        if op_type == "ARRAY":
            target = outputs[str(op["source"])]
            mod = target.modifiers.new(name=f"BS_{op_id}_ARRAY", type="ARRAY")
            mod.count = int(op.get("count", 1))
            offset = _vec3(op.get("constant_offset_mm"))
            mod.use_relative_offset = False
            mod.use_constant_offset = True
            mod.constant_offset_displace = tuple(v * MM for v in offset)
            modifiers.append({"object": target.name, "modifier": mod.name, "type": mod.type})
            continue

        if op_type == "INSTANCE":
            source = outputs[str(op["source"])]
            output_id = str(op.get("output") or op_id)
            obj = source.copy()
            obj.data = source.data
            obj.name = f"BS_{component_id}_{output_id}"
            collection.objects.link(obj)
            loc = _vec3(op.get("location_mm"))
            obj.location = tuple(v * MM for v in loc)
            outputs[output_id] = obj
            created_objects.append(obj.name)
            continue

        if op_type == "ASSIGN_BINDING":
            target = outputs[str(op["target"])]
            target["blenderskill_binding_id"] = str(op["binding_id"])
            continue

        if op_type == "ANCHOR":
            target = outputs[str(op["target"])]
            local = _vec3(op.get("local_position_mm"))
            anchors[str(op["anchor_id"])] = {
                "target_object": target.name,
                "local_position_mm": list(local),
            }
            continue

    final_objects = [outputs[str(output)].name for output in recipe.get("final_outputs", [])]
    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "component_id": component_id,
        "collection": collection.name,
        "created_objects": created_objects,
        "created_meshes": created_meshes,
        "modifier_count": len(modifiers),
        "modifiers": modifiers,
        "anchors": anchors,
        "final_objects": final_objects,
        "artifact_id": f"blender_component:{component_id}:{len(created_objects)}:{len(modifiers)}",
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "execute"]

from __future__ import annotations

"""Blender 5.1 adapter for HARD_SURFACE_RECIPE.

All recipe values use millimetres at the contract boundary. v0.21 executes recipe
geometry in canonical component coordinates and honors the declared component
origin, so CENTER_BOTTOM / edge origins do not collapse into center-origin boxes.

v0.21.1 makes surface orientation a builder guarantee rather than an authoring
concern. v0.22 adds reference-detail primitives plus measurable feature proof:
BOOLEAN_CUT/UNION must actually change evaluated solid volume, and recipe
features are persisted as compact Blender object provenance for trusted scene
validation.
"""

import json
from math import cos, pi, radians, sin
from typing import Any, Mapping

from executors.hard_surface_recipe import validate as validate_recipe

EXECUTOR_ID = "BLENDER_HARD_SURFACE_BUILDER"
EXECUTOR_VERSION = "0.22.0"
MM = 0.001
M3_TO_MM3 = 1_000_000_000.0


def _bpy():
    import bpy

    return bpy


def _bmesh():
    import bmesh

    return bmesh


def _orient_outward(mesh) -> None:
    """Force consistent outward-facing normals on a generated closed solid."""
    bmesh = _bmesh()
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        if bm.faces:
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            if bm.calc_volume(signed=True) < 0.0:
                bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(mesh)
    finally:
        bm.free()
    mesh.update()


def _finalize_mesh(mesh, origin_type: str):
    _shift_mesh_for_origin(mesh, origin_type)
    _orient_outward(mesh)
    return mesh


def _vec3(raw: Any, *, default=(0.0, 0.0, 0.0)) -> tuple[float, float, float]:
    if raw is None:
        return tuple(float(x) for x in default)
    if not isinstance(raw, (list, tuple)) or len(raw) != 3:
        raise ValueError("VEC3_REQUIRED")
    return tuple(float(x) for x in raw)


def _component_transform(recipe: Mapping[str, Any]) -> dict[str, tuple[float, float, float] | str]:
    raw = recipe.get("component_transform", {})
    if raw is None:
        raw = {}
    if not isinstance(raw, Mapping):
        raise ValueError("COMPONENT_TRANSFORM_MAPPING_REQUIRED")
    coordinate_space = str(raw.get("coordinate_space") or "ASSET_LOCAL").upper()
    if coordinate_space != "ASSET_LOCAL":
        raise ValueError("BLENDER_BUILDER_REQUIRES_ASSET_LOCAL_TRANSFORM")
    return {
        "location_mm": _vec3(raw.get("location_mm")),
        "rotation_deg": _vec3(raw.get("rotation_deg")),
        "scale": _vec3(raw.get("scale"), default=(1.0, 1.0, 1.0)),
        "coordinate_space": coordinate_space,
    }


def _component_origin(recipe: Mapping[str, Any]) -> str:
    raw = recipe.get("component_origin", {})
    if raw is None:
        return "CENTER"
    if isinstance(raw, Mapping):
        return str(raw.get("type") or "CENTER").upper()
    return str(raw).upper()


def _shift_mesh_for_origin(mesh, origin_type: str) -> None:
    if not mesh.vertices:
        return
    xs = [vertex.co.x for vertex in mesh.vertices]
    ys = [vertex.co.y for vertex in mesh.vertices]
    zs = [vertex.co.z for vertex in mesh.vertices]
    minimum = (min(xs), min(ys), min(zs))
    maximum = (max(xs), max(ys), max(zs))
    center = tuple((minimum[index] + maximum[index]) / 2.0 for index in range(3))
    shift = [0.0, 0.0, 0.0]
    origin_type = str(origin_type or "CENTER").upper()

    if "LEFT_EDGE" in origin_type:
        shift[0] = -minimum[0]
    elif "RIGHT_EDGE" in origin_type:
        shift[0] = -maximum[0]
    else:
        shift[0] = -center[0]

    if "FRONT_EDGE" in origin_type:
        shift[1] = -minimum[1]
    elif "REAR_EDGE" in origin_type:
        shift[1] = -maximum[1]
    else:
        shift[1] = -center[1]

    if "BOTTOM" in origin_type:
        shift[2] = -minimum[2]
    elif "TOP" in origin_type:
        shift[2] = -maximum[2]
    else:
        shift[2] = -center[2]

    for vertex in mesh.vertices:
        vertex.co.x += shift[0]
        vertex.co.y += shift[1]
        vertex.co.z += shift[2]
    mesh.update()


def _box_mesh(name: str, dimensions_mm: Mapping[str, Any], *, origin_type: str = "CENTER"):
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
    return _finalize_mesh(mesh, origin_type)


def _wedge_mesh(name: str, dimensions_mm: Mapping[str, Any], top_offset_mm: float = 0.0, *, origin_type: str = "CENTER"):
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
    return _finalize_mesh(mesh, origin_type)


def _profile_prism_mesh(name: str, profile: Any, length_mm: float, axis: str = "X", *, origin_type: str = "CENTER"):
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

    def vertex(point, distance):
        a, b = point
        if axis == "X":
            return (distance, a, b)
        if axis == "Y":
            return (a, distance, b)
        return (a, b, distance)

    count = len(points)
    verts = [vertex(point, -half) for point in points] + [vertex(point, half) for point in points]
    faces = [tuple(range(count - 1, -1, -1)), tuple(range(count, 2 * count))]
    for index in range(count):
        following = (index + 1) % count
        faces.append((index, following, count + following, count + index))
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return _finalize_mesh(mesh, origin_type)


def _axis_vertex(axis: str, a: float, b: float, distance: float) -> tuple[float, float, float]:
    axis = str(axis).upper()
    if axis == "X":
        return (distance, a, b)
    if axis == "Y":
        return (a, distance, b)
    if axis == "Z":
        return (a, b, distance)
    raise ValueError("PRIMITIVE_AXIS_INVALID")


def _cylinder_mesh(
    name: str,
    diameter_mm: float,
    length_mm: float,
    axis: str = "Y",
    segments: int = 32,
    *,
    origin_type: str = "CENTER",
):
    bpy = _bpy()
    radius = float(diameter_mm) * MM / 2.0
    half = float(length_mm) * MM / 2.0
    segments = int(segments)
    if radius <= 0 or half <= 0 or segments < 8:
        raise ValueError("CYLINDER_PARAMETERS_INVALID")
    ring = [(radius * cos(2.0 * pi * i / segments), radius * sin(2.0 * pi * i / segments)) for i in range(segments)]
    verts = [_axis_vertex(axis, a, b, -half) for a, b in ring] + [_axis_vertex(axis, a, b, half) for a, b in ring]
    faces: list[tuple[int, ...]] = [tuple(range(segments - 1, -1, -1)), tuple(range(segments, 2 * segments))]
    for index in range(segments):
        following = (index + 1) % segments
        faces.append((index, following, segments + following, segments + index))
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return _finalize_mesh(mesh, origin_type)


def _ring_mesh(
    name: str,
    outer_diameter_mm: float,
    inner_diameter_mm: float,
    length_mm: float,
    axis: str = "Y",
    segments: int = 32,
    *,
    origin_type: str = "CENTER",
):
    bpy = _bpy()
    outer = float(outer_diameter_mm) * MM / 2.0
    inner = float(inner_diameter_mm) * MM / 2.0
    half = float(length_mm) * MM / 2.0
    segments = int(segments)
    if outer <= inner or inner <= 0 or half <= 0 or segments < 8:
        raise ValueError("RING_PARAMETERS_INVALID")
    outer_ring = [(outer * cos(2.0 * pi * i / segments), outer * sin(2.0 * pi * i / segments)) for i in range(segments)]
    inner_ring = [(inner * cos(2.0 * pi * i / segments), inner * sin(2.0 * pi * i / segments)) for i in range(segments)]
    verts = (
        [_axis_vertex(axis, a, b, -half) for a, b in outer_ring]
        + [_axis_vertex(axis, a, b, -half) for a, b in inner_ring]
        + [_axis_vertex(axis, a, b, half) for a, b in outer_ring]
        + [_axis_vertex(axis, a, b, half) for a, b in inner_ring]
    )
    oi0, ii0, oi1, ii1 = 0, segments, 2 * segments, 3 * segments
    faces: list[tuple[int, ...]] = []
    for index in range(segments):
        following = (index + 1) % segments
        faces.extend(
            [
                (oi0 + index, oi0 + following, ii0 + following, ii0 + index),
                (oi1 + index, ii1 + index, ii1 + following, oi1 + following),
                (oi0 + index, oi1 + index, oi1 + following, oi0 + following),
                (ii0 + index, ii0 + following, ii1 + following, ii1 + index),
            ]
        )
    mesh = bpy.data.meshes.new(f"{name}_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    return _finalize_mesh(mesh, origin_type)


def _capsule_profile(width_mm: float, height_mm: float, arc_segments: int) -> list[list[float]]:
    radius = float(width_mm) / 2.0
    straight = float(height_mm) / 2.0 - radius
    if radius <= 0 or straight < 0:
        raise ValueError("CAPSULE_PARAMETERS_INVALID")
    arc_segments = int(arc_segments)
    points: list[list[float]] = []
    for index in range(arc_segments + 1):
        angle = pi * index / arc_segments
        points.append([radius * cos(angle), straight + radius * sin(angle)])
    for index in range(arc_segments + 1):
        angle = pi + pi * index / arc_segments
        points.append([radius * cos(angle), -straight + radius * sin(angle)])
    return points


def _capsule_prism_mesh(
    name: str,
    width_mm: float,
    height_mm: float,
    length_mm: float,
    axis: str = "Y",
    arc_segments: int = 8,
    *,
    origin_type: str = "CENTER",
):
    return _profile_prism_mesh(
        name,
        _capsule_profile(width_mm, height_mm, arc_segments),
        length_mm,
        axis,
        origin_type=origin_type,
    )


def _create_object(collection, component_id: str, output_id: str, mesh, raw: Mapping[str, Any], transform: Mapping[str, Any]):
    bpy = _bpy()
    name = f"BS_{component_id}_{output_id}"
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    local_location = _vec3(raw.get("location_mm"))
    base_location = tuple(transform["location_mm"])
    obj.location = tuple((base_location[index] + local_location[index]) * MM for index in range(3))
    local_rotation = _vec3(raw.get("rotation_deg"))
    base_rotation = tuple(transform["rotation_deg"])
    obj.rotation_euler = tuple(radians(base_rotation[index] + local_rotation[index]) for index in range(3))
    base_scale = tuple(transform["scale"])
    local_scale = _vec3(raw.get("scale"), default=(1.0, 1.0, 1.0))
    obj.scale = tuple(base_scale[index] * local_scale[index] for index in range(3))
    obj["blenderskill_component_id"] = component_id
    obj["blenderskill_output_id"] = output_id
    obj["blenderskill_component_location_mm"] = list(base_location)
    return obj


def _feature_ids(op: Mapping[str, Any]) -> set[str]:
    values: set[str] = set()
    if op.get("feature_id") not in (None, ""):
        values.add(str(op.get("feature_id")))
    values.update(str(value) for value in list(op.get("feature_ids", []) or []) if str(value))
    return values


def _json_list(obj: Any, key: str) -> list[Any]:
    raw = obj.get(key)
    if not raw:
        return []
    if isinstance(raw, str):
        try:
            decoded = json.loads(raw)
        except (TypeError, ValueError, json.JSONDecodeError):
            return []
        return decoded if isinstance(decoded, list) else []
    return list(raw) if isinstance(raw, (list, tuple)) else []


def _tag_feature(obj: Any, op: Mapping[str, Any], proof_type: str, metrics: Mapping[str, Any] | None = None) -> None:
    ids = _feature_ids(op)
    if not ids:
        return
    existing_ids = {str(value) for value in _json_list(obj, "blenderskill_feature_ids_json") if str(value)}
    existing_ids.update(ids)
    obj["blenderskill_feature_ids_json"] = json.dumps(sorted(existing_ids), separators=(",", ":"))
    proofs = [dict(item) for item in _json_list(obj, "blenderskill_feature_proofs_json") if isinstance(item, Mapping)]
    for feature_id in sorted(ids):
        proofs.append(
            {
                "feature_id": feature_id,
                "proof_type": str(proof_type).upper(),
                "operation_id": str(op.get("id") or ""),
                "operation": str(op.get("op") or "").upper(),
                "metrics": dict(metrics or {}),
            }
        )
    obj["blenderskill_feature_proofs_json"] = json.dumps(proofs, sort_keys=True, separators=(",", ":"))


def _evaluated_volume_mm3(obj: Any) -> float:
    bpy = _bpy()
    bmesh = _bmesh()
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        bm.transform(evaluated.matrix_world)
        return abs(float(bm.calc_volume(signed=True))) * M3_TO_MM3
    finally:
        bm.free()
        evaluated.to_mesh_clear()


def _geometry_metrics(op: Mapping[str, Any]) -> dict[str, Any]:
    kind = str(op.get("op") or "").upper()
    if kind in {"BOX", "ROUNDED_BOX", "WEDGE"}:
        dims = dict(op.get("dimensions", {}) or {})
        return {
            "width_mm": float(dims.get("x", dims.get("width", 0.0))),
            "depth_mm": float(dims.get("y", dims.get("depth", 0.0))),
            "height_mm": float(dims.get("z", dims.get("height", dims.get("thickness", 0.0)))),
        }
    if kind == "CYLINDER":
        return {"diameter_mm": float(op.get("diameter_mm", 0.0)), "length_mm": float(op.get("length_mm", 0.0))}
    if kind == "RING":
        return {
            "outer_diameter_mm": float(op.get("outer_diameter_mm", 0.0)),
            "inner_diameter_mm": float(op.get("inner_diameter_mm", 0.0)),
            "length_mm": float(op.get("length_mm", 0.0)),
        }
    if kind == "CAPSULE_PRISM":
        return {
            "width_mm": float(op.get("width_mm", 0.0)),
            "height_mm": float(op.get("height_mm", 0.0)),
            "length_mm": float(op.get("length_mm", 0.0)),
        }
    if kind == "PROFILE_PRISM":
        return {"length_mm": float(op.get("length_mm", 0.0)), "profile_point_count": len(list(op.get("profile", []) or []))}
    return {}


def execute(recipe: Mapping[str, Any], *, collection_name: str | None = None) -> dict[str, Any]:
    verdict = validate_recipe(recipe)
    if verdict["status"] != "PASS":
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": verdict["blockers"]}

    bpy = _bpy()
    component_id = str(recipe["component_id"])
    try:
        component_transform = _component_transform(recipe)
    except ValueError as exc:
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": str(exc)}]}
    origin_type = _component_origin(recipe)
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
    operation_proofs: list[dict[str, Any]] = []

    try:
        for raw in recipe.get("operations", []):
            op = dict(raw)
            op_type = str(op["op"]).upper()
            op_id = str(op["id"])

            if op_type in {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM", "CYLINDER", "RING", "CAPSULE_PRISM"}:
                output_id = str(op["output"])
                mesh_name = f"BS_{component_id}_{output_id}"
                if op_type in {"BOX", "ROUNDED_BOX"}:
                    mesh = _box_mesh(mesh_name, dict(op["dimensions"]), origin_type=origin_type)
                elif op_type == "WEDGE":
                    mesh = _wedge_mesh(mesh_name, dict(op["dimensions"]), float(op.get("top_offset_mm", 0.0)), origin_type=origin_type)
                elif op_type == "PROFILE_PRISM":
                    mesh = _profile_prism_mesh(mesh_name, op["profile"], float(op["length_mm"]), str(op.get("axis", "X")), origin_type=origin_type)
                elif op_type == "CYLINDER":
                    mesh = _cylinder_mesh(
                        mesh_name,
                        float(op["diameter_mm"]),
                        float(op["length_mm"]),
                        str(op.get("axis", "Y")),
                        int(op.get("segments", 32)),
                        origin_type=origin_type,
                    )
                elif op_type == "RING":
                    mesh = _ring_mesh(
                        mesh_name,
                        float(op["outer_diameter_mm"]),
                        float(op["inner_diameter_mm"]),
                        float(op["length_mm"]),
                        str(op.get("axis", "Y")),
                        int(op.get("segments", 32)),
                        origin_type=origin_type,
                    )
                else:
                    mesh = _capsule_prism_mesh(
                        mesh_name,
                        float(op["width_mm"]),
                        float(op["height_mm"]),
                        float(op["length_mm"]),
                        str(op.get("axis", "Y")),
                        int(op.get("arc_segments", 8)),
                        origin_type=origin_type,
                    )
                obj = _create_object(collection, component_id, output_id, mesh, op, component_transform)
                outputs[output_id] = obj
                created_objects.append(obj.name)
                created_meshes.append(mesh.name)
                metrics = _geometry_metrics(op)
                _tag_feature(obj, op, "GEOMETRY_OUTPUT", metrics)
                if _feature_ids(op):
                    operation_proofs.append({"operation_id": op_id, "proof_type": "GEOMETRY_OUTPUT", "metrics": metrics})
                if op_type == "ROUNDED_BOX":
                    width_mm = float(op.get("bevel_mm", 0.0))
                    if width_mm > 0:
                        modifier = obj.modifiers.new(name=f"BS_{op_id}_BEVEL", type="BEVEL")
                        modifier.width = width_mm * MM
                        modifier.segments = int(op.get("bevel_segments", 3))
                        modifiers.append({"object": obj.name, "modifier": modifier.name, "type": "BEVEL"})
                continue

            if op_type == "BEVEL":
                target = outputs[str(op["target"])]
                modifier = target.modifiers.new(name=f"BS_{op_id}_BEVEL", type="BEVEL")
                modifier.width = float(op["width"]) * MM
                modifier.segments = int(op.get("segments", 3))
                if op.get("limit_method"):
                    modifier.limit_method = str(op.get("limit_method")).upper()
                if op.get("angle_limit_deg") is not None:
                    modifier.angle_limit = radians(float(op.get("angle_limit_deg")))
                modifiers.append({"object": target.name, "modifier": modifier.name, "type": "BEVEL"})
                metrics = {"bevel_width_mm": float(op["width"]), "bevel_segments": int(op.get("segments", 3))}
                _tag_feature(target, op, "BEVEL", metrics)
                if _feature_ids(op):
                    operation_proofs.append({"operation_id": op_id, "proof_type": "BEVEL", "metrics": metrics})
                continue

            if op_type in {"BOOLEAN_CUT", "BOOLEAN_UNION"}:
                target = outputs[str(op["target"])]
                cutter = outputs[str(op["cutter"])]
                before_mm3 = _evaluated_volume_mm3(target)
                modifier = target.modifiers.new(name=f"BS_{op_id}_BOOL", type="BOOLEAN")
                modifier.operation = "DIFFERENCE" if op_type == "BOOLEAN_CUT" else "UNION"
                modifier.solver = "EXACT"
                modifier.object = cutter
                cutter.hide_render = True
                cutter.hide_set(True)
                bpy.context.view_layer.update()
                after_mm3 = _evaluated_volume_mm3(target)
                effect_mm3 = before_mm3 - after_mm3 if op_type == "BOOLEAN_CUT" else after_mm3 - before_mm3
                minimum_effect = float(op.get("minimum_effect_mm3", 0.001))
                metrics = {
                    "volume_before_mm3": round(before_mm3, 6),
                    "volume_after_mm3": round(after_mm3, 6),
                    "boolean_effect_mm3": round(effect_mm3, 6),
                    "material_removed_mm3": round(max(0.0, before_mm3 - after_mm3), 6),
                    "material_added_mm3": round(max(0.0, after_mm3 - before_mm3), 6),
                }
                _tag_feature(target, op, "BOOLEAN_EFFECT", metrics)
                operation_proofs.append({"operation_id": op_id, "proof_type": "BOOLEAN_EFFECT", "metrics": metrics})
                if effect_mm3 <= minimum_effect:
                    return {
                        "status": "FAIL",
                        "executor_id": EXECUTOR_ID,
                        "executor_version": EXECUTOR_VERSION,
                        "component_id": component_id,
                        "blockers": [
                            {
                                "reason": "BOOLEAN_EFFECT_NOT_OBSERVED",
                                "operation_id": op_id,
                                "operation": op_type,
                                "minimum_effect_mm3": minimum_effect,
                                **metrics,
                            }
                        ],
                        "created_objects": created_objects,
                        "modifier_count": len(modifiers) + 1,
                        "operation_proofs": operation_proofs,
                    }
                modifiers.append({"object": target.name, "modifier": modifier.name, "type": modifier.type})
                continue

            if op_type == "MIRROR":
                target = outputs[str(op["source"])]
                modifier = target.modifiers.new(name=f"BS_{op_id}_MIRROR", type="MIRROR")
                axes = str(op.get("axes", "X")).upper()
                modifier.use_axis[0] = "X" in axes
                modifier.use_axis[1] = "Y" in axes
                modifier.use_axis[2] = "Z" in axes
                modifiers.append({"object": target.name, "modifier": modifier.name, "type": modifier.type})
                _tag_feature(target, op, "MIRROR", {"axes": axes})
                continue

            if op_type == "ARRAY":
                target = outputs[str(op["source"])]
                modifier = target.modifiers.new(name=f"BS_{op_id}_ARRAY", type="ARRAY")
                modifier.count = int(op.get("count", 1))
                offset = _vec3(op.get("constant_offset_mm"))
                modifier.use_relative_offset = False
                modifier.use_constant_offset = True
                modifier.constant_offset_displace = tuple(value * MM for value in offset)
                modifiers.append({"object": target.name, "modifier": modifier.name, "type": modifier.type})
                nonzero = [abs(value) for value in offset if abs(value) > 1e-9]
                metrics = {
                    "repeat_count": int(modifier.count),
                    "offset_x_mm": offset[0],
                    "offset_y_mm": offset[1],
                    "offset_z_mm": offset[2],
                    "pitch_mm": nonzero[0] if len(nonzero) == 1 else 0.0,
                }
                _tag_feature(target, op, "REPEAT", metrics)
                if _feature_ids(op):
                    operation_proofs.append({"operation_id": op_id, "proof_type": "REPEAT", "metrics": metrics})
                continue

            if op_type == "INSTANCE":
                source = outputs[str(op["source"])]
                output_id = str(op.get("output") or op_id)
                obj = source.copy()
                obj.data = source.data
                obj.name = f"BS_{component_id}_{output_id}"
                collection.objects.link(obj)
                local_location = _vec3(op.get("location_mm"))
                base_location = tuple(component_transform["location_mm"])
                obj.location = tuple((base_location[index] + local_location[index]) * MM for index in range(3))
                outputs[output_id] = obj
                created_objects.append(obj.name)
                _tag_feature(obj, op, "INSTANCE", {"instance_count": 1})
                continue

            if op_type == "ASSIGN_BINDING":
                target = outputs[str(op["target"])]
                target["blenderskill_binding_id"] = str(op["binding_id"])
                _tag_feature(target, op, "MATERIAL_BINDING", {"binding_id": str(op["binding_id"])})
                continue

            if op_type == "ANCHOR":
                target = outputs[str(op["target"])]
                local = _vec3(op.get("local_position_mm"))
                anchors[str(op["anchor_id"])] = {"target_object": target.name, "local_position_mm": list(local)}
                continue
    except (KeyError, TypeError, ValueError) as exc:
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "executor_version": EXECUTOR_VERSION,
            "component_id": component_id,
            "blockers": [{"reason": "BLENDER_RECIPE_EXECUTION_ERROR", "details": str(exc)}],
            "created_objects": created_objects,
            "modifier_count": len(modifiers),
            "operation_proofs": operation_proofs,
        }

    bpy.context.view_layer.update()
    final_objects = [outputs[str(output)].name for output in recipe.get("final_outputs", [])]
    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "component_id": component_id,
        "component_transform": component_transform,
        "component_origin": origin_type,
        "collection": collection.name,
        "created_objects": created_objects,
        "created_meshes": created_meshes,
        "modifier_count": len(modifiers),
        "modifiers": modifiers,
        "anchors": anchors,
        "final_objects": final_objects,
        "operation_proofs": operation_proofs,
        "artifact_id": f"blender_component:{component_id}:{len(created_objects)}:{len(modifiers)}",
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "execute"]

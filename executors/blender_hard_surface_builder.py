from __future__ import annotations

"""Blender 5.1 adapter for HARD_SURFACE_RECIPE.

All recipe values use millimetres at the contract boundary. v0.21 executes recipe
geometry in canonical component coordinates and honors the declared component
origin, so CENTER_BOTTOM / edge origins do not collapse into center-origin boxes.

v0.21.1 makes surface orientation a builder guarantee rather than an authoring
concern: every generated closed solid is normalized to outward-facing normals
before it leaves the primitive constructors. Inward-facing winding made the EXACT
boolean solver treat a cutter as its own complement, so `BOOLEAN_CUT` removed no
material and silently degraded to a surface imprint.
"""

from math import radians
from typing import Any, Mapping

from executors.hard_surface_recipe import validate as validate_recipe

EXECUTOR_ID = "BLENDER_HARD_SURFACE_BUILDER"
EXECUTOR_VERSION = "0.21.1"
MM = 0.001


def _bpy():
    import bpy

    return bpy


def _bmesh():
    import bmesh

    return bmesh


def _orient_outward(mesh) -> None:
    """Force outward-facing normals on a generated solid.

    Deterministic and independent of the vertex order used to construct the mesh:
    faces are made consistent by `recalc_face_normals`, then the whole shell is
    reversed when the signed volume proves the consistent orientation points
    inward. Vertex positions, indices and object transforms are untouched, so
    dimensions and placement are unaffected.
    """
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
    """Apply origin semantics and guarantee outward orientation."""
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
    """Shift local vertices so object location denotes the declared component origin."""
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
        # BlenderSkill asset convention: FRONT is -Y, so geometry extends inward +Y.
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

    for raw in recipe.get("operations", []):
        op = dict(raw)
        op_type = str(op["op"]).upper()
        op_id = str(op["id"])

        if op_type in {"BOX", "ROUNDED_BOX", "WEDGE", "PROFILE_PRISM"}:
            output_id = str(op["output"])
            mesh_name = f"BS_{component_id}_{output_id}"
            if op_type in {"BOX", "ROUNDED_BOX"}:
                mesh = _box_mesh(mesh_name, dict(op["dimensions"]), origin_type=origin_type)
            elif op_type == "WEDGE":
                mesh = _wedge_mesh(mesh_name, dict(op["dimensions"]), float(op.get("top_offset_mm", 0.0)), origin_type=origin_type)
            else:
                mesh = _profile_prism_mesh(mesh_name, op["profile"], float(op["length_mm"]), str(op.get("axis", "X")), origin_type=origin_type)
            obj = _create_object(collection, component_id, output_id, mesh, op, component_transform)
            outputs[output_id] = obj
            created_objects.append(obj.name)
            created_meshes.append(mesh.name)
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
            modifiers.append({"object": target.name, "modifier": modifier.name, "type": "BEVEL"})
            continue

        if op_type in {"BOOLEAN_CUT", "BOOLEAN_UNION"}:
            target = outputs[str(op["target"])]
            cutter = outputs[str(op["cutter"])]
            modifier = target.modifiers.new(name=f"BS_{op_id}_BOOL", type="BOOLEAN")
            modifier.operation = "DIFFERENCE" if op_type == "BOOLEAN_CUT" else "UNION"
            modifier.solver = "EXACT"
            modifier.object = cutter
            cutter.hide_render = True
            cutter.hide_set(True)
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
            continue

        if op_type == "ASSIGN_BINDING":
            target = outputs[str(op["target"])]
            target["blenderskill_binding_id"] = str(op["binding_id"])
            continue

        if op_type == "ANCHOR":
            target = outputs[str(op["target"])]
            local = _vec3(op.get("local_position_mm"))
            anchors[str(op["anchor_id"])] = {"target_object": target.name, "local_position_mm": list(local)}
            continue

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
        "artifact_id": f"blender_component:{component_id}:{len(created_objects)}:{len(modifiers)}",
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "execute"]

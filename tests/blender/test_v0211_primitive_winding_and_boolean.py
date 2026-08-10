from __future__ import annotations

"""v0.21.1 regression: primitive winding and real boolean material removal.

Reproduces the defect found by the LAFAR service-terminal blind end-to-end test.
Before v0.21.1 every primitive emitted by BLENDER_HARD_SURFACE_BUILDER had
inward-facing normals, which made the EXACT boolean solver treat a cutter as its
own complement: `BOOLEAN_CUT` removed no material and degraded into a surface
imprint while every structural check still reported PASS.

These tests measure evaluated Blender geometry. They fail on v0.21.0.
"""

import bmesh
import bpy
from mathutils import Vector

from executors.blender_hard_surface_builder import execute

MM3 = 1.0e9  # cubic metres -> cubic millimetres
TRANSFORM = {
    "location_mm": [0.0, 0.0, 0.0],
    "rotation_deg": [0.0, 0.0, 0.0],
    "scale": [1.0, 1.0, 1.0],
    "coordinate_space": "ASSET_LOCAL",
}


def _rect_profile(width_mm: float, height_mm: float, clockwise: bool) -> list[list[float]]:
    half_w, half_h = width_mm / 2.0, height_mm / 2.0
    points = [[-half_w, -half_h], [half_w, -half_h], [half_w, half_h], [-half_w, half_h]]
    return list(reversed(points)) if clockwise else points


def _recipe(component_id: str, operations: list[dict], final_outputs: list[str]) -> dict:
    return {
        "component_id": component_id,
        "component_transform": dict(TRANSFORM),
        "component_origin": {"type": "CENTER"},
        "operations": operations,
        "final_outputs": final_outputs,
    }


def _build(recipe: dict) -> dict:
    result = execute(recipe)
    assert result["status"] == "PASS", result
    return result


def _cleanup(result: dict) -> None:
    collection = bpy.data.collections.get(result["collection"])
    for name in list(result.get("created_objects", [])):
        obj = bpy.data.objects.get(name)
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)
    for name in list(result.get("created_meshes", [])):
        mesh = bpy.data.meshes.get(name)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    if collection is not None:
        bpy.data.collections.remove(collection)


def _base_bmesh(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    return bm


def _evaluated_bmesh(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj_eval.matrix_world)
    obj_eval.to_mesh_clear()
    return bm


def _evaluated_volume_mm3(obj) -> float:
    bm = _evaluated_bmesh(obj)
    try:
        return bm.calc_volume(signed=True) * MM3
    finally:
        bm.free()


def _is_closed(bm) -> bool:
    return all(len(edge.link_faces) == 2 for edge in bm.edges)


def _outward_fraction(bm) -> float:
    """Fraction of faces whose normal points away from the mesh centroid."""
    bm.normal_update()
    centroid = sum((vert.co for vert in bm.verts), Vector((0.0, 0.0, 0.0))) / len(bm.verts)
    outward = sum(1 for face in bm.faces if (face.calc_center_median() - centroid).dot(face.normal) > 0.0)
    return outward / len(bm.faces)


def _euler_characteristic(bm) -> int:
    return len(bm.verts) - len(bm.edges) + len(bm.faces)


# ---------------------------------------------------------------------------
# TEST A - every closed primitive leaves the builder correctly oriented
# ---------------------------------------------------------------------------

def _test_a_closed_solid_orientation() -> None:
    cases: list[tuple[str, dict]] = [
        (
            "BOX",
            {"id": "p", "op": "BOX", "output": "O", "dimensions": {"width": 100, "depth": 60, "height": 40}},
        ),
        (
            "ROUNDED_BOX",
            {
                "id": "p",
                "op": "ROUNDED_BOX",
                "output": "O",
                "dimensions": {"width": 100, "depth": 60, "height": 40},
                "bevel_mm": 5,
                "bevel_segments": 3,
            },
        ),
        (
            "WEDGE",
            {
                "id": "p",
                "op": "WEDGE",
                "output": "O",
                "dimensions": {"width": 100, "depth": 60, "height": 40},
                "top_offset_mm": 18,
            },
        ),
    ]
    # PROFILE_PRISM must be orientation-correct for BOTH profile windings on every
    # axis: the builder owns orientation, the recipe author does not.
    for axis in ("X", "Y", "Z"):
        for clockwise in (False, True):
            cases.append(
                (
                    f"PROFILE_PRISM axis={axis} clockwise={clockwise}",
                    {
                        "id": "p",
                        "op": "PROFILE_PRISM",
                        "output": "O",
                        "profile": _rect_profile(100, 60, clockwise),
                        "length_mm": 40,
                        "axis": axis,
                    },
                )
            )

    for label, operation in cases:
        result = _build(_recipe("WINDING_A", [operation], ["O"]))
        try:
            obj = bpy.data.objects[result["final_objects"][0]]
            bm = _base_bmesh(obj)
            try:
                assert _is_closed(bm), f"{label}: primitive mesh is not closed"
                volume = bm.calc_volume(signed=True)
                assert volume > 0.0, f"{label}: signed volume {volume} indicates inverted shell"
                fraction = _outward_fraction(bm)
                assert fraction == 1.0, f"{label}: only {fraction:.0%} of faces face outward"
            finally:
                bm.free()

            # The evaluated result (bevel included) must stay outward-facing too.
            evaluated = _evaluated_bmesh(obj)
            try:
                assert _outward_fraction(evaluated) == 1.0, f"{label}: evaluated mesh is inverted"
                assert evaluated.calc_volume(signed=True) > 0.0, f"{label}: evaluated volume is negative"
            finally:
                evaluated.free()
        finally:
            _cleanup(result)


# ---------------------------------------------------------------------------
# TEST B - a blind pocket actually removes material
# ---------------------------------------------------------------------------

def _test_b_boolean_difference_removes_material() -> None:
    cube_mm = 100.0
    pocket_w, pocket_h, pocket_depth = 40.0, 40.0, 22.0
    overshoot = 40.0
    cutter_length = pocket_depth + overshoot
    cutter_center_y = -cube_mm / 2.0 - overshoot + cutter_length / 2.0

    result = _build(
        _recipe(
            "BOOLEAN_B",
            [
                {
                    "id": "target",
                    "op": "BOX",
                    "output": "BODY",
                    "dimensions": {"width": cube_mm, "depth": cube_mm, "height": cube_mm},
                },
                {
                    "id": "cutter",
                    "op": "BOX",
                    "output": "CUT",
                    "dimensions": {"width": pocket_w, "depth": cutter_length, "height": pocket_h},
                    "location_mm": [0.0, cutter_center_y, 0.0],
                },
                {"id": "pocket", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "CUT"},
            ],
            ["BODY"],
        )
    )
    try:
        obj = bpy.data.objects[result["final_objects"][0]]
        boolean = next(m for m in obj.modifiers if m.type == "BOOLEAN")
        assert boolean.operation == "DIFFERENCE", boolean.operation

        volume_after = _evaluated_volume_mm3(obj)
        boolean.show_viewport = False
        bpy.context.view_layer.update()
        volume_before = _evaluated_volume_mm3(obj)
        boolean.show_viewport = True
        bpy.context.view_layer.update()

        expected_removal = pocket_w * pocket_h * pocket_depth  # 35 200 mm^3
        removed = volume_before - volume_after

        assert volume_before > 0.0, f"target shell is inverted before the cut: {volume_before:.1f} mm^3"
        assert volume_after > 0.0, f"target shell is inverted after the cut: {volume_after:.1f} mm^3"
        # The defect: DIFFERENCE left the target untouched.
        assert volume_after < volume_before, (
            f"BOOLEAN_CUT removed no material: before={volume_before:.1f} after={volume_after:.1f} mm^3"
        )
        assert removed > 1000.0, f"removal {removed:.1f} mm^3 is below the material-removal epsilon"
        assert abs(removed - expected_removal) <= expected_removal * 0.01, (
            f"removed {removed:.1f} mm^3, expected {expected_removal:.1f} mm^3"
        )

        # A real cavity, not an imprint: the pocket floor plane must exist.
        evaluated = _evaluated_bmesh(obj)
        try:
            pocket_floor_y = -cube_mm / 2.0 + pocket_depth
            floor = [
                vert
                for vert in evaluated.verts
                if abs(vert.co.y * 1000.0 - pocket_floor_y) < 0.01 and abs(vert.co.x * 1000.0) <= pocket_w
            ]
            assert floor, "no vertices on the pocket floor plane"
            assert _is_closed(evaluated), "pocketed solid is not closed"
            assert _euler_characteristic(evaluated) == 2, "a blind pocket must not change surface genus"
        finally:
            evaluated.free()
    finally:
        _cleanup(result)


# ---------------------------------------------------------------------------
# TEST C - a through cut produces a real hole
# ---------------------------------------------------------------------------

def _test_c_through_cut_opens_a_hole() -> None:
    cube_mm = 100.0
    hole_w, hole_h = 40.0, 40.0

    result = _build(
        _recipe(
            "BOOLEAN_C",
            [
                {
                    "id": "target",
                    "op": "BOX",
                    "output": "BODY",
                    "dimensions": {"width": cube_mm, "depth": cube_mm, "height": cube_mm},
                },
                {
                    "id": "cutter",
                    "op": "BOX",
                    "output": "CUT",
                    "dimensions": {"width": hole_w, "depth": cube_mm + 40.0, "height": hole_h},
                },
                {"id": "bore", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "CUT"},
            ],
            ["BODY"],
        )
    )
    try:
        obj = bpy.data.objects[result["final_objects"][0]]
        boolean = next(m for m in obj.modifiers if m.type == "BOOLEAN")

        volume_after = _evaluated_volume_mm3(obj)
        boolean.show_viewport = False
        bpy.context.view_layer.update()
        volume_before = _evaluated_volume_mm3(obj)
        boolean.show_viewport = True
        bpy.context.view_layer.update()

        expected_removal = hole_w * hole_h * cube_mm  # 160 000 mm^3
        removed = volume_before - volume_after

        assert volume_after < volume_before, (
            f"through cut removed no material: before={volume_before:.1f} after={volume_after:.1f} mm^3"
        )
        assert removed > 1000.0, f"removal {removed:.1f} mm^3 is below the material-removal epsilon"
        assert abs(removed - expected_removal) <= expected_removal * 0.01, (
            f"removed {removed:.1f} mm^3, expected {expected_removal:.1f} mm^3"
        )

        evaluated = _evaluated_bmesh(obj)
        try:
            assert _is_closed(evaluated), "bored solid is not closed"
            # One tunnel through the solid => genus 1 => Euler characteristic 0.
            assert _euler_characteristic(evaluated) == 0, (
                "through cut did not open a real hole "
                f"(Euler characteristic {_euler_characteristic(evaluated)}, expected 0)"
            )
        finally:
            evaluated.free()
    finally:
        _cleanup(result)


def run() -> None:
    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_collections = set(bpy.data.collections.keys())

    _test_a_closed_solid_orientation()
    _test_b_boolean_difference_removes_material()
    _test_c_through_cut_opens_a_hole()

    assert set(bpy.data.objects.keys()) == before_objects
    assert set(bpy.data.meshes.keys()) == before_meshes
    assert set(bpy.data.collections.keys()) == before_collections

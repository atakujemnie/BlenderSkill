from __future__ import annotations

import bmesh
import bpy

from executors.blender_hard_surface_builder import execute
from executors.blender_scene_snapshot_adapter import collect
from executors.feature_contract_gate import validate as validate_features

TRANSFORM = {
    "location_mm": [0.0, 0.0, 0.0],
    "rotation_deg": [0.0, 0.0, 0.0],
    "scale": [1.0, 1.0, 1.0],
    "coordinate_space": "ASSET_LOCAL",
}


def _recipe(component_id: str, operations: list[dict], final_outputs: list[str]) -> dict:
    return {
        "component_id": component_id,
        "component_transform": dict(TRANSFORM),
        "component_origin": {"type": "CENTER"},
        "operations": operations,
        "final_outputs": final_outputs,
    }


def _cleanup(result: dict) -> None:
    collection = bpy.data.collections.get(result.get("collection"))
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


def _assert_closed_outward(obj) -> None:
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        assert bm.faces
        assert all(len(edge.link_faces) == 2 for edge in bm.edges), obj.name
        assert bm.calc_volume(signed=True) > 0.0, obj.name
    finally:
        bm.free()


def _test_sensor_detail_primitives_are_real_closed_solids() -> None:
    result = execute(
        _recipe(
            "SENSOR",
            [
                {
                    "id": "ring",
                    "op": "RING",
                    "output": "RING",
                    "outer_diameter_mm": 24,
                    "inner_diameter_mm": 18,
                    "length_mm": 5,
                    "axis": "Y",
                    "segments": 32,
                    "feature_id": "SENSOR_OUTER_RING",
                },
                {
                    "id": "lens",
                    "op": "CYLINDER",
                    "output": "LENS",
                    "diameter_mm": 18,
                    "length_mm": 4,
                    "axis": "Y",
                    "segments": 32,
                    "location_mm": [0, -4, 0],
                    "feature_id": "SENSOR_LENS",
                },
            ],
            ["RING", "LENS"],
        )
    )
    assert result["status"] == "PASS", result
    try:
        _assert_closed_outward(bpy.data.objects["BS_SENSOR_RING"])
        _assert_closed_outward(bpy.data.objects["BS_SENSOR_LENS"])
        snapshot = collect(asset_id="A22", asset_revision=1, scene_revision=1, component_ids=["SENSOR"])
        assert snapshot["status"] == "PASS", snapshot
        records = snapshot["snapshot"]["objects"]
        feature_ids = {value for record in records for value in record.get("feature_ids", [])}
        assert {"SENSOR_OUTER_RING", "SENSOR_LENS"} <= feature_ids
        assert all(record.get("evaluated_mesh_metrics", {}).get("polygons", 0) > 0 for record in records)
    finally:
        _cleanup(result)


def _test_eight_rounded_vents_require_real_boolean_effect_and_snapshot_proof() -> None:
    result = execute(
        _recipe(
            "SERVICE_PANEL",
            [
                {
                    "id": "body",
                    "op": "BOX",
                    "output": "BODY",
                    "dimensions": {"width": 420, "depth": 16, "height": 250},
                },
                {
                    "id": "slot",
                    "op": "CAPSULE_PRISM",
                    "output": "SLOT",
                    "width_mm": 12,
                    "height_mm": 110,
                    "length_mm": 30,
                    "axis": "Y",
                    "arc_segments": 8,
                    "location_mm": [-126, 0, 0],
                    "feature_id": "SERVICE_PANEL_VENTS",
                },
                {
                    "id": "repeat",
                    "op": "ARRAY",
                    "source": "SLOT",
                    "count": 8,
                    "constant_offset_mm": [36, 0, 0],
                    "feature_id": "SERVICE_PANEL_VENTS",
                },
                {
                    "id": "cut",
                    "op": "BOOLEAN_CUT",
                    "target": "BODY",
                    "cutter": "SLOT",
                    "minimum_effect_mm3": 1,
                    "feature_id": "SERVICE_PANEL_VENTS",
                },
            ],
            ["BODY"],
        )
    )
    assert result["status"] == "PASS", result
    try:
        proof = next(item for item in result["operation_proofs"] if item["operation_id"] == "cut")
        assert proof["metrics"]["material_removed_mm3"] > 1
        snapshot_result = collect(
            asset_id="A22",
            asset_revision=3,
            scene_revision=2,
            component_ids=["SERVICE_PANEL"],
        )
        assert snapshot_result["status"] == "PASS", snapshot_result
        snapshot = snapshot_result["snapshot"]
        task_pack = {
            "asset_id": "A22",
            "asset_revision": 3,
            "component_id": "SERVICE_PANEL",
            "component": {
                "id": "SERVICE_PANEL",
                "feature_contract_required": True,
                "feature_contract": {
                    "features": [
                        {
                            "feature_id": "SERVICE_PANEL_VENTS",
                            "priority": "MUST",
                            "expected_count": 8,
                            "required_operations": ["CAPSULE_PRISM", "ARRAY", "BOOLEAN_CUT"],
                            "required_proof_types": ["REPEAT", "BOOLEAN_EFFECT"],
                            "expected_measurements": {
                                "repeat_count": {"value": 8},
                                "pitch_mm": {"value": 36, "tolerance_mm": 0.01},
                                "material_removed_mm3": {"min": 1},
                            },
                        }
                    ]
                },
            },
        }
        verdict = validate_features(task_pack, _recipe("SERVICE_PANEL", [
            {"id": "body", "op": "BOX", "output": "BODY", "dimensions": {"width": 420, "depth": 16, "height": 250}},
            {"id": "slot", "op": "CAPSULE_PRISM", "output": "SLOT", "width_mm": 12, "height_mm": 110, "length_mm": 30, "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "repeat", "op": "ARRAY", "source": "SLOT", "count": 8, "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "cut", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "SLOT", "feature_id": "SERVICE_PANEL_VENTS"},
        ], ["BODY"]), snapshot)
        assert verdict["status"] == "PASS", verdict
        assert verdict["must_feature_coverage"] == 1.0
    finally:
        _cleanup(result)


def run() -> None:
    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_collections = set(bpy.data.collections.keys())
    _test_sensor_detail_primitives_are_real_closed_solids()
    _test_eight_rounded_vents_require_real_boolean_effect_and_snapshot_proof()
    assert set(bpy.data.objects.keys()) == before_objects
    assert set(bpy.data.meshes.keys()) == before_meshes
    assert set(bpy.data.collections.keys()) == before_collections

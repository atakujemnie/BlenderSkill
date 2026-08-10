from __future__ import annotations

from executors.blender_scene_snapshot_adapter import collect


def _assert_equal(label, actual, expected) -> None:
    assert actual == expected, f"{label}: actual={actual!r} expected={expected!r}"


def run() -> None:
    import bpy

    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_materials = set(bpy.data.materials.keys())

    mesh = bpy.data.meshes.new("BlenderSkillSnapshotTestMesh")
    mesh.from_pydata(
        [
            (-0.79, -0.036, -0.195),
            (0.79, -0.036, -0.195),
            (0.79, 0.036, -0.195),
            (-0.79, 0.036, -0.195),
            (-0.79, -0.036, 0.195),
            (0.79, -0.036, 0.195),
            (0.79, 0.036, 0.195),
            (-0.79, 0.036, 0.195),
        ],
        [],
        [
            (0, 1, 2, 3),
            (4, 7, 6, 5),
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (4, 0, 3, 7),
        ],
    )
    mesh.update()
    obj = bpy.data.objects.new("BlenderSkillSnapshotTestBackrest", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj["blenderskill_component_id"] = "BACKREST"
    obj["blenderskill_binding_id"] = "ASTERA_GRAPHITE_01"
    obj["blenderskill_anchor_LEFT_MOUNT"] = [-790.0, 0.0, 0.0]

    material = bpy.data.materials.new("ASTERA_GRAPHITE_01")
    obj.data.materials.append(material)
    bevel = obj.modifiers.new("Edge Bevel", "BEVEL")
    bevel.width = 0.012
    bevel.segments = 3

    before_location = obj.location.copy()
    before_rotation = obj.rotation_euler.copy()
    before_scale = obj.scale.copy()
    result = collect(
        asset_id="ASSET-005",
        asset_revision=4,
        scene_revision=1,
        component_ids=["BACKREST"],
    )

    _assert_equal("status", result["status"], "PASS")
    _assert_equal("source", result["source"], "BLENDER_5_1_DATA_API")
    snapshot = result["snapshot"]
    _assert_equal("asset_id", snapshot["asset_id"], "ASSET-005")
    _assert_equal("object_count", len(snapshot["objects"]), 1)
    record = snapshot["objects"][0]
    _assert_equal("component_id", record["component_id"], "BACKREST")
    _assert_equal("dimensions_mm", record["dimensions_mm"], [1580.0, 72.0, 390.0])
    _assert_equal("material_ids", record["material_ids"], ["ASTERA_GRAPHITE_01"])
    _assert_equal("binding_ids", record["binding_ids"], ["ASTERA_GRAPHITE_01"])
    _assert_equal("anchor_ids", record["anchor_ids"], ["LEFT_MOUNT"])
    _assert_equal("vertices", record["mesh_metrics"]["vertices"], 8)
    _assert_equal("polygons", record["mesh_metrics"]["polygons"], 6)
    _assert_equal("modifier_type", record["modifier_stack"][0]["type"], "BEVEL")

    _assert_equal("location_mutated", obj.location, before_location)
    _assert_equal("rotation_mutated", obj.rotation_euler, before_rotation)
    _assert_equal("scale_mutated", obj.scale, before_scale)

    bpy.data.objects.remove(obj, do_unlink=True)
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)
    if material.users == 0:
        bpy.data.materials.remove(material)

    _assert_equal("object_cleanup", set(bpy.data.objects.keys()), before_objects)
    _assert_equal("mesh_cleanup", set(bpy.data.meshes.keys()), before_meshes)
    _assert_equal("material_cleanup", set(bpy.data.materials.keys()), before_materials)

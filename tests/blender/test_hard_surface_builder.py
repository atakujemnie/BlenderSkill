from __future__ import annotations

from executors.blender_hard_surface_builder import execute


def run() -> None:
    import bpy

    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_collections = set(bpy.data.collections.keys())

    recipe = {
        "component_id": "RUNTIME_TEST_SEAT",
        "operations": [
            {
                "id": "body",
                "op": "ROUNDED_BOX",
                "output": "BODY",
                "dimensions": {"width": 1580, "depth": 420, "height": 82},
                "bevel_mm": 12,
                "bevel_segments": 3
            },
            {
                "id": "binding",
                "op": "ASSIGN_BINDING",
                "target": "BODY",
                "binding_id": "ASTERA_GRAPHITE_01"
            },
            {
                "id": "left_mount",
                "op": "ANCHOR",
                "target": "BODY",
                "anchor_id": "LEFT_MOUNT",
                "local_position_mm": [-790, 0, 0]
            }
        ],
        "final_outputs": ["BODY"]
    }
    result = execute(recipe)
    assert result["status"] == "PASS", result
    assert result["modifier_count"] == 1, result
    assert result["anchors"]["LEFT_MOUNT"]["local_position_mm"] == [-790.0, 0.0, 0.0]

    obj = bpy.data.objects[result["final_objects"][0]]
    dims_mm = [round(v * 1000.0, 3) for v in obj.dimensions]
    assert dims_mm == [1580.0, 420.0, 82.0], dims_mm
    assert obj["blenderskill_binding_id"] == "ASTERA_GRAPHITE_01"

    collection = bpy.data.collections.get(result["collection"])
    for name in list(result["created_objects"]):
        target = bpy.data.objects.get(name)
        if target is not None:
            bpy.data.objects.remove(target, do_unlink=True)
    for name in list(result["created_meshes"]):
        mesh = bpy.data.meshes.get(name)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    if collection is not None:
        bpy.data.collections.remove(collection)

    assert set(bpy.data.objects.keys()) == before_objects
    assert set(bpy.data.meshes.keys()) == before_meshes
    assert set(bpy.data.collections.keys()) == before_collections

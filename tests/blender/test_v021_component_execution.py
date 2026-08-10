from __future__ import annotations

from executors.component_execution_gate import execute


def run() -> None:
    import bpy

    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_collections = set(bpy.data.collections.keys())
    before_materials = set(bpy.data.materials.keys())

    task_pack = {
        "schema_version": 2,
        "asset_id": "SIDEWALK-B91",
        "asset_revision": 2,
        "component_id": "SLAB_R",
        "allowed_to_modify": ["SLAB_R"],
        "read_only": [],
        "component": {
            "id": "SLAB_R",
            "shape_class": "ROUNDED_BOX",
            "origin": {"type": "CENTER_BOTTOM"},
            "placement_required": True,
            "representation_contract": {},
            "transform": {
                "location_mm": [500.0, -500.0, 120.0],
                "rotation_deg": [0.0, 0.0, 0.0],
                "scale": [1.0, 1.0, 1.0],
                "coordinate_space": "ASSET_LOCAL",
                "explicit": True,
                "source": "TRANSFORM",
            },
        },
        "resolved_design_bindings": {
            "slab_material": {
                "binding_id": "slab_material",
                "mode": "INHERITED",
                "resource_id": "M_ACS_SidewalkSlab_B91",
                "resource_type": "MATERIAL",
                "version": "1.0.0",
                "resolved": {
                    "type": "MATERIAL",
                    "base_color": "#303438",
                    "metallic": 0.0,
                    "roughness": 0.7,
                },
                "locked": True,
            }
        },
    }
    recipe = {
        "component_id": "SLAB_R",
        "operations": [
            {
                "id": "body",
                "op": "ROUNDED_BOX",
                "output": "BODY",
                "dimensions": {"width": 994, "depth": 1000, "height": 40},
                "bevel_mm": 3,
                "bevel_segments": 2,
            },
            {"id": "binding", "op": "ASSIGN_BINDING", "target": "BODY", "binding_id": "slab_material"},
        ],
        "final_outputs": ["BODY"],
    }

    result = execute(task_pack, recipe)
    assert result["status"] == "PASS", result
    assert result["representation_status"] == "PASS", result
    assert result["materialization"]["applied_count"] == 1, result

    obj = bpy.data.objects[result["final_objects"][0]]
    world_mm = [round(obj.matrix_world.translation[index] * 1000.0, 3) for index in range(3)]
    assert world_mm == [500.0, -500.0, 120.0], world_mm
    dims_mm = [round(value * 1000.0, 3) for value in obj.dimensions]
    assert dims_mm == [994.0, 1000.0, 40.0], dims_mm

    local_z = [vertex.co.z * 1000.0 for vertex in obj.data.vertices]
    assert round(min(local_z), 3) == 0.0, min(local_z)
    assert round(max(local_z), 3) == 40.0, max(local_z)
    assert len(obj.data.materials) == 1
    assert obj.data.materials[0].name == "M_ACS_SidewalkSlab_B91"
    assert obj.data.materials[0]["blenderskill_resource_id"] == "M_ACS_SidewalkSlab_B91"

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
    material = bpy.data.materials.get("M_ACS_SidewalkSlab_B91")
    if material is not None and material.users == 0 and material.name not in before_materials:
        bpy.data.materials.remove(material)

    assert set(bpy.data.objects.keys()) == before_objects
    assert set(bpy.data.meshes.keys()) == before_meshes
    assert set(bpy.data.collections.keys()) == before_collections
    assert set(bpy.data.materials.keys()) == before_materials

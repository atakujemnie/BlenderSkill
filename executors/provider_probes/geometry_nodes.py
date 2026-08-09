from __future__ import annotations

"""Disposable Blender Geometry Nodes capability probe."""

from typing import Any


def run(provider: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return {"provider_id": "builtin_geometry_nodes", "probe_state": "BLOCKED", "cleanup_state": "NOT_APPLICABLE", "side_effects_detected": False, "capabilities": [], "warnings": [], "blockers": [{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}]}

    object_name = "__BLENDERSKILL_V018_GN_PROBE_OBJECT__"
    mesh_name = "__BLENDERSKILL_V018_GN_PROBE_MESH__"
    group_name = "__BLENDERSKILL_V018_GN_PROBE_GROUP__"
    before_objects = set(bpy.data.objects.keys())
    before_meshes = set(bpy.data.meshes.keys())
    before_groups = set(bpy.data.node_groups.keys())
    created_object = created_mesh = created_group = None
    blockers: list[dict[str, Any]] = []
    probe_state = "FAIL"
    cleanup_state = "FAIL"

    try:
        created_mesh = bpy.data.meshes.new(mesh_name)
        created_mesh.from_pydata([(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)], [], [(0, 1, 2)])
        created_mesh.update()
        created_object = bpy.data.objects.new(object_name, created_mesh)
        bpy.context.scene.collection.objects.link(created_object)

        created_group = bpy.data.node_groups.new(group_name, "GeometryNodeTree")
        created_group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        created_group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
        node_in = created_group.nodes.new("NodeGroupInput")
        node_out = created_group.nodes.new("NodeGroupOutput")
        created_group.links.new(node_in.outputs["Geometry"], node_out.inputs["Geometry"])

        modifier = created_object.modifiers.new(name="BlenderSkill GN Probe", type="NODES")
        modifier.node_group = created_group
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluated = created_object.evaluated_get(depsgraph)
        result_mesh = evaluated.to_mesh()
        try:
            if len(result_mesh.vertices) == 3 and len(result_mesh.polygons) == 1:
                probe_state = "PASS"
            else:
                blockers.append({"reason": "GEOMETRY_OUTPUT_INVALID", "vertices": len(result_mesh.vertices), "polygons": len(result_mesh.polygons)})
        finally:
            evaluated.to_mesh_clear()
    except Exception as exc:
        blockers.append({"reason": "GEOMETRY_NODES_PROBE_EXCEPTION", "error": str(exc)})
    finally:
        try:
            if created_object is not None and created_object.name in bpy.data.objects:
                bpy.data.objects.remove(created_object, do_unlink=True)
            if created_group is not None and created_group.name in bpy.data.node_groups:
                bpy.data.node_groups.remove(created_group, do_unlink=True)
            if created_mesh is not None and created_mesh.name in bpy.data.meshes:
                bpy.data.meshes.remove(created_mesh, do_unlink=True)
            after_objects = set(bpy.data.objects.keys())
            after_meshes = set(bpy.data.meshes.keys())
            after_groups = set(bpy.data.node_groups.keys())
            cleanup_state = "PASS" if (after_objects == before_objects and after_meshes == before_meshes and after_groups == before_groups) else "FAIL"
            if cleanup_state != "PASS":
                probe_state = "FAIL"
                blockers.append({"reason": "PROBE_CLEANUP_FAILED"})
        except Exception as exc:
            probe_state = "FAIL"
            blockers.append({"reason": "PROBE_CLEANUP_EXCEPTION", "error": str(exc)})

    return {
        "provider_id": "builtin_geometry_nodes",
        "probe_state": probe_state,
        "blender_version": ".".join(str(x) for x in bpy.app.version),
        "provider_version": ".".join(str(x) for x in bpy.app.version),
        "capabilities": ["GEOMETRY_NODES", "PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"] if probe_state == "PASS" else [],
        "cleanup_state": cleanup_state,
        "side_effects_detected": cleanup_state != "PASS",
        "warnings": [],
        "blockers": blockers,
    }

import bpy

from executors.provider_probes.geometry_nodes import run as run_geometry_nodes_probe


def run():
    before = (set(bpy.data.objects.keys()), set(bpy.data.meshes.keys()), set(bpy.data.node_groups.keys()))
    result = run_geometry_nodes_probe({"provider_id": "builtin_geometry_nodes", "enabled": True})
    after = (set(bpy.data.objects.keys()), set(bpy.data.meshes.keys()), set(bpy.data.node_groups.keys()))
    assert result["cleanup_state"] == "PASS", result
    assert before == after

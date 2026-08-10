from executors.blender_addon_inventory import collect_runtime_inventory
from executors.installed_provider_inventory import build_inventory


def run():
    raw = collect_runtime_inventory()
    assert raw["status"] == "PASS", raw
    inventory = build_inventory(raw)
    geometry_nodes = next(p for p in inventory["providers"] if p["provider_id"] == "builtin_geometry_nodes")
    assert geometry_nodes["discovery_state"] == "DISCOVERED"
    assert geometry_nodes["enabled"] is True
    assert geometry_nodes["probe_state"] == "PROBE_REQUIRED"

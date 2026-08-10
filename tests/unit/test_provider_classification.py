from executors.installed_provider_inventory import build_inventory


def test_unknown_addon_stays_unknown_and_has_no_domains():
    inventory = build_inventory({"blender_version": "5.1.0", "addons": [{"module_name": "mystery_addon", "display_name": "Mystery", "enabled": True}]})
    provider = next(item for item in inventory["providers"] if item["provider_id"].startswith("addon:mystery"))
    assert provider["source_kind"] == "UNKNOWN"
    assert provider["classification_known"] is False
    assert provider["domains"] == []


def test_geometry_nodes_discovery_never_implies_probe_pass():
    inventory = build_inventory({"blender_version": "5.1.0"})
    provider = next(item for item in inventory["providers"] if item["provider_id"] == "builtin_geometry_nodes")
    assert provider["probe_state"] == "PROBE_REQUIRED"

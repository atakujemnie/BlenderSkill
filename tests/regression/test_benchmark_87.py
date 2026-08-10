from executors.expected_provider_gate import evaluate as expected_gate
from executors.installed_provider_inventory import build_inventory
from executors.provider_orchestrator import evaluate as orchestrate
from executors.provider_selection_report import build_report
from executors.provider_quality import select as quality_select


def test_nc2_geometry_nodes_discovery_is_probe_required():
    inventory = build_inventory({"blender_version": "5.1.0"})
    gn = next(item for item in inventory["providers"] if item["provider_id"] == "builtin_geometry_nodes")
    assert gn["probe_state"] == "PROBE_REQUIRED"


def test_nc4_unknown_provider_is_unknown_not_utility():
    inventory = build_inventory({"blender_version": "5.1.0", "addons": [{"module_name": "mystery_v018", "enabled": True}]})
    unknown = next(item for item in inventory["providers"] if item["provider_id"].startswith("addon:mystery"))
    assert unknown["source_kind"] == "UNKNOWN"
    assert unknown["domains"] == []


def test_nc5_missing_expected_provider_is_discovery_mismatch():
    result = expected_gate([{"provider_id": "sapling_tree_gen"}], {"providers": []})
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "DISCOVERY_MISMATCH"


def test_nc6_sapling_pass_can_still_be_domain_rejected():
    inventory = {"providers": [{"provider_id": "sapling_tree_gen", "source_kind": "PROCEDURAL_GENERATOR", "domains": ["TREE", "WOODY_PLANT"], "enabled": True, "discovered": True, "probe_state": "PASS"}]}
    report = build_report(inventory, requested_domains=["GRASS"])
    candidate = report["candidates"][0]
    assert candidate["probe_state"] == "PASS"
    assert candidate["domain_state"] == "MISMATCH"
    assert candidate["selection_state"] == "REJECTED"


def test_nc8_quality_rejection_remains_visible():
    result = quality_select([{"provider_id": "low", "source_kind": "PROCEDURAL_GENERATOR", "probe_state": "PASS", "quality_tier": "C"}], "HERO")
    assert result["rejected"][0]["provider_id"] == "low"
    assert result["rejected"][0]["quality_state"] == "REJECTED"


def test_nc9_custom_fallback_blocked_with_eligible_provider():
    inventory = {
        "blender_version": "5.1.0",
        "providers": [{"provider_id": "builtin_geometry_nodes", "source_kind": "BUILTIN_BACKEND", "version": "5.1.0", "domains": ["GENERIC_PROCEDURAL"], "enabled": True, "discovered": True, "probe_state": "PASS"}],
    }
    result = orchestrate(inventory, requested_domains=["GRASS"], selected_provider_id="custom_native", allow_custom_fallback=True)
    assert result["status"] == "BLOCKED"
    assert result["stage"] == "CUSTOM_FALLBACK_GATE"

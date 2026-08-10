from executors.provider_selection_report import build_report


def test_sapling_grass_is_visible_but_rejected_for_domain_mismatch():
    inventory = {"providers": [{"provider_id": "sapling_tree_gen", "display_name": "Sapling", "version": "0.3.7", "source_kind": "PROCEDURAL_GENERATOR", "domains": ["TREE", "WOODY_PLANT"], "enabled": True, "discovered": True, "probe_state": "PASS"}]}
    report = build_report(inventory, requested_domains=["GRASS"])
    candidate = report["candidates"][0]
    assert candidate["domain_state"] == "MISMATCH"
    assert candidate["selection_state"] == "REJECTED"
    assert "REQUESTED_DOMAIN_MISMATCH" in candidate["reason"]


def test_unknown_provider_cannot_be_eligible():
    inventory = {"providers": [{"provider_id": "addon:mystery", "source_kind": "UNKNOWN", "domains": [], "enabled": True, "discovered": True, "probe_state": "PASS"}]}
    report = build_report(inventory, requested_domains=["GRASS"])
    assert report["candidates"][0]["selection_state"] == "BLOCKED"

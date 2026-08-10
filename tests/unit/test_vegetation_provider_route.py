from executors.vegetation_provider_route import evaluate


def test_non_vegetation_domain_is_blocked():
    result = evaluate({"blender_version": "5.1.0", "providers": []}, requested_domains=["TERRAIN"])
    assert result["status"] == "BLOCKED"
    assert result["blockers"][0]["reason"] == "NON_VEGETATION_DOMAIN"


def test_missing_expected_provider_remains_discovery_mismatch():
    result = evaluate(
        {"blender_version": "5.1.0", "providers": []},
        requested_domains=["GRASS"],
        expected_providers=[{"provider_id": "sapling_tree_gen"}],
    )
    assert result["status"] == "BLOCKED"
    assert result["blockers"][0]["reason"] == "DISCOVERY_MISMATCH"

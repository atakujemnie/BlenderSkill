from executors.provider_orchestrator import evaluate


def _inventory():
    return {
        "blender_version": "5.1.0",
        "providers": [
            {
                "provider_id": "builtin_geometry_nodes",
                "display_name": "Blender Geometry Nodes",
                "version": "5.1.0",
                "source_kind": "BUILTIN_BACKEND",
                "domains": ["GEOMETRY_NODES", "PARAMETRIC_GEOMETRY", "GENERIC_PROCEDURAL"],
                "enabled": True,
                "discovered": True,
                "discovery_state": "DISCOVERED",
                "probe_state": "PASS",
            },
            {
                "provider_id": "sapling_tree_gen",
                "display_name": "Sapling",
                "version": "0.3.7",
                "source_kind": "PROCEDURAL_GENERATOR",
                "domains": ["TREE", "WOODY_PLANT"],
                "enabled": True,
                "discovered": True,
                "discovery_state": "DISCOVERED",
                "probe_state": "PASS",
            },
        ],
    }


def test_pipeline_rejects_sapling_for_grass_and_selects_generic_backend():
    result = evaluate(_inventory(), requested_domains=["GRASS"], quality={"builtin_geometry_nodes": {"quality_tier": "B", "quality_score": 0.8}})
    assert result["status"] == "PASS"
    assert result["selected_provider_id"] == "builtin_geometry_nodes"
    candidates = {item["provider_id"]: item for item in result["selection_report"]["candidates"]}
    assert candidates["sapling_tree_gen"]["domain_state"] == "MISMATCH"
    assert candidates["sapling_tree_gen"]["selection_state"] == "REJECTED"


def test_custom_fallback_is_blocked_while_eligible_provider_exists():
    result = evaluate(_inventory(), requested_domains=["GRASS"], selected_provider_id="custom_native", allow_custom_fallback=True)
    assert result["status"] == "BLOCKED"
    assert result["stage"] == "CUSTOM_FALLBACK_GATE"

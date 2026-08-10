from executors.provider_probes.geometry_nodes import run as run_geometry_nodes_probe


def run():
    result = run_geometry_nodes_probe({"provider_id": "builtin_geometry_nodes", "enabled": True})
    assert result["probe_state"] == "PASS", result
    assert result["cleanup_state"] == "PASS", result
    assert result["side_effects_detected"] is False, result
    assert "GEOMETRY_NODES" in result["capabilities"]

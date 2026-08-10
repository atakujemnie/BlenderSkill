from executors.procedural_provider import evaluate


def test_probe_required_blocks_execution():
    provider = {"provider_id": "p", "execution_type": "PYTHON_API", "license_policy": "TEST", "blender_min": "5.0.0", "supports_seed": True, "probe_state": "PROBE_REQUIRED"}
    result = evaluate(provider, {"blender_version": "5.1.0", "background": True})
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "CAPABILITY_PROBE_REQUIRED" for item in result["blockers"])


def test_probe_pass_allows_compatible_provider():
    provider = {"provider_id": "p", "execution_type": "PYTHON_API", "license_policy": "TEST", "blender_min": "5.0.0", "supports_seed": True, "probe_state": "PASS", "probe": {"capabilities": []}}
    result = evaluate(provider, {"blender_version": "5.1.0", "background": True})
    assert result["status"] == "PASS"
    assert result["can_execute"] is True

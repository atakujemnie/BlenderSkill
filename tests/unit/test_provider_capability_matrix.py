from executors.provider_capability_probe_matrix import evaluate_provider


def test_unclassified_provider_is_blocked_not_pretended_pass():
    result = evaluate_provider({"provider_id": "addon:unknown", "enabled": True})
    assert result["probe_state"] == "BLOCKED"
    assert result["blockers"][0]["reason"] == "UNCLASSIFIED_PROVIDER"

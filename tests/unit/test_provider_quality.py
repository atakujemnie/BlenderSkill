from executors.provider_quality import select


def test_quality_rejection_is_explicit_and_provider_remains_reported():
    result = select([{"provider_id": "weak", "source_kind": "PROCEDURAL_GENERATOR", "probe_state": "PASS", "quality_tier": "C"}], "HERO")
    assert result["status"] == "BLOCKED"
    assert result["rejected"][0]["provider_id"] == "weak"
    assert result["rejected"][0]["quality_state"] == "REJECTED"


def test_best_eligible_quality_provider_is_selected():
    result = select([
        {"provider_id": "a", "source_kind": "PROCEDURAL_GENERATOR", "probe_state": "PASS", "quality_tier": "B", "quality_score": 0.8},
        {"provider_id": "b", "source_kind": "PROCEDURAL_GENERATOR", "probe_state": "PASS", "quality_tier": "A", "quality_score": 0.7},
    ], "MID")
    assert result["selected_provider_id"] == "b"

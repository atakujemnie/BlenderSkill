from executors.expected_provider_gate import evaluate


def _inventory(version="2.0.15"):
    return {"providers": [{"provider_id": "mpfb", "version": version, "enabled": True}]}


def test_expected_provider_accepts_range_constraint():
    result = evaluate([{"provider_id": "mpfb", "version_constraint": ">=2.0,<3.0"}], _inventory())
    assert result["status"] == "PASS"


def test_missing_expected_provider_is_discovery_mismatch():
    result = evaluate([{"provider_id": "mpfb"}], {"providers": []})
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "DISCOVERY_MISMATCH"

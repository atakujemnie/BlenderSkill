from executors.asset_execution_authorization_gate import evaluate


def _asset(stage="BLOCKOUT", state="CONSTRAINED"):
    return {
        "asset_id": "ASSET-1",
        "revision": 3,
        "stage": stage,
        "components": {
            "ROOT": {"parent": None, "state": "ACCEPTED", "anchors": {}, "dimensions": {}},
            "PART": {
                "parent": "ROOT",
                "state": state,
                "depends_on": ["ROOT"],
                "anchors": {},
                "dimensions": {},
            },
        },
        "corrections": [],
    }


def test_authorization_is_derived_from_persisted_state():
    result = evaluate(_asset(), "PART")
    assert result["status"] == "PASS", result
    assert result["validator_id"] == "ASSET_EXECUTION_AUTHORIZATION_GATE"
    assert result["validator_version"] == "0.22.0"
    assert result["source"] == "SYSTEM"
    assert result["asset_revision"] == 3


def test_pre_blockout_stage_is_not_build_authorizable():
    result = evaluate(_asset(stage="RECONSTRUCTION_MANIFEST"), "PART")
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "ASSET_STAGE_NOT_BUILDABLE" for item in result["blockers"])


def test_unaccepted_dependency_blocks_authorization():
    asset = _asset()
    asset["components"]["ROOT"]["state"] = "CONSTRAINED"
    result = evaluate(asset, "PART")
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "COMPONENT_DEPENDENCY_NOT_ACCEPTED" for item in result["blockers"])


def test_open_hard_component_correction_blocks_authorization():
    asset = _asset()
    asset["corrections"] = [
        {"id": "C1", "component_id": "PART", "priority": "HARD", "status": "OPEN"}
    ]
    result = evaluate(asset, "PART")
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "OPEN_HARD_COMPONENT_CORRECTIONS" for item in result["blockers"])


def test_structurally_accepted_component_can_be_reauthorized_for_details_stage():
    asset = _asset(stage="DETAILS", state="ACCEPTED")
    asset["components"]["PART"]["acceptance_level"] = "STRUCTURAL"
    result = evaluate(asset, "PART")
    assert result["status"] == "PASS", result
    assert result["component_acceptance_level"] == "STRUCTURAL"

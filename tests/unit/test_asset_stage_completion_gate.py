from executors.asset_stage_completion_gate import validate


def _asset(stage="STRUCTURAL_GEOMETRY", level="STRUCTURAL"):
    return {
        "asset_id": "A-STAGE-22",
        "revision": 5,
        "stage": stage,
        "enforce_feature_contracts": True,
        "components": {
            "ROOT": {"parent": None, "state": "ACCEPTED", "shape_class": "ASSEMBLY"},
            "BODY": {
                "parent": "ROOT",
                "state": "ACCEPTED",
                "acceptance_level": level,
                "shape_class": "PROFILE_PRISM",
                "feature_contract": {"features": [{"feature_id": "F1", "priority": "MUST"}]},
            },
        },
    }


def test_entering_structural_geometry_is_not_blocked_before_structural_tasks_exist():
    asset = _asset(stage="BLOCKOUT", level="NONE")
    asset["components"]["BODY"]["state"] = "CONSTRAINED"
    result = validate(asset, "STRUCTURAL_GEOMETRY")
    assert result["status"] == "PASS", result


def test_cannot_leave_structural_geometry_until_components_are_structurally_accepted():
    asset = _asset(level="BLOCKOUT")
    result = validate(asset, "DETAILS")
    assert result["status"] == "BLOCKED"
    assert result["blockers"][0]["reason"] == "ASSET_STAGE_COMPONENTS_INCOMPLETE"


def test_v021_accepted_component_without_level_is_treated_as_structural_only():
    asset = _asset()
    asset["components"]["BODY"].pop("acceptance_level")
    assert validate(asset, "DETAILS")["status"] == "PASS"
    asset["stage"] = "DETAILS"
    result = validate(asset, "MATERIALS")
    assert result["status"] == "BLOCKED"


def test_final_approval_requires_current_visual_fidelity_review():
    asset = _asset(stage="FIDELITY_AUDIT", level="FIDELITY")
    missing = validate(asset, "APPROVED", scene_revision=8, reference_revision=4)
    assert missing["status"] == "BLOCKED"
    review = {
        "status": "PASS",
        "asset_id": asset["asset_id"],
        "asset_revision": asset["revision"],
        "scene_revision": 8,
        "reference_revision": 4,
    }
    assert validate(asset, "APPROVED", fidelity_review=review, scene_revision=8, reference_revision=4)["status"] == "PASS"
    review["scene_revision"] = 7
    stale = validate(asset, "APPROVED", fidelity_review=review, scene_revision=8, reference_revision=4)
    assert stale["status"] == "BLOCKED"

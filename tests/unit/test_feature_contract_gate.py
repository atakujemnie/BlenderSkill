from executors.feature_contract_gate import validate


def _pack(feature):
    return {
        "asset_id": "A22",
        "asset_revision": 7,
        "component_id": "PANEL",
        "component": {
            "id": "PANEL",
            "feature_contract_required": True,
            "feature_contract": {"features": [feature]},
        },
    }


def _snapshot(proofs=None, feature_ids=None):
    return {
        "asset_id": "A22",
        "asset_revision": 7,
        "scene_revision": 3,
        "objects": [
            {
                "object_id": "panel",
                "component_id": "PANEL",
                "feature_ids": list(feature_ids or []),
                "feature_proofs": list(proofs or []),
            }
        ],
    }


def test_must_feature_fails_when_reference_detail_is_not_in_recipe():
    feature = {
        "feature_id": "CORNER_FASTENERS",
        "priority": "MUST",
        "expected_count": 4,
        "required_operations": ["CYLINDER"],
        "require_scene_proof": True,
    }
    recipe = {
        "component_id": "PANEL",
        "operations": [{"id": "body", "op": "ROUNDED_BOX", "output": "BODY"}],
    }
    result = validate(_pack(feature), recipe, _snapshot())
    assert result["status"] == "FAIL"
    reasons = {item["reason"] for item in result["blockers"]}
    assert "FEATURE_REQUIRED_OPERATIONS_MISSING" in reasons
    assert "FEATURE_COUNT_MISMATCH" in reasons
    assert "FEATURE_SCENE_PROOF_REQUIRED" in reasons


def test_repeated_vent_feature_passes_only_with_count_and_measured_boolean_proof():
    feature = {
        "feature_id": "SERVICE_PANEL_VENTS",
        "priority": "MUST",
        "expected_count": 8,
        "required_operations": ["CAPSULE_PRISM", "ARRAY", "BOOLEAN_CUT"],
        "required_proof_types": ["REPEAT", "BOOLEAN_EFFECT"],
        "expected_measurements": {
            "repeat_count": {"value": 8},
            "pitch_mm": {"value": 36, "tolerance_mm": 0.01},
            "material_removed_mm3": {"min": 1},
        },
        "require_scene_proof": True,
    }
    recipe = {
        "component_id": "PANEL",
        "operations": [
            {"id": "slot", "op": "CAPSULE_PRISM", "output": "SLOT", "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "repeat", "op": "ARRAY", "source": "SLOT", "count": 8, "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "cut", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "SLOT", "feature_id": "SERVICE_PANEL_VENTS"},
        ],
    }
    proofs = [
        {
            "feature_id": "SERVICE_PANEL_VENTS",
            "proof_type": "REPEAT",
            "metrics": {"repeat_count": 8, "pitch_mm": 36},
        },
        {
            "feature_id": "SERVICE_PANEL_VENTS",
            "proof_type": "BOOLEAN_EFFECT",
            "metrics": {"material_removed_mm3": 1234},
        },
    ]
    result = validate(_pack(feature), recipe, _snapshot(proofs, ["SERVICE_PANEL_VENTS"]))
    assert result["status"] == "PASS", result
    assert result["must_feature_coverage"] == 1.0


def test_should_feature_warns_but_does_not_block():
    feature = {
        "feature_id": "MICRO_CHAMFER",
        "priority": "SHOULD",
        "required_operations": ["BEVEL"],
        "require_scene_proof": True,
    }
    result = validate(_pack(feature), {"component_id": "PANEL", "operations": []}, _snapshot())
    assert result["status"] == "PASS"
    assert result["warnings"]

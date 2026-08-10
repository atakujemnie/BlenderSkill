from executors.asset_stage_completion_gate import validate as validate_stage
from executors.feature_contract_gate import validate as validate_features
from executors.visual_fidelity_review_gate import validate as validate_visual


def _pack(features):
    return {
        "asset_id": "LAFAR-SERVICE-TERMINAL-B92",
        "asset_revision": 20,
        "component_id": "DETAILS",
        "component": {
            "id": "DETAILS",
            "feature_contract_required": True,
            "feature_contract": {"features": features},
        },
    }


def _feature(feature_id, **values):
    return {"feature_id": feature_id, "priority": "MUST", **values}


def _snapshot(proofs):
    return {
        "asset_id": "LAFAR-SERVICE-TERMINAL-B92",
        "asset_revision": 20,
        "scene_revision": 8,
        "objects": [
            {
                "object_id": "terminal.details",
                "component_id": "DETAILS",
                "feature_ids": sorted({item["feature_id"] for item in proofs}),
                "feature_proofs": proofs,
            }
        ],
    }


def test_benchmark_92_blocks_flat_sensor_dots_and_missing_fasteners():
    features = [
        _feature("SENSOR_RINGS", expected_count=3, required_operations=["RING"]),
        _feature("SENSOR_LENSES", expected_count=3, required_operations=["CYLINDER"]),
        _feature("SERVICE_PANEL_FASTENERS", expected_count=4, required_operations=["CYLINDER"]),
    ]
    flat_dots = {
        "component_id": "DETAILS",
        "operations": [
            {"id": "sensor", "op": "CYLINDER", "output": "SENSOR", "feature_id": "SENSOR_LENSES"},
            {"id": "sensor_array", "op": "ARRAY", "source": "SENSOR", "count": 3, "feature_id": "SENSOR_LENSES"},
        ],
    }
    result = validate_features(_pack(features), flat_dots, _snapshot([]))
    assert result["status"] == "FAIL"
    reasons = {item["reason"] for item in result["blockers"]}
    assert "FEATURE_REQUIRED_OPERATIONS_MISSING" in reasons
    assert "FEATURE_COUNT_MISMATCH" in reasons


def test_benchmark_92_requires_eight_measured_rounded_vents():
    feature = _feature(
        "SERVICE_PANEL_VENTS",
        expected_count=8,
        required_operations=["CAPSULE_PRISM", "ARRAY", "BOOLEAN_CUT"],
        required_proof_types=["REPEAT", "BOOLEAN_EFFECT"],
        expected_measurements={
            "repeat_count": {"value": 8},
            "material_removed_mm3": {"min": 1},
        },
    )
    recipe = {
        "component_id": "DETAILS",
        "operations": [
            {"id": "slot", "op": "CAPSULE_PRISM", "output": "SLOT", "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "array", "op": "ARRAY", "source": "SLOT", "count": 8, "feature_id": "SERVICE_PANEL_VENTS"},
            {"id": "cut", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "SLOT", "feature_id": "SERVICE_PANEL_VENTS"},
        ],
    }
    no_effect = _snapshot(
        [
            {"feature_id": "SERVICE_PANEL_VENTS", "proof_type": "REPEAT", "metrics": {"repeat_count": 8}},
            {"feature_id": "SERVICE_PANEL_VENTS", "proof_type": "BOOLEAN_EFFECT", "metrics": {"material_removed_mm3": 0}},
        ]
    )
    assert validate_features(_pack([feature]), recipe, no_effect)["status"] == "FAIL"
    measured = _snapshot(
        [
            {"feature_id": "SERVICE_PANEL_VENTS", "proof_type": "REPEAT", "metrics": {"repeat_count": 8}},
            {"feature_id": "SERVICE_PANEL_VENTS", "proof_type": "BOOLEAN_EFFECT", "metrics": {"material_removed_mm3": 24000}},
        ]
    )
    assert validate_features(_pack([feature]), recipe, measured)["status"] == "PASS"


def _visual_asset():
    return {
        "asset_id": "LAFAR-SERVICE-TERMINAL-B92",
        "revision": 30,
        "components": {
            "ROOT": {"parent": None, "shape_class": "ASSEMBLY", "state": "ACCEPTED"},
            "DETAILS": {
                "parent": "ROOT",
                "state": "ACCEPTED",
                "acceptance_level": "FIDELITY",
                "feature_contract": {
                    "features": [
                        _feature("TOP_CAP_UNDERCUT", visual_required=True, qa_views=["FRONT", "SIDE"]),
                        _feature("SIDE_LED_CHANNEL", visual_required=True, qa_views=["SIDE"]),
                        _feature("SENSOR_RING_DEPTH", visual_required=True, qa_views=["SENSOR_DETAIL"]),
                        _feature("SERVICE_PANEL_FASTENERS", visual_required=True, qa_views=["FRONT"]),
                    ]
                },
            },
        },
        "enforce_feature_contracts": True,
        "stage": "FIDELITY_AUDIT",
    }


def _visual_review():
    return {
        "asset_id": "LAFAR-SERVICE-TERMINAL-B92",
        "asset_revision": 30,
        "scene_revision": 11,
        "reference_revision": 6,
        "reviewer_id": "reviewer-b92",
        "worker_id": "builder-b92",
        "reviewer_role": "INDEPENDENT_VISUAL_REVIEWER",
        "qa_views": [
            {"view_id": "FRONT", "render_artifact_id": "front", "reference_evidence_ids": ["ref-front"]},
            {"view_id": "SIDE", "render_artifact_id": "side", "reference_evidence_ids": ["ref-side"]},
            {"view_id": "SENSOR_DETAIL", "render_artifact_id": "sensor", "reference_evidence_ids": ["ref-sensor"]},
        ],
        "feature_reviews": [
            {"feature_id": "TOP_CAP_UNDERCUT", "status": "PASS", "view_ids": ["FRONT", "SIDE"]},
            {"feature_id": "SIDE_LED_CHANNEL", "status": "PASS", "view_ids": ["SIDE"]},
            {"feature_id": "SENSOR_RING_DEPTH", "status": "PASS", "view_ids": ["SENSOR_DETAIL"]},
            {"feature_id": "SERVICE_PANEL_FASTENERS", "status": "PASS", "view_ids": ["FRONT"]},
        ],
        "discovered_unmapped_features": [],
        "global_similarity_score": 0.92,
        "minimum_global_similarity_score": 0.75,
    }


def test_benchmark_92_global_score_cannot_hide_failed_must_feature():
    review = _visual_review()
    review["global_similarity_score"] = 0.99
    review["feature_reviews"][2]["status"] = "FAIL"
    result = validate_visual(_visual_asset(), review, scene_revision=11, reference_revision=6)
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "MUST_VISUAL_FEATURE_FAILED" for item in result["blockers"])


def test_benchmark_92_newly_discovered_reference_detail_blocks_final_review():
    review = _visual_review()
    review["discovered_unmapped_features"] = [
        {"temporary_id": "DISPLAY_BEZEL_STEP", "component_id": "DETAILS", "view_id": "FRONT"}
    ]
    result = validate_visual(_visual_asset(), review, scene_revision=11, reference_revision=6)
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "UNMAPPED_REFERENCE_FEATURES_DISCOVERED" for item in result["blockers"])


def test_benchmark_92_structural_success_is_not_final_success_and_review_must_be_current():
    asset = _visual_asset()
    asset["stage"] = "STRUCTURAL_GEOMETRY"
    asset["components"]["DETAILS"]["acceptance_level"] = "STRUCTURAL"
    assert validate_stage(asset, "DETAILS")["status"] == "PASS"
    asset["stage"] = "FIDELITY_AUDIT"
    asset["components"]["DETAILS"]["acceptance_level"] = "FIDELITY"
    no_review = validate_stage(asset, "APPROVED", scene_revision=11, reference_revision=6)
    assert no_review["status"] == "BLOCKED"
    visual = validate_visual(asset, _visual_review(), scene_revision=11, reference_revision=6)
    assert visual["status"] == "PASS", visual
    persisted = {
        "status": "PASS",
        "asset_id": asset["asset_id"],
        "asset_revision": asset["revision"],
        "scene_revision": 11,
        "reference_revision": 6,
    }
    assert validate_stage(asset, "APPROVED", fidelity_review=persisted, scene_revision=11, reference_revision=6)["status"] == "PASS"
    persisted["reference_revision"] = 5
    assert validate_stage(asset, "APPROVED", fidelity_review=persisted, scene_revision=11, reference_revision=6)["status"] == "BLOCKED"

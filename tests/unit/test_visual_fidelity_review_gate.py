from executors.visual_fidelity_review_gate import validate


def _asset():
    return {
        "asset_id": "TERMINAL-92",
        "revision": 12,
        "components": {
            "SENSOR": {
                "feature_contract": {
                    "features": [
                        {
                            "feature_id": "SENSOR_RING",
                            "priority": "MUST",
                            "visual_required": True,
                            "qa_views": ["FRONT", "DETAIL_SENSOR"],
                        },
                        {
                            "feature_id": "LENS_DEPTH",
                            "priority": "MUST",
                            "visual_required": True,
                            "qa_views": ["DETAIL_SENSOR"],
                        },
                    ]
                }
            }
        },
    }


def _review():
    return {
        "asset_id": "TERMINAL-92",
        "asset_revision": 12,
        "scene_revision": 4,
        "reference_revision": 9,
        "reviewer_id": "visual-reviewer-1",
        "worker_id": "builder-1",
        "reviewer_role": "INDEPENDENT_VISUAL_REVIEWER",
        "qa_views": [
            {
                "view_id": "FRONT",
                "render_artifact_id": "render-front",
                "reference_evidence_ids": ["ref-front"],
            },
            {
                "view_id": "DETAIL_SENSOR",
                "render_artifact_id": "render-sensor",
                "reference_evidence_ids": ["ref-sensor"],
            },
        ],
        "feature_reviews": [
            {"feature_id": "SENSOR_RING", "status": "PASS", "view_ids": ["DETAIL_SENSOR"]},
            {"feature_id": "LENS_DEPTH", "status": "PASS", "view_ids": ["DETAIL_SENSOR"]},
        ],
        "discovered_unmapped_features": [],
    }


def test_independent_multiview_review_passes_when_every_must_feature_passes():
    result = validate(_asset(), _review(), scene_revision=4, reference_revision=9)
    assert result["status"] == "PASS", result
    assert result["must_visual_feature_count"] == 2


def test_missing_must_feature_blocks_even_with_high_global_similarity():
    review = _review()
    review["feature_reviews"] = review["feature_reviews"][:1]
    review["global_similarity_score"] = 0.99
    result = validate(_asset(), review, scene_revision=4, reference_revision=9)
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "MUST_VISUAL_FEATURES_NOT_REVIEWED" for item in result["blockers"])


def test_reviewer_discovered_missing_reference_detail_blocks_until_contract_is_updated():
    review = _review()
    review["discovered_unmapped_features"] = [
        {"temporary_id": "DISCOVERED_FASTENER", "component_id": "PANEL", "view_id": "FRONT"}
    ]
    result = validate(_asset(), review, scene_revision=4, reference_revision=9)
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "UNMAPPED_REFERENCE_FEATURES_DISCOVERED" for item in result["blockers"])


def test_review_is_revision_bound_and_builder_cannot_review_itself():
    review = _review()
    review["reviewer_id"] = "builder-1"
    review["scene_revision"] = 3
    result = validate(_asset(), review, scene_revision=4, reference_revision=9)
    reasons = {item["reason"] for item in result["blockers"]}
    assert "VISUAL_REVIEWER_MUST_DIFFER_FROM_WORKER" in reasons
    assert "FIDELITY_REVIEW_SCENE_REVISION_STALE" in reasons

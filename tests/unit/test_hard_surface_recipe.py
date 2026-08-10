from executors.hard_surface_recipe import compact_summary, validate


def test_compact_manufactured_component_recipe_passes():
    recipe = {
        "component_id": "RIGHT_SUPPORT",
        "operations": [
            {
                "id": "body",
                "op": "ROUNDED_BOX",
                "output": "BODY",
                "dimensions": {"width": 210, "depth": 535, "height": 460},
            },
            {
                "id": "panel_cutter",
                "op": "BOX",
                "output": "PANEL_CUTTER",
                "dimensions": {"width": 55, "depth": 12, "height": 75},
            },
            {
                "id": "panel_recess",
                "op": "BOOLEAN_CUT",
                "target": "BODY",
                "cutter": "PANEL_CUTTER",
            },
            {
                "id": "edge_bevel",
                "op": "BEVEL",
                "target": "BODY",
                "width": 8,
                "segments": 3,
            },
            {
                "id": "material",
                "op": "ASSIGN_BINDING",
                "target": "BODY",
                "binding_id": "structural_material",
            },
        ],
        "final_outputs": ["BODY"],
    }
    result = validate(recipe)
    assert result["status"] == "PASS", result
    summary = compact_summary(recipe)
    assert summary["operation_count"] == 5
    assert summary["operation_types"]["BOOLEAN_CUT"] == 1


def test_recipe_rejects_boolean_before_required_geometry_exists():
    result = validate(
        {
            "component_id": "BROKEN",
            "operations": [
                {"id": "cut", "op": "BOOLEAN_CUT", "target": "BODY", "cutter": "CUTTER"},
            ],
            "final_outputs": ["BODY"],
        }
    )
    assert result["status"] == "FAIL"
    reasons = {item["reason"] for item in result["blockers"]}
    assert "BOOLEAN_TARGET_NOT_AVAILABLE" in reasons
    assert "BOOLEAN_CUTTER_NOT_AVAILABLE" in reasons

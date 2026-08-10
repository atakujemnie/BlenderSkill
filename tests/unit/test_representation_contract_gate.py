from executors.representation_contract_gate import validate


def _task_pack(shape_class: str, contract=None):
    return {
        "component_id": "PART",
        "component": {
            "id": "PART",
            "shape_class": shape_class,
            "representation_contract": contract or {},
        },
    }


def test_tactile_panel_rejects_plain_box_recipe():
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "body", "op": "ROUNDED_BOX", "output": "BODY", "dimensions": {"width": 1000, "depth": 150, "height": 10}}
        ],
        "final_outputs": ["BODY"],
    }
    result = validate(_task_pack("TACTILE_GRID_PANEL"), recipe)
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "REPRESENTATION_REQUIRED_OPERATION_MISSING"


def test_tactile_panel_accepts_instanced_or_array_representation():
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "dot", "op": "BOX", "output": "DOT", "dimensions": {"width": 10, "depth": 10, "height": 3}},
            {"id": "repeat", "op": "ARRAY", "source": "DOT", "count": 20, "constant_offset_mm": [22, 0, 0]},
        ],
        "final_outputs": ["DOT"],
    }
    result = validate(_task_pack("TACTILE_GRID_PANEL"), recipe)
    assert result["status"] == "PASS", result


def test_explicit_contract_requires_features_and_repeat_count():
    contract = {"required_feature_ids": ["SLOTS"], "minimum_repeat_count": 10}
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "bar", "op": "BOX", "output": "BAR", "dimensions": {"width": 10, "depth": 100, "height": 8}, "feature_id": "SLOTS"},
            {"id": "repeat", "op": "ARRAY", "source": "BAR", "count": 12, "constant_offset_mm": [18, 0, 0]},
        ],
        "final_outputs": ["BAR"],
    }
    result = validate(_task_pack("SLOTTED_GRATE_PLATE", contract), recipe)
    assert result["status"] == "PASS", result

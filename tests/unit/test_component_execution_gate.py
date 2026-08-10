from executors.component_execution_gate import authorize


def _pack(shape_class="ROUNDED_BOX", *, explicit=True, representation_contract=None):
    return {
        "asset_id": "ASSET-1",
        "asset_revision": 2,
        "component_id": "PART",
        "allowed_to_modify": ["PART"],
        "component": {
            "id": "PART",
            "shape_class": shape_class,
            "placement_required": explicit,
            "representation_contract": representation_contract or {},
            "transform": {
                "location_mm": [500.0, -500.0, 120.0],
                "rotation_deg": [0.0, 0.0, 0.0],
                "scale": [1.0, 1.0, 1.0],
                "coordinate_space": "ASSET_LOCAL",
                "explicit": explicit,
                "source": "TRANSFORM" if explicit else "IMPLICIT_ORIGIN",
            },
        },
    }


def test_authorized_recipe_receives_canonical_component_transform():
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "body", "op": "ROUNDED_BOX", "output": "BODY", "dimensions": {"width": 994, "depth": 994, "height": 40}}
        ],
        "final_outputs": ["BODY"],
    }
    result = authorize(_pack(), recipe)
    assert result["status"] == "PASS", result
    assert result["recipe"]["component_transform"]["location_mm"] == [500.0, -500.0, 120.0]
    assert result["recipe"]["task_pack_asset_revision"] == 2


def test_representation_failure_blocks_before_blender_mutation():
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "body", "op": "ROUNDED_BOX", "output": "BODY", "dimensions": {"width": 1000, "depth": 150, "height": 10}}
        ],
        "final_outputs": ["BODY"],
    }
    result = authorize(_pack("TACTILE_GRID_PANEL"), recipe)
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "REPRESENTATION_REQUIRED_OPERATION_MISSING" for item in result["blockers"])


def test_required_placement_cannot_silently_fall_back_to_origin():
    recipe = {
        "component_id": "PART",
        "operations": [
            {"id": "body", "op": "BOX", "output": "BODY", "dimensions": {"width": 100, "depth": 100, "height": 100}}
        ],
        "final_outputs": ["BODY"],
    }
    pack = _pack(explicit=False)
    pack["component"]["placement_required"] = True
    result = authorize(pack, recipe)
    assert result["status"] == "BLOCKED"
    assert any(item["reason"] == "EXPLICIT_COMPONENT_PLACEMENT_REQUIRED" for item in result["blockers"])

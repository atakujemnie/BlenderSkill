from executors.scene_component_validation import validate


def _pack():
    return {
        "asset_id": "ASSET-1",
        "asset_revision": 4,
        "component_id": "SLAB",
        "component": {
            "id": "SLAB",
            "transform": {"location_mm": [500, -500, 120]},
        },
        "resolved_parameters": {
            "width": {"value": 994, "unit": "mm"},
            "depth": {"value": 1000, "unit": "mm"},
            "height": {"value": 40, "unit": "mm"},
        },
        "resolved_design_bindings": {},
        "validation_contract": {
            "placement_tolerance_mm": 0.5,
            "require_dimensions_match": True,
            "dimension_tolerance_mm": 0.5,
        },
    }


def _snapshot(location=(500, -500, 120), dimensions=(994, 1000, 40), asset_revision=4, scene_revision=2):
    return {
        "asset_id": "ASSET-1",
        "asset_revision": asset_revision,
        "scene_revision": scene_revision,
        "snapshot_hash": "snapshot-hash",
        "objects": [
            {
                "object_id": "slab",
                "component_id": "SLAB",
                "object_type": "MESH",
                "transform": {"location_mm": list(location)},
                "dimensions_mm": list(dimensions),
                "material_ids": [],
            }
        ],
    }


def test_current_scene_exact_placement_and_dimensions_pass():
    result = validate(_pack(), _snapshot())
    assert result["status"] == "PASS", result
    assert result["scene_revision"] == 2


def test_wrong_component_placement_fails():
    result = validate(_pack(), _snapshot(location=(0, 0, 120)))
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "SCENE_COMPONENT_PLACEMENT_MISMATCH" for item in result["blockers"])


def test_stale_asset_revision_fails():
    result = validate(_pack(), _snapshot(asset_revision=3))
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "SCENE_ASSET_REVISION_MISMATCH" for item in result["blockers"])


def test_wrong_dimensions_fail_when_contract_requires_match():
    result = validate(_pack(), _snapshot(dimensions=(900, 1000, 40)))
    assert result["status"] == "FAIL"
    assert any(item["reason"] == "SCENE_COMPONENT_DIMENSIONS_MISMATCH" for item in result["blockers"])

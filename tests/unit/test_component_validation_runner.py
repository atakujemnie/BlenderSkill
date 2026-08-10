from executors.component_validation_runner import validate_and_publish
from executors.validation_receipt_repository import initialize, query


def _pack():
    return {
        "asset_id": "ASSET-1",
        "asset_revision": 4,
        "component_id": "SLAB",
        "allowed_to_modify": ["SLAB"],
        "component": {
            "id": "SLAB",
            "shape_class": "ROUNDED_BOX",
            "representation_contract": {},
            "transform": {
                "location_mm": [500, -500, 120],
                "rotation_deg": [0, 0, 0],
                "scale": [1, 1, 1],
                "coordinate_space": "ASSET_LOCAL",
                "explicit": True,
            },
        },
        "resolved_parameters": {
            "width": {"value": 994, "unit": "mm"},
            "depth": {"value": 1000, "unit": "mm"},
            "height": {"value": 40, "unit": "mm"},
        },
        "resolved_design_bindings": {},
        "validation_contract": {"require_dimensions_match": True},
    }


def _recipe():
    return {
        "component_id": "SLAB",
        "operations": [
            {"id": "body", "op": "ROUNDED_BOX", "output": "BODY", "dimensions": {"width": 994, "depth": 1000, "height": 40}}
        ],
        "final_outputs": ["BODY"],
    }


def _snapshot(location=(500, -500, 120)):
    return {
        "asset_id": "ASSET-1",
        "asset_revision": 4,
        "scene_revision": 2,
        "snapshot_hash": "snapshot-2",
        "objects": [
            {
                "object_id": "slab",
                "component_id": "SLAB",
                "object_type": "MESH",
                "transform": {"location_mm": list(location)},
                "dimensions_mm": [994, 1000, 40],
            }
        ],
    }


def test_runner_publishes_two_system_pass_receipts(tmp_path):
    initialize(tmp_path, "ASSET-1")
    result = validate_and_publish(tmp_path, _pack(), _recipe(), _snapshot())
    assert result["status"] == "PASS", result
    assert {item["validator_id"] for item in result["receipts"]} == {
        "REPRESENTATION_CONTRACT_GATE",
        "SCENE_COMPONENT_VALIDATION",
    }
    current = query(
        tmp_path,
        "ASSET-1",
        component_id="SLAB",
        asset_revision=4,
        scene_revision=2,
    )
    assert len(current["receipts"]) == 2
    assert all(item["source"] == "SYSTEM" for item in current["receipts"])
    assert all(item["status"] == "PASS" for item in current["receipts"])


def test_runner_persists_fail_receipt_and_cannot_report_pass_for_wrong_scene(tmp_path):
    initialize(tmp_path, "ASSET-1")
    result = validate_and_publish(tmp_path, _pack(), _recipe(), _snapshot(location=(0, 0, 120)))
    assert result["status"] == "FAIL"
    scene = result["validators"]["SCENE_COMPONENT_VALIDATION"]
    assert scene["status"] == "FAIL"
    current = query(
        tmp_path,
        "ASSET-1",
        component_id="SLAB",
        asset_revision=4,
        scene_revision=2,
        validator_ids=["SCENE_COMPONENT_VALIDATION"],
    )
    assert current["receipts"][0]["status"] == "FAIL"

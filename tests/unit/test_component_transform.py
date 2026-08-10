from executors.component_transform import normalize


def test_legacy_center_offset_becomes_explicit_asset_local_transform():
    result = normalize({"center_offset": {"x": 500, "y": -500}})
    assert result["status"] == "PASS", result
    assert result["transform"] == {
        "location_mm": [500.0, -500.0, 0.0],
        "rotation_deg": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "coordinate_space": "ASSET_LOCAL",
        "explicit": True,
        "source": "LEGACY_CENTER_OFFSET",
    }


def test_explicit_transform_is_preserved():
    result = normalize(
        {
            "transform": {
                "location_mm": [100, 200, 30],
                "rotation_deg": [0, 0, 90],
                "scale": [1, 1, 1],
                "coordinate_space": "ASSET_LOCAL",
            }
        }
    )
    assert result["status"] == "PASS", result
    assert result["transform"]["location_mm"] == [100.0, 200.0, 30.0]
    assert result["transform"]["rotation_deg"] == [0.0, 0.0, 90.0]
    assert result["transform"]["explicit"] is True


def test_zero_scale_and_invalid_coordinate_space_fail_closed():
    result = normalize(
        {
            "transform": {
                "location_mm": [0, 0, 0],
                "scale": [1, 0, 1],
                "coordinate_space": "WORLD",
            }
        }
    )
    assert result["status"] == "FAIL"
    reasons = {item["reason"] for item in result["blockers"]}
    assert "COMPONENT_COORDINATE_SPACE_INVALID" in reasons
    assert "COMPONENT_SCALE_ZERO_FORBIDDEN" in reasons

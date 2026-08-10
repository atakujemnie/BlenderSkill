from executors.asset_envelope_gate import validate


def _asset(slab_width: int, *, outside=False):
    components = {
        "ROOT": {
            "parent": None,
            "origin": {"type": "CENTER_XY_BOTTOM_Z"},
            "dimensions": {
                "width": {"value": 2000, "unit": "mm"},
                "depth": {"value": 2000, "unit": "mm"},
                "height": {"value": 160, "unit": "mm"},
            },
        },
        "SLAB_L": {
            "parent": "ROOT",
            "origin": {"type": "CENTER_BOTTOM"},
            "transform": {"location_mm": [-500, 0, 120]},
            "dimensions": {
                "width": {"value": slab_width, "unit": "mm"},
                "depth": {"value": 1000, "unit": "mm"},
                "height": {"value": 40, "unit": "mm"},
            },
        },
        "SLAB_R": {
            "parent": "ROOT",
            "origin": {"type": "CENTER_BOTTOM"},
            "transform": {"location_mm": [500, 0, 120]},
            "dimensions": {
                "width": {"value": slab_width, "unit": "mm"},
                "depth": {"value": 1000, "unit": "mm"},
                "height": {"value": 40, "unit": "mm"},
            },
        },
    }
    if outside:
        components["DRAIN"] = {
            "parent": "ROOT",
            "origin": {"type": "CENTER_BOTTOM"},
            "transform": {"location_mm": [0, -1060, 40]},
            "dimensions": {
                "width": {"value": 2000, "unit": "mm"},
                "depth": {"value": 120, "unit": "mm"},
                "height": {"value": 60, "unit": "mm"},
            },
        }
    return {
        "asset_id": "SIDEWALK",
        "components": components,
        "seam_constraints": [
            {"a": "SLAB_L", "b": "SLAB_R", "axis": "X", "expected_gap_mm": 6, "tolerance_mm": 0.5}
        ],
    }


def test_declared_six_mm_seam_rejects_geometry_that_measures_four_mm():
    result = validate(_asset(996))
    assert result["status"] == "FAIL"
    mismatch = next(item for item in result["blockers"] if item["reason"] == "SEAM_GAP_MISMATCH")
    assert mismatch["measured_gap_mm"] == 4.0
    assert mismatch["expected_gap_mm"] == 6.0


def test_six_mm_seam_passes_when_geometry_is_consistent():
    result = validate(_asset(994))
    assert result["status"] == "PASS", result
    assert result["root_aabb"] == {"min": [-1000.0, -1000.0, 0.0], "max": [1000.0, 1000.0, 160.0]}
    assert result["aabbs"]["SLAB_L"]["min"][2] == 120.0
    assert result["aabbs"]["SLAB_L"]["max"][2] == 160.0


def test_component_outside_nominal_footprint_is_rejected():
    result = validate(_asset(994, outside=True))
    assert result["status"] == "FAIL"
    assert any(
        item["reason"] == "COMPONENT_OUTSIDE_ASSET_ENVELOPE_Y" and item["component_id"] == "DRAIN"
        for item in result["blockers"]
    )

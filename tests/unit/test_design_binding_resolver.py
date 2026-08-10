from executors.design_binding_resolver import resolve


def _resources():
    return {
        "ASTERA_GRAPHITE_01": {
            "type": "MATERIAL",
            "version": "1.2",
            "locked": True,
            "roughness": 0.48,
        },
        "ASTERA_LED_UNDERGLOW_01": {
            "type": "LIGHTING_COMPONENT",
            "version": "1.4",
            "locked": True,
            "strip_width_mm": 18,
            "recess_depth_mm": 7,
            "emission_profile": "ASTERA_CIVIC_BLUE",
        },
    }


def test_inherited_locked_resources_are_reused_exactly():
    result = resolve(
        {
            "resources": _resources(),
            "bindings": {
                "material": {"resource_id": "ASTERA_GRAPHITE_01", "mode": "INHERITED"},
                "led": {"resource_id": "ASTERA_LED_UNDERGLOW_01", "mode": "INHERITED"},
            },
        }
    )
    assert result["status"] == "PASS"
    assert result["resolved_bindings"]["led"]["locked"] is True
    assert result["resolved_bindings"]["led"]["resolved"]["strip_width_mm"] == 18
    assert result["deviations"] == []


def test_locked_override_requires_authority():
    result = resolve(
        {
            "resources": _resources(),
            "bindings": {
                "led": {
                    "resource_id": "ASTERA_LED_UNDERGLOW_01",
                    "mode": "OVERRIDDEN",
                    "override": {"strip_width_mm": 25},
                }
            },
        }
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "LOCKED_RESOURCE_OVERRIDE_REQUIRES_AUTHORITY"


def test_authorized_override_is_visible_as_deviation():
    result = resolve(
        {
            "resources": _resources(),
            "bindings": {
                "led": {
                    "resource_id": "ASTERA_LED_UNDERGLOW_01",
                    "mode": "OVERRIDDEN",
                    "override": {"strip_width_mm": 20},
                    "authority_record_id": "ADR-12",
                }
            },
        }
    )
    assert result["status"] == "PASS"
    assert result["resolved_bindings"]["led"]["resolved"]["strip_width_mm"] == 20
    assert result["deviations"][0]["authority_record_id"] == "ADR-12"

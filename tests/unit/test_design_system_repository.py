from executors.design_system_repository import (
    impact_report,
    initialize,
    load,
    record_usage,
    resolve_binding,
    reverse_usage,
    save,
)


def _resource(revision: int = 1, version: str = "1.0.0") -> dict:
    return {
        "design_system_id": "ASTERA_CIVIC",
        "resource_id": "ASTERA_LED_UNDERGLOW_01",
        "kind": "LED_PROFILE",
        "version": version,
        "revision": revision,
        "locked": True,
        "payload": {"width_mm": 8.0, "temperature_k": 7200},
    }


def test_versioned_resource_and_reverse_usage(tmp_path):
    created = initialize(tmp_path, _resource())
    assert created["status"] == "PASS"

    resolved = resolve_binding(
        tmp_path,
        {
            "binding_id": "BENCH_UNDERGLOW",
            "design_system_id": "ASTERA_CIVIC",
            "resource_id": "ASTERA_LED_UNDERGLOW_01",
            "resource_version": "1.0.0",
        },
    )
    assert resolved["status"] == "PASS"
    assert resolved["locked"] is True

    usage = record_usage(
        tmp_path,
        {
            "design_system_id": "ASTERA_CIVIC",
            "resource_id": "ASTERA_LED_UNDERGLOW_01",
            "asset_id": "ASSET-005",
            "component_id": "SEAT",
            "binding_id": "BENCH_UNDERGLOW",
        },
    )
    assert usage["status"] == "PASS"
    assert usage["usage_count"] == 1

    reverse = reverse_usage(tmp_path, "ASTERA_CIVIC", "ASTERA_LED_UNDERGLOW_01")
    assert reverse["assets"] == ["ASSET-005"]
    assert reverse["usages"][0]["component_id"] == "SEAT"

    updated = _resource(revision=2, version="1.1.0")
    updated["payload"] = {"width_mm": 8.0, "temperature_k": 6800}
    saved = save(tmp_path, updated, expected_revision=1)
    assert saved["status"] == "PASS"

    old = load(tmp_path, "ASTERA_CIVIC", "ASTERA_LED_UNDERGLOW_01", revision=1)
    assert old["resource"]["version"] == "1.0.0"
    assert old["resource"]["payload"]["temperature_k"] == 7200

    impact = impact_report(tmp_path, "ASTERA_CIVIC", "ASTERA_LED_UNDERGLOW_01")
    assert impact["current_revision"] == 2
    assert impact["affected_asset_count"] == 1


def test_stale_resource_writer_is_rejected(tmp_path):
    assert initialize(tmp_path, _resource())["status"] == "PASS"
    updated = _resource(revision=2, version="1.1.0")
    result = save(tmp_path, updated, expected_revision=0)
    assert result["status"] == "CONFLICT"
    assert result["blockers"][0]["reason"] == "RESOURCE_REVISION_CONFLICT"

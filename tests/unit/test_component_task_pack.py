import json
from pathlib import Path

from executors.component_task_pack import build
from executors.parameter_graph import resolve as resolve_parameters


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _asset():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_backrest_task_pack_excludes_whole_asset_history_and_sibling_geometry():
    asset = _asset()
    params = resolve_parameters({"components": asset["components"]})["resolved"]
    bindings = {
        "structural_material": {"resource_id": "ASTERA_GRAPHITE_01", "locked": True},
        "trim_profile": {"resource_id": "ASTERA_TRIM_PROFILE_01", "locked": True},
        "info_strip_led": {"resource_id": "ASTERA_LED_INFO_BLUE_01", "locked": True},
    }
    result = build(
        {
            "asset": asset,
            "component_id": "BACKREST",
            "resolved_parameters": params,
            "resolved_bindings": bindings,
            "task_kind": "BUILD",
            "reference_evidence": [
                {
                    "reference_id": "bench_sheet",
                    "component_id": "BACKREST",
                    "view": "SIDE",
                    "roi": [690, 590, 840, 870],
                    "artifact_id": "crop:backrest-side",
                }
            ],
        }
    )
    assert result["status"] == "PASS"
    pack = result["task_pack"]
    assert pack["allowed_to_modify"] == ["BACKREST"]
    assert "SEAT" in pack["read_only"]
    assert "history" not in pack
    assert "global_dimensions_mm" not in pack
    assert pack["resolved_parameters"]["width"]["value"] == 1580.0
    assert set(pack["resolved_design_bindings"]) == {
        "structural_material",
        "trim_profile",
        "info_strip_led",
    }
    assert result["metrics"]["estimated_input_tokens"] < 4000


def test_repair_budget_and_bulk_context_protection_are_enforced():
    asset = _asset()
    result = build(
        {
            "asset": asset,
            "component_id": "SEAT",
            "task_kind": "REPAIR",
            "include_full_history": True,
        }
    )
    assert result["status"] == "FAIL"
    assert any(b["reason"] == "BULK_CONTEXT_FORBIDDEN_IN_COMPONENT_TASK" for b in result["blockers"])

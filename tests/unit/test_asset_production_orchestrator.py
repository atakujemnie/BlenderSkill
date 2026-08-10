import json
from pathlib import Path

from executors.asset_production_orchestrator import prepare_component_task


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _resources():
    return {
        "ASTERA_GRAPHITE_01": {"type": "MATERIAL", "version": "1", "locked": True},
        "ASTERA_TRIM_PROFILE_01": {"type": "PROFILE", "version": "1", "locked": True},
        "ASTERA_EDGE_PROFILE_02": {"type": "PROFILE", "version": "1", "locked": True},
        "ASTERA_LED_UNDERGLOW_01": {"type": "LIGHTING_COMPONENT", "version": "1", "locked": True},
        "ASTERA_LED_INFO_BLUE_01": {"type": "LIGHTING_COMPONENT", "version": "1", "locked": True},
        "ASTERA_UTILITY_PANEL_01": {"type": "COMPONENT", "version": "1", "locked": True},
    }


def test_orchestrator_reduces_full_bench_to_one_component_task():
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = prepare_component_task(
        {
            "asset": asset,
            "component_id": "BACKREST",
            "task_kind": "BUILD",
            "design_resources": _resources(),
            "reference_evidence": [
                {
                    "reference_id": "lafar-bench-sheet",
                    "component_id": "BACKREST",
                    "view": "SIDE",
                    "roi": [690, 590, 840, 870],
                    "artifact_id": "roi:backrest:side",
                }
            ],
        }
    )
    assert result["status"] == "PASS", result
    assert result["task_pack"]["allowed_to_modify"] == ["BACKREST"]
    assert result["metrics"]["resolved_parameter_count"] >= 10
    assert result["metrics"]["resolved_binding_count"] == 6
    assert result["metrics"]["estimated_input_tokens"] < 4000

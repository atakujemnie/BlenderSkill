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


def test_orchestrator_queries_reference_registry_by_component_and_feature():
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    registry = {
        "evidence": [
            {
                "evidence_id": "EV-BACKREST-SIDE",
                "reference_id": "lafar-bench-sheet",
                "component_id": "BACKREST",
                "view": "SIDE",
                "authority": "PRIMARY",
                "feature_ids": ["BACKREST_PROFILE"],
                "roi": [690, 590, 840, 870],
                "artifact_id": "roi:backrest:side",
                "registration_id": "reg:bench:side",
            },
            {
                "evidence_id": "EV-SEAT-TOP",
                "reference_id": "lafar-bench-sheet",
                "component_id": "SEAT",
                "view": "TOP",
                "authority": "PRIMARY",
                "feature_ids": ["SEAT_OUTLINE"],
                "roi": [100, 100, 500, 300],
                "artifact_id": "roi:seat:top",
            },
        ]
    }
    result = prepare_component_task(
        {
            "asset": asset,
            "component_id": "BACKREST",
            "task_kind": "REPAIR",
            "design_resources": _resources(),
            "reference_evidence_registry": registry,
            "reference_feature_ids": ["BACKREST_PROFILE"],
        }
    )
    assert result["status"] == "PASS", result
    evidence = result["task_pack"]["reference_evidence"]
    assert [item["evidence_id"] for item in evidence] == ["EV-BACKREST-SIDE"]
    assert evidence[0]["registration_id"] == "reg:bench:side"
    assert result["metrics"]["reference_registry_evidence_count"] == 1

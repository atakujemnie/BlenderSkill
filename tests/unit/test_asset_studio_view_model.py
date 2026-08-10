import json
from pathlib import Path

from executors.asset_studio_view_model import build
from executors.production_task_lifecycle import create, transition
from executors.scene_component_snapshot import build as build_snapshot


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def test_studio_view_model_joins_asset_tasks_and_scene_snapshot():
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
    task = create(
        {
            "task_id": "T-BACKREST",
            "asset_id": asset["asset_id"],
            "asset_revision": asset["revision"],
            "component_id": "BACKREST",
            "stage": asset["stage"],
            "allowed_to_modify": ["BACKREST"],
            "read_only": ["LEFT_SUPPORT", "RIGHT_SUPPORT", "SEAT"],
        }
    )["task"]
    task = transition(task, "READY", actor="ORCHESTRATOR", reason="READY")["task"]
    scene = build_snapshot(
        {
            "asset_id": asset["asset_id"],
            "asset_revision": asset["revision"],
            "scene_revision": 3,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, 72, 390],
                }
            ],
        }
    )["snapshot"]

    result = build(
        asset,
        tasks={"T-BACKREST": task},
        selected_component_id="BACKREST",
        scene_snapshot=scene,
        design_impacts=[{"resource_id": "ASTERA_LED_INFO_BLUE_01", "affected_asset_count": 4}],
    )
    assert result["status"] == "PASS"
    view = result["view_model"]
    assert view["asset"]["asset_id"] == asset["asset_id"]
    assert view["selected_component_id"] == "BACKREST"
    assert view["task_summary"]["READY"] == 1
    assert view["inspector"]["scene_objects"][0]["object_id"] == "bench.backrest.shell"
    assert view["design_impacts"][0]["affected_asset_count"] == 4

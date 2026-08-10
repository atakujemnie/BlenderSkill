import json
from pathlib import Path

from executors.asset_production_orchestrator import prepare_component_task
from executors.asset_studio_view_model import build as build_studio_view
from executors.design_system_repository import impact_report, initialize as initialize_resource, record_usage
from executors.production_iteration_gate import evaluate as evaluate_iteration
from executors.production_task_lifecycle import create as create_task
from executors.production_task_lifecycle import transition
from executors.production_task_repository import initialize as initialize_queue
from executors.production_task_repository import load as load_queue
from executors.production_task_repository import save as save_queue
from executors.scene_component_snapshot import build as build_snapshot


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


def _resolver_resources() -> dict:
    return {
        "ASTERA_GRAPHITE_01": {"type": "MATERIAL", "version": "1", "locked": True},
        "ASTERA_TRIM_PROFILE_01": {"type": "PROFILE", "version": "1", "locked": True},
        "ASTERA_EDGE_PROFILE_02": {"type": "PROFILE", "version": "1", "locked": True},
        "ASTERA_LED_UNDERGLOW_01": {"type": "LIGHTING_COMPONENT", "version": "1", "locked": True},
        "ASTERA_LED_INFO_BLUE_01": {"type": "LIGHTING_COMPONENT", "version": "1", "locked": True},
        "ASTERA_UTILITY_PANEL_01": {"type": "COMPONENT", "version": "1", "locked": True},
    }


def _snapshot(depth: int, seat_depth: int = 420) -> dict:
    return build_snapshot(
        {
            "asset_id": "ASSET-005",
            "asset_revision": 1,
            "scene_revision": depth,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, depth, 390],
                    "material_ids": ["ASTERA_GRAPHITE_01"],
                },
                {
                    "object_id": "bench.seat.shell",
                    "component_id": "SEAT",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, seat_depth, 82],
                    "material_ids": ["ASTERA_GRAPHITE_01"],
                },
            ],
        }
    )["snapshot"]


def test_benchmark_89_full_production_runtime(tmp_path):
    asset = json.loads(FIXTURE.read_text(encoding="utf-8"))

    resource = {
        "design_system_id": "ASTERA_CIVIC",
        "resource_id": "ASTERA_LED_INFO_BLUE_01",
        "kind": "LED_PROFILE",
        "version": "1.0.0",
        "revision": 1,
        "locked": True,
        "payload": {"strip_width_mm": 8, "color_temperature_k": 7200},
    }
    assert initialize_resource(tmp_path, resource)["status"] == "PASS"
    assert record_usage(
        tmp_path,
        {
            "design_system_id": "ASTERA_CIVIC",
            "resource_id": "ASTERA_LED_INFO_BLUE_01",
            "asset_id": asset["asset_id"],
            "component_id": "BACKREST",
            "binding_id": "info_strip_led",
        },
    )["status"] == "PASS"
    impact = impact_report(tmp_path, "ASTERA_CIVIC", "ASTERA_LED_INFO_BLUE_01")
    assert impact["affected_assets"] == ["ASSET-005"]

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
    prepared = prepare_component_task(
        {
            "asset": asset,
            "component_id": "BACKREST",
            "task_kind": "REPAIR",
            "design_resources": _resolver_resources(),
            "reference_evidence_registry": registry,
            "reference_feature_ids": ["BACKREST_PROFILE"],
        }
    )
    assert prepared["status"] == "PASS", prepared
    assert prepared["task_pack"]["allowed_to_modify"] == ["BACKREST"]
    assert prepared["metrics"]["estimated_input_tokens"] < 4000
    assert [item["evidence_id"] for item in prepared["task_pack"]["reference_evidence"]] == ["EV-BACKREST-SIDE"]

    task = create_task(
        {
            "task_id": "T-BACKREST",
            "asset_id": asset["asset_id"],
            "asset_revision": asset["revision"],
            "component_id": "BACKREST",
            "stage": asset["stage"],
            "task_kind": "REPAIR",
            "allowed_to_modify": prepared["task_pack"]["allowed_to_modify"],
            "read_only": prepared["task_pack"]["read_only"],
        }
    )["task"]
    task = transition(task, "READY", actor="ORCHESTRATOR", reason="DEPENDENCIES_SATISFIED")["task"]
    task = transition(task, "RUNNING", actor="WORKER", reason="CLAIMED", worker_id="benchmark-worker")["task"]

    assert initialize_queue(tmp_path, asset["asset_id"], {task["task_id"]: task})["status"] == "PASS"
    loaded_queue = load_queue(tmp_path, asset["asset_id"])
    assert loaded_queue["queue"]["queue_revision"] == 1

    before = _snapshot(72)
    after = _snapshot(76)
    iteration = evaluate_iteration(
        {
            "task": task,
            "current_asset_revision": asset["revision"],
            "scene_before": before,
            "scene_after": after,
            "validations": [
                {"validator_id": "ASSEMBLY_ANCHOR_GATE", "status": "PASS"},
                {"validator_id": "HARD_SURFACE_RECIPE", "status": "PASS"},
            ],
        }
    )
    assert iteration["status"] == "PASS", iteration
    assert iteration["result"]["scene_diff"]["changed_object_count"] == 1

    reviewed = transition(task, "REVIEW", actor="WORKER", reason="ITERATION_COMPLETE", result=iteration["result"])
    assert reviewed["status"] == "PASS"
    approved = transition(reviewed["task"], "APPROVED", actor="REVIEWER", reason="VALIDATED")
    assert approved["status"] == "PASS"

    saved_queue = save(
        tmp_path,
        asset["asset_id"],
        {approved["task"]["task_id"]: approved["task"]},
        expected_queue_revision=1,
    )
    assert saved_queue["status"] == "PASS"
    assert saved_queue["queue_revision"] == 2

    studio = build_studio_view(
        asset,
        tasks={approved["task"]["task_id"]: approved["task"]},
        selected_component_id="BACKREST",
        scene_snapshot=after,
        design_impacts=[impact],
    )
    assert studio["status"] == "PASS"
    assert studio["view_model"]["selected_component_id"] == "BACKREST"
    assert studio["view_model"]["task_summary"]["APPROVED"] == 1

    illegal = evaluate_iteration(
        {
            "task": task,
            "current_asset_revision": asset["revision"] + 1,
            "scene_before": before,
            "scene_after": _snapshot(76, seat_depth=430),
            "validations": [{"validator_id": "ASSEMBLY_ANCHOR_GATE", "status": "PASS"}],
        }
    )
    reasons = {item["reason"] for item in illegal["blockers"]}
    assert illegal["status"] == "FAIL"
    assert "ITERATION_ASSET_REVISION_STALE" in reasons
    assert "MUTATION_SCOPE_VIOLATION" in reasons

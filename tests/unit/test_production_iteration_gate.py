from executors.production_iteration_gate import evaluate
from executors.production_task_lifecycle import create, transition
from executors.scene_component_snapshot import build as build_snapshot


def _running_task() -> dict:
    task = create(
        {
            "task_id": "T-BACKREST",
            "asset_id": "ASSET-005",
            "asset_revision": 17,
            "component_id": "BACKREST",
            "stage": "STRUCTURAL_GEOMETRY",
            "allowed_to_modify": ["BACKREST"],
            "read_only": ["SEAT"],
        }
    )["task"]
    task = transition(task, "READY", actor="ORCHESTRATOR", reason="READY")["task"]
    return transition(task, "RUNNING", actor="WORKER", reason="CLAIMED", worker_id="worker-1")["task"]


def _snapshot(backrest_depth: int, seat_depth: int = 480) -> dict:
    return build_snapshot(
        {
            "asset_id": "ASSET-005",
            "asset_revision": 17,
            "scene_revision": backrest_depth,
            "objects": [
                {
                    "object_id": "bench.backrest.shell",
                    "component_id": "BACKREST",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, backrest_depth, 390],
                },
                {
                    "object_id": "bench.seat.shell",
                    "component_id": "SEAT",
                    "object_type": "MESH",
                    "dimensions_mm": [1580, seat_depth, 75],
                },
            ],
        }
    )["snapshot"]


def test_iteration_gate_allows_scoped_passing_worker_result():
    result = evaluate(
        {
            "task": _running_task(),
            "current_asset_revision": 17,
            "scene_before": _snapshot(72),
            "scene_after": _snapshot(76),
            "validations": [
                {"validator_id": "ASSEMBLY_ANCHOR_GATE", "status": "PASS"},
                {"validator_id": "GEOMETRIC_INTEGRITY", "status": "PASS"},
            ],
        }
    )
    assert result["status"] == "PASS"
    assert result["result"]["validation_status"] == "PASS"
    assert result["result"]["scene_diff"]["changed_object_count"] == 1


def test_iteration_gate_rejects_sibling_mutation_and_stale_revision():
    result = evaluate(
        {
            "task": _running_task(),
            "current_asset_revision": 18,
            "scene_before": _snapshot(72, 480),
            "scene_after": _snapshot(76, 490),
            "validations": [{"validator_id": "ASSEMBLY_ANCHOR_GATE", "status": "PASS"}],
        }
    )
    assert result["status"] == "FAIL"
    reasons = {item["reason"] for item in result["blockers"]}
    assert "ITERATION_ASSET_REVISION_STALE" in reasons
    assert "MUTATION_SCOPE_VIOLATION" in reasons

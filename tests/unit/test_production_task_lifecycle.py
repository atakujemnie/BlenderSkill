from executors.production_task_lifecycle import create, next_ready, promote_ready, transition


def _task(task_id: str, component_id: str, dependencies: list[str] | None = None) -> dict:
    result = create(
        {
            "task_id": task_id,
            "asset_id": "ASSET-005",
            "asset_revision": 17,
            "component_id": component_id,
            "stage": "STRUCTURAL_GEOMETRY",
            "dependencies": dependencies or [],
            "allowed_to_modify": [component_id],
            "read_only": ["SEAT"] if component_id != "SEAT" else ["BACKREST"],
        }
    )
    assert result["status"] == "PASS"
    return result["task"]


def test_dependency_queue_promotes_only_unblocked_tasks():
    tasks = {
        "T-SEAT": _task("T-SEAT", "SEAT"),
        "T-BACKREST": _task("T-BACKREST", "BACKREST", ["T-SEAT"]),
    }
    promoted = promote_ready(tasks)
    assert promoted["status"] == "PASS"
    assert promoted["tasks"]["T-SEAT"]["status"] == "READY"
    assert promoted["tasks"]["T-BACKREST"]["status"] == "BLOCKED"
    assert next_ready(promoted["tasks"])["task"]["task_id"] == "T-SEAT"


def test_task_requires_result_and_validation_before_approval():
    task = _task("T-BACKREST", "BACKREST")
    task = transition(task, "READY", actor="ORCHESTRATOR", reason="READY")["task"]
    task = transition(task, "RUNNING", actor="WORKER", reason="CLAIMED", worker_id="worker-1")["task"]

    no_result = transition(task, "REVIEW", actor="WORKER", reason="DONE")
    assert no_result["status"] == "FAIL"
    assert no_result["blockers"][0]["reason"] == "TASK_RESULT_REQUIRED_FOR_REVIEW"

    reviewed = transition(
        task,
        "REVIEW",
        actor="WORKER",
        reason="DONE",
        result={"validation_status": "PASS", "scene_revision": 4},
    )
    assert reviewed["status"] == "PASS"

    approved = transition(reviewed["task"], "APPROVED", actor="REVIEWER", reason="ACCEPTED")
    assert approved["status"] == "PASS"
    assert approved["task"]["status"] == "APPROVED"
    assert approved["task"]["attempt"] == 1

from executors.production_task_lifecycle import create, transition
from executors.production_task_repository import initialize, list_revisions, load, save, upsert_task


def _task(task_id: str, component_id: str) -> dict:
    result = create(
        {
            "task_id": task_id,
            "asset_id": "ASSET-005",
            "asset_revision": 17,
            "component_id": component_id,
            "stage": "STRUCTURAL_GEOMETRY",
            "allowed_to_modify": [component_id],
            "read_only": ["SEAT"] if component_id != "SEAT" else ["BACKREST"],
        }
    )
    assert result["status"] == "PASS"
    return result["task"]


def test_persistent_task_queue_revisions(tmp_path):
    seat = _task("T-SEAT", "SEAT")
    created = initialize(tmp_path, "ASSET-005", {"T-SEAT": seat})
    assert created["status"] == "PASS"
    assert created["queue"]["queue_revision"] == 1

    seat_ready = transition(seat, "READY", actor="ORCHESTRATOR", reason="READY")["task"]
    saved = save(tmp_path, "ASSET-005", {"T-SEAT": seat_ready}, expected_queue_revision=1)
    assert saved["status"] == "PASS"
    assert saved["queue_revision"] == 2

    old = load(tmp_path, "ASSET-005", revision=1)
    current = load(tmp_path, "ASSET-005")
    assert old["queue"]["tasks"]["T-SEAT"]["status"] == "QUEUED"
    assert current["queue"]["tasks"]["T-SEAT"]["status"] == "READY"
    assert list_revisions(tmp_path, "ASSET-005")["revisions"] == [1, 2]


def test_task_queue_rejects_stale_writer_and_supports_upsert(tmp_path):
    assert initialize(tmp_path, "ASSET-005", {})["status"] == "PASS"
    task = _task("T-BACKREST", "BACKREST")
    inserted = upsert_task(tmp_path, "ASSET-005", task, expected_queue_revision=1)
    assert inserted["status"] == "PASS"
    assert inserted["queue_revision"] == 2

    stale = save(tmp_path, "ASSET-005", {"T-BACKREST": task}, expected_queue_revision=1)
    assert stale["status"] == "CONFLICT"
    assert stale["blockers"][0]["reason"] == "TASK_QUEUE_REVISION_CONFLICT"

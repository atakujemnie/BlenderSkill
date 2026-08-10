from executors.production_task_lifecycle import create, transition


def _review_task():
    created = create(
        {
            "task_id": "T-PART",
            "asset_id": "ASSET-1",
            "asset_revision": 4,
            "component_id": "PART",
            "stage": "STRUCTURAL_GEOMETRY",
            "allowed_to_modify": ["PART"],
            "read_only": [],
            "required_validation_ids": ["SCENE_COMPONENT_VALIDATION", "REPRESENTATION_CONTRACT_GATE"],
        }
    )
    task = transition(created["task"], "READY", actor="ORCHESTRATOR", reason="READY")["task"]
    task = transition(task, "RUNNING", actor="WORKER", reason="RUN", worker_id="worker")["task"]
    reviewed = transition(
        task,
        "REVIEW",
        actor="WORKER",
        reason="DONE",
        result={"validation_status": "PASS", "scene_revision": 3},
    )
    assert reviewed["status"] == "PASS"
    return reviewed["task"]


def _receipt(receipt_id, validator_id, *, scene_revision=3, source="SYSTEM"):
    return {
        "receipt_id": receipt_id,
        "validator_id": validator_id,
        "validator_version": "0.21.0",
        "asset_id": "ASSET-1",
        "asset_revision": 4,
        "component_id": "PART",
        "scene_revision": scene_revision,
        "status": "PASS",
        "source": source,
    }


def test_worker_validation_status_alone_cannot_approve_strict_task():
    task = _review_task()
    result = transition(task, "APPROVED", actor="REVIEWER", reason="APPROVE")
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "TRUSTED_VALIDATION_RECEIPTS_REQUIRED"


def test_receipts_must_match_exact_scene_and_system_source():
    task = _review_task()
    result = transition(
        task,
        "APPROVED",
        actor="REVIEWER",
        reason="APPROVE",
        validation_receipts=[
            _receipt("R1", "SCENE_COMPONENT_VALIDATION", scene_revision=2),
            _receipt("R2", "REPRESENTATION_CONTRACT_GATE", source="WORKER"),
        ],
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "TRUSTED_VALIDATION_RECEIPTS_REQUIRED"


def test_exact_trusted_receipts_allow_approval_and_are_recorded():
    task = _review_task()
    result = transition(
        task,
        "APPROVED",
        actor="REVIEWER",
        reason="APPROVE",
        validation_receipts=[
            _receipt("R1", "SCENE_COMPONENT_VALIDATION"),
            _receipt("R2", "REPRESENTATION_CONTRACT_GATE"),
        ],
    )
    assert result["status"] == "PASS", result
    assert result["task"]["status"] == "APPROVED"
    assert result["task"]["approval_receipt_ids"] == ["R2", "R1"] or result["task"]["approval_receipt_ids"] == ["R1", "R2"]

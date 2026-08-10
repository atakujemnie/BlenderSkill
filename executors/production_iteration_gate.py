from __future__ import annotations

"""Gate a worker iteration before it can enter human/machine review."""

from typing import Any, Mapping

from executors.production_task_lifecycle import validate_task
from executors.scene_component_snapshot import assert_mutation_scope

EXECUTOR_ID = "PRODUCTION_ITERATION_GATE"
EXECUTOR_VERSION = "0.19.0"
PASS_LIKE = {"PASS", "NOT_REQUIRED"}


def evaluate(report: Mapping[str, Any]) -> dict[str, Any]:
    task = report.get("task")
    if not isinstance(task, Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ITERATION_TASK_REQUIRED"}],
        }
    task_verdict = validate_task(task)
    if task_verdict["status"] != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": task_verdict["blockers"],
        }
    if str(task.get("status") or "").upper() != "RUNNING":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "ITERATION_TASK_MUST_BE_RUNNING"}],
        }

    current_asset_revision = report.get("current_asset_revision")
    input_revision = task.get("input_revision")
    blockers: list[dict[str, Any]] = []
    if current_asset_revision is not None and input_revision is not None:
        if int(current_asset_revision) != int(input_revision):
            blockers.append(
                {
                    "reason": "ITERATION_ASSET_REVISION_STALE",
                    "task_revision": int(input_revision),
                    "current_revision": int(current_asset_revision),
                }
            )

    before = report.get("scene_before")
    after = report.get("scene_after")
    if not isinstance(before, Mapping) or not isinstance(after, Mapping):
        blockers.append({"reason": "ITERATION_SCENE_SNAPSHOTS_REQUIRED"})
        scope = None
    else:
        scope = assert_mutation_scope(
            before,
            after,
            allowed_to_modify=[str(value) for value in list(task.get("allowed_to_modify", []) or [])],
        )
        blockers.extend(scope.get("blockers", []))

    validation_results: list[dict[str, Any]] = []
    for raw in list(report.get("validations", []) or []):
        if not isinstance(raw, Mapping):
            blockers.append({"reason": "ITERATION_VALIDATION_RECORD_INVALID"})
            continue
        record = dict(raw)
        validator_id = str(record.get("validator_id") or record.get("executor_id") or "UNKNOWN")
        status = str(record.get("status") or "UNVERIFIED").upper()
        validation_results.append({"validator_id": validator_id, "status": status})
        if status not in PASS_LIKE:
            blockers.append(
                {
                    "reason": "ITERATION_VALIDATION_NOT_PASSED",
                    "validator_id": validator_id,
                    "status": status,
                }
            )
    if not validation_results and not bool(report.get("allow_no_validations", False)):
        blockers.append({"reason": "ITERATION_VALIDATION_REQUIRED"})

    scene_diff = scope.get("diff") if isinstance(scope, Mapping) else None
    result_record = {
        "validation_status": "PASS" if not blockers else "FAIL",
        "asset_revision": current_asset_revision,
        "scene_before_hash": before.get("snapshot_hash") if isinstance(before, Mapping) else None,
        "scene_after_hash": after.get("snapshot_hash") if isinstance(after, Mapping) else None,
        "scene_diff": scene_diff,
        "validations": validation_results,
    }
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "task_id": task.get("task_id"),
        "component_id": task.get("component_id"),
        "result": result_record,
        "blockers": blockers,
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "evaluate"]

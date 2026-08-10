from __future__ import annotations

"""Deterministic component-task lifecycle for the asset production studio."""

from copy import deepcopy
from typing import Any, Mapping

EXECUTOR_ID = "PRODUCTION_TASK_LIFECYCLE"
EXECUTOR_VERSION = "0.19.0"
TASK_STATUSES = {
    "QUEUED",
    "READY",
    "RUNNING",
    "REVIEW",
    "APPROVED",
    "BLOCKED",
    "FAILED",
    "CANCELLED",
}
TERMINAL_STATUSES = {"APPROVED", "CANCELLED"}
TRANSITIONS = {
    "QUEUED": {"READY", "BLOCKED", "CANCELLED"},
    "READY": {"RUNNING", "BLOCKED", "CANCELLED"},
    "RUNNING": {"REVIEW", "FAILED", "BLOCKED", "CANCELLED"},
    "REVIEW": {"APPROVED", "READY", "BLOCKED", "CANCELLED"},
    "BLOCKED": {"READY", "CANCELLED"},
    "FAILED": {"READY", "CANCELLED"},
    "APPROVED": set(),
    "CANCELLED": set(),
}


def validate_task(task: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    required = ("task_id", "asset_id", "asset_revision", "component_id", "stage")
    missing = [field for field in required if task.get(field) in (None, "")]
    if missing:
        blockers.append({"reason": "TASK_FIELDS_REQUIRED", "fields": missing})
    status = str(task.get("status", "QUEUED")).upper()
    if status not in TASK_STATUSES:
        blockers.append({"reason": "TASK_STATUS_INVALID", "status": status})
    allowed = {str(value) for value in list(task.get("allowed_to_modify", []) or [])}
    read_only = {str(value) for value in list(task.get("read_only", []) or [])}
    overlap = sorted(allowed & read_only)
    if overlap:
        blockers.append({"reason": "TASK_MUTATION_SCOPE_OVERLAP", "component_ids": overlap})
    if str(task.get("component_id") or "") and str(task.get("component_id")) not in allowed:
        blockers.append({"reason": "TASK_COMPONENT_NOT_MUTABLE"})
    dependencies = [str(value) for value in list(task.get("dependencies", []) or [])]
    if str(task.get("task_id") or "") in dependencies:
        blockers.append({"reason": "TASK_SELF_DEPENDENCY"})
    return {
        "status": "PASS" if not blockers else "FAIL",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
    }


def create(spec: Mapping[str, Any]) -> dict[str, Any]:
    task = {
        "schema_version": 1,
        "task_id": str(spec.get("task_id") or ""),
        "asset_id": str(spec.get("asset_id") or ""),
        "asset_revision": spec.get("asset_revision"),
        "component_id": str(spec.get("component_id") or ""),
        "stage": str(spec.get("stage") or ""),
        "task_kind": str(spec.get("task_kind", "BUILD")).upper(),
        "status": "QUEUED",
        "priority": int(spec.get("priority", 100)),
        "dependencies": sorted(str(value) for value in list(spec.get("dependencies", []) or [])),
        "allowed_to_modify": sorted(str(value) for value in list(spec.get("allowed_to_modify", []) or [])),
        "read_only": sorted(str(value) for value in list(spec.get("read_only", []) or [])),
        "input_revision": spec.get("input_revision", spec.get("asset_revision")),
        "task_pack_hash": spec.get("task_pack_hash"),
        "worker_id": None,
        "attempt": 0,
        "blockers": [],
        "result": None,
        "history": [
            {
                "from": None,
                "to": "QUEUED",
                "actor": str(spec.get("actor") or "SYSTEM"),
                "reason": "TASK_CREATED",
            }
        ],
    }
    verdict = validate_task(task)
    return {
        "status": verdict["status"],
        "validator_id": EXECUTOR_ID,
        "task": task,
        "blockers": verdict["blockers"],
    }


def dependency_state(task: Mapping[str, Any], tasks: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    missing: list[str] = []
    incomplete: list[dict[str, str]] = []
    for dependency_id in list(task.get("dependencies", []) or []):
        dependency = tasks.get(str(dependency_id))
        if not isinstance(dependency, Mapping):
            missing.append(str(dependency_id))
            continue
        status = str(dependency.get("status") or "").upper()
        if status != "APPROVED":
            incomplete.append({"task_id": str(dependency_id), "status": status})
    blockers: list[dict[str, Any]] = []
    if missing:
        blockers.append({"reason": "TASK_DEPENDENCY_MISSING", "task_ids": sorted(missing)})
    if incomplete:
        blockers.append({"reason": "TASK_DEPENDENCY_NOT_APPROVED", "dependencies": incomplete})
    return {
        "status": "PASS" if not blockers else "BLOCKED",
        "validator_id": EXECUTOR_ID,
        "blockers": blockers,
    }


def transition(
    task: Mapping[str, Any],
    target_status: str,
    *,
    actor: str,
    reason: str,
    worker_id: str | None = None,
    blockers: list[Mapping[str, Any]] | None = None,
    result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    verdict = validate_task(task)
    if verdict["status"] != "PASS":
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": verdict["blockers"],
        }
    current = str(task.get("status", "QUEUED")).upper()
    target = str(target_status).upper()
    if target not in TASK_STATUSES:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_STATUS_INVALID", "status": target}],
        }
    if target not in TRANSITIONS[current]:
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_TRANSITION_INVALID", "from": current, "to": target}],
        }
    next_task = deepcopy(dict(task))
    next_task["status"] = target
    next_task["blockers"] = [dict(value) for value in list(blockers or [])]
    if target == "RUNNING":
        next_task["attempt"] = int(next_task.get("attempt", 0)) + 1
        next_task["worker_id"] = worker_id or next_task.get("worker_id")
    elif worker_id is not None:
        next_task["worker_id"] = worker_id
    if result is not None:
        next_task["result"] = dict(result)
    if target == "REVIEW" and not isinstance(next_task.get("result"), Mapping):
        return {
            "status": "FAIL",
            "validator_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_RESULT_REQUIRED_FOR_REVIEW"}],
        }
    if target == "APPROVED":
        result_record = next_task.get("result")
        if not isinstance(result_record, Mapping) or str(result_record.get("validation_status") or "").upper() != "PASS":
            return {
                "status": "FAIL",
                "validator_id": EXECUTOR_ID,
                "blockers": [{"reason": "PASSING_VALIDATION_REQUIRED_FOR_APPROVAL"}],
            }
    history = list(next_task.get("history", []) or [])
    history.append(
        {
            "from": current,
            "to": target,
            "actor": str(actor),
            "reason": str(reason),
            "attempt": int(next_task.get("attempt", 0)),
        }
    )
    next_task["history"] = history
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "task": next_task,
        "blockers": [],
    }


def promote_ready(tasks: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    updated: dict[str, dict[str, Any]] = {str(task_id): deepcopy(dict(task)) for task_id, task in tasks.items()}
    promoted: list[str] = []
    blocked: list[dict[str, Any]] = []
    for task_id in sorted(updated):
        task = updated[task_id]
        if str(task.get("status", "")).upper() not in {"QUEUED", "BLOCKED"}:
            continue
        dependency = dependency_state(task, updated)
        if dependency["status"] == "PASS":
            moved = transition(task, "READY", actor="ORCHESTRATOR", reason="DEPENDENCIES_SATISFIED")
            if moved["status"] == "PASS":
                updated[task_id] = moved["task"]
                promoted.append(task_id)
        else:
            if str(task.get("status", "")).upper() == "QUEUED":
                moved = transition(
                    task,
                    "BLOCKED",
                    actor="ORCHESTRATOR",
                    reason="DEPENDENCIES_UNRESOLVED",
                    blockers=dependency["blockers"],
                )
                if moved["status"] == "PASS":
                    updated[task_id] = moved["task"]
            blocked.append({"task_id": task_id, "blockers": dependency["blockers"]})
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "tasks": updated,
        "promoted": promoted,
        "blocked": blocked,
    }


def next_ready(tasks: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    candidates = [
        dict(task)
        for task in tasks.values()
        if isinstance(task, Mapping) and str(task.get("status", "")).upper() == "READY"
    ]
    candidates.sort(key=lambda task: (int(task.get("priority", 100)), str(task.get("task_id"))))
    return {
        "status": "PASS",
        "validator_id": EXECUTOR_ID,
        "task": candidates[0] if candidates else None,
        "ready_count": len(candidates),
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "TASK_STATUSES",
    "TRANSITIONS",
    "create",
    "dependency_state",
    "next_ready",
    "promote_ready",
    "transition",
    "validate_task",
]

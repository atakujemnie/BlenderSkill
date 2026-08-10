from __future__ import annotations

"""Operational service layer for the local Asset Production Studio.

v0.21 closes the blind-test gaps between persistent production state and actual
geometry execution: stage authorization, component execution authorization,
trusted validation receipts, envelope validation and component/task state
convergence are enforced here instead of being prompt-only conventions.
"""

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from executors.asset_envelope_gate import validate as validate_asset_envelope
from executors.asset_production_orchestrator import prepare_component_task
from executors.asset_repository import initialize as initialize_asset
from executors.asset_repository import load as load_asset
from executors.asset_repository import save as save_asset
from executors.asset_state_runtime import ASSET_STAGES, add_correction, advance_stage, resolve_correction
from executors.asset_studio_view_model import build as build_studio_view
from executors.design_system_repository import impact_report, load as load_design_resource
from executors.parameter_graph import resolve as resolve_parameters
from executors.production_task_lifecycle import create as create_task_record
from executors.production_task_lifecycle import promote_ready, transition
from executors.production_task_repository import initialize as initialize_task_queue
from executors.production_task_repository import load as load_task_queue
from executors.production_task_repository import save as save_task_queue
from executors.reference_evidence_registry import query as query_evidence
from executors.reference_evidence_repository import initialize as initialize_evidence
from executors.reference_evidence_repository import load as load_evidence
from executors.reference_evidence_repository import remove as remove_evidence_record
from executors.reference_evidence_repository import upsert as upsert_evidence_record
from executors.scene_component_snapshot import build as build_scene_snapshot
from executors.scene_snapshot_repository import load as load_scene_snapshot
from executors.scene_snapshot_repository import publish as publish_scene_snapshot
from executors.validation_receipt_repository import initialize as initialize_validation_receipts
from executors.validation_receipt_repository import publish as publish_validation_receipt_record
from executors.validation_receipt_repository import query as query_validation_receipts

EXECUTOR_ID = "PRODUCTION_STUDIO_SERVICE"
EXECUTOR_VERSION = "0.21.0"
_GEOMETRY_STAGE_INDEX = ASSET_STAGES.index("BLOCKOUT")
_DEFAULT_GEOMETRY_VALIDATORS = ("SCENE_COMPONENT_VALIDATION", "REPRESENTATION_CONTRACT_GATE")


def _assets_dir(root: str | Path) -> Path:
    return Path(root).expanduser().resolve() / "assets"


def _task_queue_or_empty(root: str | Path, asset_id: str) -> tuple[dict[str, dict[str, Any]], int]:
    loaded = load_task_queue(root, asset_id)
    if loaded.get("status") == "PASS":
        return (
            {str(task_id): dict(task) for task_id, task in loaded["queue"]["tasks"].items()},
            int(loaded["queue"]["queue_revision"]),
        )
    reasons = {str(item.get("reason")) for item in loaded.get("blockers", []) if isinstance(item, Mapping)}
    if "TASK_QUEUE_NOT_FOUND" in reasons:
        return {}, 0
    raise RuntimeError(f"TASK_QUEUE_LOAD_FAILED:{loaded.get('blockers', [])}")


def _evidence_or_empty(root: str | Path, asset_id: str) -> tuple[dict[str, Any], int]:
    loaded = load_evidence(root, asset_id)
    if loaded.get("status") == "PASS":
        return dict(loaded["registry"]), int(loaded["registry"]["revision"])
    if loaded.get("status") == "NOT_FOUND":
        return {"asset_id": asset_id, "revision": 0, "evidence": []}, 0
    raise RuntimeError(f"REFERENCE_EVIDENCE_LOAD_FAILED:{loaded.get('blockers', [])}")


def _scene_or_none(root: str | Path, asset_id: str) -> tuple[dict[str, Any] | None, int]:
    loaded = load_scene_snapshot(root, asset_id)
    if loaded.get("status") == "PASS":
        snapshot = dict(loaded["snapshot"])
        return snapshot, int(snapshot.get("scene_revision", 0))
    if loaded.get("status") == "NOT_FOUND":
        return None, 0
    raise RuntimeError(f"SCENE_SNAPSHOT_LOAD_FAILED:{loaded.get('blockers', [])}")


def _resource_catalog(root: str | Path, asset: Mapping[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    catalog: dict[str, dict[str, Any]] = {}
    impacts: list[dict[str, Any]] = []
    seen_impacts: set[tuple[str, str]] = set()
    bindings = asset.get("bindings", {})
    if not isinstance(bindings, Mapping):
        return catalog, impacts
    design_system_ids = [str(value) for value in list(asset.get("design_system_ids", []) or [])]
    for raw in bindings.values():
        if not isinstance(raw, Mapping):
            continue
        resource_id = str(raw.get("resource_id") or "")
        if not resource_id or resource_id in catalog:
            continue
        for design_system_id in design_system_ids:
            loaded = load_design_resource(root, design_system_id, resource_id)
            if loaded.get("status") != "PASS":
                continue
            resource = dict(loaded["resource"])
            payload = dict(resource.get("payload", {}) or {})
            catalog[resource_id] = {
                "resource_id": resource_id,
                "type": resource.get("kind"),
                "version": resource.get("version"),
                "revision": resource.get("revision"),
                "locked": bool(resource.get("locked", False)),
                **payload,
            }
            impact_key = (design_system_id, resource_id)
            if impact_key not in seen_impacts:
                impact = impact_report(root, design_system_id, resource_id)
                if impact.get("status") == "PASS":
                    impacts.append({"design_system_id": design_system_id, **dict(impact)})
                seen_impacts.add(impact_key)
            break
    impacts.sort(key=lambda item: (str(item.get("design_system_id")), str(item.get("resource_id"))))
    return catalog, impacts


def list_assets(root: str | Path) -> dict[str, Any]:
    directory = _assets_dir(root)
    assets: list[dict[str, Any]] = []
    if not directory.is_dir():
        return {"status": "PASS", "executor_id": EXECUTOR_ID, "assets": [], "asset_count": 0}
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if not path.is_dir() or not (path / "asset.json").is_file():
            continue
        loaded = load_asset(root, path.name)
        if loaded.get("status") != "PASS":
            assets.append({"asset_id": path.name, "status": "INVALID", "blockers": loaded.get("blockers", [])})
            continue
        asset = loaded["asset"]
        tasks, queue_revision = _task_queue_or_empty(root, path.name)
        task_statuses: dict[str, int] = {}
        for task in tasks.values():
            status = str(task.get("status") or "UNKNOWN").upper()
            task_statuses[status] = task_statuses.get(status, 0) + 1
        assets.append(
            {
                "asset_id": asset.get("asset_id"),
                "name": asset.get("name"),
                "revision": asset.get("revision"),
                "stage": asset.get("stage"),
                "component_count": len(dict(asset.get("components", {}) or {})),
                "open_corrections": sum(
                    1
                    for item in list(asset.get("corrections", []) or [])
                    if isinstance(item, Mapping) and str(item.get("status", "OPEN")).upper() == "OPEN"
                ),
                "queue_revision": queue_revision,
                "task_statuses": dict(sorted(task_statuses.items())),
                "status": "PASS",
            }
        )
    return {"status": "PASS", "executor_id": EXECUTOR_ID, "assets": assets, "asset_count": len(assets)}


def create_asset(root: str | Path, asset: Mapping[str, Any]) -> dict[str, Any]:
    if bool(asset.get("enforce_asset_envelope", False)):
        envelope = validate_asset_envelope(asset)
        if envelope.get("status") != "PASS":
            return {**envelope, "executor_id": EXECUTOR_ID, "failed_stage": "ASSET_ENVELOPE"}
    created = initialize_asset(root, asset)
    if created.get("status") != "PASS":
        return created
    asset_id = str(asset["asset_id"])
    queue = initialize_task_queue(root, asset_id, {})
    evidence = initialize_evidence(root, asset_id, {"evidence": []})
    validation = initialize_validation_receipts(root, asset_id)
    blockers: list[dict[str, Any]] = []
    for result in (queue, evidence, validation):
        if result.get("status") != "PASS":
            blockers.extend(result.get("blockers", []))
    return {
        "status": "PASS" if not blockers else "PARTIAL",
        "executor_id": EXECUTOR_ID,
        "asset_id": asset_id,
        "asset_revision": int(asset.get("revision", 0)),
        "queue_revision": queue.get("queue", {}).get("queue_revision"),
        "reference_revision": evidence.get("registry", {}).get("revision"),
        "validation_revision": validation.get("revision"),
        "blockers": blockers,
    }


def get_studio(root: str | Path, asset_id: str, *, component_id: str | None = None) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = dict(loaded["asset"])
    tasks, queue_revision = _task_queue_or_empty(root, asset_id)
    registry, reference_revision = _evidence_or_empty(root, asset_id)
    scene_snapshot, scene_revision = _scene_or_none(root, asset_id)
    _catalog, impacts = _resource_catalog(root, asset)

    selected = str(component_id or "")
    if not selected:
        components = dict(asset.get("components", {}) or {})
        selected = str(next(iter(components), ""))

    view = build_studio_view(
        asset,
        tasks=tasks,
        selected_component_id=selected or None,
        scene_snapshot=scene_snapshot,
        design_impacts=impacts,
    )
    if view.get("status") != "PASS":
        return view
    model = dict(view["view_model"])
    inspector = dict(model.get("inspector", {}) or {})

    evidence = query_evidence(registry, component_id=selected)
    inspector["reference_evidence"] = list(evidence.get("evidence", []) or []) if evidence.get("status") == "PASS" else []
    parameters = resolve_parameters({"components": asset.get("components", {})})
    inspector["resolved_parameters"] = (
        dict(parameters.get("resolved", {}).get(selected, {}) or {}) if parameters.get("status") == "PASS" else {}
    )
    component = dict(asset.get("components", {}).get(selected, {}) or {})
    binding_ids = [str(value) for value in list(component.get("binding_ids", []) or [])]
    inspector["design_bindings"] = {
        binding_id: dict(asset.get("bindings", {}).get(binding_id, {}) or {})
        for binding_id in binding_ids
        if isinstance(asset.get("bindings", {}).get(binding_id), Mapping)
    }
    model["inspector"] = inspector
    model["tasks"] = [dict(task) for task in sorted(tasks.values(), key=lambda item: str(item.get("task_id")))]
    model["runtime_revisions"] = {
        "asset": int(asset.get("revision", 0)),
        "task_queue": queue_revision,
        "reference_evidence": reference_revision,
        "scene": scene_revision,
    }
    validation = query_validation_receipts(
        root,
        asset_id,
        component_id=selected,
        asset_revision=int(asset.get("revision", 0)),
    )
    model["validation_revision"] = validation.get("revision", 0)
    inspector["validation_receipts"] = list(validation.get("receipts", []) or [])
    model["inspector"] = inspector
    return {"status": "PASS", "executor_id": EXECUTOR_ID, "view_model": model, "blockers": []}


def add_asset_correction(
    root: str | Path,
    asset_id: str,
    correction: Mapping[str, Any],
    *,
    expected_asset_revision: int,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_revision = int(loaded["asset"].get("revision", 0))
    if current_revision != int(expected_asset_revision):
        return _revision_conflict("ASSET_REVISION_CONFLICT", expected_asset_revision, current_revision)
    changed = add_correction(loaded["asset"], correction)
    if changed.get("status") != "PASS":
        return changed
    saved = save_asset(root, changed["asset"], expected_revision=current_revision)
    return {
        **saved,
        "executor_id": EXECUTOR_ID,
        "asset_revision": changed.get("revision") if saved.get("status") == "PASS" else current_revision,
    }


def resolve_asset_correction(
    root: str | Path,
    asset_id: str,
    correction_id: str,
    *,
    expected_asset_revision: int,
    resolution: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_revision = int(loaded["asset"].get("revision", 0))
    if current_revision != int(expected_asset_revision):
        return _revision_conflict("ASSET_REVISION_CONFLICT", expected_asset_revision, current_revision)
    changed = resolve_correction(loaded["asset"], correction_id, resolution=resolution)
    if changed.get("status") != "PASS":
        return changed
    saved = save_asset(root, changed["asset"], expected_revision=current_revision)
    return {
        **saved,
        "executor_id": EXECUTOR_ID,
        "asset_revision": changed.get("revision") if saved.get("status") == "PASS" else current_revision,
    }


def advance_asset_stage(
    root: str | Path,
    asset_id: str,
    new_stage: str,
    *,
    expected_asset_revision: int,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_revision = int(loaded["asset"].get("revision", 0))
    if current_revision != int(expected_asset_revision):
        return _revision_conflict("ASSET_REVISION_CONFLICT", expected_asset_revision, current_revision)
    if bool(loaded["asset"].get("enforce_asset_envelope", False)):
        envelope = validate_asset_envelope(loaded["asset"])
        if envelope.get("status") != "PASS":
            return {**envelope, "executor_id": EXECUTOR_ID, "failed_stage": "ASSET_ENVELOPE"}
    changed = advance_stage(loaded["asset"], new_stage)
    if changed.get("status") != "PASS":
        return changed
    saved = save_asset(root, changed["asset"], expected_revision=current_revision)
    return {
        **saved,
        "executor_id": EXECUTOR_ID,
        "asset_revision": changed.get("revision") if saved.get("status") == "PASS" else current_revision,
    }


def authorize_component(
    root: str | Path,
    asset_id: str,
    component_id: str,
    authorization: Mapping[str, Any],
    *,
    expected_asset_revision: int,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = loaded["asset"]
    current_revision = int(asset.get("revision", 0))
    if current_revision != int(expected_asset_revision):
        return _revision_conflict("ASSET_REVISION_CONFLICT", expected_asset_revision, current_revision)
    components = {str(key): dict(value) for key, value in dict(asset.get("components", {}) or {}).items()}
    component = components.get(str(component_id))
    if component is None:
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "COMPONENT_NOT_FOUND", "component_id": str(component_id)}]}
    if str(authorization.get("status") or "").upper() != "PASS" or not str(authorization.get("validator_id") or ""):
        return {"status": "BLOCKED", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "EXECUTION_AUTHORIZATION_PASS_REQUIRED"}]}
    dependencies = [str(value) for value in list(component.get("depends_on", []) or [])]
    incomplete = [dep for dep in dependencies if str(components.get(dep, {}).get("state") or "") != "ACCEPTED"]
    if incomplete:
        return {
            "status": "BLOCKED",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "COMPONENT_DEPENDENCY_NOT_ACCEPTED", "component_ids": sorted(incomplete)}],
        }
    state = str(component.get("state") or "DECLARED").upper()
    if state not in {"CONSTRAINED", "DIRTY", "UNVERIFIED", "FAIL"}:
        return {"status": "BLOCKED", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "COMPONENT_STATE_NOT_AUTHORIZABLE", "state": state}]}
    cp = deepcopy(dict(asset))
    cp_components = {str(key): dict(value) for key, value in dict(cp.get("components", {}) or {}).items()}
    cp_component = dict(cp_components[str(component_id)])
    cp_component["state"] = "READY_TO_BUILD"
    cp_component["execution_authorization"] = dict(authorization)
    cp_components[str(component_id)] = cp_component
    cp["components"] = cp_components
    cp["revision"] = current_revision + 1
    history = list(cp.get("history", []) or [])
    history.append({"revision": cp["revision"], "event": "COMPONENT_AUTHORIZED", "component_id": str(component_id), "validator_id": authorization.get("validator_id")})
    cp["history"] = history
    saved = save_asset(root, cp, expected_revision=current_revision)
    return {**saved, "executor_id": EXECUTOR_ID, "asset_revision": cp["revision"] if saved.get("status") == "PASS" else current_revision}


def _geometry_task_authorization(asset: Mapping[str, Any], component: Mapping[str, Any], requested_stage: str, task_kind: str) -> dict[str, Any]:
    current_stage = str(asset.get("stage") or "").upper()
    try:
        current_index = ASSET_STAGES.index(current_stage)
        requested_index = ASSET_STAGES.index(requested_stage)
    except ValueError:
        return {"status": "FAIL", "blockers": [{"reason": "TASK_STAGE_INVALID", "stage": requested_stage}]}
    if requested_index > current_index:
        return {
            "status": "BLOCKED",
            "blockers": [{"reason": "TASK_STAGE_NOT_AUTHORIZED", "asset_stage": current_stage, "task_stage": requested_stage}],
        }
    if requested_index < _GEOMETRY_STAGE_INDEX:
        return {"status": "PASS", "blockers": []}
    state = str(component.get("state") or "DECLARED").upper()
    if task_kind == "BUILD" and state != "READY_TO_BUILD":
        return {"status": "BLOCKED", "blockers": [{"reason": "COMPONENT_BUILD_NOT_AUTHORIZED", "state": state}]}
    if task_kind == "REPAIR" and state not in {"READY_TO_BUILD", "DIRTY", "UNVERIFIED", "FAIL", "ACCEPTED"}:
        return {"status": "BLOCKED", "blockers": [{"reason": "COMPONENT_REPAIR_NOT_AUTHORIZED", "state": state}]}
    return {"status": "PASS", "blockers": []}


def create_production_task(
    root: str | Path,
    asset_id: str,
    spec: Mapping[str, Any],
    *,
    expected_queue_revision: int,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = loaded["asset"]
    component_id = str(spec.get("component_id") or "")
    components = dict(asset.get("components", {}) or {})
    if component_id not in components:
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "COMPONENT_NOT_FOUND", "component_id": component_id}],
        }
    requested_stage = str(spec.get("stage") or asset.get("stage") or "").upper()
    task_kind = str(spec.get("task_kind", "BUILD")).upper()
    authorization = _geometry_task_authorization(asset, components[component_id], requested_stage, task_kind)
    if authorization["status"] != "PASS":
        return {**authorization, "executor_id": EXECUTOR_ID}
    validation_contract = components[component_id].get("validation", {})
    declared_validators = []
    if isinstance(validation_contract, Mapping):
        declared_validators = list(validation_contract.get("required_validator_ids", []) or [])
    required_validators = list(spec.get("required_validation_ids", []) or declared_validators)
    if ASSET_STAGES.index(requested_stage) >= _GEOMETRY_STAGE_INDEX and not required_validators:
        required_validators = list(_DEFAULT_GEOMETRY_VALIDATORS)
    task_spec = {
        **dict(spec),
        "asset_id": asset_id,
        "asset_revision": int(asset.get("revision", 0)),
        "stage": requested_stage,
        "task_kind": task_kind,
        "allowed_to_modify": list(spec.get("allowed_to_modify", []) or [component_id]),
        "read_only": list(spec.get("read_only", []) or sorted(set(components) - {component_id})),
        "required_validation_ids": required_validators,
    }
    created = create_task_record(task_spec)
    if created.get("status") != "PASS":
        return created
    task = created["task"]

    tasks, queue_revision = _task_queue_or_empty(root, asset_id)
    if queue_revision != int(expected_queue_revision):
        return _revision_conflict("TASK_QUEUE_REVISION_CONFLICT", expected_queue_revision, queue_revision)
    if str(task["task_id"]) in tasks:
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_ALREADY_EXISTS", "task_id": str(task["task_id"])}],
        }
    tasks[str(task["task_id"])] = task
    if queue_revision == 0:
        saved = initialize_task_queue(root, asset_id, tasks)
        if saved.get("status") == "PASS":
            return {
                "status": "PASS",
                "executor_id": EXECUTOR_ID,
                "queue_revision": int(saved["queue"]["queue_revision"]),
                "task": task,
            }
        return saved
    saved = save_task_queue(root, asset_id, tasks, expected_queue_revision=queue_revision)
    return {**saved, "executor_id": EXECUTOR_ID, "task": task if saved.get("status") == "PASS" else None}


def publish_validation_receipt(root: str | Path, asset_id: str, receipt: Mapping[str, Any], *, expected_validation_revision: int | None = None) -> dict[str, Any]:
    return {
        **publish_validation_receipt_record(root, asset_id, receipt, expected_revision=expected_validation_revision),
        "executor_id": EXECUTOR_ID,
    }


def _accept_component_state(root: str | Path, asset_id: str, component_id: str) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = loaded["asset"]
    current_revision = int(asset.get("revision", 0))
    components = {str(key): dict(value) for key, value in dict(asset.get("components", {}) or {}).items()}
    component = components.get(str(component_id))
    if component is None:
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "COMPONENT_NOT_FOUND", "component_id": str(component_id)}]}
    cp = deepcopy(dict(asset))
    cp_components = {str(key): dict(value) for key, value in dict(cp.get("components", {}) or {}).items()}
    updated = dict(cp_components[str(component_id)])
    updated["state"] = "ACCEPTED"
    cp_components[str(component_id)] = updated
    cp["components"] = cp_components
    cp["revision"] = current_revision + 1
    history = list(cp.get("history", []) or [])
    history.append({"revision": cp["revision"], "event": "COMPONENT_ACCEPTED", "component_id": str(component_id)})
    cp["history"] = history
    saved = save_asset(root, cp, expected_revision=current_revision)
    return {**saved, "executor_id": EXECUTOR_ID, "asset_revision": cp["revision"] if saved.get("status") == "PASS" else current_revision}


def transition_production_task(
    root: str | Path,
    asset_id: str,
    task_id: str,
    target_status: str,
    *,
    expected_queue_revision: int,
    actor: str,
    reason: str,
    worker_id: str | None = None,
    blockers: list[Mapping[str, Any]] | None = None,
    result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    tasks, queue_revision = _task_queue_or_empty(root, asset_id)
    if queue_revision != int(expected_queue_revision):
        return _revision_conflict("TASK_QUEUE_REVISION_CONFLICT", expected_queue_revision, queue_revision)
    task = tasks.get(str(task_id))
    if task is None:
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "TASK_NOT_FOUND", "task_id": str(task_id)}],
        }
    receipts: list[Mapping[str, Any]] | None = None
    if str(target_status).upper() == "APPROVED" and list(task.get("required_validation_ids", []) or []):
        result_record = task.get("result")
        if result is not None:
            result_record = result
        if not isinstance(result_record, Mapping) or result_record.get("scene_revision") is None:
            return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "TASK_SCENE_REVISION_REQUIRED_FOR_APPROVAL"}]}
        validation = query_validation_receipts(
            root,
            asset_id,
            component_id=str(task.get("component_id")),
            asset_revision=int(task.get("asset_revision", 0)),
            scene_revision=int(result_record["scene_revision"]),
            validator_ids=[str(value) for value in list(task.get("required_validation_ids", []) or [])],
        )
        receipts = list(validation.get("receipts", []) or [])
    changed = transition(
        task,
        target_status,
        actor=actor,
        reason=reason,
        worker_id=worker_id,
        blockers=blockers,
        result=result,
        validation_receipts=receipts,
    )
    if changed.get("status") != "PASS":
        return changed
    tasks[str(task_id)] = changed["task"]
    saved = save_task_queue(root, asset_id, tasks, expected_queue_revision=queue_revision)
    if saved.get("status") != "PASS":
        return {**saved, "executor_id": EXECUTOR_ID, "task": None}
    response = {**saved, "executor_id": EXECUTOR_ID, "task": changed["task"]}
    if str(target_status).upper() == "APPROVED":
        accepted = _accept_component_state(root, asset_id, str(task.get("component_id")))
        if accepted.get("status") != "PASS":
            return {
                **response,
                "status": "PARTIAL",
                "blockers": [{"reason": "TASK_APPROVED_COMPONENT_STATE_SYNC_FAILED", "details": accepted.get("blockers", [])}],
            }
        response["asset_revision"] = accepted.get("asset_revision")
        response["component_state"] = "ACCEPTED"
    return response


def promote_production_tasks(
    root: str | Path,
    asset_id: str,
    *,
    expected_queue_revision: int,
) -> dict[str, Any]:
    tasks, queue_revision = _task_queue_or_empty(root, asset_id)
    if queue_revision != int(expected_queue_revision):
        return _revision_conflict("TASK_QUEUE_REVISION_CONFLICT", expected_queue_revision, queue_revision)
    promoted = promote_ready(tasks)
    if promoted.get("status") != "PASS":
        return promoted
    saved = save_task_queue(root, asset_id, promoted["tasks"], expected_queue_revision=queue_revision)
    return {
        **saved,
        "executor_id": EXECUTOR_ID,
        "promoted": promoted.get("promoted", []),
        "blocked": promoted.get("blocked", []),
    }


def publish_scene(
    root: str | Path,
    asset_id: str,
    report: Mapping[str, Any],
    *,
    component_ids: list[str] | None = None,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_asset_revision = int(loaded["asset"].get("revision", 0))
    declared_asset_revision = report.get("asset_revision", current_asset_revision)
    if int(declared_asset_revision) != current_asset_revision:
        return _revision_conflict("SCENE_ASSET_REVISION_CONFLICT", current_asset_revision, int(declared_asset_revision))

    if report.get("snapshot_hash") and isinstance(report.get("objects"), list):
        snapshot = dict(report)
    else:
        built = build_scene_snapshot(
            {
                "asset_id": asset_id,
                "asset_revision": current_asset_revision,
                "scene_revision": report.get("scene_revision"),
                "objects": report.get("objects", []),
            },
            component_ids=component_ids,
        )
        if built.get("status") != "PASS":
            return built
        snapshot = built["snapshot"]
    return {**publish_scene_snapshot(root, snapshot), "executor_id": EXECUTOR_ID}


def upsert_reference_evidence(
    root: str | Path,
    asset_id: str,
    evidence: Mapping[str, Any],
    *,
    expected_reference_revision: int,
) -> dict[str, Any]:
    _registry, revision = _evidence_or_empty(root, asset_id)
    if revision != int(expected_reference_revision):
        return _revision_conflict("REFERENCE_EVIDENCE_REVISION_CONFLICT", expected_reference_revision, revision)
    if revision == 0:
        initialized = initialize_evidence(root, asset_id, {"evidence": [dict(evidence)]})
        if initialized.get("status") != "PASS":
            return initialized
        return {
            "status": "PASS",
            "executor_id": EXECUTOR_ID,
            "revision": int(initialized["registry"]["revision"]),
            "evidence_count": 1,
        }
    return {
        **upsert_evidence_record(
            root,
            asset_id,
            evidence,
            expected_revision=revision,
        ),
        "executor_id": EXECUTOR_ID,
    }


def delete_reference_evidence(
    root: str | Path,
    asset_id: str,
    evidence_id: str,
    *,
    expected_reference_revision: int,
) -> dict[str, Any]:
    _registry, revision = _evidence_or_empty(root, asset_id)
    if revision != int(expected_reference_revision):
        return _revision_conflict("REFERENCE_EVIDENCE_REVISION_CONFLICT", expected_reference_revision, revision)
    if revision == 0:
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "REFERENCE_EVIDENCE_ID_NOT_FOUND", "evidence_id": str(evidence_id)}],
        }
    return {
        **remove_evidence_record(
            root,
            asset_id,
            evidence_id,
            expected_revision=revision,
        ),
        "executor_id": EXECUTOR_ID,
    }


def prepare_task(
    root: str | Path,
    asset_id: str,
    component_id: str,
    *,
    task_kind: str = "BUILD",
    feature_ids: list[str] | None = None,
    views: list[str] | None = None,
    max_input_tokens: int | None = None,
    reference_artifacts: Mapping[str, Mapping[str, Any]] | None = None,
    reference_artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = loaded["asset"]
    registry, _revision = _evidence_or_empty(root, asset_id)
    catalog, _impacts = _resource_catalog(root, asset)
    spec: dict[str, Any] = {
        "asset": asset,
        "component_id": component_id,
        "task_kind": task_kind,
        "design_resources": catalog,
        "reference_evidence_registry": registry,
        "reference_feature_ids": list(feature_ids or []),
        "reference_views": list(views or []),
    }
    if reference_artifacts is not None:
        spec["reference_artifacts"] = reference_artifacts
        spec["reference_artifact_root"] = reference_artifact_root
    if max_input_tokens is not None:
        spec["max_input_tokens"] = int(max_input_tokens)
    result = prepare_component_task(spec)
    return {**result, "executor_id": EXECUTOR_ID}


def _revision_conflict(reason: str, expected: int, actual: int) -> dict[str, Any]:
    return {
        "status": "CONFLICT",
        "executor_id": EXECUTOR_ID,
        "blockers": [{"reason": reason, "expected": int(expected), "actual": int(actual)}],
    }


__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "add_asset_correction",
    "advance_asset_stage",
    "authorize_component",
    "create_asset",
    "create_production_task",
    "delete_reference_evidence",
    "get_studio",
    "list_assets",
    "prepare_task",
    "promote_production_tasks",
    "publish_scene",
    "publish_validation_receipt",
    "resolve_asset_correction",
    "transition_production_task",
    "upsert_reference_evidence",
]

from __future__ import annotations

"""Run trusted component validators and persist revision-bound receipts."""

from pathlib import Path
from typing import Any, Mapping

from executors.representation_contract_gate import EXECUTOR_VERSION as REPRESENTATION_VERSION
from executors.representation_contract_gate import validate as validate_representation
from executors.scene_component_validation import EXECUTOR_VERSION as SCENE_VALIDATION_VERSION
from executors.scene_component_validation import validate as validate_scene_component
from executors.validation_receipt_repository import load as load_receipts
from executors.validation_receipt_repository import publish as publish_receipt
from executors.validation_receipt_repository import query as query_receipts

EXECUTOR_ID = "COMPONENT_VALIDATION_RUNNER"
EXECUTOR_VERSION = "0.21.0"


def _receipt_id(validator_id: str, task_pack: Mapping[str, Any], snapshot: Mapping[str, Any]) -> str:
    return ":".join(
        (
            "validation",
            str(validator_id),
            str(task_pack.get("asset_id") or ""),
            f"a{int(task_pack.get('asset_revision') or 0)}",
            str(task_pack.get("component_id") or ""),
            f"s{int(snapshot.get('scene_revision') or 0)}",
        )
    )


def _publish_or_reuse(
    root: str | Path,
    task_pack: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    verdict: Mapping[str, Any],
    *,
    validator_version: str,
) -> dict[str, Any]:
    validator_id = str(verdict.get("validator_id") or "")
    receipt_id = _receipt_id(validator_id, task_pack, snapshot)
    existing = query_receipts(
        root,
        str(task_pack.get("asset_id") or ""),
        component_id=str(task_pack.get("component_id") or ""),
        asset_revision=int(task_pack.get("asset_revision") or 0),
        scene_revision=int(snapshot.get("scene_revision") or 0),
        validator_ids=[validator_id],
    )
    for receipt in list(existing.get("receipts", []) or []):
        if str(receipt.get("receipt_id") or "") == receipt_id:
            return {"status": "PASS", "reused": True, "receipt": dict(receipt)}

    loaded = load_receipts(root, str(task_pack.get("asset_id") or ""))
    expected_revision = int(loaded.get("revision", 0)) if loaded.get("status") == "PASS" else None
    receipt = {
        "receipt_id": receipt_id,
        "validator_id": validator_id,
        "validator_version": validator_version,
        "asset_id": task_pack.get("asset_id"),
        "asset_revision": int(task_pack.get("asset_revision") or 0),
        "component_id": task_pack.get("component_id"),
        "scene_revision": int(snapshot.get("scene_revision") or 0),
        "status": str(verdict.get("status") or "FAIL").upper(),
        "source": "SYSTEM",
        "snapshot_hash": snapshot.get("snapshot_hash"),
        "blockers": [dict(item) for item in list(verdict.get("blockers", []) or []) if isinstance(item, Mapping)],
    }
    published = publish_receipt(
        root,
        str(task_pack.get("asset_id") or ""),
        receipt,
        expected_revision=expected_revision,
    )
    return {**published, "reused": False}


def validate_and_publish(
    root: str | Path,
    task_pack: Mapping[str, Any],
    recipe: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    representation = validate_representation(task_pack, recipe)
    scene = validate_scene_component(task_pack, snapshot)

    representation_receipt = _publish_or_reuse(
        root,
        task_pack,
        snapshot,
        representation,
        validator_version=REPRESENTATION_VERSION,
    )
    scene_receipt = _publish_or_reuse(
        root,
        task_pack,
        snapshot,
        scene,
        validator_version=SCENE_VALIDATION_VERSION,
    )
    persistence_failures = [
        result
        for result in (representation_receipt, scene_receipt)
        if str(result.get("status") or "").upper() != "PASS"
    ]
    validation_blockers = [
        *list(representation.get("blockers", []) or []),
        *list(scene.get("blockers", []) or []),
    ]
    status = "PASS" if not persistence_failures and not validation_blockers else "FAIL"
    return {
        "status": status,
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "component_id": task_pack.get("component_id"),
        "asset_revision": task_pack.get("asset_revision"),
        "scene_revision": snapshot.get("scene_revision"),
        "validators": {
            "REPRESENTATION_CONTRACT_GATE": representation,
            "SCENE_COMPONENT_VALIDATION": scene,
        },
        "receipts": [
            result.get("receipt")
            for result in (representation_receipt, scene_receipt)
            if isinstance(result.get("receipt"), Mapping)
        ],
        "blockers": [
            *[dict(item) for item in validation_blockers if isinstance(item, Mapping)],
            *[
                {"reason": "VALIDATION_RECEIPT_PERSISTENCE_FAILED", "details": result.get("blockers", [])}
                for result in persistence_failures
            ],
        ],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "validate_and_publish"]

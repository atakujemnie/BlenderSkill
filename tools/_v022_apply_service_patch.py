from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"PATCH_{label}_EXPECTED_ONCE_FOUND_{count}")
    return text.replace(old, new, 1)


def patch_service() -> None:
    path = ROOT / "executors" / "production_studio_service.py"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "from executors.asset_state_runtime import ASSET_STAGES, add_correction, advance_stage, resolve_correction\n",
        "from executors.asset_state_runtime import ASSET_STAGES, add_correction, advance_stage, resolve_correction\n"
        "from executors.asset_stage_completion_gate import acceptance_level_for_stage\n"
        "from executors.asset_stage_completion_gate import validate as validate_stage_completion\n",
        "STAGE_IMPORT",
    )
    text = replace_once(
        text,
        "from executors.design_system_repository import impact_report, load as load_design_resource\n",
        "from executors.design_system_repository import impact_report, load as load_design_resource\n"
        "from executors.fidelity_review_repository import initialize as initialize_fidelity_reviews\n"
        "from executors.fidelity_review_repository import load as load_fidelity_review\n"
        "from executors.fidelity_review_repository import publish as publish_fidelity_review_record\n",
        "FIDELITY_REPO_IMPORT",
    )
    text = replace_once(
        text,
        "from executors.validation_receipt_repository import query as query_validation_receipts\n",
        "from executors.validation_receipt_repository import query as query_validation_receipts\n"
        "from executors.visual_fidelity_review_gate import validate as validate_visual_fidelity_review\n",
        "VISUAL_GATE_IMPORT",
    )
    text = replace_once(text, 'EXECUTOR_VERSION = "0.21.0"', 'EXECUTOR_VERSION = "0.22.0"', "VERSION")

    old_create = """    validation = initialize_validation_receipts(root, asset_id)\n    blockers: list[dict[str, Any]] = []\n    for result in (queue, evidence, validation):\n"""
    new_create = """    validation = initialize_validation_receipts(root, asset_id)\n    fidelity = initialize_fidelity_reviews(root, asset_id)\n    blockers: list[dict[str, Any]] = []\n    for result in (queue, evidence, validation, fidelity):\n"""
    text = replace_once(text, old_create, new_create, "CREATE_FIDELITY_REPO")

    old_return = '        "validation_revision": validation.get("revision"),\n        "blockers": blockers,\n'
    new_return = '        "validation_revision": validation.get("revision"),\n        "fidelity_review_revision": fidelity.get("revision", 0),\n        "blockers": blockers,\n'
    text = replace_once(text, old_return, new_return, "CREATE_RETURN")

    old_stage = """    if bool(loaded[\"asset\"].get(\"enforce_asset_envelope\", False)):\n        envelope = validate_asset_envelope(loaded[\"asset\"])\n        if envelope.get(\"status\") != \"PASS\":\n            return {**envelope, \"executor_id\": EXECUTOR_ID, \"failed_stage\": \"ASSET_ENVELOPE\"}\n    changed = advance_stage(loaded[\"asset\"], new_stage)\n"""
    new_stage = """    if bool(loaded[\"asset\"].get(\"enforce_asset_envelope\", False)):\n        envelope = validate_asset_envelope(loaded[\"asset\"])\n        if envelope.get(\"status\") != \"PASS\":\n            return {**envelope, \"executor_id\": EXECUTOR_ID, \"failed_stage\": \"ASSET_ENVELOPE\"}\n    scene, scene_revision = _scene_or_none(root, asset_id)\n    _registry, reference_revision = _evidence_or_empty(root, asset_id)\n    fidelity = load_fidelity_review(root, asset_id)\n    fidelity_review = fidelity.get(\"review\") if fidelity.get(\"status\") == \"PASS\" else None\n    completion = validate_stage_completion(\n        loaded[\"asset\"],\n        new_stage,\n        fidelity_review=fidelity_review,\n        scene_revision=scene_revision if scene is not None else 0,\n        reference_revision=reference_revision,\n    )\n    if completion.get(\"status\") != \"PASS\":\n        return {**completion, \"executor_id\": EXECUTOR_ID, \"failed_stage\": \"ASSET_STAGE_COMPLETION\"}\n    changed = advance_stage(loaded[\"asset\"], new_stage)\n"""
    text = replace_once(text, old_stage, new_stage, "STAGE_GATE")

    old_validators = """    required_validators = list(spec.get(\"required_validation_ids\", []) or declared_validators)\n    if ASSET_STAGES.index(requested_stage) >= _GEOMETRY_STAGE_INDEX and not required_validators:\n        required_validators = list(_DEFAULT_GEOMETRY_VALIDATORS)\n"""
    new_validators = """    required_validators = list(spec.get(\"required_validation_ids\", []) or declared_validators)\n    if ASSET_STAGES.index(requested_stage) >= _GEOMETRY_STAGE_INDEX and not required_validators:\n        required_validators = list(_DEFAULT_GEOMETRY_VALIDATORS)\n    feature_contract_enabled = bool(\n        asset.get(\"enforce_feature_contracts\", False)\n        or components[component_id].get(\"feature_contract_required\", False)\n        or components[component_id].get(\"feature_contract\")\n    )\n    if feature_contract_enabled and \"FEATURE_CONTRACT_GATE\" not in required_validators:\n        required_validators.append(\"FEATURE_CONTRACT_GATE\")\n"""
    text = replace_once(text, old_validators, new_validators, "DYNAMIC_VALIDATORS")

    old_accept = """def _accept_component_state(root: str | Path, asset_id: str, component_id: str) -> dict[str, Any]:\n"""
    new_accept = """def _accept_component_state(\n    root: str | Path, asset_id: str, component_id: str, *, task_stage: str, receipt_ids: list[str]\n) -> dict[str, Any]:\n"""
    text = replace_once(text, old_accept, new_accept, "ACCEPT_SIGNATURE")
    old_accept_fields = """    updated = dict(cp_components[str(component_id)])\n    updated[\"state\"] = \"ACCEPTED\"\n    cp_components[str(component_id)] = updated\n"""
    new_accept_fields = """    updated = dict(cp_components[str(component_id)])\n    updated[\"state\"] = \"ACCEPTED\"\n    updated[\"acceptance_level\"] = acceptance_level_for_stage(task_stage)\n    updated[\"last_validation_receipt_ids\"] = sorted(str(value) for value in receipt_ids if str(value))\n    cp_components[str(component_id)] = updated\n"""
    text = replace_once(text, old_accept_fields, new_accept_fields, "ACCEPT_FIELDS")
    old_history = '    history.append({"revision": cp["revision"], "event": "COMPONENT_ACCEPTED", "component_id": str(component_id)})\n'
    new_history = '    history.append({"revision": cp["revision"], "event": "COMPONENT_ACCEPTED", "component_id": str(component_id), "stage": str(task_stage), "acceptance_level": updated["acceptance_level"]})\n'
    text = replace_once(text, old_history, new_history, "ACCEPT_HISTORY")
    old_call = '        accepted = _accept_component_state(root, asset_id, str(task.get("component_id")))\n'
    new_call = '        accepted = _accept_component_state(root, asset_id, str(task.get("component_id")), task_stage=str(task.get("stage") or ""), receipt_ids=list(changed["task"].get("approval_receipt_ids", []) or []))\n'
    text = replace_once(text, old_call, new_call, "ACCEPT_CALL")
    old_response = '        response["component_state"] = "ACCEPTED"\n'
    new_response = '        response["component_state"] = "ACCEPTED"\n        response["component_acceptance_level"] = acceptance_level_for_stage(str(task.get("stage") or ""))\n'
    text = replace_once(text, old_response, new_response, "ACCEPT_RESPONSE")

    insert_before = "\ndef _revision_conflict(reason: str, expected: int, actual: int) -> dict[str, Any]:\n"
    new_functions = '''\ndef publish_fidelity_review(\n    root: str | Path,\n    asset_id: str,\n    review: Mapping[str, Any],\n    *,\n    expected_review_revision: int,\n) -> dict[str, Any]:\n    loaded = load_asset(root, asset_id)\n    if loaded.get("status") != "PASS":\n        return loaded\n    asset = loaded["asset"]\n    scene, scene_revision = _scene_or_none(root, asset_id)\n    if scene is None:\n        return {"status": "BLOCKED", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "FIDELITY_REVIEW_SCENE_REQUIRED"}]}\n    _registry, reference_revision = _evidence_or_empty(root, asset_id)\n    verdict = validate_visual_fidelity_review(\n        asset,\n        review,\n        scene_revision=scene_revision,\n        reference_revision=reference_revision,\n    )\n    record = {\n        **dict(review),\n        "asset_id": asset_id,\n        "asset_revision": int(asset.get("revision", 0)),\n        "scene_revision": scene_revision,\n        "reference_revision": reference_revision,\n        "status": verdict.get("status"),\n        "source": "SYSTEM",\n        "validator_id": verdict.get("validator_id"),\n        "validator_version": verdict.get("validator_version"),\n        "blockers": verdict.get("blockers", []),\n        "warnings": verdict.get("warnings", []),\n    }\n    saved = publish_fidelity_review_record(\n        root, asset_id, record, expected_revision=expected_review_revision\n    )\n    return {\n        **saved,\n        "status": verdict.get("status") if saved.get("status") == "PASS" else saved.get("status"),\n        "executor_id": EXECUTOR_ID,\n        "review": record,\n        "blockers": verdict.get("blockers", []) if saved.get("status") == "PASS" else saved.get("blockers", []),\n    }\n\n\ndef get_fidelity_review(root: str | Path, asset_id: str) -> dict[str, Any]:\n    loaded = load_fidelity_review(root, asset_id)\n    return {**loaded, "executor_id": EXECUTOR_ID}\n'''
    text = replace_once(text, insert_before, new_functions + insert_before, "FIDELITY_FUNCTIONS")

    old_studio_revision = """    model[\"validation_revision\"] = validation.get(\"revision\", 0)\n    inspector[\"validation_receipts\"] = list(validation.get(\"receipts\", []) or [])\n"""
    new_studio_revision = """    model[\"validation_revision\"] = validation.get(\"revision\", 0)\n    inspector[\"validation_receipts\"] = list(validation.get(\"receipts\", []) or [])\n    fidelity = load_fidelity_review(root, asset_id)\n    model[\"fidelity_review_revision\"] = fidelity.get(\"revision\", 0) if fidelity.get(\"status\") == \"PASS\" else 0\n    inspector[\"fidelity_review\"] = fidelity.get(\"review\") if fidelity.get(\"status\") == \"PASS\" else None\n"""
    text = replace_once(text, old_studio_revision, new_studio_revision, "STUDIO_FIDELITY")

    path.write_text(text, encoding="utf-8")


def patch_orchestrator() -> None:
    path = ROOT / "executors" / "asset_production_orchestrator.py"
    text = path.read_text(encoding="utf-8")
    old = '        "reference_evidence": deduplicated_evidence,\n    }\n'
    new = '        "reference_evidence": deduplicated_evidence,\n    }\n    if spec.get("reference_artifacts") is not None:\n        task_spec["reference_artifacts"] = spec.get("reference_artifacts")\n        task_spec["reference_artifact_root"] = spec.get("reference_artifact_root")\n'
    text = replace_once(text, old, new, "ORCHESTRATOR_ARTIFACTS")
    text = text.replace('EXECUTOR_VERSION = "0.19.0"', 'EXECUTOR_VERSION = "0.22.0"', 1)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    patch_service()
    patch_orchestrator()
    print("v0.22 service patch applied")

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "15_asset_production/503_FIDELITY_ENFORCEMENT_AND_DETERMINISTIC_ASSEMBLY.md"
BENCHMARK = "07_examples/91_LAFAR_SIDEWALK_FIDELITY_ENFORCEMENT_V021_REGRESSION_BENCHMARK.md"


def patch_service() -> None:
    path = ROOT / "executors/production_studio_service.py"
    text = path.read_text(encoding="utf-8")
    import_line = "from executors.asset_execution_authorization_gate import evaluate as evaluate_asset_execution_authorization\n"
    if import_line not in text:
        text = text.replace(
            "from executors.asset_envelope_gate import validate as validate_asset_envelope\n",
            "from executors.asset_envelope_gate import validate as validate_asset_envelope\n" + import_line,
            1,
        )

    replacement = '''def authorize_component(
    root: str | Path,
    asset_id: str,
    component_id: str,
    authorization: Mapping[str, Any] | None = None,
    *,
    expected_asset_revision: int,
) -> dict[str, Any]:
    """Request authorization; PASS is derived only from persisted system state."""
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    asset = loaded["asset"]
    current_revision = int(asset.get("revision", 0))
    if current_revision != int(expected_asset_revision):
        return _revision_conflict("ASSET_REVISION_CONFLICT", expected_asset_revision, current_revision)

    gate = evaluate_asset_execution_authorization(asset, str(component_id))
    if gate.get("status") != "PASS":
        return {**gate, "executor_id": EXECUTOR_ID}

    cp = deepcopy(dict(asset))
    cp_components = {str(key): dict(value) for key, value in dict(cp.get("components", {}) or {}).items()}
    cp_component = dict(cp_components[str(component_id)])
    cp_component["state"] = "READY_TO_BUILD"
    cp_component["execution_authorization"] = {
        **dict(gate),
        "request_actor": str((authorization or {}).get("actor") or "SYSTEM"),
        "request_reason": str((authorization or {}).get("reason") or "AUTHORIZE_COMPONENT"),
    }
    cp_components[str(component_id)] = cp_component
    cp["components"] = cp_components
    cp["revision"] = current_revision + 1
    history = list(cp.get("history", []) or [])
    history.append(
        {
            "revision": cp["revision"],
            "event": "COMPONENT_AUTHORIZED",
            "component_id": str(component_id),
            "validator_id": gate.get("validator_id"),
        }
    )
    cp["history"] = history
    saved = save_asset(root, cp, expected_revision=current_revision)
    return {
        **saved,
        "executor_id": EXECUTOR_ID,
        "asset_revision": cp["revision"] if saved.get("status") == "PASS" else current_revision,
        "authorization": gate if saved.get("status") == "PASS" else None,
    }


'''
    text, count = re.subn(
        r"def authorize_component\(.*?\n\ndef _geometry_task_authorization",
        replacement + "def _geometry_task_authorization",
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("AUTHORIZE_COMPONENT_PATCH_FAILED")

    receipt_replacement = '''def publish_validation_receipt(
    root: str | Path,
    asset_id: str,
    receipt: Mapping[str, Any],
    *,
    expected_validation_revision: int | None = None,
) -> dict[str, Any]:
    """Persist a trusted receipt only for the current persisted asset and scene."""
    loaded = load_asset(root, asset_id)
    if loaded.get("status") != "PASS":
        return loaded
    current_asset_revision = int(loaded["asset"].get("revision", 0))
    if int(receipt.get("asset_revision", 0)) != current_asset_revision:
        return _revision_conflict(
            "VALIDATION_RECEIPT_ASSET_REVISION_STALE",
            current_asset_revision,
            int(receipt.get("asset_revision", 0)),
        )
    scene, current_scene_revision = _scene_or_none(root, asset_id)
    if scene is None:
        return {
            "status": "BLOCKED",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "VALIDATION_RECEIPT_SCENE_REQUIRED"}],
        }
    if int(receipt.get("scene_revision", 0)) != current_scene_revision:
        return _revision_conflict(
            "VALIDATION_RECEIPT_SCENE_REVISION_STALE",
            current_scene_revision,
            int(receipt.get("scene_revision", 0)),
        )
    component_id = str(receipt.get("component_id") or "")
    if component_id not in dict(loaded["asset"].get("components", {}) or {}):
        return {
            "status": "FAIL",
            "executor_id": EXECUTOR_ID,
            "blockers": [{"reason": "VALIDATION_RECEIPT_COMPONENT_NOT_FOUND", "component_id": component_id}],
        }
    return {
        **publish_validation_receipt_record(
            root,
            asset_id,
            receipt,
            expected_revision=expected_validation_revision,
        ),
        "executor_id": EXECUTOR_ID,
    }


'''
    text, count = re.subn(
        r"def publish_validation_receipt\(.*?\n\ndef _accept_component_state",
        receipt_replacement + "def _accept_component_state",
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("VALIDATION_RECEIPT_PATCH_FAILED")
    path.write_text(text, encoding="utf-8")


def patch_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))

    additions = [
        ("COMPONENT_TRANSFORM", "executors/component_transform.py", ["tests/unit/test_component_transform.py"]),
        ("ASSET_ENVELOPE_GATE", "executors/asset_envelope_gate.py", ["tests/unit/test_asset_envelope_gate.py", "tests/regression/test_benchmark_91.py"]),
        ("REPRESENTATION_CONTRACT_GATE", "executors/representation_contract_gate.py", ["tests/unit/test_representation_contract_gate.py", "tests/regression/test_benchmark_91.py"]),
        ("COMPONENT_EXECUTION_GATE", "executors/component_execution_gate.py", ["tests/unit/test_component_execution_gate.py", "tests/blender/test_v021_component_execution.py"]),
        ("VALIDATION_RECEIPT_REPOSITORY", "executors/validation_receipt_repository.py", ["tests/unit/test_validation_receipt_repository.py", "tests/unit/test_v021_trusted_task_approval.py", "tests/regression/test_benchmark_91.py"]),
        ("REFERENCE_EVIDENCE_MATERIALIZER", "executors/reference_evidence_materializer.py", ["tests/unit/test_reference_evidence_materializer.py"]),
        ("BLENDER_DESIGN_RESOURCE_ADAPTER", "executors/blender_design_resource_adapter.py", ["tests/blender/test_v021_component_execution.py"]),
        ("ASSET_EXECUTION_AUTHORIZATION_GATE", "executors/asset_execution_authorization_gate.py", ["tests/unit/test_asset_execution_authorization_gate.py", "tests/regression/test_benchmark_91.py"]),
    ]

    executors = list(manifest.get("executors", []))
    by_id = {str(item.get("id")): index for index, item in enumerate(executors) if isinstance(item, dict)}
    for executor_id, executor_path, tests in additions:
        item = {
            "id": executor_id,
            "contract": CONTRACT,
            "executor": executor_path,
            "maturity": "EXECUTOR_READY",
            "tests": tests,
        }
        if executor_id in by_id:
            executors[by_id[executor_id]] = item
        else:
            executors.append(item)
            by_id[executor_id] = len(executors) - 1

    updates = {
        "PRODUCTION_STUDIO_SERVICE": ["tests/integration/test_v021_studio_http.py", "tests/regression/test_benchmark_91.py"],
        "COMPONENT_TASK_PACK": ["tests/unit/test_component_task_pack.py", "tests/regression/test_benchmark_91.py"],
        "BLENDER_HARD_SURFACE_BUILDER": ["tests/blender/test_hard_surface_builder.py", "tests/blender/test_v021_component_execution.py"],
        "PRODUCTION_TASK_LIFECYCLE": ["tests/unit/test_production_task_lifecycle.py", "tests/unit/test_v021_trusted_task_approval.py"],
    }
    for item in executors:
        if not isinstance(item, dict) or item.get("id") not in updates:
            continue
        item["contract"] = CONTRACT
        tests = list(item.get("tests", []))
        for test in updates[item["id"]]:
            if test not in tests:
                tests.append(test)
        item["tests"] = tests
    manifest["executors"] = executors

    skills = list(manifest.get("skills", []))
    skill_ids = {str(item.get("id")) for item in skills if isinstance(item, dict)}
    if "ASSET_EXECUTION_AUTHORIZATION_GATE" not in skill_ids:
        skills.append(
            {
                "id": "ASSET_EXECUTION_AUTHORIZATION_GATE",
                "purpose": "Derive component build authorization from persisted asset state instead of caller-supplied PASS claims.",
                "contract": CONTRACT,
                "executor": "executors/asset_execution_authorization_gate.py",
                "maturity": "EXECUTOR_READY",
                "dependencies": ["ASSET_STATE_RUNTIME"],
                "benchmark": BENCHMARK,
                "routing_keywords": ["authorization", "component", "build", "v0.21"],
                "tests": ["tests/unit/test_asset_execution_authorization_gate.py", "tests/regression/test_benchmark_91.py"],
            }
        )
    manifest["skills"] = skills

    tests = list(manifest.get("tests", []))
    new_test = "tests/unit/test_asset_execution_authorization_gate.py"
    if new_test not in tests:
        tests.append(new_test)
    manifest["tests"] = tests
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    patch_service()
    patch_manifest()
    print("v0.21 hardening patch applied")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "15_asset_production/503_FIDELITY_ENFORCEMENT_AND_DETERMINISTIC_ASSEMBLY.md"
BENCHMARK = "07_examples/91_LAFAR_SIDEWALK_FIDELITY_ENFORCEMENT_V021_REGRESSION_BENCHMARK.md"


def main() -> None:
    path = ROOT / "MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        {
            "id": "SCENE_COMPONENT_VALIDATION",
            "contract": CONTRACT,
            "executor": "executors/scene_component_validation.py",
            "maturity": "EXECUTOR_READY",
            "tests": ["tests/unit/test_scene_component_validation.py", "tests/regression/test_benchmark_91.py"],
        },
        {
            "id": "COMPONENT_VALIDATION_RUNNER",
            "contract": CONTRACT,
            "executor": "executors/component_validation_runner.py",
            "maturity": "EXECUTOR_READY",
            "tests": ["tests/unit/test_component_validation_runner.py", "tests/regression/test_benchmark_91.py"],
        },
    ]
    executors = list(manifest.get("executors", []))
    indexes = {str(item.get("id")): index for index, item in enumerate(executors) if isinstance(item, dict)}
    for item in additions:
        if item["id"] in indexes:
            executors[indexes[item["id"]]] = item
        else:
            executors.append(item)
    manifest["executors"] = executors

    skills = list(manifest.get("skills", []))
    skill_ids = {str(item.get("id")) for item in skills if isinstance(item, dict)}
    skill_additions = [
        {
            "id": "SCENE_COMPONENT_VALIDATION",
            "purpose": "Validate one component against current revision-bound compact scene evidence.",
            "contract": CONTRACT,
            "executor": "executors/scene_component_validation.py",
            "maturity": "EXECUTOR_READY",
            "dependencies": ["SCENE_COMPONENT_SNAPSHOT", "COMPONENT_TASK_PACK"],
            "benchmark": BENCHMARK,
            "routing_keywords": ["scene", "component", "validation", "placement", "dimensions"],
            "tests": ["tests/unit/test_scene_component_validation.py", "tests/regression/test_benchmark_91.py"],
        },
        {
            "id": "COMPONENT_VALIDATION_RUNNER",
            "purpose": "Run trusted deterministic component validators and persist their revision-bound receipts.",
            "contract": CONTRACT,
            "executor": "executors/component_validation_runner.py",
            "maturity": "EXECUTOR_READY",
            "dependencies": ["SCENE_COMPONENT_VALIDATION", "REPRESENTATION_CONTRACT_GATE", "VALIDATION_RECEIPT_REPOSITORY"],
            "benchmark": BENCHMARK,
            "routing_keywords": ["trusted", "validation", "receipt", "approval"],
            "tests": ["tests/unit/test_component_validation_runner.py", "tests/regression/test_benchmark_91.py"],
        },
    ]
    for item in skill_additions:
        if item["id"] not in skill_ids:
            skills.append(item)
            skill_ids.add(item["id"])
    manifest["skills"] = skills

    tests = list(manifest.get("tests", []))
    for test in ("tests/unit/test_scene_component_validation.py", "tests/unit/test_component_validation_runner.py"):
        if test not in tests:
            tests.append(test)
    manifest["tests"] = tests
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

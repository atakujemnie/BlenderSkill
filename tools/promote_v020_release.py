from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.20.0"
BENCHMARK = "07_examples/90_LAFAR_OPERATIONAL_PRODUCTION_STUDIO_V020_REGRESSION_BENCHMARK.md"
CONTRACT = "15_asset_production/502_OPERATIONAL_PRODUCTION_STUDIO_API.md"

NEW_SKILLS = [
    {
        "id": "REFERENCE_EVIDENCE_REPOSITORY",
        "purpose": "Persist asset-scoped reference evidence registries with immutable revisions and stale-writer protection.",
        "contract": CONTRACT,
        "executor": "executors/reference_evidence_repository.py",
        "maturity": "EXECUTOR_READY",
        "dependencies": ["REFERENCE_EVIDENCE_REGISTRY"],
        "benchmark": BENCHMARK,
        "routing_keywords": ["evidence", "persistence", "reference", "revision"],
    },
    {
        "id": "SCENE_SNAPSHOT_REPOSITORY",
        "purpose": "Persist compact scene snapshots with immutable revision history and optimistic concurrency.",
        "contract": CONTRACT,
        "executor": "executors/scene_snapshot_repository.py",
        "maturity": "EXECUTOR_READY",
        "dependencies": ["SCENE_COMPONENT_SNAPSHOT"],
        "benchmark": BENCHMARK,
        "routing_keywords": ["scene", "snapshot", "persistence", "revision"],
    },
    {
        "id": "BLENDER_SCENE_SNAPSHOT_ADAPTER",
        "purpose": "Read Blender 5.1 scene data into compact production snapshots without mutating the scene.",
        "contract": CONTRACT,
        "executor": "executors/blender_scene_snapshot_adapter.py",
        "maturity": "EXECUTOR_READY",
        "dependencies": ["SCENE_COMPONENT_SNAPSHOT"],
        "benchmark": BENCHMARK,
        "routing_keywords": ["blender", "measurement", "scene", "snapshot"],
    },
    {
        "id": "PRODUCTION_STUDIO_SERVICE",
        "purpose": "Operational service layer for asset, correction, task, evidence, scene and task-pack workflows.",
        "contract": CONTRACT,
        "executor": "executors/production_studio_service.py",
        "maturity": "EXECUTOR_READY",
        "dependencies": [
            "ASSET_REPOSITORY",
            "ASSET_PRODUCTION_ORCHESTRATOR",
            "DESIGN_SYSTEM_REPOSITORY",
            "PRODUCTION_TASK_REPOSITORY",
            "REFERENCE_EVIDENCE_REPOSITORY",
            "SCENE_SNAPSHOT_REPOSITORY",
        ],
        "benchmark": BENCHMARK,
        "routing_keywords": ["api", "asset", "production", "studio"],
    },
    {
        "id": "DESIGN_STUDIO_SERVICE",
        "purpose": "Operational listing, mutation and impact inspection for shared design-system resources.",
        "contract": CONTRACT,
        "executor": "executors/design_studio_service.py",
        "maturity": "EXECUTOR_READY",
        "dependencies": ["DESIGN_SYSTEM_REPOSITORY"],
        "benchmark": BENCHMARK,
        "routing_keywords": ["design system", "impact", "resource", "studio"],
    },
]

NEW_EXECUTORS = [
    {
        "id": "REFERENCE_EVIDENCE_REPOSITORY",
        "contract": CONTRACT,
        "executor": "executors/reference_evidence_repository.py",
        "maturity": "EXECUTOR_READY",
        "tests": [
            "tests/unit/test_reference_evidence_repository.py",
            "tests/integration/test_production_studio_service.py",
        ],
    },
    {
        "id": "SCENE_SNAPSHOT_REPOSITORY",
        "contract": CONTRACT,
        "executor": "executors/scene_snapshot_repository.py",
        "maturity": "EXECUTOR_READY",
        "tests": [
            "tests/unit/test_scene_snapshot_repository.py",
            "tests/integration/test_production_studio_service.py",
        ],
    },
    {
        "id": "BLENDER_SCENE_SNAPSHOT_ADAPTER",
        "contract": CONTRACT,
        "executor": "executors/blender_scene_snapshot_adapter.py",
        "maturity": "EXECUTOR_READY",
        "tests": ["tests/blender/test_scene_snapshot_adapter.py"],
    },
    {
        "id": "PRODUCTION_STUDIO_SERVICE",
        "contract": CONTRACT,
        "executor": "executors/production_studio_service.py",
        "maturity": "EXECUTOR_READY",
        "tests": [
            "tests/integration/test_production_studio_service.py",
            "tests/integration/test_production_studio_http.py",
            "tests/regression/test_benchmark_90.py",
        ],
    },
    {
        "id": "DESIGN_STUDIO_SERVICE",
        "contract": CONTRACT,
        "executor": "executors/design_studio_service.py",
        "maturity": "EXECUTOR_READY",
        "tests": ["tests/integration/test_production_studio_http.py"],
    },
]

NEW_TESTS = [
    "tests/blender/test_scene_snapshot_adapter.py",
    "tests/integration/test_production_studio_http.py",
    "tests/integration/test_production_studio_service.py",
    "tests/regression/test_benchmark_90.py",
    "tests/unit/test_reference_evidence_repository.py",
    "tests/unit/test_scene_snapshot_repository.py",
]

NEW_EXECUTOR_FILES = [
    "executors/blender_scene_snapshot_adapter.py",
    "executors/design_studio_service.py",
    "executors/production_studio_service.py",
    "executors/reference_evidence_repository.py",
    "executors/scene_snapshot_repository.py",
]


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _upsert_by_id(values: list[dict], item: dict) -> None:
    for index, current in enumerate(values):
        if current.get("id") == item["id"]:
            values[index] = item
            return
    values.append(item)


def _write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


def promote_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["version"] = VERSION
    manifest["benchmark"] = BENCHMARK
    manifest["runtime_verification_version"] = VERSION
    benchmarks = list(manifest.get("benchmarks") or [])
    _append_unique(benchmarks, BENCHMARK)
    manifest["benchmarks"] = benchmarks
    modules = list(manifest.get("modules") or [])
    _append_unique(modules, BENCHMARK)
    _append_unique(modules, CONTRACT)
    manifest["modules"] = modules
    manifest["module_count"] = len(modules)

    skills = list(manifest.get("skills") or [])
    for item in NEW_SKILLS:
        _upsert_by_id(skills, item)
    manifest["skills"] = skills

    executors = list(manifest.get("executors") or [])
    for item in NEW_EXECUTORS:
        _upsert_by_id(executors, item)
    manifest["executors"] = executors

    tests = list(manifest.get("tests") or [])
    for test in NEW_TESTS:
        _append_unique(tests, test)
    manifest["tests"] = tests

    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def promote_executor_versions() -> None:
    for rel in NEW_EXECUTOR_FILES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        text, count = re.subn(
            r'EXECUTOR_VERSION\s*=\s*"[^"]+"',
            f'EXECUTOR_VERSION = "{VERSION}"',
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"EXECUTOR_VERSION_NOT_FOUND:{rel}")
        path.write_text(text, encoding="utf-8")


def promote_metadata() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pyproject = re.sub(r'(?m)^version = "[^"]+"$', f'version = "{VERSION}"', pyproject, count=1)
    _write("pyproject.toml", pyproject)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lines = readme.splitlines()
    banner = "> Current production runtime: v0.20.0 — operational persistent Production Studio API and live GUI."
    if lines and lines[0].startswith("> Current production runtime:"):
        lines[0] = banner
    else:
        lines = [banner, "", *lines]
    _write("README.md", "\n".join(lines).rstrip() + "\n")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    heading = "## 0.20.0 — Operational Production Studio"
    if heading not in changelog:
        section = """## 0.20.0 — Operational Production Studio

- Promoted the local Production Studio from inspection shell to operational workflow engine.
- Added revisioned scene-snapshot and reference-evidence repositories with optimistic concurrency.
- Added read-only Blender 5.1 scene snapshot adapter and real Blender regression coverage.
- Added Production Studio and Design Studio service layers over canonical repositories.
- Added loopback-first JSON HTTP API and live asset/design-system Studio interfaces.
- Added canonical Benchmark 90 for persistent operational Studio workflow, scoped context and restart-safe state.

"""
        changelog = section + changelog
    _write("CHANGELOG.md", changelog)

    prompt_path = ROOT / "06_prompts/60_SYSTEM_PROMPT.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    runtime_line = (
        "Runtime release: v0.20.0. Operational asset production MUST route through persistent repositories, "
        "component-scoped task packs and the Production Studio service/API when applicable."
    )
    if runtime_line not in prompt:
        prompt = prompt.rstrip() + "\n\n" + runtime_line + "\n"
    prompt_path.write_text(prompt, encoding="utf-8")

    validator_path = ROOT / "tools/validate_release_metadata.py"
    validator = validator_path.read_text(encoding="utf-8")
    validator = re.sub(r'TARGET_VERSION = "[^"]+"', f'TARGET_VERSION = "{VERSION}"', validator, count=1)
    validator = re.sub(r'TARGET_BENCHMARK = "[^"]+"', f'TARGET_BENCHMARK = "{BENCHMARK}"', validator, count=1)
    validator = validator.replace(r"0\.19\.0", r"0\.20\.0")
    validator = validator.replace('"0.19.0"', '"0.20.0"')
    validator_path.write_text(validator, encoding="utf-8")

    release_path = ROOT / ".github/workflows/release.yml"
    release = release_path.read_text(encoding="utf-8")
    release = release.replace("0.18.0", VERSION)
    release = release.replace(r"0\.18\.0", r"0\.20\.0")
    release = release.replace("v0.18.0", "v0.20.0")
    release = release.replace(
        "BlenderSkill v0.18.0 — Runtime Verification & Contract Convergence",
        "BlenderSkill v0.20.0 — Operational Production Studio",
    )
    release = release.replace("Require main and v0.18.0", "Require main and v0.20.0")
    release_path.write_text(release, encoding="utf-8")


def main() -> None:
    promote_manifest()
    promote_executor_versions()
    promote_metadata()
    print("Prepared BlenderSkill v0.20.0 source metadata")


if __name__ == "__main__":
    main()

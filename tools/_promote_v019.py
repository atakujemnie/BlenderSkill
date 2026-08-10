from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.19.0"
BENCHMARK_88 = "07_examples/88_LAFAR_STREET_BENCH_ASSET_RUNTIME_BENCHMARK.md"
BENCHMARK_89 = "07_examples/89_LAFAR_PRODUCTION_STUDIO_V019_REGRESSION_BENCHMARK.md"
CONTRACT_500 = "15_asset_production/500_ASSET_PRODUCTION_RUNTIME.md"
CONTRACT_501 = "15_asset_production/501_PRODUCTION_STUDIO_RUNTIME.md"

RUNTIME_ENTRIES = [
    {
        "id": "ASSET_STATE_RUNTIME",
        "purpose": "Persistent canonical asset/component state and correction semantics.",
        "contract": CONTRACT_500,
        "executor": "executors/asset_state_runtime.py",
        "tests": ["tests/unit/test_asset_state_runtime.py"],
        "dependencies": [],
        "routing_keywords": ["asset", "component", "correction", "state"],
    },
    {
        "id": "ASSET_REPOSITORY",
        "purpose": "Revisioned filesystem persistence for canonical asset state.",
        "contract": CONTRACT_500,
        "executor": "executors/asset_repository.py",
        "tests": ["tests/unit/test_asset_repository.py"],
        "dependencies": ["ASSET_STATE_RUNTIME"],
        "routing_keywords": ["asset", "persistence", "repository", "revision"],
    },
    {
        "id": "PARAMETER_GRAPH",
        "purpose": "Deterministic relational parameter resolution without LLM arithmetic.",
        "contract": CONTRACT_500,
        "executor": "executors/parameter_graph.py",
        "tests": ["tests/unit/test_parameter_graph.py"],
        "dependencies": ["ASSET_STATE_RUNTIME"],
        "routing_keywords": ["dimension", "parameter", "relation", "constraint"],
    },
    {
        "id": "DESIGN_BINDING_RESOLVER",
        "purpose": "Resolve inherited/overridden/custom design-system bindings and locks.",
        "contract": CONTRACT_500,
        "executor": "executors/design_binding_resolver.py",
        "tests": ["tests/unit/test_design_binding_resolver.py"],
        "dependencies": ["ASSET_STATE_RUNTIME"],
        "routing_keywords": ["binding", "design", "resource", "override"],
    },
    {
        "id": "REFERENCE_EVIDENCE_REGISTRY",
        "purpose": "Index and route component/feature scoped multi-view reference evidence.",
        "contract": CONTRACT_500,
        "executor": "executors/reference_evidence_registry.py",
        "tests": ["tests/unit/test_asset_production_orchestrator.py"],
        "dependencies": [],
        "routing_keywords": ["evidence", "reference", "roi", "view"],
    },
    {
        "id": "COMPONENT_TASK_PACK",
        "purpose": "Token-bounded component mutation pack with explicit mutable/read-only scope.",
        "contract": CONTRACT_500,
        "executor": "executors/component_task_pack.py",
        "tests": ["tests/unit/test_component_task_pack.py"],
        "dependencies": ["PARAMETER_GRAPH", "DESIGN_BINDING_RESOLVER", "REFERENCE_EVIDENCE_REGISTRY"],
        "routing_keywords": ["component", "context", "task", "token"],
    },
    {
        "id": "ASSET_PRODUCTION_ORCHESTRATOR",
        "purpose": "Prepare one component production task from persistent asset truth.",
        "contract": CONTRACT_500,
        "executor": "executors/asset_production_orchestrator.py",
        "tests": ["tests/unit/test_asset_production_orchestrator.py"],
        "dependencies": ["ASSET_STATE_RUNTIME", "PARAMETER_GRAPH", "DESIGN_BINDING_RESOLVER", "COMPONENT_TASK_PACK"],
        "routing_keywords": ["asset", "component", "orchestrator", "production"],
    },
    {
        "id": "HARD_SURFACE_RECIPE",
        "purpose": "Deterministic intermediate representation for manufactured hard-surface construction.",
        "contract": CONTRACT_500,
        "executor": "executors/hard_surface_recipe.py",
        "tests": ["tests/unit/test_hard_surface_recipe.py"],
        "dependencies": ["COMPONENT_TASK_PACK"],
        "routing_keywords": ["hard surface", "recipe", "geometry", "manufactured"],
    },
    {
        "id": "BLENDER_HARD_SURFACE_BUILDER",
        "purpose": "Blender 5.1 executor for deterministic hard-surface recipe operations.",
        "contract": CONTRACT_500,
        "executor": "executors/blender_hard_surface_builder.py",
        "tests": ["tests/blender/test_hard_surface_builder.py"],
        "dependencies": ["HARD_SURFACE_RECIPE"],
        "routing_keywords": ["blender", "builder", "hard surface", "recipe"],
    },
    {
        "id": "ASSEMBLY_ANCHOR_GATE",
        "purpose": "Validate explicit component anchor relations and assembly tolerances.",
        "contract": CONTRACT_500,
        "executor": "executors/assembly_anchor_gate.py",
        "tests": ["tests/unit/test_assembly_anchor_gate.py"],
        "dependencies": ["ASSET_STATE_RUNTIME"],
        "routing_keywords": ["anchor", "assembly", "mount", "tolerance"],
    },
    {
        "id": "DESIGN_SYSTEM_REPOSITORY",
        "purpose": "Versioned reusable design resources with reverse usage and impact analysis.",
        "contract": CONTRACT_501,
        "executor": "executors/design_system_repository.py",
        "tests": ["tests/unit/test_design_system_repository.py"],
        "dependencies": ["DESIGN_BINDING_RESOLVER"],
        "routing_keywords": ["design system", "impact", "resource", "version"],
    },
    {
        "id": "PRODUCTION_TASK_LIFECYCLE",
        "purpose": "Deterministic dependency-aware production task state machine.",
        "contract": CONTRACT_501,
        "executor": "executors/production_task_lifecycle.py",
        "tests": ["tests/unit/test_production_task_lifecycle.py"],
        "dependencies": ["COMPONENT_TASK_PACK"],
        "routing_keywords": ["approval", "queue", "review", "task"],
    },
    {
        "id": "PRODUCTION_TASK_REPOSITORY",
        "purpose": "Persistent revisioned task queues with optimistic concurrency.",
        "contract": CONTRACT_501,
        "executor": "executors/production_task_repository.py",
        "tests": ["tests/unit/test_production_task_repository.py"],
        "dependencies": ["PRODUCTION_TASK_LIFECYCLE"],
        "routing_keywords": ["persistence", "queue", "revision", "task"],
    },
    {
        "id": "SCENE_COMPONENT_SNAPSHOT",
        "purpose": "Compact deterministic Blender scene/component snapshots and structural diffs.",
        "contract": CONTRACT_501,
        "executor": "executors/scene_component_snapshot.py",
        "tests": ["tests/unit/test_scene_component_snapshot.py"],
        "dependencies": ["BLENDER_HARD_SURFACE_BUILDER"],
        "routing_keywords": ["diff", "scene", "snapshot", "scope"],
    },
    {
        "id": "PRODUCTION_ITERATION_GATE",
        "purpose": "Block stale or out-of-scope worker iterations before review.",
        "contract": CONTRACT_501,
        "executor": "executors/production_iteration_gate.py",
        "tests": ["tests/unit/test_production_iteration_gate.py"],
        "dependencies": ["PRODUCTION_TASK_LIFECYCLE", "SCENE_COMPONENT_SNAPSHOT"],
        "routing_keywords": ["gate", "mutation", "review", "validation"],
    },
    {
        "id": "ASSET_STUDIO_VIEW_MODEL",
        "purpose": "Compact production Studio UI model over canonical runtime records.",
        "contract": CONTRACT_501,
        "executor": "executors/asset_studio_view_model.py",
        "tests": ["tests/unit/test_asset_studio_view_model.py"],
        "dependencies": ["ASSET_STATE_RUNTIME", "PRODUCTION_TASK_LIFECYCLE", "SCENE_COMPONENT_SNAPSHOT", "DESIGN_SYSTEM_REPOSITORY"],
        "routing_keywords": ["asset", "gui", "inspector", "studio"],
    },
]

RELEASE_TESTS = [
    "tests/blender/test_hard_surface_builder.py",
    "tests/regression/test_benchmark_89.py",
    "tests/unit/test_assembly_anchor_gate.py",
    "tests/unit/test_asset_production_orchestrator.py",
    "tests/unit/test_asset_repository.py",
    "tests/unit/test_asset_state_runtime.py",
    "tests/unit/test_asset_studio_view_model.py",
    "tests/unit/test_component_task_pack.py",
    "tests/unit/test_design_binding_resolver.py",
    "tests/unit/test_design_system_repository.py",
    "tests/unit/test_hard_surface_recipe.py",
    "tests/unit/test_parameter_graph.py",
    "tests/unit/test_production_iteration_gate.py",
    "tests/unit/test_production_task_lifecycle.py",
    "tests/unit/test_production_task_repository.py",
    "tests/unit/test_scene_component_snapshot.py",
]


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


def promote_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["version"] = VERSION
    manifest["runtime_verification_version"] = VERSION
    manifest["benchmark"] = BENCHMARK_89

    for benchmark in (BENCHMARK_88, BENCHMARK_89):
        if benchmark not in manifest.setdefault("benchmarks", []):
            manifest["benchmarks"].append(benchmark)

    for module in (BENCHMARK_88, BENCHMARK_89, CONTRACT_500, CONTRACT_501):
        if module not in manifest.setdefault("modules", []):
            manifest["modules"].append(module)
    manifest["module_count"] = len(manifest["modules"])

    skill_by_id = {str(item.get("id")): item for item in manifest.setdefault("skills", [])}
    executor_by_id = {str(item.get("id")): item for item in manifest.setdefault("executors", [])}
    for entry in RUNTIME_ENTRIES:
        skill = {
            "id": entry["id"],
            "purpose": entry["purpose"],
            "contract": entry["contract"],
            "executor": entry["executor"],
            "maturity": "EXECUTOR_READY",
            "dependencies": entry["dependencies"],
            "benchmark": BENCHMARK_89,
            "routing_keywords": entry["routing_keywords"],
        }
        executor = {
            "id": entry["id"],
            "contract": entry["contract"],
            "executor": entry["executor"],
            "maturity": "EXECUTOR_READY",
            "tests": entry["tests"],
        }
        if entry["id"] in skill_by_id:
            skill_by_id[entry["id"]].clear()
            skill_by_id[entry["id"]].update(skill)
        else:
            manifest["skills"].append(skill)
            skill_by_id[entry["id"]] = skill
        if entry["id"] in executor_by_id:
            executor_by_id[entry["id"]].clear()
            executor_by_id[entry["id"]].update(executor)
        else:
            manifest["executors"].append(executor)
            executor_by_id[entry["id"]] = executor

    tests = manifest.setdefault("tests", [])
    for test in RELEASE_TESTS:
        if test not in tests:
            tests.append(test)

    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def promote_executor_versions() -> None:
    for entry in RUNTIME_ENTRIES:
        path = ROOT / entry["executor"]
        content = path.read_text(encoding="utf-8")
        content, count = re.subn(
            r'(?m)^EXECUTOR_VERSION\s*=\s*["\'][^"\']+["\']',
            f'EXECUTOR_VERSION = "{VERSION}"',
            content,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"EXECUTOR_VERSION_NOT_FOUND:{entry['executor']}")
        path.write_text(content, encoding="utf-8")


def promote_metadata() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pyproject, count = re.subn(r'(?m)^version\s*=\s*"[^"]+"', f'version = "{VERSION}"', pyproject, count=1)
    if count != 1:
        raise RuntimeError("PYPROJECT_VERSION_NOT_FOUND")
    write("pyproject.toml", pyproject)

    validator_path = ROOT / "tools/validate_release_metadata.py"
    validator = validator_path.read_text(encoding="utf-8")
    validator = validator.replace('TARGET_VERSION = "0.18.0"', f'TARGET_VERSION = "{VERSION}"')
    validator = validator.replace(
        'TARGET_BENCHMARK = "07_examples/87_LAFAR_RUNTIME_CAPABILITY_PROBE_V018_REGRESSION_BENCHMARK.md"',
        f'TARGET_BENCHMARK = "{BENCHMARK_89}"',
    )
    validator = validator.replace(r"\bv?0\.18\.0\b", r"\bv?0\.19\.0\b")
    validator = validator.replace(r"(?:^|\n)#+\s*(?:\[)?0\.18\.0", r"(?:^|\n)#+\s*(?:\[)?0\.19\.0")
    validator = validator.replace('if "0.18.0" not in system_prompt:', 'if "0.19.0" not in system_prompt:')
    validator_path.write_text(validator, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if VERSION not in readme:
        readme = f"> Current production runtime: v{VERSION} — persistent asset/design/task state and Production Studio.\n\n" + readme
    readme_path.write_text(readme, encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    if not re.search(r"(?:^|\n)#+\s*(?:\[)?0\.19\.0", changelog):
        release = """## 0.19.0 — Production Studio Runtime\n\n- Promoted persistent asset/component production state and relational parameter graph to release executors.\n- Added versioned design-system repository with reverse usage and impact reporting.\n- Added persistent dependency-aware production task queues and approval lifecycle.\n- Added compact scene/component snapshots, structural diffs and mutation-scope enforcement.\n- Routed component/feature reference evidence into token-bounded task packs.\n- Added Production Iteration Gate and standalone Asset Production Studio GUI.\n- Added canonical Benchmark 89 for the Lafar street-bench production workflow.\n\n"""
        changelog = release + changelog
    changelog_path.write_text(changelog, encoding="utf-8")

    system_path = ROOT / "06_prompts/60_SYSTEM_PROMPT.md"
    system_prompt = system_path.read_text(encoding="utf-8")
    if VERSION not in system_prompt:
        system_prompt += f"\n\nRuntime release: v{VERSION}. Component production MUST route through persistent asset state, scoped task packs and validation gates when applicable.\n"
    system_path.write_text(system_prompt, encoding="utf-8")


def main() -> None:
    promote_manifest()
    promote_executor_versions()
    promote_metadata()
    print(json.dumps({"status": "PASS", "version": VERSION, "executors": len(RUNTIME_ENTRIES)}))


if __name__ == "__main__":
    main()

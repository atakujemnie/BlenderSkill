from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.21.0"
BENCHMARK = "07_examples/91_LAFAR_SIDEWALK_FIDELITY_ENFORCEMENT_V021_REGRESSION_BENCHMARK.md"
CONTRACT = "15_asset_production/503_FIDELITY_ENFORCEMENT_AND_DETERMINISTIC_ASSEMBLY.md"


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "> Current production runtime: v0.20.0 — operational persistent Production Studio API and live GUI.",
        "> Current production runtime: v0.21.0 — fidelity enforcement, deterministic assembly and trusted validation.",
        1,
    )
    old = (
        "## Current release\n\n"
        "**v0.18.0 — Runtime Verification & Contract Convergence.**\n\n"
        "v0.13 adds a second authoring domain beside reference reconstruction: procedural organic/environment generation. "
        "The first benchmark target is a Lafar planter containing a reconstructed hard-surface container plus generated vegetation.\n\n\n"
    )
    new = (
        "## Current release\n\n"
        "**v0.21.0 — Fidelity Enforcement & Deterministic Assembly.**\n\n"
        "v0.21 closes the false-success path exposed by the blind Lafar sidewalk test. Canonical component placement now survives task compilation, "
        "representation contracts fail closed, geometry tasks cannot bypass persisted stage/build authorization, design-system MATERIAL bindings are "
        "materialized in Blender, and strict task approval requires trusted revision-bound validation receipts rather than worker self-certification. "
        "Task approval converges back to `component.state=ACCEPTED`.\n\n"
        "Canonical regression: **Benchmark 91 — Lafar Sidewalk Fidelity Enforcement v0.21**.\n\n"
        "## v0.21 Fidelity Enforcement & Deterministic Assembly\n\n"
        "```text\n"
        "persistent asset state\n"
        "-> canonical component transform + origin\n"
        "-> envelope / seam constraints\n"
        "-> execution authorization\n"
        "-> scoped task pack\n"
        "-> representation contract\n"
        "-> deterministic Blender execution + real material binding\n"
        "-> current scene snapshot\n"
        "-> trusted validation receipts\n"
        "-> APPROVED + component ACCEPTED\n"
        "```\n\n"
    )
    if old in text:
        text = text.replace(old, new, 1)
    elif "**v0.21.0 — Fidelity Enforcement & Deterministic Assembly.**" not in text:
        marker = "## Current release\n"
        text = text.replace(marker, marker + "\n**v0.21.0 — Fidelity Enforcement & Deterministic Assembly.**\n\nCanonical regression: **Benchmark 91**.\n", 1)
    path.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if text.startswith("## 0.21.0"):
        return
    entry = """## 0.21.0 — Fidelity Enforcement & Deterministic Assembly

- Added canonical component transforms/origin semantics so placement cannot disappear between asset state, task packs and Blender execution.
- Added asset-envelope and seam validation, including mathematical negative controls from the Lafar sidewalk blind test.
- Added representation-contract enforcement so tactile grids, slotted grates and recessed features cannot silently degrade to generic boxes.
- Added component execution authorization and blocked geometry tasks that request a stage ahead of persisted asset state.
- Added immutable trusted validation receipts bound to validator, asset revision, component and scene revision; worker self-certification no longer approves strict geometry tasks.
- Converged task approval back into persistent `component.state=ACCEPTED`.
- Added reference-evidence materialization into concrete local attachment descriptors while preserving component token budgets.
- Added Blender design-resource materialization so resolved MATERIAL bindings become real Blender material slots.
- Added immediate Blender view-layer refresh after deterministic mutations and a real Blender 5.1 proof for transform/origin/material behavior.
- Removed demo-specific Studio startup state and silent live-to-demo fallback.
- Added canonical Benchmark 91 — Lafar Sidewalk Fidelity Enforcement.

"""
    path.write_text(entry + text, encoding="utf-8")


def skill(skill_id: str, purpose: str, executor: str, tests: list[str], dependencies: list[str] | None = None) -> dict:
    return {
        "id": skill_id,
        "purpose": purpose,
        "contract": CONTRACT,
        "executor": executor,
        "maturity": "EXECUTOR_READY",
        "dependencies": dependencies or [],
        "benchmark": BENCHMARK,
        "routing_keywords": ["asset", "fidelity", "geometry", "v0.21"],
        "tests": tests,
    }


def update_manifest() -> None:
    path = ROOT / "MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["version"] = VERSION
    manifest["benchmark"] = BENCHMARK
    manifest["runtime_verification_version"] = VERSION
    benchmarks = list(manifest.get("benchmarks", []))
    if BENCHMARK not in benchmarks:
        benchmarks.append(BENCHMARK)
    manifest["benchmarks"] = benchmarks
    modules = list(manifest.get("modules", []))
    for module in (BENCHMARK, CONTRACT):
        if module not in modules:
            modules.append(module)
    manifest["modules"] = modules
    manifest["module_count"] = len(modules)

    additions = [
        skill("COMPONENT_TRANSFORM", "Normalize canonical component placement and coordinate-space provenance.", "executors/component_transform.py", ["tests/unit/test_component_transform.py"]),
        skill("ASSET_ENVELOPE_GATE", "Validate component extents and mathematical seam constraints against the asset envelope.", "executors/asset_envelope_gate.py", ["tests/unit/test_asset_envelope_gate.py", "tests/regression/test_benchmark_91.py"], ["COMPONENT_TRANSFORM", "PARAMETER_GRAPH"]),
        skill("REPRESENTATION_CONTRACT_GATE", "Reject recipes that cannot represent required physical component features.", "executors/representation_contract_gate.py", ["tests/unit/test_representation_contract_gate.py", "tests/regression/test_benchmark_91.py"], ["HARD_SURFACE_RECIPE"]),
        skill("COMPONENT_EXECUTION_GATE", "Authorize scoped recipes, preserve canonical placement and gate Blender mutation.", "executors/component_execution_gate.py", ["tests/unit/test_component_execution_gate.py", "tests/blender/test_v021_component_execution.py"], ["COMPONENT_TRANSFORM", "REPRESENTATION_CONTRACT_GATE", "BLENDER_HARD_SURFACE_BUILDER"]),
        skill("VALIDATION_RECEIPT_REPOSITORY", "Persist immutable trusted validator receipts bound to exact production revisions.", "executors/validation_receipt_repository.py", ["tests/unit/test_validation_receipt_repository.py", "tests/unit/test_v021_trusted_task_approval.py", "tests/regression/test_benchmark_91.py"]),
        skill("REFERENCE_EVIDENCE_MATERIALIZER", "Resolve scoped reference metadata into concrete local multimodal attachment descriptors.", "executors/reference_evidence_materializer.py", ["tests/unit/test_reference_evidence_materializer.py"]),
        skill("BLENDER_DESIGN_RESOURCE_ADAPTER", "Materialize resolved design-system MATERIAL bindings as real Blender materials.", "executors/blender_design_resource_adapter.py", ["tests/blender/test_v021_component_execution.py"], ["DESIGN_BINDING_RESOLVER"]),
    ]
    skills = list(manifest.get("skills", []))
    by_id = {str(item.get("id")): index for index, item in enumerate(skills) if isinstance(item, dict)}
    for item in additions:
        existing = by_id.get(item["id"])
        if existing is None:
            skills.append(item)
            by_id[item["id"]] = len(skills) - 1
        else:
            skills[existing] = item
    for item in skills:
        if not isinstance(item, dict):
            continue
        if item.get("id") == "PRODUCTION_STUDIO_SERVICE":
            item["contract"] = CONTRACT
            item["benchmark"] = BENCHMARK
            tests = list(item.get("tests", []))
            for test in ("tests/integration/test_v021_studio_http.py", "tests/regression/test_benchmark_91.py"):
                if test not in tests:
                    tests.append(test)
            item["tests"] = tests
        if item.get("id") == "COMPONENT_TASK_PACK":
            item["contract"] = CONTRACT
            item["benchmark"] = BENCHMARK
        if item.get("id") == "BLENDER_HARD_SURFACE_BUILDER":
            item["contract"] = CONTRACT
            item["benchmark"] = BENCHMARK
            tests = list(item.get("tests", []))
            if "tests/blender/test_v021_component_execution.py" not in tests:
                tests.append("tests/blender/test_v021_component_execution.py")
            item["tests"] = tests
        if item.get("id") == "PRODUCTION_TASK_LIFECYCLE":
            item["contract"] = CONTRACT
            item["benchmark"] = BENCHMARK
            tests = list(item.get("tests", []))
            if "tests/unit/test_v021_trusted_task_approval.py" not in tests:
                tests.append("tests/unit/test_v021_trusted_task_approval.py")
            item["tests"] = tests
    manifest["skills"] = skills

    tests = list(manifest.get("tests", []))
    for test in (
        "tests/blender/test_v021_component_execution.py",
        "tests/integration/test_v021_studio_http.py",
        "tests/regression/test_benchmark_91.py",
        "tests/unit/test_asset_envelope_gate.py",
        "tests/unit/test_component_execution_gate.py",
        "tests/unit/test_component_transform.py",
        "tests/unit/test_reference_evidence_materializer.py",
        "tests/unit/test_representation_contract_gate.py",
        "tests/unit/test_v021_trusted_task_approval.py",
        "tests/unit/test_validation_receipt_repository.py",
    ):
        if test not in tests:
            tests.append(test)
    manifest["tests"] = tests
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    update_readme()
    update_changelog()
    update_manifest()
    print(json.dumps({"status": "PASS", "version": VERSION, "benchmark": BENCHMARK}))


if __name__ == "__main__":
    main()

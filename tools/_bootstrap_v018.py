from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"

VERSION = "0.18.0"
BENCHMARK = "07_examples/87_LAFAR_RUNTIME_CAPABILITY_PROBE_V018_REGRESSION_BENCHMARK.md"
NEW_MODULES = [
    "00_governance/15_RUNTIME_VERIFICATION_EXTENSION_V018.md",
    "00_governance/16_RUNTIME_VERIFICATION_SKILL_REGISTRY_V018.md",
    "05_execution/80_CONTRACT_EXECUTOR_TEST_PARITY_GATE.md",
    "05_execution/81_REAL_BLENDER_RUNTIME_VALIDATION.md",
    "06_prompts/73_RUNTIME_VERIFICATION_PROMPT.md",
    "07_examples/87_LAFAR_RUNTIME_CAPABILITY_PROBE_V018_REGRESSION_BENCHMARK.md",
    "12_procedural_generation/237_PROVIDER_STATE_PROTOCOL.md",
    "12_procedural_generation/238_CANONICAL_PROVIDER_REGISTRY.md",
    "12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md",
    "12_procedural_generation/240_PROVIDER_CAPABILITY_PROBE_EXECUTION.md",
    "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md",
]

EXECUTORS = [
    ("PROVIDER_STATE_PROTOCOL", "12_procedural_generation/237_PROVIDER_STATE_PROTOCOL.md", "executors/provider_contracts.py", ["tests/unit/test_provider_contracts.py"]),
    ("CANONICAL_PROVIDER_REGISTRY", "12_procedural_generation/238_CANONICAL_PROVIDER_REGISTRY.md", "executors/provider_registry.py", ["tests/unit/test_provider_registry.py"]),
    ("BLENDER_RUNTIME_ADDON_DISCOVERY", "12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md", "executors/blender_addon_inventory.py", ["tests/unit/test_provider_discovery.py", "tests/blender/test_runtime_discovery.py"]),
    ("INSTALLED_PROVIDER_DISCOVERY", "12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md", "executors/installed_provider_inventory.py", ["tests/unit/test_provider_classification.py", "tests/integration/test_v017_fixture_compatibility.py"]),
    ("EXPECTED_PROVIDER_GATE", "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md", "executors/expected_provider_gate.py", ["tests/unit/test_expected_provider_gate.py"]),
    ("PROCEDURAL_GENERATOR_PROVIDER", "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md", "executors/procedural_provider.py", ["tests/unit/test_provider_selection.py"]),
    ("PROVIDER_CAPABILITY_PROBE", "12_procedural_generation/240_PROVIDER_CAPABILITY_PROBE_EXECUTION.md", "executors/provider_probe_runner.py", ["tests/blender/test_geometry_nodes_probe.py", "tests/blender/test_probe_cleanup.py"]),
    ("PROVIDER_QUALITY_SELECT", "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md", "executors/provider_quality.py", ["tests/unit/test_provider_quality.py"]),
    ("PROVIDER_SELECTION_REPORT", "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md", "executors/provider_selection_report.py", ["tests/unit/test_provider_report.py"]),
    ("PROVIDER_DECISION_PIPELINE", "12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md", "executors/provider_orchestrator.py", ["tests/integration/test_provider_pipeline.py"]),
]

ALL_TESTS = sorted({test for _, _, _, tests in EXECUTORS for test in tests} | {
    "tests/unit/test_version_constraints.py",
    "tests/unit/test_registry_parity.py",
    "tests/blender/run_suite.py",
})


def update_manifest() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["manifest_schema_version"] = 2
    manifest["version"] = VERSION
    manifest["benchmark"] = BENCHMARK
    benchmarks = list(manifest.get("benchmarks") or [])
    if BENCHMARK not in benchmarks:
        benchmarks.append(BENCHMARK)
    manifest["benchmarks"] = benchmarks
    modules = list(manifest.get("modules") or [])
    for module in NEW_MODULES:
        if module not in modules:
            modules.append(module)
    manifest["modules"] = modules
    manifest["module_count"] = len(modules)

    manifest["skills"] = [
        {
            "id": skill_id,
            "purpose": {
                "PROVIDER_STATE_PROTOCOL": "Canonical provider evidence state vocabulary and normalization.",
                "CANONICAL_PROVIDER_REGISTRY": "Canonical static provider identity/classification registry.",
                "BLENDER_RUNTIME_ADDON_DISCOVERY": "Read-only discovery from the active Blender runtime.",
                "INSTALLED_PROVIDER_DISCOVERY": "Normalize runtime discovery into canonical provider records.",
                "EXPECTED_PROVIDER_GATE": "Verify expected provider presence and version constraints.",
                "PROCEDURAL_GENERATOR_PROVIDER": "Evaluate provider runtime compatibility and probe evidence.",
                "PROVIDER_CAPABILITY_PROBE": "Run isolated explicit provider capability probes.",
                "PROVIDER_QUALITY_SELECT": "Evaluate provider quality tier for usage class.",
                "PROVIDER_SELECTION_REPORT": "Preserve auditable provider selection evidence.",
                "PROVIDER_DECISION_PIPELINE": "Canonical discovery-to-selection provider pipeline.",
            }[skill_id],
            "contract": contract,
            "executor": executor,
            "maturity": "EXECUTOR_READY",
            "dependencies": [],
            "benchmark": BENCHMARK,
            "routing_keywords": sorted({"provider", "runtime", "blender", skill_id.lower()}),
        }
        for skill_id, contract, executor, _ in EXECUTORS
    ]
    manifest["executors"] = [
        {"id": skill_id, "contract": contract, "executor": executor, "maturity": "EXECUTOR_READY", "tests": tests}
        for skill_id, contract, executor, tests in EXECUTORS
    ]
    manifest["tests"] = ALL_TESTS
    manifest["generated_artifacts"] = [
        {"path": "_FULL_LIBRARY.md", "builder": "tools/build_full_library.py"},
        {"path": "_RUNTIME_INDEX.json", "builder": "tools/build_runtime_index.py", "max_bytes": 153600},
    ]
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    old = "**v0.17.0 — runtime provider discovery, capability inventory and selection transparency.**"
    new = "**v0.18.0 — Runtime Verification & Contract Convergence.**"
    if old in text:
        text = text.replace(old, new, 1)
    marker = "## v0.17 runtime provider discovery and selection transparency"
    section = """## v0.18 Runtime Verification & Contract Convergence\n\nv0.18 moves BlenderSkill from documented provider behavior to executable runtime evidence. Provider states and metadata are canonicalized, discovery is non-executing, capability probes are explicit and cleanup-verified, version constraints replace exact-only gating, and provider selection preserves discovery/probe/domain/compatibility/license/quality evidence independently.\n\nNormal CI is read-only. A separate pinned Blender 5.1.x workflow proves runtime discovery and a real Geometry Nodes evaluation. `MANIFEST.json` uses schema v2, `_RUNTIME_INDEX.json` is the compact routing entry point, and release tagging is isolated to the manual release workflow.\n\nCanonical regression: **Benchmark 87 — Lafar Runtime Capability Probe v0.18**.\n\n"""
    if "## v0.18 Runtime Verification & Contract Convergence" not in text and marker in text:
        text = text.replace(marker, section + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if "## 0.18.0" in text:
        return
    section = """## 0.18.0\n\nv0.18.0 is the **Runtime Verification & Contract Convergence** release.\n\nKey changes:\n- introduced one canonical provider state protocol and one canonical JSON provider registry;\n- removed duplicate provider metadata from active executors and retained the old catalog only as a registry-backed compatibility facade;\n- made Blender add-on discovery non-executing and preserved unknown providers as `UNKNOWN`;\n- added explicit capability-probe adapters and real cleanup validation;\n- changed Geometry Nodes discovery from implied PASS to `PROBE_REQUIRED` until a real Blender probe succeeds;\n- added dependency-free provider version constraints and a complete auditable decision pipeline;\n- added contract/executor/test parity validation, pytest/ruff structure and v0.17 compatibility fixtures;\n- introduced `MANIFEST` schema v2 and deterministic `_RUNTIME_INDEX.json`;\n- consolidated active Router/Registry/System Prompt semantics instead of stacking historical overrides;\n- split read-only normal CI, pinned Blender runtime CI and the only write-enabled release workflow;\n- removed the v0.17 metadata-upgrade chain from active CI/release;\n- added Benchmark 87 and real Blender runtime discovery/Geometry Nodes/cleanup tests.\n\nCanonical benchmark: **87 — Lafar Runtime Capability Probe v0.18 Regression**.\n\n"""
    text = text.replace("# Changelog\n\n", "# Changelog\n\n" + section, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update_manifest()
    update_readme()
    update_changelog()
    from tools.build_full_library import main as build_full_library
    from tools.build_runtime_index import main as build_runtime_index

    build_full_library()
    build_runtime_index()


if __name__ == "__main__":
    main()

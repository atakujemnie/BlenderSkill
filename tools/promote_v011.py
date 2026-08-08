from __future__ import annotations

"""Idempotently promote canonical repository metadata to BlenderSkill v0.11.0."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.11.0"
BENCHMARK = "07_examples/80_LAFAR_STREET_LAMP_V010_EXECUTION_DETAIL_REGRESSION_BENCHMARK.md"
NEW_MODULES = [
    "05_execution/73_EXECUTION_AUTHORIZATION_GATE.md",
    "05_execution/74_PERSISTENT_NODE_STATE_AND_CHECKPOINTS.md",
    "05_execution/75_NODE_SCOPED_ORCHESTRATION.md",
    "07_examples/80_LAFAR_STREET_LAMP_V010_EXECUTION_DETAIL_REGRESSION_BENCHMARK.md",
    "08_scripts/97_EXECUTION_AUTHORIZATION_STATE_PATTERN.md",
    "08_scripts/98_REFERENCE_CONFLICT_ARBITRATION_PATTERN.md",
    "10_reconstruction/184_REFERENCE_CONFLICT_ARBITRATION.md",
    "10_reconstruction/185_PER_VIEW_EVIDENCE_AND_DERIVED_PARAMETER_PROVENANCE.md",
    "10_reconstruction/186_APPEARANCE_OWNER_COVERAGE_AND_REPORT_NAMESPACES.md",
    "10_reconstruction/187_RDL_DIAGNOSTIC_GEOMETRY_AND_NEUTRAL_SHADING.md",
    "10_reconstruction/188_CANONICAL_SKILL_RUNTIME_PINNING_AND_ANALYSIS_REUSE.md",
    "11_playbooks/119_CIVIC_STREET_LAMP.md",
]

manifest_path = ROOT / "MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["version"] = VERSION
manifest["benchmark"] = BENCHMARK
manifest.setdefault("benchmarks", [])
if BENCHMARK not in manifest["benchmarks"]:
    manifest["benchmarks"].append(BENCHMARK)
manifest.setdefault("modules", [])
for module in NEW_MODULES:
    if module not in manifest["modules"]:
        manifest["modules"].append(module)
manifest["module_count"] = len(manifest["modules"])
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

release_block = """## Current release

**v0.11.0 — enforced reconstruction execution, conflict arbitration and detail closure.**

v0.11 is driven by the Lafar Street Lamp v0.10 benchmark. v0.10 produced the strongest reconstruction so far, but exposed that the state machine was still advisory: `ready_nodes=[]` did not prevent a monolithic RDL0→RDL5 builder, `BUILT_UNVERIFIED` did not stop dependent geometry, and a local SIDE/detail conflict could be resolved too literally.

Canonical v0.11 execution:

```text
eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> build exactly one node
-> persist BUILT_UNVERIFIED
-> source-anchored per-view QA
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> only ACCEPTED unlocks dependants
```

v0.11 also adds persistent node/checkpoint state, per-property conflict arbitration, per-view evidence contracts, derived-parameter provenance, Appearance Owner Coverage, neutral diagnostic RDL geometry, canonical runtime pinning and benchmark 80 for the Lafar Street Lamp.

Runtime remains downstream of `APPEARANCE_FIDELITY_GATE` and `RECON_FIDELITY_GATE`.

"""
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
start = readme.index("## Current release")
markers = [m for m in ("## Core v0.11 concepts", "## Core v0.10 concepts") if m in readme]
if not markers:
    raise RuntimeError("README core concepts marker not found")
marker = min(markers, key=readme.index)
end = readme.index(marker)
tail = readme[end:]
if tail.startswith("## Core v0.10 concepts"):
    tail = tail.replace("## Core v0.10 concepts", "## Core v0.11 concepts", 1)
readme_path.write_text(readme[:start] + release_block + tail, encoding="utf-8")

changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
if "## 0.11.0" not in changelog:
    block = """## 0.11.0

v0.11.0 is the **enforced reconstruction execution + reference-conflict closure** release, driven by the Lafar Street Lamp v0.10 benchmark.

Key changes:
- canonical `EXECUTION_AUTHORIZATION_GATE`: no READY_TO_BUILD + authorization, no production mutation;
- persistent node/checkpoint state and BUILT_UNVERIFIED hard barrier;
- node-scoped orchestration instead of monolithic multi-RDL builders;
- per-property `REFERENCE_CONFLICT_RESOLVER`, including equal-authority BLOCKED behavior;
- per-view ORTHO/HERO/DETAIL evidence contracts and derived-parameter provenance;
- `APPEARANCE_OWNER_COVERAGE` and separate Shape/Appearance/Evidence namespaces;
- RDL0 diagnostic geometry and neutral RDL0–RDL3 form QA;
- canonical BlenderSkill version/commit/single-root runtime pinning;
- benchmark 80 and civic street-lamp playbook;
- v0.9, v0.10 and v0.11 regression tests retained in CI.

Canonical manifest version: **0.11.0**. Canonical module count: **234**. Canonical benchmark: **80 — Lafar Street Lamp v0.10 Execution and Detail Regression**.

"""
    changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + block, 1)
    changelog_path.write_text(changelog, encoding="utf-8")

print(f"Promoted repository metadata to v{VERSION}; modules={manifest['module_count']}")

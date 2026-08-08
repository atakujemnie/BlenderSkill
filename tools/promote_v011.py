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
benchmarks = list(manifest.get("benchmarks", []))
if BENCHMARK not in benchmarks:
    benchmarks.append(BENCHMARK)
manifest["benchmarks"] = benchmarks
modules = list(manifest.get("modules", []))
for path in NEW_MODULES:
    if path not in modules:
        modules.append(path)
manifest["modules"] = modules
manifest["module_count"] = len(modules)
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
start = readme.index("## Current release")
end_marker = "## Core v0.10 concepts"
end = readme.index(end_marker)
release_block = """## Current release

**v0.11.0 — enforced reconstruction execution, conflict arbitration and detail closure.**

v0.11 is driven by the Lafar Street Lamp v0.10 benchmark. v0.10 produced the strongest reconstruction so far, but the run exposed that the state machine was still advisory: `ready_nodes=[]` did not prevent a monolithic RDL0→RDL5 builder, `BUILT_UNVERIFIED` did not stop dependent geometry, and a local SIDE/detail conflict could be resolved too literally.

The v0.11 invariant is executable:

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

Additional v0.11 closure:
- persistent node/checkpoint state;
- per-property `REFERENCE_CONFLICT_RESOLVER`;
- per-view evidence contracts for ortho / hero / detail;
- source provenance for significant derived parameters;
- `APPEARANCE_OWNER_COVERAGE` with separate Shape/Appearance/Evidence namespaces;
- RDL0 diagnostic geometry and neutral RDL0–RDL3 shading;
- canonical BlenderSkill version/commit/source-root pinning;
- benchmark 80 for the Lafar Street Lamp.

Runtime remains downstream of `APPEARANCE_FIDELITY_GATE` and `RECON_FIDELITY_GATE`.

"""
readme = readme[:start] + release_block + readme[end:].replace("## Core v0.10 concepts", "## Core v0.11 concepts", 1)
readme_path.write_text(readme, encoding="utf-8")

changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
if "## 0.11.0" not in changelog:
    block = """## 0.11.0

v0.11.0 is the **enforced reconstruction execution + reference-conflict closure** release, driven by the Lafar Street Lamp v0.10 benchmark.

The lamp was the best reconstruction so far (human assessment about 7.5/10), proving that v0.10 improved form and appearance understanding. It also exposed the next gap: the agent could still organize code node-by-node while executing the whole RDL0→RDL5 asset in one monolithic run, despite `ready_nodes=[]` and without acceptance between nodes.

### Hard execution authorization
- added `05_execution/73_EXECUTION_AUTHORIZATION_GATE.md` and `executors/execution_authorization_gate.py`;
- `CONSTRAINED` is eligibility, not permission to build;
- production mutation requires persisted `READY_TO_BUILD` plus canonical authorization;
- parent/dependency acceptance and previous RDL barriers are rechecked immediately before mutation.

### Persistent node state
- added `05_execution/74_PERSISTENT_NODE_STATE_AND_CHECKPOINTS.md` and `executors/node_state_store.py`;
- `BUILT_UNVERIFIED` is a hard branch stop;
- only `RECONSTRUCTION_NODE_GATE` can transition a built node to `ACCEPTED`;
- checkpoints separate `shape_nodes`, `appearance_owners`, `evidence` and `conflicts`.

### Node-scoped orchestration
- added `05_execution/75_NODE_SCOPED_ORCHESTRATION.md`;
- code organization into `node_*()` functions no longer counts as node-by-node execution;
- deterministic replay is allowed, but cannot mint new acceptance evidence.

### Conflict arbitration and per-view proof
- added `184_REFERENCE_CONFLICT_ARBITRATION.md` and `executors/reference_conflict_resolver.py`;
- added `185_PER_VIEW_EVIDENCE_AND_DERIVED_PARAMETER_PROVENANCE.md`;
- explicit dimensions own named dimensions, not unrelated local form;
- detail/hero/ortho evidence uses different proof modes;
- equal-authority contradictory interpretations remain BLOCKED instead of being averaged or silently selected.

### Appearance-owner closure
- added `186_APPEARANCE_OWNER_COVERAGE_AND_REPORT_NAMESPACES.md` and `executors/appearance_owner_coverage.py`;
- `APPEARANCE_FIDELITY_GATE` v0.2 requires canonical MUST-owner inventory closure for strict L4/L5;
- missing or unverified MUST owners block appearance acceptance.

### Diagnostic form before finish
- added `187_RDL_DIAGNOSTIC_GEOMETRY_AND_NEUTRAL_SHADING.md`;
- RDL0 must create falsifiable grey diagnostic geometry;
- RDL0–RDL3 source-fit QA defaults to neutral diagnostic shading;
- production material response belongs to RDL5.

### Runtime source integrity and reuse
- added `188_CANONICAL_SKILL_RUNTIME_PINNING_AND_ANALYSIS_REUSE.md` and `executors/runtime_source_pin.py`;
- benchmark runs require version/commit/source-root pinning and one active executor root;
- repeated one-off analysis helpers trigger canonical executor reuse/migration review.

### Benchmark and playbook
- added benchmark `80_LAFAR_STREET_LAMP_V010_EXECUTION_DETAIL_REGRESSION_BENCHMARK.md`;
- added `119_CIVIC_STREET_LAMP.md`;
- regression target: human reference fidelity >= 8.5/10, zero unauthorized mutations, zero children built on unaccepted hosts, zero missing MUST appearance owners.

### Tests
- added `tools/test_v011_execution_enforcement.py`;
- v0.9 and v0.10 regression suites remain active and were updated for the stricter v0.11 contracts.

Canonical manifest version: **0.11.0**.
Canonical module count: **234**.
Canonical benchmark: **80 — Lafar Street Lamp v0.10 Execution and Detail Regression**.

"""
    changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + block, 1)
    changelog_path.write_text(changelog, encoding="utf-8")

print(f"Promoted repository metadata to v{VERSION}; modules={manifest['module_count']}")

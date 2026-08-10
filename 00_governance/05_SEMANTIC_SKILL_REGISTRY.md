# Semantic Skill Registry

Version: 0.18.0
Status: CURRENT CONTRACT

This file is the active semantic registry entry point. Historical version-specific override tables are not stacked here. Domain details remain in their current layer indexes and contracts; historical behavior remains in Git history, CHANGELOG and regression benchmarks.

## Runtime verification skills

| Skill ID | Contract | Executor | Maturity |
|---|---|---|---|
| BLENDER_RUNTIME_ADDON_DISCOVERY | `12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md` | `executors/blender_addon_inventory.py` | EXECUTOR_READY |
| INSTALLED_PROVIDER_DISCOVERY | `12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md` | `executors/installed_provider_inventory.py` | EXECUTOR_READY |
| EXPECTED_PROVIDER_GATE | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/expected_provider_gate.py` | EXECUTOR_READY |
| PROCEDURAL_GENERATOR_PROVIDER | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/procedural_provider.py` | EXECUTOR_READY |
| PROVIDER_CAPABILITY_PROBE | `12_procedural_generation/240_PROVIDER_CAPABILITY_PROBE_EXECUTION.md` | `executors/provider_probe_runner.py` | EXECUTOR_READY |
| PROVIDER_QUALITY_SELECT | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_quality.py` | EXECUTOR_READY |
| PROVIDER_SELECTION_REPORT | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_selection_report.py` | EXECUTOR_READY |
| PROVIDER_DECISION_PIPELINE | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_orchestrator.py` | EXECUTOR_READY |

The detailed v0.18 runtime registry is `00_governance/16_RUNTIME_VERIFICATION_SKILL_REGISTRY_V018.md`.

## Reconstruction domain

Reconstruction skills are routed from `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` and the current Knowledge Router. Core semantic families include reference ingestion/measurement, Shape Graph, representation selection, node execution authorization, mutation postconditions, assembly integrity, registered visual/numeric evidence, RDL barriers, geometric integrity, appearance fidelity and final reconstruction fidelity.

## Game-ready domain

Game-ready skills remain under `04_game_ready/`, `08_scripts/`, `09_engine/` and current execution contracts. Runtime finishing is permitted only after upstream geometry/appearance/reconstruction gates required by the task have passed.

## Location design-system domain

Location/faction/family identity resolves through the `14_design_system/` layer. Stable canonical IDs, shared materials, branding and inherited design language are reused rather than regenerated per asset.

## Procedural and vegetation domain

Procedural provider identity is owned by `data/provider_registry.json`; runtime suitability is owned by the v0.18 discovery/probe/decision pipeline. Composition and visual-quality gates under `12_procedural_generation/` remain separate from provider capability.

## Maturity rule

`EXECUTOR_READY` is an executable claim, not a documentation label. It requires contract/executor/test parity validated by `tools/validate_registry_parity.py`. `CONTRACT_READY` means the contract may be routed but executable enforcement is not yet release-authoritative.

## Runtime index

Agents should enter the registry through `_RUNTIME_INDEX.json`, select the minimal matching contracts, then load detailed modules. `_FULL_LIBRARY.md` is not the default routing surface.

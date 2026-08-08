# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.5.0** — benchmark-driven agent execution, game-ready completion and runtime handoff.

The release baseline is the real Lafar Civic Bollard reconstruction benchmark, used to improve both output quality and execution efficiency.

## Purpose

The repository contains modular Markdown skills plus reusable Python executor candidates for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical knowledge source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from the modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — agent rules, routing, task packs, completion levels and state machines
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — `bpy`, BMesh, context, automation strategy and Blender 5.1 runtime compatibility
- `03_modeling` — hard-surface, topology, UV, trim sheets, floating details and authoring workflows
- `04_game_ready` — runtime optimization, materials, LOD, bake gate, emissive handoff and export constraints
- `05_execution` — execution, validation, QA, regression, repair and completeness reporting
- `06_prompts` — planner/reviewer/repair prompts and system prompt
- `07_examples` — examples and real benchmarks
- `08_scripts` — reusable audit/validation patterns
- `09_engine` — engine profile, project pipeline and asset-catalog integration contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executor candidates
- `99_sources` — technical sources

## v0.5 completion model

The agent must distinguish:

```text
RECONSTRUCTION_COMPLETE
-> MODELING_COMPLETE
-> GAME_READY_COMPLETE
-> PIPELINE_INTEGRATED
```

A good Blender render or successful mesh export is not automatically a complete game asset.

`GAME_READY_COMPLETE` requires runtime material/bake closure, LOD/collision/export validation and an Engine Profile when engine-specific behavior must be proven.

`PIPELINE_INTEGRATED` additionally requires actual project catalog/import registration when the project uses one.

## Semantic execution

Before generating ad-hoc Blender Python, the agent checks `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`.

Current reusable candidate executors include:
- reference measurement;
- axisymmetric profile/revolve geometry;
- radial repeat/annulus validation;
- topology-intent mesh validation;
- Blender runtime compatibility discovery;
- non-destructive QA scene isolation;
- completion-level evaluation.

Candidates stay `CONTRACT_READY` until real runtime benchmarks prove them `EXECUTOR_READY`.

## Efficiency policy

The agent should not transport raw data or unchanged code through LLM context unnecessarily.

Core patterns:

```text
compute locally -> aggregate -> decision-grade summary
```

and:

```text
plan -> write code artifact -> execute -> compact result -> targeted patch
```

Generated 300–600 line build scripts belong on disk, not repeatedly in the model context.

## Surface/runtime policy

v0.5 separates:
- geometry/reference fidelity;
- Blender material lookdev;
- runtime texture/bake state;
- emissive authoring;
- engine bloom/exposure/tone mapping;
- project asset registration.

Maintained civic materials should be subtly varied rather than perfectly sterile or covered in generic grunge.

## Benchmarks

Canonical benchmarks include:
- Lafar Street Bench reconstruction;
- Lafar Civic Bollard end-to-end game-asset benchmark.

The Bollard baseline recorded approximately 60k tokens and a 9/10 human visual assessment. v0.5 targets at least 35% token reduction on an equivalent run without quality/runtime regression.

## Repository rules

1. Prefer updating an existing canonical module over creating a parallel skill with duplicated responsibility.
2. Add a new skill only when it introduces a distinct responsibility or reusable primitive.
3. Keep semantic intent separate from temporary Blender indices, UI state and one-off operator sequences.
4. Validate changes against existing modules before merging them into the library.
5. `MANIFEST.json` defines the modules compiled into `_FULL_LIBRARY.md`.
6. GitHub Actions regenerates `_FULL_LIBRARY.md` after canonical Markdown changes.
7. A candidate executor is not promoted to `EXECUTOR_READY` without runtime evidence.
8. A library release should improve benchmark quality or reduce cost at equal quality — more documentation alone is not progress.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- evidence-driven reconstruction
- game-ready hard-surface production
- glTF/GLB as a neutral runtime baseline unless an Engine Profile overrides it

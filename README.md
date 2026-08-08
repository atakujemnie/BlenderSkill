# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.6.0** — deterministic bake/runtime closure, stable UV/LOD contracts and incremental execution.

v0.6 is based on the second real Lafar Civic Bollard production run. v0.5 already improved reconstruction and decision quality, but the continuation still consumed roughly 36k tokens while the agent repeatedly debugged bake/UV/export infrastructure. v0.6 turns those discovered rules into reusable contracts and executor candidates.

## Purpose

The repository contains modular Markdown skills plus reusable Python executors/candidates for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical knowledge source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from the modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — agent rules, routing, task packs, completion levels and state machines
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — `bpy`, BMesh, context, automation strategy and Blender 5.1 runtime compatibility
- `03_modeling` — hard-surface, topology, UV, trim sheets, floating details and authoring workflows
- `04_game_ready` — runtime optimization, material closure, deterministic bake, UV/LOD contracts, emissive handoff and export constraints
- `05_execution` — execution, validation, QA, incremental dirty-stage cache, long-running jobs, regression and completeness reporting
- `06_prompts` — planner/reviewer/repair prompts and system prompt
- `07_examples` — examples and real benchmarks
- `08_scripts` — reusable audit/validation/import-safety patterns
- `09_engine` — engine profile, runtime packaging, project pipeline and asset-catalog integration contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executors/candidates
- `99_sources` — technical sources

## Completion model

The agent distinguishes:

```text
RECONSTRUCTION_COMPLETE
-> MODELING_COMPLETE
-> GAME_READY_COMPLETE
-> PIPELINE_INTEGRATED
```

A good Blender render or successful mesh export is not automatically a complete game asset.

`GAME_READY_COMPLETE` requires runtime material/bake closure, LOD/collision/export validation and an Engine Profile when engine-specific behavior must be proven.

`PIPELINE_INTEGRATED` additionally requires actual project catalog/import registration when the project uses one.

## v0.6 bake/runtime model

The game-ready surface pipeline is now explicit:

```text
UV_CONTRACT
-> DIRTY_GRAPH
-> BAKE DIRTY CHANNELS ONLY
-> BAKE_VALIDATE
-> RUNTIME MATERIAL BIND
-> PACKAGE EXPORT
-> PACKAGE READBACK
-> BAKED-RUNTIME QA
-> COMPLETION GATE
```

Key rules:
- `bpy.ops.object.bake()` must return `FINISHED`; `CANCELLED` is FAIL even without a Python exception;
- every contributing material must have the correct selected+active image target;
- BaseColor, Metallic and Emissive use explicit authored-channel semantics rather than blindly relying on render passes;
- AO/ray-dependent baking isolates unrelated render-visible scene objects;
- bake source and consuming LODs share a stable semantic `UV_CONTRACT_ID`;
- `.001/.002` Blender name suffixes are never canonical part identity;
- decals/dynamic displays with foreign UV spaces remain separate from structural bake atlases;
- local channel repairs do not force full accepted-channel rebakes;
- tool timeout does not automatically mean the long-running Blender job failed;
- exported runtime material/texture/node structure is read back and validated;
- final visual QA uses the baked runtime material on a runtime LOD mesh, not only the procedural authoring shader.

## Semantic execution

Before generating ad-hoc Blender Python, the agent checks `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`.

Current reusable executors/candidates include:
- reference measurement;
- axisymmetric profile/revolve geometry;
- radial repeat/annulus validation;
- topology-intent mesh validation;
- Blender runtime compatibility discovery;
- non-destructive QA scene isolation;
- completion-level evaluation;
- semantic UV atlas ownership/remapping;
- deterministic multi-material bake target/channel helpers;
- semantic baked-image validation;
- glTF package node/material/image readback.

`MESH_VALIDATE` is the first packaged executor promoted to `EXECUTOR_READY` after successful use in Blender 5.1 during the Bollard continuation benchmark. Other new v0.6 bake/UV/package executors remain `CONTRACT_READY` until the next real run validates them end-to-end.

## Efficiency policy

The agent should not transport raw data or unchanged code through LLM context unnecessarily.

Core patterns:

```text
compute locally -> aggregate -> decision-grade summary
```

```text
plan -> write code artifact -> execute -> compact result -> targeted patch
```

and for expensive runtime closure:

```text
accepted artifact + unchanged dependencies -> REUSE
changed dependency -> dirty affected artifacts only
```

Generated build/bake/export scripts belong on disk, not repeatedly in model context.

## Surface/runtime policy

The library separates:
- geometry/reference fidelity;
- Blender material lookdev;
- runtime texture/bake state;
- emissive authoring;
- engine bloom/exposure/tone mapping;
- runtime module packaging;
- project asset registration.

Maintained civic materials should be subtly varied rather than perfectly sterile or covered in generic grunge.

## Benchmarks

Canonical benchmarks include:
- Lafar Street Bench reconstruction;
- Lafar Civic Bollard end-to-end reconstruction/game-asset benchmark;
- Lafar Civic Bollard bake/runtime regression benchmark.

The first Bollard run recorded approximately 60k tokens with a 9/10 human visual assessment. The later v0.5 game-ready continuation had already consumed about 36k tokens at the captured point while still debugging bake/runtime closure. The v0.6 stage benchmark targets a standard accepted hard-surface prop game-ready finish in roughly <=15k operational tokens where asset complexity permits, with no repeated discovery of solved bake/UV/export infrastructure.

## Repository rules

1. Prefer updating an existing canonical module over creating a parallel skill with duplicated responsibility.
2. Add a new skill only when it introduces a distinct responsibility or reusable primitive.
3. Keep semantic intent separate from temporary Blender indices, UI state and one-off operator sequences.
4. Validate changes against existing modules before merging them into the library.
5. `MANIFEST.json` defines the modules compiled into `_FULL_LIBRARY.md`.
6. GitHub Actions regenerates `_FULL_LIBRARY.md` after canonical Markdown changes.
7. A candidate executor is not promoted to `EXECUTOR_READY` without runtime evidence.
8. A library release should improve benchmark quality or reduce cost at equal quality — more documentation alone is not progress.
9. Project-specific packaging facts should be persisted in Engine/Project profiles instead of rediscovered from sibling asset scripts.
10. A local bake/export repair should not invalidate unrelated accepted artifacts without a dependency reason.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- evidence-driven reconstruction
- game-ready hard-surface production
- deterministic procedural-to-runtime material closure
- glTF/GLB as a neutral runtime baseline unless an Engine Profile overrides it

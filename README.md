# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.7.0** — runtime-proof integrity, cache coherence, canonical project paths and executable stage reuse.

v0.7 is based on the final continuation of the real Lafar Civic Bollard pipeline test. After the earlier captured ~36k-token game-ready continuation, another ~45k tokens were consumed closing runtime integration, for roughly ~81k post-v0.5 continuation tokens. The final asset was correct and reached `PIPELINE_INTEGRATED`, but the run exposed a new bottleneck: the agent was spending context proving infrastructure that should already be encoded in the project profile and execution layer.

## Purpose

The repository contains modular Markdown skills plus reusable Python executors/candidates for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical knowledge source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — state/task routing, semantic skills, completion evidence and execution policy
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — Blender 5.1 API strategy, runtime compatibility and image-datablock cache coherence
- `03_modeling` — hard-surface, topology, UV, trim sheets, floating details and authoring workflows
- `04_game_ready` — runtime optimization, deterministic bake, UV/LOD contracts, emissive and export constraints
- `05_execution` — QA, dirty-stage cache, executable pipeline DAG, post-export invariants, test-oracle integrity and completeness
- `06_prompts` — planner/reviewer/repair prompts and system prompt
- `07_examples` — examples and real benchmark/post-mortem runs
- `08_scripts` — reusable validation/import-safety patterns
- `09_engine` — engine/project profiles, canonical runtime roots, packaging, catalog and engine smoke-test contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executors/candidates
- `99_sources` — technical sources

## Completion model

```text
RECONSTRUCTION_COMPLETE
-> MODELING_COMPLETE
-> GAME_READY_COMPLETE
-> PIPELINE_INTEGRATED
```

A Blender render, successful bake, exported glTF or Blender re-import is not automatically a complete runtime asset.

### Level C — `GAME_READY_COMPLETE`

Requires, as applicable:
- final geometry/LOD/collision validation;
- runtime material closure;
- stable UV contract;
- semantic bake validation;
- disk/Blender image-cache coherence;
- canonical output path preflight;
- package readback;
- post-export round-trip invariant validation;
- baked-runtime QA.

### Level D — `PIPELINE_INTEGRATED`

Additionally requires target-runtime proof. v0.7 distinguishes:

```text
Blender glTF import
= Level C round-trip evidence

ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
= valid Level D evidence kinds
```

`executors/completion_gate.py` no longer accepts a bare `runtime_import_or_instantiation: PASS` as Level D proof.

## v0.7 execution model

The central change is an enforced dependency DAG:

```text
changed input
-> PIPELINE_DAG_PLAN
-> dirty dependency closure
-> execute only dirty stages
-> reuse accepted independent artifacts
-> validate
```

A local repair must not default to:

```text
build -> decals -> bake all -> export -> import -> test
```

when only a subset depends on the change.

Examples:
- stale Blender image datablock -> reload/binding QA; baked PNG remains clean;
- wrong runtime output root -> package/readback/engine test dirty; texture pixels remain clean;
- underside geometry change -> geometry + actually dependent bake channels + export/round-trip/test; separate decal atlas normally remains clean.

## Image cache coherence

The final Bollard run proved a silent Blender failure class:

```text
accepted new PNG on disk
+
old bpy.data.images datablock with same name
=
runtime material renders stale pixels
```

v0.7 adds `IMAGE_CACHE_COHERENCE` and `executors/image_cache_coherence.py`.

When disk is authoritative:

```text
validate file
-> load/reload Blender image datablock
-> verify canonical filepath/colorspace/dimensions
-> verify material binding
-> runtime QA
```

Do not rebake a correct texture merely because Blender is displaying an older cached image.

## Canonical runtime path

A real directory is not necessarily an engine-visible directory.

v0.7 adds `RUNTIME_PATH_RESOLVE` and forbids per-script root guessing.

Authority:

```text
validated project profile
> build/engine asset-root definition
> production loader config
> engine test fixture
> sibling exporter
> heuristic search
```

For the currently verified RPG project profile:

```text
engine asset directory = <repo>/Assets
game asset root       = <repo>/Assets/GameAssets
forbidden lookalike   = <repo>/GameAssets
```

These facts are stored in `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md` and should be reused until project configuration invalidates them.

## Post-export invariants

v0.7 explicitly re-measures the final exported/re-imported artifact.

This exists because the Bollard source looked correct while exported LOD0 became 1048 mm instead of the locked 1050 mm after underside/fillet changes.

Protected invariants may include:
- dimensions;
- contact datum;
- LOD family/counts;
- triangle budgets;
- material/image survival;
- UV/custom data;
- handedness/asymmetry.

## Test oracle integrity

A green-looking shell command is not enough.

Unsafe without verified `pipefail`:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

because `$?` can belong to `tail` rather than the test process.

v0.7 adds `TEST_ORACLE` and `executors/test_oracle.py` for direct-process return-code capture.

New regression assertions should perform a controlled bite test when safe:

```text
correct baseline
-> intentionally change one expectation
-> intended assertion fails with expected message
-> restore
-> final test passes
```

Crash/abort/load failure is not a valid bite.

## Semantic execution

Before ad-hoc Python/shell/project code, check `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`.

New v0.7 semantic skills include:
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `TEST_ORACLE`;
- `ENGINE_INTEGRATION_PROOF`.

New candidate executors include:
- `executors/image_cache_coherence.py`;
- `executors/pipeline_dag.py`;
- `executors/runtime_path_resolver.py`;
- `executors/export_roundtrip_validate.py`;
- `executors/test_oracle.py`.

They remain `CONTRACT_READY` until the next real benchmark exercises the packaged implementations.

`MESH_VALIDATE` remains `EXECUTOR_READY` from real Blender 5.1 evidence.

## Benchmarks

Canonical benchmarks now include:
- Lafar Street Bench reconstruction;
- Lafar Civic Bollard end-to-end asset benchmark;
- Lafar Civic Bollard bake/runtime regression benchmark;
- Lafar Civic Bollard final pipeline-integration regression benchmark.

Known cost evidence:

```text
first Bollard full baseline                  ~60k tokens
captured v0.5 game-ready continuation        ~36k tokens
additional final integration continuation    ~45k tokens
post-v0.5 continuation combined              ~81k tokens
```

Preferred v0.7 target once an asset is already `GAME_READY_COMPLETE` and the matching project profile exists:

```yaml
pipeline_integration_tokens: <= 10000
project_profile_rediscovery_calls: 0
false_green_test_results: 0
ambiguous_runtime_root_writes: 0
full_pipeline_restarts_after_local_repair: 0
blender_import_used_as_level_d_proof: 0
```

These are benchmark goals, not universal limits.

## Repository rules

1. Prefer updating an existing canonical responsibility over creating duplicate parallel skills.
2. Add a new skill only for a distinct reusable responsibility/failure class.
3. Keep semantic identity separate from transient Blender names/UI state.
4. `MANIFEST.json` defines the canonical modules compiled into `_FULL_LIBRARY.md`.
5. GitHub Actions regenerates `_FULL_LIBRARY.md`; never edit the snapshot manually.
6. Candidate executors are not promoted without real runtime evidence.
7. A release should improve quality, proof strength or cost — documentation volume alone is not progress.
8. Validated project facts belong in profiles and should not be rediscovered per asset.
9. Local repairs execute the DAG dirty closure, not the whole pipeline by habit.
10. Level D requires target-engine evidence with a trustworthy test oracle.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- evidence-driven reconstruction
- game-ready hard-surface production
- deterministic procedural-to-runtime material closure
- incremental dependency-driven execution
- target-engine integration proof
- glTF/GLB neutral baseline unless an Engine Profile overrides it

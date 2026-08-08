# Knowledge Router

Agent nie powinien ładować całej biblioteki do każdego zadania.

Najpierw stosuj `00_governance/06_TASK_PACK_PROTOCOL.md`. Router wybiera najmniejszy wymagany pakiet dla bieżącego STATE, task subtype i **zmierzonego rodzaju porażki**.

## Session startup / first scene mutation

Use `SESSION_PREFLIGHT`:
- Agent Charter;
- Semantic Skill Registry;
- Tool Discovery and Registry;
- Tool Call and Token Efficiency;
- Agent Tool API Profile;
- Blender 5.1 Compatibility Matrix;
- Scene Inspection.

Route version-sensitive discovery to `RUNTIME_COMPAT`.

If a validated project profile matches the active repository, load it once and persist:
- project/profile ID;
- canonical runtime asset root;
- packaging facts;
- build/test target facts.

For the known RPG repository use `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md` while its evidence remains valid.

Do not rediscover these facts per asset.

## New hard-surface asset

Load:
- Agent Charter;
- State Machine;
- Semantic Skill Registry;
- Asset Brief Schema;
- Reference Decomposition;
- Feature Contract;
- Modeling Decision Tree;
- Hard Surface Workflow;
- Game Asset Contract;
- Completion Levels;
- Build Plan;
- Execution Protocol;
- Retry Budget;
- Visual QA.

Set `TARGET_COMPLETION_LEVEL` during CONTRACT/PLAN.
Do not preload UV/material/LOD/export modules before their state is reached.

## Axisymmetric / rotational hard-surface asset

Typical triggers: bollard/post, round base/collar/cap, cylindrical housing, stacked radial profile.

Route primary rotational form to `AXISYMMETRIC_PROFILE` before writing another local lathe helper.
Route repeated circular fasteners/anchors to `RADIAL_REPEAT`.
Keep asymmetric panels, decals and local emitters as separate feature owners.

## Existing asset repair

Load only:
- current Feature Contract;
- Scene Inspection;
- relevant semantic skill;
- Idempotency/Recovery;
- Code Artifact/Patch Protocol if code changes;
- Retry Budget;
- regression/QA for the changed owner.

If the repair occurs after accepted runtime stages, additionally route through `PIPELINE_DAG_PLAN` before replaying build/bake/export.

## Blender API problem

Load API Strategy, Compatibility Matrix, Tool Registry/Profile, Context/Mode/Selection, Scene Inspection and Retry Budget.

Use `RUNTIME_COMPAT` instead of guessing enum/property/path behavior.

## Procedural panel line / narrow groove

Route to `HS_PANEL_LINE`.
If the host is SubD-controlled or pinching/flow matters, also route to `SUBD_TOPOLOGY_CONTROL`.
Do not use panel-line skill for wide/deep recesses or silhouette-changing cuts.

## Subdivision topology problem

Route to `SUBD_TOPOLOGY_CONTROL` + Topology/Normals/Shading + BMesh/API rules.

## Mesh / topology validation

Route to `MESH_VALIDATE`.

Every mesh declares topology intent:
- `CLOSED_SOLID`;
- `OPEN_ASSEMBLY_PART`;
- `SURFACE_DETAIL`;
- `COLLISION`.

`MESH_VALIDATE` is `EXECUTOR_READY`; session runtime binding must still be verified.

## Civic material looks too clean / procedural

Route to `MATERIAL_FINISH_CIVIC`.
Load maintained-civic material playbook + procedural material authoring + material-vs-lighting evidence.

Do not add generic uniform grunge.

## Integrated emissive / guidance feature

Route to `EMISSIVE_HANDOFF`.
Keep emitter correctness separate from engine bloom/exposure/tone mapping.

## UV atlas shared by bake source and LODs

Route to `UV_ATLAS_CONTRACT`.

Use semantic part IDs rather than transient Blender `.001/.002` names.
Missing atlas assignment is a hard FAIL.
Bake source and every consuming runtime LOD must share the declared contract.

## Procedural/high-to-low -> runtime bake

Route to `BAKE_RUNTIME_TEXTURES`.
Load:
- Bake Gate;
- Bake Execution and Channel Semantics;
- UV Atlas/LOD Stability;
- Bake Output Validation;
- Image Datablock Cache Coherence;
- Dirty-Stage Cache;
- Pipeline DAG;
- Long-Running Job Protocol;
- active Engine/Project profile.

Preferred executors:
- `bake_runtime_textures.py`;
- `uv_atlas_contract.py`;
- `bake_validate.py`;
- `image_cache_coherence.py`;
- `qa_scene_isolation.py`;
- `pipeline_dag.py`.

A separate high-poly is not mandatory for every procedural-to-texture bake.
Do not rerun every channel after a local repair.

## Bake/runtime diagnostic routing

Route from strongest measured evidence:

```text
bpy bake returns CANCELLED / active-image warning
-> BAKE_RUNTIME_TEXTURES target binding

AO nearly black / global occlusion
-> QA_SCENE_ISOLATE

metal BaseColor black after DIFFUSE-style bake
-> authored BaseColor channel semantics

metallic constant/wrong material regions
-> scalar channel extraction + BAKE_VALIDATE

emissive white/full atlas/clipped hue
-> emission color*strength normalization + region validation

atlas assignments missing or LODs sample wrong regions
-> UV_ATLAS_CONTRACT

DISK MAP VALID + UV VALID + MATERIAL LINKS VALID + RUNTIME RENDER STALE/WRONG
-> IMAGE_CACHE_COHERENCE

external texture changed after earlier runtime material was built
-> IMAGE_CACHE_COHERENCE before any rebake
```

Do not rebuild UVs or rebake accepted textures when the evidence points to stale in-memory image data.

## Image/datablock cache mismatch

Route to `IMAGE_CACHE_COHERENCE`.

Load:
- `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`;
- Bake Output Validation;
- runtime material binding context.

Expected fix for disk-authoritative accepted texture:

```text
canonical file -> reload/synchronize bpy.data.images -> verify binding -> runtime QA
```

Not:

```text
rebake all channels
```

## Local repair after accepted runtime stages

Route to `PIPELINE_DAG_PLAN` + Dirty-Stage Cache.

Before executing a chain such as:

```text
build -> decals -> bake -> export -> import -> engine test
```

emit dirty/reuse plan.

Examples:
- stale image datablock -> runtime image binding/QA dirty, textures clean;
- wrong output directory -> export/copy/readback/engine test dirty, baked pixels clean;
- underside geometry change -> geometry + actual dependent bake channels + export/roundtrip/test dirty; separate decal asset normally clean.

Full pipeline replay without dependency evidence is a regression.

## Game-ready finishing

Use Task Pack `GAME_READY_FINISH`.

Preferred skills:
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `ASSET_COMPLETION`.

Before Level C:
1. resolve runtime output root if exporting externally;
2. validate LOD/collision/UV;
3. execute only dirty bake stages;
4. validate baked maps;
5. synchronize disk-authoritative images with Blender datablocks;
6. bind runtime material;
7. export/package readback;
8. round-trip final exported artifact;
9. verify hard dimensions/contact/material survival;
10. baked-runtime QA;
11. completion gate.

A procedural authoring render does not prove runtime bake/export correctness.

## Runtime asset root / ambiguous project paths

Route to `RUNTIME_PATH_RESOLVE`.

Load:
- active Project Asset Pipeline Profile;
- `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`.

Authority order:

```text
project profile
> build/engine asset-directory definition
> production loader configuration
> engine regression fixture
> sibling exporter
> heuristic search
```

If both `<repo>/GameAssets` and `<repo>/Assets/GameAssets` exist, never pick by name/first match.

For the verified RPG profile, runtime root is `<repo>/Assets/GameAssets`; `<repo>/GameAssets` is a forbidden lookalike root until project configuration changes.

## Runtime module packaging / export readback

Route to `RUNTIME_PACKAGE_VALIDATE` and/or `EXPORT_VALIDATE`.

Persist project facts such as:
- one-file multi-node vs separate LOD files;
- node suffix pattern;
- collision packaging;
- handedness/mirror compensation;
- material/image URI expectations.

Do not inspect long sibling exporters again when the active profile already contains these facts.

## Post-export hard-invariant check

Route to `EXPORT_ROUNDTRIP_VALIDATE`.

Load:
- `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`;
- runtime package contract;
- hard dimensions/Feature Contract.

Measure the **re-imported exported artifact**.
Check dimensions and ground/contact datum separately.

A source asset measuring 1050 mm does not prove the exported LOD still measures 1050 mm after fillets/export transforms.

Blender round-trip is Level C evidence only.

## Python module/helper reused by another stage

Load Code Artifact/Patch Protocol + Import-Safe Python Module Pattern.

Reusable modules must be import-safe and scratch collections explicit.
Do not let helper import trigger build/bake/export at top level.

## Project/catalog integration

Use `PIPELINE_INTEGRATION` only when target is Level D.

Load:
- Project Asset Pipeline Profile;
- Runtime Asset Root contract;
- Runtime Packaging contract;
- Asset Catalog Integration;
- Engine Integration Smoke-Test Contract;
- Test Oracle contract;
- Completeness Report.

## Engine test / Level D proof

Route to `ENGINE_INTEGRATION_PROOF` + `TEST_ORACLE`.

Required distinction:

```text
Blender glTF import PASS
-> export round-trip evidence / Level C

Engine::Model::Load or target engine instantiation PASS
-> Level D runtime evidence
```

`runtime_import_or_instantiation` must carry evidence kind:
- `ENGINE_PRODUCTION_LOADER`;
- `ENGINE_REGRESSION_TEST`;
- `ENGINE_INSTANTIATION`.

A bare `PASS` is insufficient in v0.7 completion gate.

## Suspicious test success / shell pipelines

Route to `TEST_ORACLE`.

Unsafe:

```bash
./test 2>&1 | tail -20
echo $?
```

unless executable status is explicitly preserved.

Prefer direct process execution.

For a new regression assertion, a valid bite test means:
- controlled mutation;
- intended assertion fails with expected message;
- not a crash/load failure;
- mutation restored;
- final test exits 0.

## Project-specific known RPG integration

When the active repository matches the verified profile:

`09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md`

reuse:
- engine asset directory `<repo>/Assets`;
- game asset root `<repo>/Assets/GameAssets`;
- one glTF containing `_LOD0.._LODn` nodes;
- X mirror export compensation while still valid;
- catalog source `Source/Engine/AssetCatalog.cpp`;
- production model loader `Engine::Model::Load`;
- narrow regression source `Tests/ModelTests.cpp`;
- debug build directory `Build/windows-debug`;
- target `ModelTests`;
- direct executable exit status.

Do not rediscover these facts with repeated `ls/find/grep` unless profile freshness is invalidated.

## Asset modularny

Additionally load Modularity/Instancing + Modular Architecture Example.

## Animated asset

Additionally load Animation/Rigging.

## Reviewer

Load Feature Contract, Visual QA, Final Validation, Completion Levels, Completeness Report and Reviewer Prompt.

## Token/output budget

Use:

```text
compute locally -> aggregate -> decision-grade summary
```

For source code:

```text
symbol/path lookup -> targeted range -> patch -> execute -> compact result
```

For runtime repair:

```text
measured failure -> semantic route -> DAG dirty closure -> execute only dirty -> validate
```

Do not echo full generated scripts, raw arrays or full logs without diagnostic need.

## Retry budget

After first proven failure, diagnose and permit one corrected retry of the same strategy.
After second proven failure: re-inspect + strategy switch/blocker.

Transport timeout is not a proven failure until job/artifact inspection says so.

A false green/ambiguous test status is `UNVERIFIED`, not success.

## Reference reconstruction

Start with Semantic Skill Registry + Task Pack + Reconstruction Controller.
Load detail/modeling skills only when the current reconstruction gate requires them.

Technical sheet ANALYZE uses `RECON_TECHNICAL_SHEET_ANALYZE` and `REFERENCE_MEASURE`.
After analysis PASS, reuse cached ROI/authority/dimensions.

## Full 1:1 reconstruction

Core:
- Semantic Skill Registry;
- Task Pack Protocol;
- Reconstruction Controller;
- Definition of 1:1;
- Reconstruction State Machine;
- Completion Levels.

Then load only current stage modules.

### Concept sheet ingest
102–109, 160, 168, 170, script 91, prompt 67.

### Geometry solve
110–123, 128–134, appropriate playbooks, `AXISYMMETRIC_PROFILE`, `RADIAL_REPEAT` as applicable.

### Rear/bottom
119, 135, playbook 113.

### Surface
124–127, 140, material/light playbooks.

### Reconstruction QA
141–148, scripts 81/83/86–90/92, prompt 65.

### Benchmarks
- `07_examples/73_LAFAR_STREET_BENCH_RECONSTRUCTION_BENCHMARK.md`
- `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`
- `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`
- `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`
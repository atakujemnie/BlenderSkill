# Changelog

## Unreleased

No canonical changes after the v0.7.0 release baseline yet.

## 0.7.0

v0.7.0 is the **runtime-proof integrity + project infrastructure reuse** release. It is based on the final Lafar Civic Bollard continuation after v0.6 bake closure.

The user reported approximately **45k additional tokens** for this final segment. Combined with the previous ~36k-token continuation, the post-v0.5 completion work consumed roughly **81k tokens**. The asset ultimately reached `PIPELINE_INTEGRATED`, but the run exposed silent cache, path, round-trip and test-oracle failures that should never be rediscovered on the next asset.

### Blender image cache coherence
- added `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`;
- external file freshness is explicitly separated from `bpy.data.images` freshness;
- correct PNG + stale Blender image datablock is classified as `STALE_IMAGE_DATABLOCK`;
- disk-authoritative textures are reloaded/synchronized before runtime-material QA;
- stale runtime binding normally dirties binding/QA only, not the accepted baked texture;
- added `executors/image_cache_coherence.py`.

### Executable incremental pipeline
- added `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`;
- Dirty-Stage Cache is now enforced through explicit dependency closure rather than treated as advisory prose;
- a local repair must emit execute/reuse plan before replaying build/bake/export stages;
- geometry, decal, individual bake channels, runtime material, package, round-trip, catalog and engine test can be invalidated independently;
- added pure-Python `executors/pipeline_dag.py` candidate;
- full pipeline replay after a local repair is now a benchmark regression unless the DAG proves every stage dirty.

### Post-export invariant validation
- added `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`;
- final exported/re-imported artifact must re-pass protected hard dimensions, contact datum and other declared invariants;
- source geometry PASS no longer implies exported artifact PASS;
- Blender round-trip evidence is explicitly Level C evidence, not Level D engine proof;
- added `executors/export_roundtrip_validate.py` candidate.

### Runtime root/path contract
- added `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`;
- filesystem existence is separated from engine visibility;
- canonical path authority is profile > build/engine definition > production loader > engine test > sibling exporter > heuristic;
- per-script root guessing is forbidden when one Runtime Path Context can be injected;
- wrong sibling output trees are handled as packaging/path dirtiness rather than texture rebake;
- added `executors/runtime_path_resolver.py`.

### Verified RPG project profile
- added `09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md` from the real Bollard integration evidence;
- verified engine asset directory: `<repo>/Assets`;
- verified runtime game-asset root: `<repo>/Assets/GameAssets`;
- `<repo>/GameAssets` recorded as a forbidden lookalike root for this project configuration;
- persisted one-file multi-node LOD packaging, `_LODn` convention, current X-mirror compensation, catalog source, production loader, CMake debug build directory and `ModelTests` target/binary;
- future matching assets should not rediscover these facts through repeated shell probing.

### Engine integration proof
- added `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`;
- target-engine production loader/test/instantiation is required for Level D;
- Blender glTF re-import remains Level C round-trip evidence;
- engine test should reuse existing project infrastructure and pin real contract failures rather than irrelevant implementation details;
- loader exceptions should become readable non-interactive test failures when possible.

### Test-oracle integrity
- added `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`;
- explicitly captures the shell trap `./test | tail; echo $?`, where `$?` can belong to `tail`;
- direct executable/subprocess exit status is preferred;
- test results distinguish assertion failure, load failure, crash and ambiguous status;
- new regression assertions should perform a controlled bite test when safe;
- crash/abort is not accepted as proof that the intended assertion bites;
- added `executors/test_oracle.py`.

### Completion gate hardening
- `executors/completion_gate.py` now requires exported round-trip invariants for `GAME_READY_COMPLETE`;
- `PIPELINE_INTEGRATED` runtime import/instantiation must include an evidence kind;
- accepted Level D evidence kinds are `ENGINE_PRODUCTION_LOADER`, `ENGINE_REGRESSION_TEST`, `ENGINE_INSTANTIATION`;
- a bare string `PASS` for runtime import no longer closes Level D;
- existing Bollard run proved the old gate correctly blocked Level D while runtime import was `UNVERIFIED`; the new evidence-kind extension remains `CONTRACT_READY` until the next run tests it directly.

### Project profile schema
- expanded `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md` with canonical runtime paths, forbidden lookalike roots, loader, build system, narrow runtime test target/binary and test-oracle policy;
- project profiles now carry exactly the infrastructure facts that consumed repeated discovery calls in the Bollard run;
- profile freshness/invalidation is explicit when build/importer/catalog configuration changes.

### Routing and task packs
- `SESSION_PREFLIGHT` can resolve matching project profile/runtime root once;
- `GAME_READY_FINISH` now includes image-cache coherence, Pipeline DAG, runtime-root preflight and export round-trip invariants;
- `PIPELINE_INTEGRATION` now requires canonical runtime root, target-engine smoke test and trustworthy test oracle;
- Knowledge Router adds direct routes for stale image cache, local dirty-stage repair, ambiguous runtime roots, post-export dimension/contact regressions and false-green shell tests;
- System Prompt distinguishes Level C round-trip evidence from Level D engine evidence and forbids habitual full pipeline replay.

### New semantic skills
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `RUNTIME_PATH_RESOLVE`;
- `TEST_ORACLE`;
- `ENGINE_INTEGRATION_PROOF`.

All new v0.7 executors remain `CONTRACT_READY` pending the next real benchmark. `MESH_VALIDATE` remains `EXECUTOR_READY`.

### B9 benchmark
- added `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`;
- records the stale image datablock, 1048-vs-1050 mm exported dimension regression, wrong runtime root, false `EXIT=0`, invalid first bite-test interpretation, unnecessary stage replay and repeated build-system discovery;
- preferred v0.7 target after Level C with matching profile: <=10k integration tokens, zero project-profile rediscovery, zero false-green test results, zero ambiguous runtime-root writes and zero full pipeline restarts after local repair.

Canonical module count after manifest release: **198**.

## 0.6.0

v0.6.0 is the **deterministic bake/runtime closure** release, based on the ~36k-token captured game-ready continuation of the real Lafar Civic Bollard run.

Key changes:
- deterministic bake execution with checked `FINISHED` result and correct active image-node binding;
- explicit BaseColor/Roughness/Metallic/AO/Normal/Emissive channel semantics;
- semantic `UV_CONTRACT_ID` shared by bake source and LODs;
- incremental Dirty-Stage Cache and long-running job protocol;
- semantic bake validation;
- import-safe build/bake/export modules;
- runtime packaging/readback contract;
- executors for bake, UV atlas, image validation and glTF package readback;
- `MESH_VALIDATE` promoted to `EXECUTOR_READY`;
- B8 benchmark `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`;
- canonical module count: **190**.

## 0.5.0

v0.5.0 is the first benchmark-driven **agent execution + completion** release.

Key changes:
- explicit completion levels from reconstruction through pipeline integration;
- Blender 5.1 compatibility matrix and runtime preflight;
- reusable reference/profile/radial/mesh/runtime/QA/completion executors;
- maintained-civic material finish model;
- emissive authoring/runtime separation;
- Game-Ready Bake Gate;
- floating detail/decal hardening;
- asset catalog integration contract;
- Task Packs, routing and benchmark-driven efficiency targets;
- first full Lafar Civic Bollard B7 benchmark;
- canonical module count: **182**.

## 0.3.0

Added full Reconstruction Layer:
- evidence/provenance model;
- concept-sheet segmentation;
- authority/conflict system;
- dimension graph and locks;
- landmark/calibration system;
- geometry inference rules;
- exact feature/material/branding handling;
- parametric reconstruction workflow;
- multi-view QA/regression gates;
- blueprint/photo/stylized modes;
- Lafar Street Bench benchmark.

## 0.2.0

Added production layer:
- camera/reference matching;
- Visual Feature Map;
- high/low-poly workflow;
- baking pipeline;
- trim sheets;
- decals/floating details;
- curve/Geometry Nodes/procedural material authoring;
- texture packing/mip safety;
- asset variants/randomization;
- automated visual diff;
- reference fidelity levels;
- authoring-to-runtime handoff;
- engine profile/adapter;
- deterministic QA render/diff patterns.

Architecture decision retained across releases:
- modular MD files are canonical;
- `_FULL_LIBRARY.md` is generated from `MANIFEST.json`.
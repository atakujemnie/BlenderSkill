# Lafar Civic Bollard — Pipeline Integration Regression Benchmark

## Purpose

This benchmark records the final continuation of the real Astera/Lafar civic bollard run after v0.6 bake/runtime closure work.

User-reported cost for this final continuation: approximately **45k additional tokens**. Combined with the preceding approximately 36k-token continuation segment, the post-v0.5 completion work consumed roughly **81k tokens**.

The asset eventually reached `PIPELINE_INTEGRATED`, but the path exposed several silent or falsely interpreted failure classes that v0.7 must eliminate.

## Final accepted runtime facts

```yaml
asset: Astera civic bollard
runtime_module: astera_bollard.gltf
lod_packaging: ONE_FILE_MULTI_NODE
lods:
  LOD0_tris: 2844
  LOD1_tris: 1152
  LOD2_tris: 480
  LOD3_tris: 128
collision_tris: 88
hard_dimensions_mm: [210, 210, 1050]
runtime_asset_root: <repo>/Assets/GameAssets
catalog_id: astera_bollard
engine_loader_test: ModelTests / Engine::Model::Load
completion: PIPELINE_INTEGRATED
```

## Observed v0.6-era failure classes

### F1 — stale Blender image datablock

The baked PNGs on disk were correct, UVs were correct and material links appeared correct, but the runtime material still rendered old pixels.

Cause:

```text
bpy.data.images.get(...)
-> reused existing datablock
-> external file had newer accepted bake
-> image datablock was not reloaded
```

Required v0.7 behavior:
- disk-vs-memory authority is explicit;
- accepted disk bake triggers image synchronization/reload before runtime QA;
- stale image cache routes to binding/cache repair, not rebake/UV repair.

### F2 — exported hard dimension regression

Round-trip import found LOD0 at 1048 mm instead of the technical-sheet 1050 mm.

Cause:
- underside geometry/profile change;
- base fillet removed the true contact point;
- source looked plausible but exported bounds failed the hard contract.

Required v0.7 behavior:
- post-export invariants include dimensions and ground datum;
- export round-trip runs before catalog completion;
- repair dirties only dependent stages through the pipeline DAG.

### F3 — Blender import was not engine proof

Blender successfully imported the glTF, but Level D remained correctly unresolved until the custom engine loader was exercised.

Required v0.7 behavior:

```text
Blender round-trip = Level C evidence
Engine production loader/test = Level D evidence
```

### F4 — wrong but valid filesystem tree

The asset was exported to:

```text
<repo>/GameAssets/...
```

while the engine read from:

```text
<repo>/Assets/GameAssets/...
```

Both looked plausible and existed.

Required v0.7 behavior:
- runtime asset root resolved from project/build/engine authority before export;
- no per-script root guessing;
- project profile stores the verified root;
- wrong sibling root is explicitly forbidden for this project profile.

### F5 — false green test from shell pipeline

Unsafe invocation:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

reported the status of `tail`, not necessarily `ModelTests.exe`.

An apparent `EXIT=0` was therefore meaningless.

Required v0.7 behavior:
- capture executable exit status directly or use `pipefail` correctly;
- distinguish assertion failure from crash/abort;
- no Level D PASS from ambiguous test status.

### F6 — invalid first bite-test interpretation

A deliberately broken expected triangle count initially produced exit 3 because the process aborted while loading the asset from the wrong root. That was incorrectly interpreted as proof the assertion 'bit'.

After the runtime path was fixed:
- wrong expected tris -> clean `EXIT=1`;
- expected regression message appeared;
- expectation restored -> `EXIT=0`.

Required v0.7 behavior:
- bite test must fail for the intended assertion;
- crash/loader failure is not an assertion bite.

### F7 — unnecessary pipeline replay

After a local underside geometry repair the workflow re-executed build, decals, all bake passes and export as a manual chain.

This bypassed the spirit of the v0.6 Dirty-Stage Cache.

Required v0.7 behavior:
- pipeline execution is DAG-planned;
- independent clean stages are reused;
- stage execution/reuse counts are benchmarked.

### F8 — repeated build-system discovery

The agent spent multiple shell calls locating CMake configuration, test binaries and the existing `ModelTests` pattern.

Required v0.7 behavior:
- project profile stores build directory, narrow test target, binary, loader and catalog source;
- future assets consume the profile directly.

## What v0.6 did well

v0.6 concepts materially helped:
- runtime bake closure was completed instead of deferred;
- semantic channel bake rules produced correct BaseColor/ORM/Normal/Emissive;
- completion gate correctly refused Level D while runtime import remained unverified;
- final accepted asset had all four LODs in budget and correct hard dimensions after repair.

The problem was no longer primarily missing knowledge. It was **execution proof, cache coherence, project-profile completeness and enforced stage reuse**.

## v0.7 regression requirements

A comparable future asset should satisfy:

```yaml
v0_7_targets:
  false_green_test_results: 0
  ambiguous_runtime_roots: 0
  stale_image_datablock_regressions: 0
  full_pipeline_restarts_after_local_repair: 0
  blender_import_used_as_level_d_proof: 0
  new_engine_assertions_with_valid_bite_test: 100_percent_when_safe
  project_profile_rediscovery_calls: 0_when_profile_matches
```

Preferred efficiency targets after `GAME_READY_COMPLETE` is already reached:

```yaml
pipeline_integration_finish:
  preferred_tokens: <= 10000
  preferred_project_discovery_calls: <= 2
  full_texture_rebakes: 0_unless_dependencies_changed
  engine_test_runs:
    green_baseline_or_final: <= 2
    controlled_bite_test: <= 1_failure_plus_restore
```

These are benchmark goals, not universal hard limits.

## Release implication

v0.7 is successful only if the next benchmark demonstrates that solved infrastructure is reused:
- canonical runtime path comes from profile;
- stage DAG prevents unrelated recomputation;
- post-export invariants catch dimension/contact drift early;
- image cache freshness is explicit;
- Level D is closed only by a trustworthy target-engine test oracle.
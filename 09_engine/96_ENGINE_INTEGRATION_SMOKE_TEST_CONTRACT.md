# Engine Integration Smoke-Test Contract

## Purpose

`PIPELINE_INTEGRATED` requires evidence from the **target runtime path and loader**, not merely from Blender or a file parser.

The engine test must also prove the space in which its invariants are evaluated. A dimension assertion over local vertex positions is not world-space proof when the runtime node can carry an unapplied transform.

## Proof hierarchy

```text
package JSON/readback
< Blender round-trip import
< engine production loader test
< engine instantiation/render smoke test
```

Use the strongest level required by the active completion target.

## Level D minimum

For `PIPELINE_INTEGRATED`, the minimum accepted runtime evidence is normally one of:
- target engine production loader successfully loads the registered asset;
- existing engine regression test invokes the same loader on the exported asset;
- actual engine scene instantiation succeeds.

A Blender `bpy.ops.import_scene.gltf` PASS is Level C round-trip evidence only.

## Reuse existing project test infrastructure

Before creating a new test harness:
1. read the active Project Asset Pipeline Profile;
2. locate the configured narrow model/import test target;
3. inspect the nearest existing asset test pattern;
4. extend it with only the asset invariants that previously failed or are contract-critical.

Do not rediscover the build system with broad shell exploration when profile facts are already known.

## Recommended engine-side assertions

Asset-specific tests may pin:
- asset can be resolved from runtime asset root;
- loader returns expected LOD group/nodes;
- LOD triangle counts or budget bounds;
- hard dimensions/tolerance on runtime vertex data;
- ground datum;
- required UV channel presence;
- required PBR image bindings;
- vertex colors/custom attributes when relied upon;
- alpha/cutout semantics;
- material count/names where contract-critical.

Do not pin irrelevant implementation details that make tests brittle without protecting a real contract.

## Coordinate-space declaration

Every dimension/contact assertion must declare one of:

```text
LOCAL_VERTEX_SPACE
NODE_TRANSFORMED_SPACE
ENGINE_WORLD_SPACE
```

A test that reads raw accessor/vertex positions is normally `LOCAL_VERTEX_SPACE`.

It must not be described as proof of final runtime size when non-identity node transforms are permitted and the production loader may ignore them.

## Node transform policy

The active Project Asset Pipeline Profile must declare the runtime policy for node transforms.

Possible policies:

```text
IDENTITY_TRS_REQUIRED
TRANSFORMS_APPLIED_BY_LOADER
TRANSFORMS_BAKED_BY_EXPORTER
UNVERIFIED
```

If the production loader does **not** apply glTF node transforms:
- runtime mesh nodes must use identity/baked TRS according to project policy;
- package readback must fail on non-identity runtime node transforms;
- local-vertex dimension assertions are accepted only together with the identity-transform proof.

This protects against a false green where local vertices still measure 2600 mm but the glTF node contains an unconsumed scale.

## Runtime attribute proof

Successful loading is not enough to prove the renderable primitive contract.

For textured materials, package/engine evidence should pin required attributes such as:

```text
POSITION
NORMAL
TEXCOORD_0
```

when required by the runtime material.

The Lafar Wayfinding Pylon benchmark produced a valid/loadable glTF with images and materials but no `TEXCOORD_0` after UV-layer-name mismatch during mesh joining. This must be a hard package/runtime FAIL, not a later visual surprise.

## Loader exceptions and automation

A loader exception used in an automated test must become a readable test failure where practical.

Avoid modal dialogs/abort-only behavior that blocks the agent and hides the failure cause.

Classify:

```text
ASSET_NOT_FOUND
PARSE_FAIL
MATERIAL_MISSING
ATTRIBUTE_MISSING
LOD_CONTRACT_FAIL
DIMENSION_FAIL
NODE_TRANSFORM_FAIL
TEST_ASSERTION_FAIL
PROCESS_CRASH
```

## Bite-test requirement

A newly added regression assertion should prove it can fail through `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md` when safe.

The bite test must fail for the intended assertion with a readable message, then be fully restored and green.

A crash/abort is not a valid bite.

A valid bite test proves only the assertion class it mutates. Example:
- changing build geometry height and seeing `DIMENSION_FAIL` proves geometry-drift detection;
- it does **not** prove node-scale detection unless the controlled mutation is specifically a node transform and the intended transform assertion bites.

## Catalog integration

If the project uses an asset catalog:

```text
export to canonical runtime root
-> package readback
-> transform/attribute contract
-> catalog registration/readback
-> engine loader test using runtime path/catalog convention
-> completion gate
```

Registering a catalog entry without proving the target file is visible to the engine is insufficient.

## Completion evidence

Persist:

```yaml
engine_smoke_test:
  loader: Engine::Model::Load
  asset_id: ...
  runtime_path: ...
  build_target: ...
  build_status: PASS
  test_exit_code: 0
  process_status: PASS
  coordinate_space: LOCAL_VERTEX_SPACE
  node_transform_policy: IDENTITY_TRS_REQUIRED
  package_transform_check: PASS
  assertions:
    lod_family: PASS
    dimensions: PASS
    required_attributes: PASS
    materials: PASS
  bite_test: PASS | NOT_REQUIRED | NOT_SAFE
  status: PASS
```

Only this kind of target-runtime evidence may satisfy `runtime_import_or_instantiation` for Level D.

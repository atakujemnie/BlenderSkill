# Project Asset Pipeline Profile Schema

## Purpose

An agent often needs project conventions such as naming, asset roots, decal atlases, material libraries, export destinations, runtime packaging rules, build targets and engine smoke-test commands.

It must not discover these by reading entire sibling asset build/export scripts or probing the build tree for every asset unless no validated profile exists.

This module defines a compact project-level profile separate from the runtime `ENGINE_PROFILE.md`.

The Engine Profile answers: **what the engine accepts**.

The Project Asset Pipeline Profile answers: **how this project authors, packages, stores, tests and integrates assets**.

For detailed runtime packaging semantics also use:
- `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`;
- `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`;
- `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`.

## Suggested files

Generic schema instance:

```text
PROJECT_ASSET_PIPELINE_PROFILE.md
```

Repository-specific validated profiles may live under:

```text
09_engine/profiles/
```

Example:

```text
09_engine/profiles/RPG_PROJECT_ASSET_PIPELINE_PROFILE.md
```

A child profile may add brand/family conventions but must not silently override engine constraints.

## Schema

```yaml
project_asset_pipeline:
  profile_id: PROJECT_NAME_V1

  units:
    blender_unit: meter
    unit_scale: 1.0
    up_axis: Z

  naming:
    static_mesh: "SM_{brand}_{asset}_{variant}_LOD{n}"
    collision: "COL_{brand}_{asset}_{variant}"
    material: "M_{brand}_{name}"
    decal: "D_{brand}_{name}"

  runtime_paths:
    project_root: ...
    engine_asset_directory: ...
    game_asset_root: ...
    source_root: ...
    textures_root: ...
    decal_root: ...
    export_root: ...
    checkpoints_root: ...
    authority: PROFILE | CMAKE_DEFINE | ENGINE_CONFIG | LOADER_CODE | ...
    forbidden_lookalike_roots: []

  material_library:
    canonical_materials: []
    reusable_pbr_sets: []
    forbidden_brand_reuse: []

  decal_pipeline:
    atlas_path: ...
    atlas_layout_source: ...
    uv_convention: ...
    logo_policy: TEXTURE_OR_DECAL

  authoring:
    preferred_sides_for_cylinders: [24, 32]
    default_bevel_segments_game_ready: 2
    apply_scale_before_export: true

  export:
    format: GLTF_SEPARATE
    preset: ...
    destination: ...

  runtime_packaging:
    lod_packaging: ONE_FILE_MULTI_NODE | SEPARATE_FILE_PER_LOD | ...
    lod_node_pattern: "{mesh}_LOD{n}"
    collision_source: EXTERNAL_PREFAB | SEPARATE_FILE | EMBEDDED_NODE | ...
    collision_naming: ...
    handedness_compensation: NONE | MIRROR_X | MIRROR_Y | MIRROR_Z | ...
    handedness_verified_by: ...
    mirror_only_for_asset_classes: []
    runtime_material_policy: ...
    image_uri_policy: ...
    dynamic_material_policy: ...
    export_readback_required: true

  asset_catalog:
    required: true
    stable_id_rule: ...
    registration_source: ...
    conflict_policy: ...

  engine_loader:
    production_loader: ...
    runtime_asset_root_source: ...

  build_and_test:
    build_system: CMAKE | MSBUILD | NINJA | CUSTOM | ...
    debug_build_directory: ...
    runtime_test_target: ...
    runtime_test_source: ...
    runtime_test_binary: ...
    build_command: ...
    test_command: ...
    test_oracle_policy: DIRECT_PROCESS | PIPEFAIL_VERIFIED | TOOL_NATIVE
    bite_test_required_for_new_regression_assertion: true

  provenance:
    sources: []
    last_verified: ...
```

Only include conventions actually evidenced by project files, build configuration, runtime readback or explicit user instruction.

## Discovery order

When project conventions are needed:

```text
1. active validated Project Asset Pipeline Profile
2. explicit current task/user instruction
3. current asset manifest/config
4. engine/build definition
5. narrowly targeted project file lookup
6. sibling build/export/test script as last-resort evidence
```

Do not read a large unrelated build script merely to infer one naming, LOD grouping, handedness, path or test rule when a compact profile already provides it.

## Runtime path rule

A directory existing on disk is not evidence that the engine reads it.

If two plausible roots exist, such as:

```text
<repo>/GameAssets
<repo>/Assets/GameAssets
```

resolve against the engine/build/loader authority and persist the result.

Do not let bake, decal and export scripts each implement independent root-walking heuristics.

Use `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`.

## Sibling-script rule

If no profile exists and a sibling script must be inspected:
- search exact relevant identifiers first;
- read the smallest relevant range;
- extract only verified conventions;
- validate runtime-sensitive facts through actual exported/imported behavior where possible;
- update the Project Asset Pipeline Profile;
- do not copy sibling geometry dimensions or feature logic into the current asset.

A sibling asset is evidence for pipeline convention, not evidence for current geometry.

## Packaging facts worth persisting

When discovered once, persist facts such as:
- canonical engine-visible asset root;
- whether one asset uses one glTF containing all `_LODn` nodes or separate files;
- how LOD node names are parsed;
- whether collision lives in prefab primitives, a separate file or embedded nodes;
- whether the importer/engine changes handedness;
- whether export-side mirror compensation is required and on which axis;
- how readable logos/text are used to verify handedness;
- which runtime material names must survive export;
- expected BaseColor/Normal/ORM/Emissive image URI policy;
- whether decals/dynamic displays remain separate materials;
- whether catalog registration is required after export;
- which production loader proves Level D;
- the narrow build target/test binary used for asset regression tests;
- how the real test process exit code is captured.

These are project facts. Future assets should consume them without reopening long sibling exporters or re-running broad build-system discovery.

## Test infrastructure rule

Once a project test target is verified, persist it.

A future asset should not spend several shell calls rediscovering CMake presets, test binaries or source locations.

New regression assertions use `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md` and `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md`.

## Handedness verification

Do not infer handedness correctness from a symmetric prop.

Prefer an asymmetric proof:
- readable logo/text;
- left/right service panel;
- directional port;
- asymmetric decal.

Record the evidence in `handedness_verified_by`.

## Conflict precedence

```text
Engine Profile constraints
> explicit current task requirements
> approved Project Asset Pipeline Profile
> current asset configuration
> sibling asset convention
```

If the current task explicitly names an object/material/export rule, do not silently replace it with an older project convention.

## Profile freshness

Project facts can become stale.

Mark affected fields `UNVERIFIED` and re-resolve after changes to:
- build-system asset-root definitions;
- engine loader configuration;
- importer handedness/LOD grouping;
- catalog implementation;
- test/build directory layout;
- runtime material conventions.

Do not invalidate unrelated stable profile fields.

## Brand/family scope

A child brand profile may define:
- manufacturer prefix;
- shared material names;
- decal atlas;
- typography/logo handling;
- common construction language.

It must not define dimensions for new products unless those dimensions are a real family standard documented as such.

## Runtime status

Missing Project Asset Pipeline Profile does not make geometry invalid, but project integration status is:

```text
PROJECT_PIPELINE_UNVERIFIED
```

until conventions required by the task are confirmed.

If runtime root or packaging facts required for game-ready export are unknown:

```text
RUNTIME_PACKAGING_UNVERIFIED
```

Do not guess path, one-file/separate-LOD, collision or mirror policy.

## Efficiency requirement

Once conventions are extracted into a validated profile, cache and reuse them across assets in the same project scope. Do not repeatedly re-read original discovery scripts or re-probe the build tree.
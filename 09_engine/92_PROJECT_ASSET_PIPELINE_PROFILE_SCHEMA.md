# Project Asset Pipeline Profile Schema

## Purpose

An agent often needs project conventions such as naming, asset roots, decal atlases, material libraries, export destinations and runtime packaging rules.

It must not discover these by reading entire sibling asset build/export scripts unless no profile exists.

This module defines a compact project-level profile separate from the runtime `ENGINE_PROFILE.md`.

The Engine Profile answers: **what the engine accepts**.

The Project Asset Pipeline Profile answers: **how this project authors, packages and organizes assets**.

For detailed runtime packaging semantics also use:

`09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`

## Suggested file

```text
PROJECT_ASSET_PIPELINE_PROFILE.md
```

A project may have narrower child profiles, for example:

```text
LAFAR_ASSET_PIPELINE.md
ASTERA_ASSET_PIPELINE.md
```

Child profiles may add brand/family conventions but must not silently override engine constraints.

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

  paths:
    source_root: ...
    textures_root: ...
    decal_root: ...
    export_root: ...
    checkpoints_root: ...

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
    format: GLB
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

  provenance:
    sources: []
    last_verified: ...
```

Only include conventions that are actually evidenced by project files, runtime readback or explicit user instruction.

## Discovery order

When project conventions are needed:

```text
1. active Project Asset Pipeline Profile
2. explicit task prompt / user instruction
3. current asset manifest/config
4. narrowly targeted project file lookup
5. sibling build/export script as last-resort evidence
```

Do not read a large unrelated build script merely to infer one naming, LOD grouping, handedness or decal path rule when a compact profile can provide it.

## Sibling-script rule

If no profile exists and a sibling script must be inspected:
- search for exact relevant identifiers first;
- read the smallest relevant range;
- extract only verified conventions;
- validate runtime-sensitive facts through actual exported/imported behavior where possible;
- write/update the Project Asset Pipeline Profile;
- do not copy sibling geometry dimensions or feature logic into the current asset.

A sibling asset is evidence for pipeline convention, not evidence for current geometry.

## Packaging facts worth persisting

When discovered once, persist facts such as:
- whether one asset uses one glTF containing all `_LODn` nodes or separate files;
- how LOD node names are parsed;
- whether collision lives in prefab primitives, a separate file or embedded nodes;
- whether the importer/engine changes handedness;
- whether export-side mirror compensation is required and on which axis;
- how readable logos/text are used to verify handedness;
- which runtime material names must survive export;
- expected BaseColor/Normal/ORM/Emissive image URI policy;
- whether decals/dynamic displays remain separate materials;
- whether catalog registration is required after export.

These are project facts. Once verified, future assets should consume them without reopening long sibling exporters.

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

## Brand/family scope

A child brand profile may define:
- manufacturer prefix;
- shared material names;
- decal atlas;
- typography/logo handling;
- common construction language.

It must not define dimensions for new products unless those dimensions are a real family standard documented as such.

## Runtime status

Missing Project Asset Pipeline Profile does not make geometry invalid, but project-integration status is:

```text
PROJECT_PIPELINE_UNVERIFIED
```

until conventions required by the task are confirmed.

If packaging facts required for game-ready export are unknown:

```text
RUNTIME_PACKAGING_UNVERIFIED
```

Do not guess one-file/separate-LOD, collision or mirror policy.

## Efficiency requirement

Once conventions are extracted into a validated profile, cache and reuse them across assets in the same project/brand scope. Do not repeatedly re-read the original discovery scripts.

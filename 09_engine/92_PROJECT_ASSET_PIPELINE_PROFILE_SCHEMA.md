# Project Asset Pipeline Profile Schema

## Purpose

An agent often needs project conventions such as naming, asset roots, decal atlases, material libraries and export destinations.

It must not discover these by reading entire sibling asset build scripts unless no profile exists.

This module defines a compact project-level profile separate from the runtime `ENGINE_PROFILE.md`.

The Engine Profile answers: **what the engine accepts**.

The Project Asset Pipeline Profile answers: **how this project authors and organizes assets**.

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

  provenance:
    sources: []
    last_verified: ...
```

Only include conventions that are actually evidenced by project files or explicit user instruction.

## Discovery order

When project conventions are needed:

```text
1. active Project Asset Pipeline Profile
2. explicit task prompt / user instruction
3. current asset manifest/config
4. narrowly targeted project file lookup
5. sibling build script as last-resort evidence
```

Do not read a large unrelated build script merely to infer one naming rule or decal path when a compact profile can provide it.

## Sibling-script rule

If no profile exists and a sibling script must be inspected:
- search for exact relevant identifiers first;
- read the smallest relevant range;
- extract only verified conventions;
- write/update the Project Asset Pipeline Profile;
- do not copy sibling geometry dimensions or feature logic into the current asset.

A sibling asset is evidence for pipeline convention, not evidence for current geometry.

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

## Efficiency requirement

Once conventions are extracted into a validated profile, cache and reuse them across assets in the same project/brand scope. Do not repeatedly re-read the original discovery scripts.

# Location Material Language Library

## Purpose

A location must reuse one persistent material language instead of regenerating unrelated textures per asset.

## Canonical behavior

Before authoring materials for an asset:

```text
resolve location_id
-> resolve project game_asset_root
-> look for <game_asset_root>/Materials/Locations/<location_id>
-> if present: read and reuse material_language.json
-> if missing: create the library skeleton and manifest
-> report the exact library path to the user
-> only then add/reuse/adapt texture sets
```

Default RPG layout:

```text
<repo>/Assets/GameAssets/Materials/Locations/<location_id>/
  material_language.json
  textures/
  atlases/
  masks/
  references/
  previews/
  source/
```

The path is persistent project state. Subsequent prompts should point to this folder instead of rebuilding materials from scratch.

## Manifest contract

`material_language.json` stores at minimum:
- `schema_version`;
- `location_id`;
- `library_version`;
- `material_families`;
- `surface_rules`;
- `texture_sets`.

Material families define visual language such as graphite composite, brushed metal, wet soil, bark, leaf, concrete, painted polymer or glass. Surface rules define shared responses such as wetness, road grime, seam dirt, edge wear and contact darkening.

## Reuse-first rule

```text
existing compatible family
-> reuse

existing family needs local variation
-> adapt/tint/mask/weather

no compatible family
-> create new family inside the same location library
```

Do not create a private texture root beside one asset when a location library exists.

## Completion output

Every material-authoring task returns:
- `location_id`;
- material-library path;
- manifest path;
- reused families;
- new families/texture sets added.

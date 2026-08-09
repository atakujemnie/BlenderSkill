# Benchmark 83 — Lafar Planter v0.14 Visual Quality and Efficiency Regression

## Purpose

Re-run the same three Lafar planter targets that exposed v0.13 weaknesses. v0.14 must preserve technical correctness while raising visible quality and reducing context/code churn.

## Regression source

Human review of the v0.13 result identified:
- generic/even planting with weak massing and rhythm;
- medium/low-quality vegetation sources;
- sterile/procedural material response;
- no persistent shared material language for the location;
- approximately 80k tokens spent on three planters, including repeated project-local infrastructure.

## Required v0.14 route

```text
location/project preflight
-> LOCATION_MATERIAL_LIBRARY find-or-create
-> installed provider/library discovery + runtime probe
-> PROVIDER_QUALITY_SELECT for requested usage class
-> library-first vegetation source selection
-> physical planter composition gate
-> PLANTING_COMPOSITION_QUALITY
-> reference composition fidelity when reference-driven
-> location material-language reuse/adaptation
-> EARLY VISUAL QUALITY BARRIER
-> only then runtime LOD/bake/export/integration
-> CONTEXT_BUDGET_GATE
```

## Material-language acceptance

For each location run:
- resolve one stable `location_id`;
- return exact material-library path;
- reuse existing compatible material families before creating new textures;
- if no library exists, bootstrap it under the project profile and persist `material_language.json`;
- all new approved material families/texture sets are added to the same library.

Default RPG target:

`<repo>/Assets/GameAssets/Materials/Locations/<location_id>/`

## Vegetation quality acceptance

- HERO source: quality tier A unless explicitly waived;
- MID source: A or B;
- BACKGROUND: A/B/C;
- runtime compatibility alone cannot authorize a lower-quality provider;
- visible clone repetition and periodic placement are gated;
- composition uses masses/patches/height layers rather than only individual collision-free anchors;
- physical root/stem/wall constraints from v0.13 remain mandatory.

## Material acceptance

Reject:
- obvious procedural waves/periodicity unless materially justified;
- globally uniform grunge;
- one-off per-asset texture language when a location library exists;
- sterile constant roughness where the reference implies wetness, dirt, seam accumulation or contact variation.

## Efficiency acceptance

Target for the complete three-planter regression:
- context <= 30k tokens;
- stretch target <= 20k;
- no full persisted source echo;
- no unchanged-source reread without a concrete missing fact;
- project-local generated logic <= 400 lines where reusable executors cover the infrastructure;
- zero reusable-executor misses for provider probing, material-library resolution, quality selection and composition gating.

## Regression targets

```text
v0.13 runtime correctness retained
+ source quality suitable for usage class
+ composition quality PASS
+ shared location material language resolved
+ early visual gate PASS before runtime finishing
+ context budget PASS
```

A technically correct but visually generic planter remains a regression failure.

# Benchmark 84 — Lafar Restaurant v0.15 Full Location Reconstruction Regression

## Failure source

The v0.14 agent received the complete Lafar Restaurant reference set and a direct instruction to build the location asset-by-asset. The result was an under-authored blockout: generic floor/walls/ceiling, repeated weak chairs, missing central bar complex, missing backbar/rack/vegetation/material language, poor lighting, spatial penetrations and low correspondence to the hero concept.

This benchmark converts that failure into a release gate.

## Required route

```text
LOCATION_REFERENCE_INGEST
-> LOCATION_DESIGN_SYSTEM_GATE
-> LOCATION_SCENE_GRAPH
-> LOCATION_ASSET_MANIFEST
-> ARCHITECTURAL_ASSEMBLY
-> HERO_COMPOSITION
-> accepted fixed assets
-> furniture clusters
-> SPATIAL_RELATION_GATE
-> LOCATION_CLEARANCE_GATE
-> material/lighting/vegetation/props
-> LOCATION_REFERENCE_FIDELITY_GATE
-> LOCATION_COMPLETENESS_GATE
```

## Acceptance targets

- 100% required architectural systems present;
- 100% required HERO assets present and final;
- 100% required assets not `MISSING` or `PROXY` in final mode;
- zero unintended architecture/furniture penetrations;
- zero blocked required guest/service paths;
- no final instance sourced from unaccepted asset geometry;
- Location Design System PASS;
- reference composition score >= 0.85 unless a stronger calibrated threshold is available;
- HERO anchor scale error <= 3%;
- important orientation error <= 5°;
- location completeness PASS.

## Mandatory negative controls

Each mutation below must make the benchmark fail:

1. remove the main bar;
2. replace one required HERO asset with `PROXY`;
3. move a chair 200 mm into a wall;
4. block a declared guest aisle below minimum width;
5. replace location materials with one uniform grey material family;
6. mark a required spatial relation unsatisfied;
7. lower composition score below threshold.

A validator that stays green on any matching defect cannot own v0.15 acceptance.

# Benchmark 85 — Lafar Location Design System v0.16 Regression

## Why this benchmark exists

Repeated Lafar/Astera asset work showed that even improved individual reconstruction can drift because every task recreates materials, branding, emissive treatment and reusable subcomponents. The benchmark tests whether BlenderSkill can externalize that shared language once and reuse it.

## Fixture

Use existing accepted/known Lafar/Astera evidence from civic assets such as bench, planter, lamp, recycler/wayfinding where available. The benchmark does not require rebuilding all geometry.

## Required output structure

```text
<project>/Blender/DesignSystems/lafar/
    LOCATION_DESIGN_SYSTEM.md
    design_system.json
    sources.json
    asset_library_manifest.json
    LAFAR_ASSET_LIBRARY.blend   # when Blender resource packaging is exercised
    materials/
    branding/
    components/
    decals/
    profiles/
    nodegroups/
    families/
    organizations/astera_civic_systems/
```

The manifest links the v0.14 runtime material library:

```text
<project>/Assets/GameAssets/Materials/Locations/lafar/
```

## Minimum Lafar/Astera semantic fixture

At least these conceptual IDs must be representable:

```text
MAT_ASTERA_GRAPHITE_COMPOSITE_A
MAT_ASTERA_BRUSHED_ALUMINIUM_A
BRAND_ASTERA_PRIMARY
BRAND_ASTERA_SYMBOL
EDGE_ASTERA_CIVIC_OUTER_A
LIGHT_ASTERA_CIVIC_BLUE_A
WEATHER_LAFAR_MAINTAINED_WET_A
```

A reusable component such as an Astera utility/service panel should be registered when a valid source exists; absence of a real reusable source must not be filled with invented geometry solely to satisfy the benchmark.

## Pure-Python regression requirements

1. Missing design-system path + `create_if_missing=true` creates one canonical root and returns it.
2. Second resolve reuses exactly the same root.
3. Manifest final validation rejects a merely bootstrapped/empty system.
4. A populated READY Lafar manifest passes.
5. Inheritance resolves `LOCATION -> ORGANIZATION -> FAMILY` deterministically.
6. Locked Astera identity token override fails.
7. Hash-identical promoted resource is reused rather than duplicated.
8. Same resource ID with different hash fails.
9. Bench-like usage of canonical material/branding/lighting/weathering families passes conformance.
10. An unregistered one-off "almost equivalent" material fails without waiver.
11. Existing v0.9–v0.15 regression suites remain green.

## Blender runtime benchmark requirements

When run in the real Blender/RPG environment:
- create/update `LAFAR_ASSET_LIBRARY.blend` through Python;
- package only reusable approved datablocks;
- load at least one canonical Material and one reusable Object/NodeGroup through `bpy.data.libraries.load`;
- verify readback names against `asset_library_manifest.json`;
- prove a subsequent asset can consume resources without regenerating them.

## Success criterion

The benchmark succeeds when a future prompt can state only the location/organization/family plus its asset-specific references and receive the same canonical material/branding/form language without reconstructing that shared context from scratch.

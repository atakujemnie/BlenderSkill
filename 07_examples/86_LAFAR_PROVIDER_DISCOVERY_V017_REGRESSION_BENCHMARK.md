# Benchmark 86 — Lafar Provider Discovery v0.17 Regression

## Failure being prevented

A Lafar planter run reported no vegetation libraries and selected a custom procedural fallback while the active Blender 5.1 environment was known to contain multiple relevant add-ons. The report failed to distinguish ready-made vegetation asset libraries from procedural generators.

## Declared Blender environment fixture

```text
Blender 5.1
MPFB (MakeHuman for Blender) 2.0.15 — enabled
A.N.T. Landscape 0.2.0
Geo Nodes Guide 0.1.0
IvyGen 0.1.5
MCP 1.0.0 — enabled
Meshy official plugin 0.6.0
Sapling Tree Gen 0.3.7
Sverchok 1.4.0
```

The regression fixture intentionally contains no registered ready vegetation Asset Library.

## Required inventory result

The normalized inventory must contain canonical IDs:

```text
mpfb
ant_landscape
geo_nodes_guide
ivygen
mcp
meshy
sapling_tree_gen
sverchok
builtin_geometry_nodes
```

`ready_asset_sources_count` may be zero. `procedural_generators_count` must not therefore be zero.

## Vegetation routing check

For `requested_domain=GRASS`:
- Sapling must remain visible and be rejected as domain mismatch, not omitted;
- IvyGen must remain visible and be rejected as domain mismatch, not omitted;
- Sverchok must remain visible as a generic procedural candidate;
- Blender Geometry Nodes must remain visible as a generic built-in candidate;
- an empty Asset Library bucket must not produce the phrase/semantic state `NO_VEGETATION_PROVIDER`.

## Negative controls

1. Remove Sapling from discovery while keeping it in the expected-provider fixture -> `EXPECTED_PROVIDER_GATE FAIL` with `DISCOVERY_MISMATCH`.
2. Select Sapling for GRASS without an explicit capability override -> `PROVIDER_SELECTION_REPORT BLOCKED`.
3. Empty Asset Library + present procedural generators -> inventory PASS and generators remain reported.

## Acceptance

v0.17 passes only when discovery completeness is independently validated before fallback selection.
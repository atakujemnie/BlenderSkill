# Vegetation Provider Routing v0.17

## Source hierarchy

```text
approved project/Asset Library vegetation
-> specialized generator matching requested plant domain
-> general procedural backend
-> custom native generator
```

The hierarchy is evaluated only after installed-provider discovery.

## Domain routing examples

- `TREE`, `WOODY_PLANT` -> ready asset source, then Sapling if probed/suitable.
- `VINE`, `SURFACE_GROWTH` -> ready asset source, then IvyGen if probed/suitable.
- `GRASS`, `GROUNDCOVER`, ornamental broadleaf -> ready asset source; if no specialized provider exists, evaluate Geometry Nodes/Sverchok/general procedural route.
- `TERRAIN` -> A.N.T. Landscape or another terrain provider; it is not a vegetation source.

## Reporting law

When a ready vegetation Asset Library is absent but generators are installed, report exactly that distinction.

Example:

```text
READY_ASSET_SOURCE: NONE
PROCEDURAL_GENERATORS: Sapling, IvyGen, Sverchok, Geometry Nodes
REQUESTED_DOMAIN: GRASS
SPECIALIZED_MATCH: NONE
SELECTED_GENERAL_BACKEND: Geometry Nodes
```

Do not say `no vegetation providers`.

## Custom generator fallback

A custom generator requires:
- complete discovery inventory;
- expected-provider gate PASS when applicable;
- visible rejection reason for every stronger candidate;
- provider selection report;
- existing v0.14 quality-tier gate.

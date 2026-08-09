# Location Definition of Done

## Levels

```text
A LOCATION_STRUCTURE_COMPLETE
B LOCATION_LAYOUT_COMPLETE
C LOCATION_ART_DIRECTION_COMPLETE
D LOCATION_GAME_READY_COMPLETE
E LOCATION_PIPELINE_INTEGRATED
```

## A — STRUCTURE
Reference ingest, Design System, Scene Graph, Asset Manifest and architecture PASS.

## B — LAYOUT
A + required HERO/fixed assets accepted, zoning/spatial relations/circulation/clearance PASS, no final proxies.

## C — ART DIRECTION
B + shared material/light language, vegetation/props where required and Location Reference Fidelity PASS.

## D — GAME READY
C + runtime partitioning, source-asset LOD/collision, runtime material/texture/export validation.

## E — PIPELINE INTEGRATED
D + canonical runtime path/catalog and target-engine load/instantiation evidence.

The first failing level is the real status. Do not report `DONE` without the named highest passed level.

# Modular Architecture Assembly

## Purpose

Build floor, walls, corners, ceilings, openings, doors and partitions as an explicit system before furniture population.

## Required order

1. FFL/ground datum and footprint.
2. Wall axes and height.
3. Openings and door modules.
4. Corner/termination modules.
5. Floor raster.
6. Ceiling raster/channels.
7. Glass partitions/fixed greenery/recesses.
8. junction validation.

## Interface rules

Every module declares width/height/depth, pivot, interface edges, seam/gap policy, protected dimensions and repeatability.

Run assembly tests:
- A+A;
- A+B;
- repeated chain;
- inner/outer corner;
- end cap;
- wall-floor;
- wall-ceiling;
- opening boundary.

No final loose population until architecture stage passes.

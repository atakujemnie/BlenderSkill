# Grass, Ground Cover and Small Plants

## Target classes

Grass blades, sedges, reeds, flowers, weeds, moss clumps, succulent/rosette clusters, small Lafar alien plants and decorative planter fill.

## Authoring hierarchy

```text
blade/leaf primitive
-> plant clump
-> variation family
-> scatter population
```

Do not jump directly from one mesh to millions of realized blades.

## Geometry Nodes principles

- instance-first;
- expose density, height, width, bend, seed and variation selector;
- keep plant/clump variation separate from spatial scatter seed;
- realize only at the stage that requires mesh-level operations;
- provide exclusion/mask inputs;
- use semantic attributes for wind and variation.

## Density

Density is expressed as an ecological/visual contract, not as `Random Value` with an arbitrary count. Define target count or density per area, minimum spacing, cluster behavior and exclusion zones.

## Runtime

Small plants should preferentially share atlas/material families and instanced source meshes. Dense background fields may route to cards/impostors; hero planter plants may retain real leaf geometry longer.

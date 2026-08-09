# Benchmark 82 — Lafar Planter + Vegetation v0.13

## Purpose

First end-to-end benchmark for the procedural-generation layer. The target combines an exact/controlled hard-surface civic planter with procedural vegetation and therefore exercises the boundary between v0.12 reconstruction integrity and v0.13 organic generation.

## Required scenario

Create one Lafar planter composition containing:
- one hard-surface planter/container;
- soil insert;
- at least two accepted vegetation source variants;
- deterministic placement/variation seeds;
- runtime LOD plan;
- exportable game-ready assembly.

## Acceptance gates

### A. Container
- existing Shape/Appearance/Geometric Integrity gates pass when reference-driven;
- interior soil footprint/depth measured and persisted;
- no invalid wall/soil interpenetration.

### B. Provider
- active Blender 5.1 provider probe is recorded;
- no use of a provider solely because documentation claims compatibility;
- version-blocked providers remain blocked.

### C. Botanical generation
- `VEGETATION_BOTANICAL_GRAMMAR: PASS`;
- integer seed and parameter hash recorded;
- semantic parts recorded;
- fixed-seed reproduction signature stable;
- `VEGETATION_GENERATION_GATE: PASS`.

### D. Placement/composition
- deterministic scatter/anchor result;
- exclusions and minimum spacing respected;
- zero rootballs outside usable soil;
- zero stems intersecting planter wall;
- root depth <= soil depth;
- intentional canopy overlap allowed but visible clone repetition is reviewed.

### E. Runtime
For benchmark MID vegetation, initial target:
- authoring geometry may exceed runtime budget;
- LOD0 <= 30k triangles per source plant;
- LOD1 <= 14k;
- LOD2 <= 5k;
- LOD3 <= 1.2k;
- <= 3 material slots per source plant unless project profile overrides;
- leaf cards recommended when dense foliage exceeds LOD1 budget;
- impostor recommendation evaluated for background use;
- wind semantic attributes present before engine handoff;
- source variants are instanced where possible.

### F. Regression targets

```text
0 guessed third-party operator signatures
0 unseeded procedural production assets
0 fixed-seed reproduction mismatches
0 planter-wall/root/stem physical violations
0 runtime claims from raw high-poly generator output
0 lost provider/seed/provenance metadata
```

## Expected lesson

v0.13 passes only if BlenderSkill can create and control a vegetation system, not merely invoke a tree generator.

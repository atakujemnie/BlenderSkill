# Lafar Planter and Vegetation Playbook

## Asset architecture

```text
LAFAR_PLANTER_ASSEMBLY
├── PLANTER_CONTAINER   existing hard-surface/reconstruction owner
├── SOIL_INSERT         container-dependent owner
├── VEGETATION_FAMILY   procedural owner
└── COMPOSITION         cross-owner fit/placement contract
```

## Phase 1 — planter

If driven by concept/technical art, run the existing v0.12 reconstruction pipeline through `GEOMETRIC_INTEGRITY_GATE` and required fidelity gate. Explicitly expose the interior soil footprint/depth as composition data.

## Phase 2 — vegetation specification

For every required plant family define:
- form class;
- target height/crown range;
- stem/leaf language;
- branching/internode/phyllotaxis rules;
- season/color/material family;
- variation count;
- deterministic seeds.

Lafar flora may be alien but must be internally coherent.

## Phase 3 — provider

Probe built-in GN first for custom flora. Optional routes: NodeToPython for graph compilation, Sapling for trees, IvyGen for surface growth, compatible asset providers for licensed source plants.

## Phase 4 — variation family

Generate a small set of accepted source members, not every scene instance as unique heavy geometry. Preserve semantic parts and provenance.

## Phase 5 — planter composition

Create plant anchors inside the usable soil volume. Validate rootball depth/footprint and wall clearance. Then apply canopy composition and visual density.

## Phase 6 — runtime

Run `VEGETATION_RUNTIME_PREP` per source member. Prefer instancing of accepted source variants in the planter and across Lafar. Add wind attributes before export; use existing package/round-trip/runtime gates afterward.

## QA views

Use neutral hero, top and side views to check:
- planter silhouette;
- soil level;
- plant anchoring;
- density/negative space;
- wall penetration;
- excessive clone repetition;
- crown envelope.

## Do not

- realize every leaf/instance early;
- use one plant seed repeated identically around a plaza;
- hide wall/root penetration under soil material;
- accept a 100k+ triangle authoring plant as runtime-ready without an explicit budget plan.

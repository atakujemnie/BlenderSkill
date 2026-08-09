# Planter Container and Vegetation Composition

## Why this is a separate owner

The planter is hard-surface geometry; vegetation is procedural organic geometry. Their composition introduces independent physical constraints that neither sub-pipeline can prove alone.

## Container contract

Record:
- interior soil footprint;
- soil depth/top datum;
- wall thickness and forbidden wall volume;
- drainage/insert volumes if they reduce usable soil;
- visible soil surface;
- composition/exclusion zones.

## Plant contract

Each planted member records:
- root/stem anchor position;
- rootball radius/depth approximation;
- stem radius/contact;
- crown radius/height envelope;
- variant/seed.

## Hard constraints

```text
rootball inside usable soil footprint
rootball depth <= usable soil depth
stem does not penetrate planter wall
plant root/contact datum meets soil surface
required plant spacing satisfied
```

Canopy overlap may be allowed and often desirable; rootball overlap is warning/policy unless physically impossible.

## Composition validation

Run after both the planter interior and plant anchor specs exist, before claiming the combined prop accepted.

## Executor

`executors/planter_composition.py` currently supports rectangular and circular interior footprints. Blender adapters may later add arbitrary signed-distance/mesh-volume probes.

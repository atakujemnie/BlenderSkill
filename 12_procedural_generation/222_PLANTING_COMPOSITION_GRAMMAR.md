# Planting Composition Grammar

## Purpose

A valid planter is not a list of collision-free plant coordinates. Composition must describe masses, layers, rhythm, asymmetry and negative space.

## CompositionSpec

Record as applicable:
- focal masses and secondary masses;
- height layers;
- dominant/secondary/fill species shares;
- patch/cluster size ranges;
- canopy-overlap policy;
- exposed-soil target range;
- ground-cover target;
- asymmetry target;
- focal offset;
- rhythm/regularity policy;
- height-profile mode;
- intentional gaps/negative-space regions.

## Default visual laws

- prefer patches/masses over evenly spaced individual specimens;
- avoid visible periodic spacing unless the reference explicitly specifies it;
- repeated source variants require rotation/scale/morphology variation;
- canopy overlap may be deliberate even when rootball overlap is not;
- one dominant layer should not erase all secondary structure;
- composition must read as one planted system at gameplay distance.

## Validation

Physical `PLANTER_VEGETATION_COMPOSITION` remains mandatory. This grammar adds a separate visual/compositional owner; physical PASS cannot imply composition PASS.

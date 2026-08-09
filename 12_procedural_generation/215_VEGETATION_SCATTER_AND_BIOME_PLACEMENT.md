# Vegetation Scatter and Biome Placement

## Rule

Scatter is constrained placement, not random duplication.

## Inputs

```yaml
seed: integer
target_count: ...
min_spacing_m: ...
max_slope_deg: ...
min_biome_weight: ...
exclusion_regions: ...
proximity_fields: ...
cluster_policy: ...
variant_family: ...
```

Surface sampling may be performed by Blender/Geometry Nodes. Semantic selection must remain reproducible.

## Constraints

- slope;
- altitude/height band when relevant;
- surface/material/biome mask;
- wall/path/door exclusion;
- planter interior containment;
- minimum spacing;
- clustering or patchiness;
- proximity to water/architecture/lighting if the design specifies it.

## Two seeds

Prefer separate seeds for:
1. plant morphology/variant;
2. spatial placement.

This lets layout change without silently regenerating every plant shape.

## Validation

Persist selected candidate IDs/positions or a stable placement signature. Re-running with the same candidate set/spec/seed must yield the same placement signature.

## Executor

`executors/vegetation_scatter.py` performs deterministic semantic selection over pre-sampled candidates.

# Game-Ready Location Partitioning and Instancing

Runtime work starts after Location Completeness PASS.

Prefer:
- repeated accepted assets as instances;
- source-level LOD/collision rather than duplicate-specific geometry;
- static architecture partitioned by streaming/visibility needs;
- shared location material families/atlases where appropriate;
- occlusion/portal strategy aligned with actual room topology;
- preservation of accepted transforms and spatial relations.

Optimization must not silently merge geometry in a way that destroys protected openings, material boundaries, collision or placement invariants.

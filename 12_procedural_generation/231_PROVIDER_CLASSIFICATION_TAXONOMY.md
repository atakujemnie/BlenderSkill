# Provider Classification Taxonomy

## Source kind is not domain

Classify every discovered provider by both `source_kind` and `domains`.

### Source kinds

- `READY_ASSET_SOURCE` — library of reusable ready-made assets/materials.
- `PROCEDURAL_GENERATOR` — creates geometry/content algorithmically in Blender.
- `EXTERNAL_GENERATOR` — external service/process that can return generated assets.
- `UTILITY` — workflow/integration/helper tool, not a direct content source for the requested domain.
- `BUILTIN_BACKEND` — built-in Blender capability such as Geometry Nodes.

### Canonical domain examples

```text
TREE
WOODY_PLANT
GRASS
GROUNDCOVER
VINE
SURFACE_GROWTH
TERRAIN
PARAMETRIC_GEOMETRY
GEOMETRY_NODES
CHARACTER
EXTERNAL_3D_GENERATION
INTEGRATION
```

## Known v0.17 classifications

| Provider | Source kind | Domains |
|---|---|---|
| Blender Geometry Nodes | BUILTIN_BACKEND | GEOMETRY_NODES, PARAMETRIC_GEOMETRY, GENERIC_PROCEDURAL |
| Sapling Tree Gen | PROCEDURAL_GENERATOR | TREE, WOODY_PLANT |
| IvyGen | PROCEDURAL_GENERATOR | VINE, SURFACE_GROWTH |
| A.N.T. Landscape | PROCEDURAL_GENERATOR | TERRAIN |
| Sverchok | PROCEDURAL_GENERATOR | PARAMETRIC_GEOMETRY, GENERIC_PROCEDURAL |
| Meshy official plugin | EXTERNAL_GENERATOR | EXTERNAL_3D_GENERATION |
| MPFB / MakeHuman for Blender | PROCEDURAL_GENERATOR | CHARACTER |
| Geo Nodes Guide | UTILITY | GEOMETRY_NODES |
| MCP | UTILITY | INTEGRATION |

These classifications describe role, not runtime availability. Availability comes only from active runtime discovery/probe.

A provider may be visible in the report and still be rejected for the requested domain.
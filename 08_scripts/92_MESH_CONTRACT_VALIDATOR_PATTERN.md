# Mesh Contract Validator Pattern

## Skill ID

`MESH_VALIDATE`

## Purpose

Validate render meshes against an explicit per-object topology contract instead of reporting generic statements such as "no mesh defects" while boundary edges are still present.

## Topology intent is mandatory

Every mesh object entering GAME_READY validation declares one of:

```text
CLOSED_SOLID
OPEN_ASSEMBLY_PART
SURFACE_DETAIL
COLLISION
```

### `CLOSED_SOLID`

Requires:
- zero boundary edges;
- zero non-manifold edges;
- zero loose vertices/edges;
- zero zero-area faces;
- no duplicate vertices within configured tolerance.

### `OPEN_ASSEMBLY_PART`

Boundary edges are permitted only when:
- the exact boundary is intentional;
- it is covered/sealed by another owned assembly part;
- runtime backface assumptions permit it;
- the Feature/Game Asset Contract records the exception.

The validator must report the boundary count even when accepted.

### `SURFACE_DETAIL`

Floating/decal-like geometry may be open, but must additionally validate:
- visibility from intended views;
- no accidental z-fighting;
- no hidden placement behind the host surface;
- no unintended silhouette change unless owned by the feature.

### `COLLISION`

Use the active Engine Profile requirements. Prefer closed simple volumes unless the engine explicitly supports other collision forms.

## Compact report

```yaml
mesh_validation:
  object: BOL_MainBody
  topology_intent: CLOSED_SOLID
  status: FAIL
  verts: 128
  tris: 192
  boundary_edges: 64
  non_manifold_edges: 64
  loose_vertices: 0
  duplicate_vertices: 0
  zero_area_faces: 0
  uv_present: true
  reasons:
    - CLOSED_SOLID_HAS_BOUNDARY_EDGES
```

## Assembly-level validation

Also report:
- aggregate dimensions;
- origin/pivot;
- transforms;
- total triangles;
- material slots/submeshes;
- feature ownership;
- interpenetration/occlusion exceptions when relevant.

## Visibility validation for floating details

A floating feature is not valid merely because:
- the object exists;
- emission/material assignment is correct;
- its vertices are numerically near the host surface.

For a visible feature, require at least one visibility proof:
- QA render contains feature pixels in its ROI;
- ray/occlusion test shows the detail is not hidden by host geometry;
- geometric offset is proven outside the host surface along the correct normal.

This specifically prevents a local emitter or panel from being created inside a cylinder and silently disappearing.

## Candidate executor

`executors/mesh_validate.py`

Registry maturity stays `CONTRACT_READY` until benchmarked against the active Blender runtime and the project's topology policies.

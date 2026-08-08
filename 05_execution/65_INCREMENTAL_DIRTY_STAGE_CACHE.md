# Incremental Dirty-Stage Cache

## Purpose

A local fix must not force the agent to rerun the entire build/bake/export pipeline when earlier accepted artifacts are still valid.

The cache tracks dependencies and marks only affected stages/channels as dirty.

This is an execution-efficiency contract, not merely an optimization suggestion.

---

# Core model

```text
INPUT FACT
-> dependency graph
-> dirty artifacts only
-> targeted execution
-> validation
-> update signatures
```

Persist the cache as compact structured state or a small project-side file.

---

# Artifact record

```yaml
artifact:
  id: TEXTURE_EMISSIVE
  path: .../astera_bollard_emissive.png
  status: PASS
  dependencies:
    - UV_CONTRACT_ACS_BOLLARD_V1
    - MATERIAL_EMISSIVE_GRAPH
    - EMIT_REFERENCE_STRENGTH
  signature:
  dirty: false
  last_validation:
```

---

# Canonical dependencies

Typical artifacts:

```text
BLOCKOUT
FINAL_GEOMETRY
UV_CONTRACT
BASECOLOR
NORMAL
AO
ROUGHNESS
METALLIC
ORM
EMISSIVE
RUNTIME_MATERIAL
LOD0
LOD1
LOD2
LOD3
COLLISION
EXPORT_MODULE
EXPORT_COLLISION
CATALOG_ENTRY
```

---

# Dirty propagation examples

## Emission normalization change

```text
EMIT_REFERENCE_STRENGTH changed
-> EMISSIVE dirty
-> RUNTIME_MATERIAL dirty only if binding/parameter changes
-> EXPORT_MODULE dirty
```

Do not rebake BaseColor/Normal/AO/Roughness/Metallic.

## AO isolation fix

```text
AO source/isolation changed
-> AO dirty
-> ORM dirty
-> EXPORT_MODULE dirty
```

Do not rebake BaseColor/Normal/Emissive.

## Base Color graph change

```text
material Base Color graph changed
-> BaseColor dirty
-> EXPORT_MODULE dirty
```

Other channels remain clean unless they share the changed nodes/data.

## UV contract change

```text
UV contract changed
-> all maps using that UV set dirty
-> all LOD mesh UV validation dirty
-> runtime material QA dirty
-> export dirty
```

## Geometry change

At minimum consider:
- AO dirty;
- Normal dirty when geometry/tangent source changes;
- geometry-position/object-coordinate procedural channels dirty;
- affected LOD/export meshes dirty;
- collision only if collision-relevant volume changed.

Do not blindly dirty all material channels if they are independent of geometry.

## Decal change

If decals use a separate project atlas/material:

```text
decal content changed
-> decal asset/material dirty
-> export dirty
```

Structural PBR maps remain clean.

---

# Signatures

A signature may use:
- stable content hash;
- selected parameter hash;
- file modification state plus explicit dependencies;
- another deterministic project mechanism.

Do not hash or serialize the entire Blender scene when a narrow parameter signature is sufficient.

---

# Accepted artifact reuse

Before running an expensive operation:

```text
if artifact PASS
and dirty == false
and dependencies unchanged
-> REUSE
```

Report:

```yaml
bake_plan:
  reuse:
    - BaseColor
    - Normal
    - AO
    - Roughness
    - Metallic
  execute:
    - Emissive
```

This report should be small enough to remain in active context.

---

# Failure behavior

A failed artifact does not automatically invalidate siblings.

Example:
- Emissive mask outside allowed emitter region -> Emissive FAIL;
- BaseColor PASS remains valid.

Invalidate siblings only when they share the failed dependency.

---

# Pipeline boundary

Changing exported packaging without changing mesh/material data should not force rebake.

Changing runtime material bindings without changing texture content should not force rebake.

Changing catalog registration should not force Blender rebuild/export unless the project contract explicitly requires regenerated metadata inside the asset.

---

# Benchmark metric

Track:

```text
full_stage_recomputes
channels_rebaked
clean_artifacts_reused
expensive_operations_avoided
```

A v0.6 agent should reduce full bake reruns substantially compared with the v0.5 bollard continuation benchmark.

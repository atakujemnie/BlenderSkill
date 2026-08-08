# Game-Ready Texture Bake Gate

## Purpose

A Blender material that looks correct is not automatically a runtime material.

Before claiming `GAME_READY_COMPLETE`, every Blender-only material effect must have an explicit runtime disposition:

```text
BAKE
RECREATE_IN_ENGINE
EXPORT_NATIVELY_VERIFIED
REMOVE_BY_DESIGN
```

No effect may remain in an undefined state.

---

# Important correction

A separate high-poly mesh is **not required for every bake**.

Different bake purposes have different source requirements.

### Procedural/material bake
Can bake directly from the authoring material/mesh when the purpose is to convert Blender procedural information into textures, for example:
- BaseColor variation;
- roughness breakup;
- emissive masks;
- procedural dirt/wear;
- tile/detail masks.

### High-to-low geometry bake
Requires an appropriate source surface when transferring geometric detail, for example:
- high-poly normal detail;
- curvature/AO dependent on high-resolution geometry;
- sculpted wear;
- recessed seams/fasteners moved from geometry to normal maps.

Do not block all texture baking merely because a separate high-poly object does not exist.

---

# Bake decision matrix

For every surface feature record:

```yaml
surface_feature:
  id: MAT_DETAIL_03
  description: fine powder-coat roughness variation
  authoring_source: PROCEDURAL_SHADER
  runtime_strategy: BAKE
  target_channel: ORM.R
  required_resolution: 1024
```

Common outputs:
- BaseColor;
- Normal;
- ORM or project-specific packed channels;
- Emissive;
- Alpha/masks when required.

The Engine Profile defines actual packing and color-space requirements.

---

# Bake preconditions

Before bake:
- final/approved low mesh exists;
- UVs are final enough for runtime;
- texel density is accepted;
- intended overlaps are documented;
- tangent/normal strategy is known;
- material segmentation is stable;
- output resolution/padding are defined;
- high-to-low source/cage exists when the requested channel requires it.

Do not bake before silhouette and primary geometry are accepted.

---

# Civic hard-surface finishing

For dark civic/game props, the bake gate should explicitly consider whether the runtime needs:
- broad low-frequency roughness variation;
- subtle micro-normal breakup;
- restrained dirt accumulation at protected joints/base interfaces;
- sparse wear on contact/maintenance edges;
- brushed directionality for metal;
- decal/signage alpha or color;
- emissive mask.

A perfectly uniform roughness field is usually a deliberate material decision, not a default.

Do not add random grunge everywhere. Variation must follow material/manufacturing/exposure logic.

---

# Geometry-to-normal transfer decision

A small feature may leave LOD0 geometry and become texture detail at lower LOD or final runtime if:
- it does not materially affect protected silhouette;
- parallax is not required at expected viewing distance;
- normal-map representation survives mip reduction;
- the feature remains recognizable where required.

Examples:
- fine vertical seams;
- tiny panel fasteners;
- shallow service markings;
- micro wear.

Do not bake away a reference-critical deep recess or silhouette break merely to hit a triangle target.

---

# Validation

Required checks depend on outputs, but normally include:
- no missing islands;
- no unintended projection bleed;
- padding/mip safety;
- normal orientation/tangent consistency;
- correct color-space treatment;
- channel packing matches Engine Profile;
- emissive mask aligns with emitting geometry;
- exported runtime material references the produced textures.

A texture file existing on disk is not sufficient evidence.

---

# Gate result

```yaml
bake_gate:
  required: true
  basecolor: PASS
  normal: PASS
  orm: PASS
  emissive: PASS
  runtime_material_binding: PASS
  status: PASS
```

If procedural materials are still Blender-only and no verified runtime replacement exists:

```text
GAME_READY_COMPLETE = FAIL
reason = BLENDER_ONLY_MATERIAL_STATE
```

---

# Skip conditions

Bake may be skipped only if one of these is proven:
- target engine natively recreates the intended material through a validated pipeline;
- the material is intentionally constant/simple and needs no texture data;
- the requested completion level stops before game-ready runtime material production.

Record the reason. Never silently skip the bake because the Blender viewport already looks good.

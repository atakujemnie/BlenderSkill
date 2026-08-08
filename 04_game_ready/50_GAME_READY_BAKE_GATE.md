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

For actual bake execution use:
- `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`;
- `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`;
- `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`;
- `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

The gate defines **what must be true**. The v0.6 execution layer defines **how the agent performs and proves it efficiently**.

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
- tile/detail masks;
- procedural micro-normal/bump detail.

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
  target_channel: ORM.G
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
- UV contract is explicit and validated;
- runtime LODs that share textures declare the same `UV_CONTRACT_ID`;
- texel density tradeoff is accepted;
- intended overlaps are documented;
- tangent/normal strategy is known;
- material segmentation is stable;
- output resolution/padding are defined;
- external UV owners such as decals/dynamic displays are identified;
- high-to-low source/cage exists when the requested channel requires it;
- runtime scene has an isolation plan for AO/ray-dependent passes.

Do not bake before silhouette and primary geometry are accepted.

Missing UV atlas assignment is FAIL. Do not silently continue.

---

# Channel semantics are part of the gate

The bake must preserve the **authored runtime property**, not merely produce a plausible image.

Examples:
- metallic BaseColor must not be inferred from a DIFFUSE response that can be black for metal;
- metallic scalar must not become 1.0 across unrelated dielectric regions;
- non-emitting materials must remain black in Emissive even if their Principled emission color default is non-black;
- authoring emission strength must not clip texture RGB and destroy hue;
- AO must not be contaminated by unrelated render-visible helper geometry.

Use the v0.6 channel semantics protocol.

---

# Operator success gate

A bake call is PASS only if:
1. all contributing material slots have the correct selected+active target image node;
2. the bake operator returns `FINISHED`;
3. the output image passes semantic validation.

No Python exception is **not** sufficient evidence.

`{'CANCELLED'}` is FAIL.

---

# Civic hard-surface finishing

For dark civic/game props, the bake gate should explicitly consider whether runtime needs:
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

# Incremental execution

Bake is multi-artifact work.

Do not rebake accepted channels after a local repair unless a dependency changed.

Examples:

```text
AO isolation fix -> AO + packed ORM dirty
Emissive normalization fix -> Emissive dirty
UV contract fix -> all channels using that UV set dirty
```

Use the Dirty-Stage Cache and record reused vs recomputed channels.

---

# Validation

Required checks depend on outputs, but normally include:
- no missing islands/semantic parts;
- no unintended projection bleed;
- padding/mip safety;
- normal orientation/tangent consistency;
- correct color-space treatment;
- channel packing matches Engine Profile;
- material-family region expectations;
- emissive mask aligns with emitting geometry/UV regions;
- no unexplained all-zero/all-one/constant maps;
- exported runtime material references produced textures;
- baked runtime mesh/material visually passes QA.

A texture file existing on disk is not sufficient evidence.

Use `BAKE_VALIDATE` where available.

---

# Runtime package closure

The bake gate is not complete at image generation.

Required closure:

```text
baked images PASS
-> runtime material binding PASS
-> runtime LOD UV contract PASS
-> export PASS
-> exported material/image readback PASS
-> baked-runtime QA PASS
```

If project packaging has specific LOD/handedness/material rules, apply `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`.

---

# Gate result

```yaml
bake_gate:
  uv_contract: PASS
  operator_binding: PASS
  basecolor: PASS
  normal: PASS
  orm:
    ao: PASS
    roughness: PASS
    metallic: PASS
  emissive: PASS
  runtime_material_binding: PASS
  export_readback: PASS
  baked_runtime_qa: PASS
  reused_channels: []
  recomputed_channels: []
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
- requested completion level stops before game-ready runtime material production.

Record the reason. Never silently skip bake because Blender viewport already looks good.

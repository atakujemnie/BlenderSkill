# Blender Agent Skill — Game Assets Trim Sheet UV Texturing

## Purpose

This module defines how a Blender AI agent classifies game-asset surfaces, decides when trim sheets are appropriate, maps UVs to reusable trim regions deterministically, and validates a production-safe result.

It replaces the previous short trim-sheet note with a production skill while keeping this canonical path stable.

The agent must reason in terms of:

`surface strategy -> trim region -> UV orientation -> physical texture scale -> material reuse -> validation`

not in terms of manual UV Editor clicks.

---

## 1. Relationship to other canonical skills

This skill owns **reusable banded UV/material mapping**.

It does not own:
- geometric seam creation — use `blender-agent-procedural-hard-surface-panel-lines.md` or the relevant geometry skill;
- general UV/PBR policy — see `03_modeling/34_UV_TEXEL_DENSITY_MATERIALS.md`;
- decals and unique local graphics — see `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`;
- runtime material portability — see `04_game_ready/43_TEXTURE_MATERIAL_RUNTIME.md`;
- draw-call/instancing policy — see `04_game_ready/46_DRAW_CALLS_INSTANCING_AND_BATCHING.md`;
- mip/padding/compression policy — see `04_game_ready/47_TEXTURE_PACKING_AND_MIP_SAFETY.md`.

Trim sheets are therefore one part of a hybrid production strategy, not a replacement for geometry, decals, tiling materials, or unique bakes.

---

## 2. When to use trim sheets

Prefer this skill when most of the following are true:
- the asset belongs to a modular or repeated family;
- many assets share the same material language;
- the surface is a long strip, border, rail, frame, casing edge, profile, seal, vent band, panel border, or emissive band;
- detail can be reused without unique storytelling;
- reducing unique texture sets is valuable;
- the trim can preserve its intended direction and physical scale.

Typical candidates:
- wall and corridor modules;
- door/window frames;
- façade modules;
- benches, bollards, railings and kiosks;
- repeated furniture frames;
- sci-fi panel borders;
- emissive strips;
- rubber seals and painted/metallic trims.

---

## 3. When not to use trim sheets

Do not force a trim workflow when:
- the feature changes silhouette and therefore belongs in geometry;
- the surface needs a unique high-to-low bake over most of its area;
- unique wear, damage or narrative information dominates;
- the shape is strongly organic and cannot be mapped coherently to reusable bands;
- a broad homogeneous surface is better served by a tiling material;
- a small unique graphic is better served by a decal;
- the available trim catalog has no semantically compatible region.

Hero assets may still use trim sheets for structural sub-parts, but unique surfaces should not be made generic merely to satisfy reuse.

---

## 4. Surface strategy decision tree

Before creating UVs, classify each semantically coherent visible surface group:

```text
SURFACE
|
+-- repeated structural strip / frame / border
|      -> TRIM
|
+-- broad homogeneous surface
|      -> TILING
|
+-- small unique graphic / marking
|      -> DECAL
|
+-- unique hero surface / bespoke baked detail
|      -> UNIQUE_UV_OR_BAKE
|
+-- tiny depth-only repeated detail
       -> GEOMETRY / NORMAL / TRIM HYBRID
```

The agent must not default to a unique texture set before this classification.

---

## 5. Semantic trim-sheet contract

### Trim sheet

```yaml
trim_sheet:
  id: LAFAR_TRIMS_01
  material_name: MTL_LAFAR_TRIMS_01
  orientation: HORIZONTAL
  uv_space: [0.0, 0.0, 1.0, 1.0]
  texture_resolution_px: [2048, 2048]
  texture_set:
    base_color: /textures/LAFAR_TRIMS_01_basecolor.png
    normal: /textures/LAFAR_TRIMS_01_normal.png
    roughness: /textures/LAFAR_TRIMS_01_roughness.png
    metallic: /textures/LAFAR_TRIMS_01_metallic.png
```

### Trim region

```yaml
trim_region:
  id: PAINTED_METAL_EDGE_MEDIUM
  u_min: 0.0
  u_max: 1.0
  v_min: 0.68
  v_max: 0.80
  role: STRUCTURAL_EDGE
  material_family: PAINTED_METAL
  profile_class: EDGE
  width_class: MEDIUM
  direction: U
  allow_u_tiling: true
  allow_mirror: true
```

### Surface assignment

Persistent intent should use a semantic face-group identifier, attribute, or other stable region identity.

```yaml
trim_assignment:
  object: Bench_Frame
  surface_id: OUTER_FRAME
  strategy: TRIM
  trim_sheet: LAFAR_TRIMS_01
  trim_region: PAINTED_METAL_EDGE_MEDIUM
  orientation: AUTO
  texel_density_px_per_m: 512
  allow_overlap: SHARED_TRIM_ONLY
```

Raw face indices may be used as short-lived execution data, but must not be the only persistent identity because topology edits can invalidate them.

---

## 6. Standard semantic operations

The execution layer should expose operations equivalent to:

- `TRIM_ANALYZE_ASSET`
- `TRIM_CLASSIFY_SURFACES`
- `TRIM_SELECT_REGION`
- `TRIM_UNWRAP_LINEAR_STRIP`
- `TRIM_ALIGN_TO_REGION`
- `TRIM_MATCH_PHYSICAL_SCALE`
- `TRIM_APPLY_MATERIAL`
- `TRIM_VALIDATE`
- `TRIM_REPAIR`

The LLM should normally call these semantic operations instead of generating a new low-level UV implementation for every asset.

---

## 7. Face/surface grouping

A trim assignment begins with coherent surface groups.

Good groups are:
- geometrically continuous or intentionally related;
- materially coherent;
- similarly oriented;
- semantically reusable.

Example:

```text
Bench_Frame
+-- OUTER_FRAME       -> TRIM
+-- INNER_SUPPORTS    -> TRIM or TILING
+-- UNDERSIDE_HIDDEN  -> simplified TILING/TRIM
+-- SEAT_BRACKETS     -> TRIM
+-- LOGO_REGION       -> DECAL
```

Do not combine unrelated surfaces merely because they are adjacent in topology.

---

## 8. Region-selection logic

Choose a trim region by semantic compatibility, in this order:

1. material family;
2. role/function;
3. profile class;
4. width class / physical appearance;
5. directional constraints;
6. visibility importance;
7. family consistency with sibling assets.

A heavy painted structural edge must not receive a plastic decorative band merely because that region happens to fit the UV island.

For a coherent asset family, reuse the same approved region for the same semantic role whenever possible.

---

## 9. Orientation rules

For a horizontal trim sheet:
- the long/repeating axis normally spans `U`;
- band identity is controlled by the selected `V` interval.

For a vertical trim sheet, invert the logic.

When `orientation=AUTO`:
1. determine the dominant world/object-space direction of the surface group;
2. determine the trim's repeat direction;
3. choose a discrete UV rotation that preserves the material's intended direction;
4. validate the result visually.

Do not mirror directional wear, text, brushing, gradients, asymmetrical normal details or one-way patterns unless the trim region explicitly permits mirroring.

---

## 10. Physical scale and texel density

`texel_density` must always carry a unit. Prefer an explicit field such as:

`texel_density_px_per_m`

Do not store a bare value such as `512` without defining whether it means px/m, px/cm, or a project-specific class.

### Important trim-specific rule

A trim sheet is not ordinary unique UV packing.

Across the **band width**, the region often represents a specific physical trim width/profile. The agent must preserve that design relationship and must not arbitrarily rescale the island just to hit a generic texel-density number.

Along the **repeat direction**, scaling/tiling may be permitted when the trim was authored for repetition.

Therefore `TRIM_MATCH_PHYSICAL_SCALE` should consider:
- texture resolution;
- trim-region pixel width/height;
- represented real-world trim width, when defined;
- project texel-density target;
- whether U/V tiling is permitted.

Project tolerances may define warning/fail bands. Suggested percentages are heuristics, not universal standards.

---

## 11. UV mapping strategies

Use the simplest valid strategy.

### Linear strip mapping
For rails, frames, bands and near-rectangular strips.

### Aligned quad strip
For connected quad sequences that must maintain continuous spacing and orientation.

### Box-like decomposition
For rectangular frame objects where different sides map independently to the same compatible trim family.

### Hybrid mapping
A single object may legitimately use:
- trim sheet for structural borders;
- tiling material for broad surfaces;
- decals for branding;
- unique UV/bake for hero regions.

Hybrid classification is often preferable to forcing the whole object into one technique.

---

## 12. Intentional UV reuse and overlap

Trim sheets intentionally reuse the same texture regions across multiple surfaces and assets.

Therefore overlap is **not automatically an error**.

Classify overlap as:
- `INTENTIONAL_SHARED_TRIM` — allowed;
- `INTENTIONAL_MIRROR` — allowed only if region semantics permit;
- `ACCIDENTAL_CROSS_REGION` — fail;
- `ACCIDENTAL_INCOMPATIBLE_STACK` — fail.

Validation must distinguish intentional trim reuse from accidental UV collisions.

---

## 13. Tiling along the trim axis

A region may allow UVs to extend/repeat along its long axis only if:
- the texture was authored as repeatable in that direction;
- sampler/wrap behavior in the target runtime supports it;
- repetition cannot sample neighboring atlas regions incorrectly;
- padding/mips remain safe.

`allow_u_tiling` or `allow_v_tiling` must be part of the region contract when relevant.

Do not assume atlas boundaries are safe under repeat wrapping.

---

## 14. Materials and runtime cost

Trim sheets can reduce unique texture memory and improve visual consistency, but they do **not automatically guarantee fewer draw calls**.

Actual runtime cost depends on:
- material slots;
- shader/render state;
- engine batching;
- texture bindings;
- instancing strategy.

The agent should reuse the same material instance/data-block when possible and avoid duplicate material slots that point to equivalent trim materials.

A heuristic such as `1 material ideal, 2 acceptable, 3+ justify` may be useful for simple environment props, but it is not a global engine rule. The engine profile has final authority.

---

## 15. Decal and tiling fallback

Use decals for:
- logos;
- numbers;
- warnings;
- local UI labels;
- unique marks.

Use tiling materials for:
- large homogeneous walls;
- floors;
- ceilings;
- broad painted-metal panels without banded detail.

Never distort a trim region to solve a problem that belongs to another texturing strategy.

---

## 16. Hidden surfaces

Hidden/internal surfaces may receive:
- simplified tiling mapping;
- a generic low-priority trim region;
- intentionally stacked UVs;
- no high-fidelity treatment when they cannot be observed and runtime allows it.

Do not spend premium trim logic on invisible cavities without a project requirement.

---

## 17. Blender API strategy

Prefer direct data access and controlled BMesh/data-layer operations over UI-dependent editing.

The executor should:
- resolve the semantic surface group;
- ensure/reuse the UV map;
- inspect UV loops for the selected polygons;
- unwrap/project by a deterministic algorithm or a controlled operator adapter;
- rotate/scale/translate UV coordinates directly;
- ensure/reuse the intended material data-block and slot;
- validate the resulting loops against the region contract.

Any context-sensitive unwrap operator must be isolated behind a tested adapter and followed by deterministic UV transformation and validation.

---

## 18. Suggested executor architecture

```text
blender_agent/
  trim_sheets/
    analysis.py
    surface_groups.py
    region_catalog.py
    region_selection.py
    uv_mapping.py
    physical_scale.py
    material_assignment.py
    validation.py
    repair.py
```

Example high-level contract:

```python
result = trim.apply(
    target="Bench_Frame",
    surface="OUTER_FRAME",
    sheet="LAFAR_TRIMS_01",
    region="PAINTED_METAL_EDGE_MEDIUM",
    orientation="AUTO",
    physical_scale="PROJECT",
)
```

---

## 19. Validation

Every autonomous trim operation must validate at least:

### Structural
- target mesh exists;
- semantic surface group resolves;
- UV layer exists;
- trim material exists/is reused;
- selected region exists in the catalog.

### UV
- assigned loops remain in the allowed band orthogonal to the repeat axis;
- any out-of-0..1 tiling is explicitly allowed;
- no accidental sampling of neighboring trim regions;
- orientation is correct;
- mirroring is semantically allowed;
- overlap classification is intentional.

### Scale
- physical trim width/profile is plausible and consistent;
- texel-density class/target is respected where applicable;
- sibling assets using the same semantic region remain consistent.

### Runtime
- duplicate materials are not created;
- material-slot growth is justified;
- mip/padding rules remain safe;
- the target engine can reproduce the material behavior.

---

## 20. Validation report

```yaml
trim_validation:
  object: Bench_Frame
  surface: OUTER_FRAME
  region: PAINTED_METAL_EDGE_MEDIUM
  result: PASS
  checks:
    semantic_surface_resolved: PASS
    region_role_compatible: PASS
    orientation: PASS
    band_bounds: PASS
    repeat_axis: PASS
    overlap: INTENTIONAL_SHARED_TRIM
    physical_scale: PASS
    texel_density_px_per_m:
      target: 512
      measured: 498
      status: PASS
    material_reuse: PASS
```

Do not return PASS merely because UV coordinates exist.

---

## 21. Repair strategy

Repair the narrowest failure:

- wrong semantic region -> re-run region selection;
- wrong orientation -> rotate/reverse the strip;
- stretching -> split into more coherent surface groups;
- wrong physical width -> correct band/scale selection;
- generic density mismatch -> recalculate scale without violating the trim profile;
- cross-region leakage -> clamp/re-fit orthogonal band occupancy;
- inappropriate trim strategy -> reclassify as TILING, DECAL, UNIQUE or GEOMETRY;
- excessive material slots -> consolidate equivalent materials.

Prefer local repair over complete remapping when the failure is local.

---

## 22. Common failure modes

- choosing a region by geometric fit instead of semantic material role;
- rotating directional trim incorrectly;
- treating any UV overlap as invalid even though trim reuse is intentional;
- using a bare, unitless `texel_density` value;
- stretching the narrow axis of a trim until its physical profile is wrong;
- allowing UV tiling to sample neighboring atlas regions;
- creating duplicate materials for the same trim sheet;
- forcing unique hero surfaces into generic trim regions;
- forcing large homogeneous surfaces into a narrow trim band;
- assuming trim sheets automatically reduce draw calls;
- persisting only raw polygon indices after topology-changing operations.

---

## 23. Autonomous decision table

| Condition | Action |
|---|---|
| Repeated structural border/profile | TRIM |
| Broad homogeneous area | TILING |
| Unique local graphic | DECAL |
| Unique baked hero area | UNIQUE_UV_OR_BAKE |
| Feature changes silhouette | GEOMETRY |
| No compatible trim region | Escalate/reclassify |
| Directional region + requested mirror | Validate direction before mirroring |
| Shared trim overlap | Allow and classify intentionally |
| Runtime sampler cannot safely repeat atlas axis | Keep UV inside safe region / use alternative |

---

## 24. Completion criteria

A trim-sheet assignment is complete only when:

```text
[ ] surface strategy is classified
[ ] semantic surface group is stable
[ ] trim region is semantically compatible
[ ] material is reused rather than duplicated unnecessarily
[ ] UV orientation is correct
[ ] physical trim scale is correct
[ ] texel-density unit/target is explicit where used
[ ] intentional overlap/tiling is classified
[ ] UVs do not leak into unrelated regions
[ ] mip/padding behavior is safe
[ ] runtime material behavior is supported
[ ] validation report is PASS or documented WARN
```

---

## 25. Final instruction

Think in terms of **surface strategy and resource reuse**, not manual UV manipulation.

The correct pipeline is:

`classify -> choose region -> map -> preserve physical scale -> reuse material -> validate -> repair`

Trim sheets are successful when they preserve the asset's design language while reducing unnecessary unique texture work without creating hidden runtime or UV problems.
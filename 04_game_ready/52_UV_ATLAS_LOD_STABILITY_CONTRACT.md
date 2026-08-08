# UV Atlas and LOD Stability Contract

## Purpose

A baked runtime texture is useful only if the bake source and every runtime mesh sample the same semantic UV layout.

This contract prevents a common silent failure:

```text
bake source uses correct atlas
runtime LODs keep raw/default UVs
-> exported model reads valid textures through wrong coordinates
```

It also prevents object-name suffixes such as `.001` from silently breaking atlas assignment.

---

# 1. Stable semantic part identity

Do not use transient Blender object names as the primary UV atlas key.

Bad:

```python
UV_RECTS.get(obj.name)
```

because Blender may rename duplicates:

```text
BOL_MainBody
BOL_MainBody.001
BOL_MainBody.002
```

Preferred identity:

```text
semantic_part_id = BODY_MAIN
uv_contract_id = ACS_BOLLARD_V1
```

Store identity in:
- explicit build data;
- custom property;
- Feature Contract / object registry;
- another deterministic semantic identifier.

Name normalization may be used as a compatibility fallback, but it must emit a warning and must not be the canonical identity mechanism.

---

# 2. UV contract data model

Example:

```yaml
uv_contract:
  id: ACS_BOLLARD_V1
  texture_size: 1024
  padding_px: 16
  parts:
    BODY_MAIN:
      rect: [0.00, 0.00, 1.00, 0.46]
      owner: STRUCTURAL_ATLAS
    BASE_PLATE:
      rect: [0.00, 0.56, 1.00, 0.76]
      owner: STRUCTURAL_ATLAS
    BRAND_DECAL:
      owner: PROJECT_DECAL_ATLAS
      external: true
    DISPLAY_DYNAMIC:
      owner: DYNAMIC_SCREEN
      dedicated_uv_0_1: true
```

Every runtime mesh part must resolve to exactly one declared UV owner.

---

# 3. One contract across bake source and LODs

Atlas assignment belongs in the reusable mesh/LOD construction path, not only in the bake script.

Required:

```text
build part
-> assign semantic part ID
-> assign/validate UV contract
-> construct bake source OR runtime LOD
```

Do not implement:

```text
build runtime LODs with default UV
build second bake source
apply atlas only to bake source
```

That pipeline can produce perfect textures and a broken exported model.

---

# 4. Missing assignment is a hard failure

Never silently skip a part when no atlas record is found.

Required behavior:

```yaml
uv_contract_validation:
  required_parts: 9
  assigned_parts: 8
  missing:
    - BODY_MAIN
  status: FAIL
```

Do not continue to bake/export.

---

# 5. Lower LOD behavior

A lower LOD may omit a semantic part, but remaining parts must retain their UV ownership and contract.

Example:

```text
LOD0: BODY + BASE + PANEL + BOLTS + EMITTER
LOD1: BODY + BASE + PANEL + EMITTER
LOD2: BODY + BASE + EMITTER
```

The removal of `BOLTS` must not cause surviving parts to be repacked into new atlas regions if all LODs are expected to share the same texture set.

If LOD-specific repacking is intentionally used, it becomes a different `UV_CONTRACT_ID` and requires its own texture/binding strategy.

---

# 6. Semantic correspondence

Simply normalizing arbitrary existing UV bounds into the same rectangle does not always guarantee meaningful correspondence between LODs.

For procedural/parametric assets prefer UV generation from stable geometric parameters:
- revolution angle + profile distance;
- local planar coordinates;
- normalized part coordinates;
- explicit seam/axis rules.

This lets different segment counts sample corresponding locations.

A generic min/max remap may be acceptable only when the distortion and cross-LOD correspondence have been validated for that part class.

---

# 7. Dedicated spaces must remain dedicated

Do not mix these into the structural bake atlas unless explicitly required:
- shared project decal atlas;
- logo atlas;
- dynamic display surface;
- video/render-target surface;
- externally tiled materials;
- lightmap UV.

Dynamic displays normally require their own deterministic full `0..1` UV space.

---

# 8. Padding and edge bleed

Atlas rectangles must reserve sufficient padding for:
- bake margin;
- mip filtering;
- compression;
- bilinear sampling.

Record padding in pixels and derive normalized gutter from texture resolution.

Do not let bake margin cross semantic part boundaries.

---

# 9. Texel density

Fixed atlas regions may intentionally have unequal texel density.

This is acceptable when documented and driven by:
- projected size;
- visual importance;
- repeated placement frequency;
- reference detail density;
- runtime budget.

Do not pretend a 1024 atlas can maintain impossible uniform density on a very tall/long asset.

Record the tradeoff explicitly.

---

# 10. Validation

Before bake:
- unique contract ID;
- all required part IDs resolved;
- no undeclared rect overlap;
- rects inside 0..1;
- padding sufficient;
- dedicated/external UV owners excluded from structural atlas;
- runtime LOD meshes report same contract ID.

After export:
- read back UV set presence;
- verify expected material/texture binding;
- render/inspect baked runtime LOD0;
- sample at least one known region per material family when debugging.

---

# Compact report

```yaml
uv_contract:
  id: ACS_BOLLARD_V1
  texture_size: 1024
  required_parts: 9
  assigned_parts: 9
  external_parts:
    - BRAND_DECAL
  lods:
    LOD0: PASS
    LOD1: PASS
    LOD2: PASS
    LOD3: PASS
  rect_overlap: PASS
  padding: PASS
  status: PASS
```

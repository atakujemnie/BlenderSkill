# Bake Output Validation Pattern

## Purpose

Baked images require semantic validation. File existence and a successful operator return are necessary but not sufficient.

The validator should reduce image data locally and return compact statistics/failing regions rather than full pixel arrays.

---

# Generic image checks

For every output record:
- dimensions;
- color space;
- per-channel min/max/mean;
- nonzero fraction;
- clipped-low/clipped-high fraction when meaningful;
- unexpected constant-image detection;
- file path and modification state.

Example:

```yaml
image:
  channel: emissive
  size: [1024, 1024]
  min_rgb: [0.0, 0.0, 0.0]
  max_rgb: [0.259, 0.745, 1.0]
  nonzero_fraction: 0.052
  status: PASS
```

Do not send the complete pixel buffer to the LLM.

---

# BaseColor checks

Validate against material expectations.

Examples:
- expected metallic/brushed-aluminium atlas region must not become black merely because a DIFFUSE response was baked;
- dark graphite may legitimately be near black, so use region/material-aware thresholds rather than one global minimum;
- unexplained white/black full-atlas output is FAIL.

When a known UV region belongs to a material family, sample/aggregate that region separately.

---

# Normal checks

For tangent-space normals:
- verify image is not all zero/black;
- verify blue/Z component is generally positive where expected;
- detect impossible/degenerate constant values according to the material contract;
- verify color space is Non-Color;
- verify runtime tangent basis separately.

Do not require an arbitrary exact mean such as `[0.5, 0.5, 1.0]`; procedural detail may legitimately shift the distribution.

---

# AO checks

AO must not be globally black/near-zero because an unrelated render-visible object enclosed the asset.

Also do not require AO to have strong variation when the geometry is genuinely unoccluded.

Use configured expectations:

```yaml
ao_expectation:
  allow_constant_white: false
  max_near_black_fraction: 0.10
  required_occluded_regions:
    - BASE_RECESS
```

The specific thresholds belong to the asset/project validator.

---

# Roughness checks

Validate:
- values inside expected 0..1 range;
- not unexpectedly constant when authored breakup is required;
- material-family regions roughly match intended roughness bands;
- no color-space transform.

A maintained civic asset with authored roughness breakup should not collapse to one uniform scalar after bake.

---

# Metallic checks

Validate known material regions:
- metal regions contain high metallic values where expected;
- dielectric/composite/rubber regions remain near zero;
- the entire atlas must not become 1.0 because scalar channel extraction accidentally used the wrong default/socket behavior.

Region-aware validation is preferred over global mean.

---

# Emissive checks

Emissive must be validated spatially.

Given approved emitter UV rectangles/masks:

```text
expected emitter signal
unexpected signal outside emitters
padding bleed allowance
clipping/hue preservation
```

Required report:

```yaml
emissive:
  approved_signal_px: 52000
  outside_signal_px: 1800
  outside_allowed_padding: 0
  max_rgb: [0.259, 0.745, 1.0]
  clipped_channels: []
  status: PASS
```

A full/mostly white emissive atlas is FAIL when only small light strips are emitters.

Baking Principled `Emission Color` without considering zero `Emission Strength` can produce false white emission on non-emitting materials; this validator must detect that spatially.

---

# UV-region diagnostics

The validator may consume the same semantic UV contract as the bake source.

For each atlas owner:
- aggregate mean/min/max;
- check expected signal type;
- detect foreign contamination;
- detect missing part output.

Do not infer regions from `.001` object names. Use stable semantic part IDs.

---

# Runtime material check

After image validation, verify the runtime material actually references the accepted outputs.

For glTF metallic-roughness baseline:
- BaseColor -> correct base color texture;
- ORM/project packed texture -> correct roughness/metallic channel interpretation;
- Normal -> correct normal texture;
- Emissive -> correct emissive texture;
- decal material remains separate if required.

Engine Profile may override packing.

---

# Export readback

Parse the exported runtime file/manifest and verify:
- expected image URIs;
- expected material names;
- expected LOD nodes;
- dynamic/decal materials preserved separately;
- no accidental missing texture.

Do not trust Blender-side material state alone.

---

# Baked-runtime visual QA

Final visual comparison for texture closure must use:

```text
runtime LOD mesh
+
baked runtime material
```

not the original procedural authoring material.

If authoring render passes but baked-runtime render fails, the bake stage is FAIL.

---

# Progressive diagnostics

Default output: `SUMMARY`.

On failure:
1. identify map;
2. identify semantic region/channel;
3. return aggregate stats for only that region;
4. raw pixel data only as last resort.

This validator exists partly to prevent large image arrays from entering model context.

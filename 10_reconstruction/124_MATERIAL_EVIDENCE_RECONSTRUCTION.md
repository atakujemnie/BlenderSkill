# Material Evidence Reconstruction

## Purpose

Reconstruct material identity from reference evidence rather than assigning plausible material names.

v0.10 separates:

```text
MATERIAL_SEGMENTATION
```

from:

```text
MATERIAL_APPEARANCE
```

Both are required for target fidelity L4/L5 when the reference visibly depends on material contrast.

## Material identity

For each visible region establish:
- material family;
- base-color family;
- metallic/dielectric behavior;
- roughness range and roughness ordering vs neighbors;
- surface directionality / anisotropy;
- micro-normal frequency/amplitude;
- transparency/glass response;
- emissive behavior;
- wear/maintenance character when reference-significant.

## Evidence priority

Property-level priority:
1. explicit material palette / annotation;
2. detail close-up;
3. calibrated material sample if available;
4. hero render;
5. orthographic view.

Do not use one source as authority for every material property.

## Material segmentation

First reconstruct correct material boundaries.

A correct shader applied to the wrong region is FAIL.

For each region persist:

```yaml
material_region:
  id: SIDE_ALUMINIUM_R
  boundary_owner: SIDE_TRIM_PATH_R
  source_reference_ids: [...]
  required_views: [FRONT, SIDE, HERO]
```

## Material appearance

Then prove the region reads like the reference material under a stable QA rig.

Example:

```yaml
material_appearance:
  id: SIDE_ALUMINIUM_R
  family: BRUSHED_ALUMINIUM
  metallic: 1.0
  roughness_range: [0.25, 0.38]
  directionality: REQUIRED
  brush_frame: LOCAL_LONG_AXIS
  neutral_lookdev_rig_id: civic_neutral_v2
```

A material slot named `M_Astera_BrushedAluminium` does not prove this record.

## Directional materials

For brushed/ground/anodized surfaces, record:
- direction frame;
- direction changes at part boundaries;
- anisotropy or directional normal/roughness behavior;
- whether highlight width/orientation matches evidence under neutral lighting.

Wrong direction can make a correct geometry region read as a different manufactured part.

## Neutral lookdev requirement

Use a fixed neutral QA rig when material response is an acceptance owner:
- fixed world/key/fill;
- fixed exposure;
- fixed view transform;
- bloom disabled for base material proof;
- stable camera.

Persist rig/settings in provenance.

Hero lighting is supporting evidence, not the only proof.

## Emissive separation

Validate separately:
1. emitter geometry/region;
2. recess/visibility;
3. authored color/intensity;
4. runtime bloom.

Do not let bloom widen or brighten an emitter until it hides wrong geometry.

## Do not bake lighting into albedo

Highlight, shadow and ambient in concept art are not material base color.

Use lighting-vs-material disentanglement before color matching.

## Material uncertainty

A label such as `dark titanium composite` may be design language rather than literal physical composition.

Record uncertainty and combine annotation with appearance evidence.

Do not default to `metallic=1` solely from the word `titanium`.

## Surface hierarchy

For civic hard-surface:

```text
material family
-> macro part-to-part variation
-> meso maintenance/exposure pattern
-> micro manufacturing texture
-> sparse evidence-driven wear
```

Uniform global Noise/grunge is not material reconstruction.

## L4/L5 acceptance

### L4
Required:
- segmentation PASS;
- material-family response PASS;
- directionality where evidence requires it;
- emissive/glass ownership PASS;
- source-anchored material evidence record.

### L5
Additionally:
- reference-significant microstructure;
- wear/detail hierarchy;
- branding/decal integration where material-dependent.

## Proof record

```yaml
material_regions:
  status: PASS
  evidence_kind: MATERIAL_APPEARANCE_VALIDATION
  validator_id: APPEARANCE_REFERENCE_VALIDATE
  provenance_id: mat_appearance_...
  source_reference_ids: [...]
  missing_must: 0
```

This feeds `APPEARANCE_FIDELITY_GATE`.

# Edge, Material and Detail Fidelity

## Purpose

Turn G4/G5 from descriptive cleanup stages into evidence-bearing reconstruction stages.

The target is not merely a valid mesh with named materials. The target is the same product language visible in the reference.

---

## Edge language is geometry evidence

For each required edge family record:

```yaml
edge_family:
  id: OUTER_PROTECTIVE_CORNER
  importance: MUST
  members: [...]
  source_reference_ids: [...]
  profile_type: FILLET
  radius_samples_mm: [...]
  start_end_landmarks: [...]
  continuity: G1_or_G2
  required_views: [FRONT, SIDE, HERO]
```

Validation checks:
- family placement;
- radius/chamfer profile;
- where the treatment begins/ends;
- continuity around corners;
- transition into neighboring edge families;
- preservation of protected hard dimensions.

The last item is necessary but not sufficient.

A bevel that keeps the bounding box but uses the wrong radius/profile is FAIL.

---

## Hard-surface plane hierarchy

Before material lookdev verify the product still contains the reference plane hierarchy:
- primary flat planes;
- secondary stepped planes;
- recessed fields;
- trim caps;
- shadow gaps;
- protective radii.

Excessively smooth continuous curvature can erase intended hard-surface structure while keeping the outer contour nearly correct.

Use neutral/matcap or clay validation before relying on materials.

---

## Material segmentation vs material appearance

### Segmentation
Answers:

```text
which pixels/regions belong to which material family?
```

### Appearance
Answers:

```text
do those regions respond like the reference material?
```

Both are required for L4/L5.

Material appearance owners may validate:
- metallic/dielectric distinction;
- roughness hierarchy;
- anisotropy/directionality;
- specular width;
- micro-normal frequency/amplitude;
- transparency/glass response;
- emissive intensity and recession;
- local wear hierarchy.

A Principled material with the correct name is not a material appearance PASS.

---

## Neutral lighting contract

For material comparison create a calibrated neutral-light QA setup:
- fixed exposure;
- fixed view transform;
- neutral world/key/fill;
- no stylized bloom;
- no environment that hides roughness differences.

Persist:

```yaml
lookdev_rig_id: neutral_civic_v2
exposure: ...
view_transform: ...
```

The same rig must be used for comparable material evidence.

Hero lighting may be used as supporting evidence, not as the only material proof.

---

## Directional materials

For brushed/anodized/ground metal, directionality is a first-class requirement.

Record:
- tangent/orientation frame;
- visible brush direction;
- anisotropy strength/range;
- whether direction changes across separate manufactured parts.

Wrong brush direction can make correct geometry read as a different assembly.

---

## Emissive discipline

Validate separately:
1. emitter geometry/region;
2. recess/occlusion;
3. authored emissive color/intensity;
4. runtime bloom/glow.

Reference reconstruction compares the emitter itself under controlled conditions.

Do not let bloom:
- widen a thin emitter until it resembles the reference by accident;
- hide wrong base geometry;
- convert subtle orientation lighting into a neon tube.

---

## Detail tiers

### Structural meso detail — MUST when visible
Examples:
- service-panel perimeter;
- plinth split;
- rear service bands;
- utility recess;
- major fastener clusters;
- trim termination;
- underside service-cover layout.

### Surface micro detail — target-dependent
Examples:
- brushed scratches;
- microbead composite texture;
- fine roughness variation;
- dust in creases;
- touch marks;
- rain streaks.

Do not classify visible structural boundaries as optional microdetail merely because they are small in pixels.

---

## Detail density and omission

Compare reference detail density by semantic region.

Example:

```yaml
detail_region:
  id: REAR_CENTER
  reference_features: 7
  must_features: 4
  candidate_features: 4
  unauthorized_features: 0
  missing_must: 0
```

A candidate can fail by being too empty even when every object it did build is individually valid.

It can also fail by adding unauthorized sci-fi decoration.

---

## Surface target by fidelity

### L3
Geometry and structural feature match. Surface may remain neutral.

### L4
Required:
- material segmentation;
- material family response;
- edge-family fidelity;
- emissive/glass ownership;
- major trim/junction appearance.

### L5
Additionally required:
- all MUST meso details accounted for;
- reference-significant microstructure;
- branding/decal exactness;
- calibrated final appearance evidence;
- no missing MUST detail owners.

---

## Final evidence bundle

```yaml
appearance_fidelity:
  edge_families:
    status: PASS
    evidence_kind: EDGE_FAMILY_VALIDATION
    ...
  part_boundaries:
    status: PASS
    evidence_kind: PART_BOUNDARY_VALIDATION
    ...
  trim_paths:
    status: PASS
    evidence_kind: TRIM_PATH_VALIDATION
    ...
  material_regions:
    status: PASS
    evidence_kind: MATERIAL_APPEARANCE_VALIDATION
    ...
  detail_coverage:
    status: PASS
    evidence_kind: DETAIL_COVERAGE
    must_missing: 0
  emissive_regions:
    status: PASS
    evidence_kind: EMISSIVE_REGION_VALIDATION
```

This bundle is consumed by `APPEARANCE_FIDELITY_GATE` and then by final `RECON_FIDELITY_GATE`.
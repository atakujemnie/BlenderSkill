# Reference-Anchored Appearance Validator Pattern

## Purpose

Implementation pattern for producing compact appearance evidence without trusting builder-authored PASS flags.

---

## Inputs

```yaml
validator_input:
  candidate_artifact: <blend/object/render artifact>
  source_reference_id: <registered source>
  registration_id: <view registration>
  appearance_owner_id: <boundary/trim/edge/material/detail owner>
  source_roi: [x0, y0, x1, y1]
  owner_class: <PART_BOUNDARY|TRIM_PATH|EDGE_FAMILY|...>
```

---

## Separation rule

The validator reads:
- saved candidate artifact or isolated QA render;
- persisted source evidence;
- persisted registration;
- appearance owner contract.

It does not read `builder.accepted = True` or use builder completion state as evidence.

---

## Boundary/trim metric pattern

For projected geometry:
1. render isolated candidate with stable QA rig;
2. use the existing global registration;
3. crop the owner ROI without local translation/warp;
4. extract candidate and reference boundary/path masks;
5. compare path distances/endpoints/width samples;
6. emit compact metrics.

Example:

```yaml
status: PASS
evidence_kind: TRIM_PATH_VALIDATION
validator_id: APPEARANCE_REFERENCE_VALIDATE
validator_version: 0.1.0
provenance_id: trim_r_side_004
source_reference_id: tech_sheet_v1
registration_id: side_reg_002
owner_id: SIDE_TRIM_R
metrics:
  mean_path_error_px: 1.6
  p95_path_error_px: 3.8
  width_error_pct: 4.1
  missing_length_pct: 0.0
```

---

## Edge-family pattern

Use neutral/clay rendering and/or geometric section samples.

Record:
- sample stations;
- reference-fit/profile artifact;
- candidate profile;
- radius/chamfer residual;
- start/end landmark error;
- protected-dimension regression.

Do not accept merely because the bevel modifier exists.

---

## Material appearance pattern

Use a fixed calibrated lookdev rig.

Compare semantic properties rather than raw final-beauty pixels when the reference lighting is stylized:
- region boundary;
- metallic/dielectric class;
- roughness ordering;
- directionality/aniso presence;
- local contrast against adjacent material;
- emissive emitter width/intensity under bloom-disabled render.

Store the rig ID and render settings in provenance.

---

## Detail coverage pattern

Create a reference feature inventory before final QA.

```yaml
features:
  - id: REAR_SERVICE_BAND_01
    importance: MUST
    source_reference_id: rear_view_v1
    source_roi: [...]
    status: PASS
  - id: LOWER_PLINTH_SEAM_R
    importance: MUST
    status: FAIL
```

Aggregate only explicit feature records.

Do not infer `coverage=100%` from the number of objects in the candidate scene.

---

## Anti-gaming checks

Validator should reject or downgrade records when:
- source_reference_id is missing for reference-derived evidence;
- registration_id is missing for projected evidence;
- ROI lies outside the registered image;
- local warp/translation is used after global registration;
- candidate render contains LOD/collision/proxy contamination;
- evidence artifact predates the current host/node revision;
- validator_id is not canonical for the owner class.

---

## Output

Always return compact data:

```yaml
status: PASS|FAIL|UNVERIFIED
owner_id: ...
evidence_kind: ...
validator_id: APPEARANCE_REFERENCE_VALIDATE
provenance_id: ...
source_reference_ids: [...]
registration_id: ...
metrics: {...}
blockers: [...]
```

Raw images/masks remain artifacts and are referenced by provenance rather than embedded in the gate record.
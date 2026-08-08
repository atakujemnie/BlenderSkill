# Reconstruction Fidelity Gate

## Purpose

Provide the hard, proof-bearing transition from reference reconstruction to runtime work.

v0.10 extends the gate after the Lafar Street Bench v0.9 benchmark demonstrated:

```text
hard dimensions PASS
+ outer silhouette PASS
+ local builder gates PASS
+ game-ready package PASS
!=
faithful reconstruction
```

For target fidelity L4/L5, internal product architecture and appearance are now mandatory upstream owners.

---

## Core rule

```text
RECONSTRUCTION FIDELITY FAIL / UNVERIFIED
!=
known deviation that runtime may hide
```

If a HARD/MUST/CANONICAL owner fails, pipeline returns to its earliest owner.

`PASS` is an evidence state, not a builder comment.

---

## v0.10 gate order

```text
registered source set
-> hard dimensions
-> canonical global silhouette/views
-> D0/D1 landmarks and proportions
-> MUST geometry/features
-> Appearance Contract closure when target >= L4
-> APPEARANCE_FIDELITY_GATE when target >= L4
-> authority/deviation closure
-> RECON_FIDELITY_GATE
-> only then topology/LOD/UV/bake/export/runtime
```

The appearance gate does not replace canonical geometry proof. It closes the class of failures that global silhouette cannot see:
- part boundaries;
- trim paths;
- junctions;
- edge families;
- material response;
- detail coverage;
- final matched appearance views.

---

## Proof-bearing PASS

Every required owner carries at minimum:

```yaml
status: PASS
evidence_kind: <allowed kind>
validator_id: <canonical validator>
provenance_id: <artifact/report id>
```

Reference-derived evidence additionally requires:

```yaml
source_reference_id: ref_...
```

or:

```yaml
source_reference_ids: [...]
```

Projected evidence additionally requires:

```yaml
registration_id: reg_...
```

A bare:

```yaml
status: PASS
```

is `UNVERIFIED` in strict mode.

---

## Canonical validator rule

If a canonical validator exists for the owner, local builder acceptance cannot substitute for it.

Examples:

```text
view/silhouette/ROI -> REFERENCE_OVERLAY_VALIDATE
appearance boundary/trim/material -> APPEARANCE_REFERENCE_VALIDATE
node acceptance -> RECONSTRUCTION_NODE_GATE
layer order -> LAYER_STACK_VALIDATE
appearance aggregate -> APPEARANCE_FIDELITY_GATE
final aggregate -> RECON_FIDELITY_GATE
```

A local helper may produce a measurement artifact. It may not certify the final owner itself.

This explicitly blocks circular chains such as:

```text
builder infers R165
-> builder constructs R165
-> builder-local Gate checks R165
-> reference PASS
```

The last transition is invalid without source-anchored evidence.

---

## Allowed evidence classes

Examples:

```text
NUMERIC_MEASUREMENT
REGISTERED_OVERLAY
SILHOUETTE_DIFF
LANDMARK_PROJECTION
FEATURE_ROI
LAYER_STACK
RAY_VISIBILITY
MATERIAL_SEGMENTATION
PART_BOUNDARY_VALIDATION
TRIM_PATH_VALIDATION
JUNCTION_VALIDATION
EDGE_FAMILY_VALIDATION
MATERIAL_APPEARANCE_VALIDATION
EMISSIVE_REGION_VALIDATION
DETAIL_COVERAGE
AUTHORITY_DECISION
APPEARANCE_FIDELITY_GATE
```

Allowed evidence depends on owner class.

`OBJECT_EXISTS` is never sufficient for a visible MUST feature.

---

## Minimal v0.10 contract

```yaml
fidelity_gate:
  strict_evidence: true
  target_fidelity: L5
  achieved_fidelity: L5

  hard_dimensions:
    status: PASS
    evidence_kind: NUMERIC_MEASUREMENT
    validator_id: REFERENCE_MEASURE
    provenance_id: bounds_report_v4
    source_reference_id: sheet_v3

  canonical_views:
    FRONT:
      status: PASS
      evidence_kind: REGISTERED_OVERLAY
      validator_id: REFERENCE_OVERLAY_VALIDATE
      provenance_id: front_compare_004
      source_reference_id: sheet_front_v3
      registration_id: front_reg_004
    SIDE:
      status: PASS
      evidence_kind: REGISTERED_OVERLAY
      validator_id: REFERENCE_OVERLAY_VALIDATE
      provenance_id: side_compare_004
      source_reference_id: sheet_side_v3
      registration_id: side_reg_004

  landmarks_d0_d1:
    status: PASS
    evidence_kind: LANDMARK_PROJECTION
    validator_id: REFERENCE_OVERLAY_VALIDATE
    provenance_id: landmarks_004
    source_reference_id: sheet_v3
    registration_id: canonical_reg_set_004

  must_features:
    - id: SIDE_TRIM_R
      status: PASS
      evidence_kind: TRIM_PATH_VALIDATION
      validator_id: APPEARANCE_REFERENCE_VALIDATE
      provenance_id: trim_r_004
      source_reference_ids: [sheet_side_v3, hero_v2]
      registration_id: side_reg_004

  material_segmentation:
    status: PASS
    evidence_kind: MATERIAL_SEGMENTATION
    validator_id: APPEARANCE_REFERENCE_VALIDATE
    provenance_id: matseg_004
    source_reference_ids: [material_sheet_v1, hero_v2]

  appearance_fidelity:
    status: PASS
    evidence_kind: APPEARANCE_FIDELITY_GATE
    validator_id: APPEARANCE_FIDELITY_GATE
    provenance_id: appearance_gate_004

  deviations: []
```

The output must contain `can_advance_to_runtime`.

---

## Canonical-view proof

For every required `FRONT/SIDE/TOP/REAR/BOTTOM/HERO` view:
- use one global registration for that view;
- candidate/reference use compatible projection, physical scale and crop policy;
- no local warp/translation to improve one feature;
- record compact metrics or explicit blocker;
- `QA_SCENE_ISOLATE` proves collision/export/LOD proxies did not contaminate the render.

If a reference view is unavailable, do not silently omit it. Resolve via View Authority Matrix with explicit `NOT_REQUIRED_BY_AUTHORITY` or alternative proof.

---

## Appearance owner requirement for L4/L5

The final gate consumes `APPEARANCE_FIDELITY_GATE`, which itself is non-compensating for required categories.

A candidate cannot pass because:
- dimensions are perfect but side trim path is wrong;
- global silhouette is high-IoU but rear panel architecture is missing;
- material names are correct but brushed aluminium has no directionality;
- all built details are valid but half the reference MUST details were silently omitted.

---

## Severity / authority

`HARD`, `MUST`, `CANONICAL`:
- no automatic waiver;
- `OPEN` blocks;
- close only as `RESOLVED` or `ACCEPTED_BY_AUTHORITY`;
- authority acceptance requires `authority_source` and `authority_record_id`.

The modeling agent is not authority simply because it can justify an interpretation.

`SOFT` may remain known limitation only if target fidelity permits it.

---

## Conflicts inside technical sheets

Distinguish evidence types:
- `PRINTED_DIMENSION`;
- `ORTHO_DIMENSION_LINE`;
- `PROMPT_HARD_VALUE`;
- `PROMPT_RANGE`;
- `ORTHO_SILHOUETTE_INFERENCE`;
- `PIXEL_INFERENCE`;
- `HERO/PERSPECTIVE_INFERENCE`;
- `MATERIAL/DETAIL_INFERENCE`.

Resolve authority per property.

A printed dimension may control width without controlling trim path or material boundary.

Pixel inference cannot silently overwrite a printed dimension; a printed dimension cannot silently overwrite unrelated appearance evidence.

---

## Fidelity levels

Use `05_execution/59_REFERENCE_FIDELITY_PROTOCOL.md`.

For hero/important civic props default target remains L4/L5.

v0.10 interpretation:
- L3: geometry/structural match may remain neutral-surface;
- L4: internal product architecture, edge language and material appearance required;
- L5: complete MUST detail coverage, branding and reference-significant microstructure required.

`achieved_fidelity` cannot be manually declared above proof owners.

---

## Anti-gaming

Do not pass through:
- correct `Dimensions` with wrong internal architecture;
- alpha silhouette while trim/panel boundaries are wrong;
- builder-local numeric gates derived from builder constants;
- collision/export proxy rendered instead of asset;
- high global IoU with failed MUST ROI;
- object existence without feature visibility;
- correct material slot names without material appearance evidence;
- successful export/engine loader with unresolved appearance/reconstruction FAIL;
- arbitrary triangle-count padding;
- bare PASS without provenance/validator/source;
- `ACCEPTED_BY_AUTHORITY` without authority record.

---

## Executor

`executors/fidelity_gate.py`

The executor aggregates compact reports. It does not perform measurements.

Evidence producers remain:
- `REFERENCE_MEASURE`;
- `REFERENCE_OVERLAY_VALIDATE`;
- `APPEARANCE_REFERENCE_VALIDATE`;
- `LAYER_STACK_VALIDATE`;
- material/appearance validators;
- `APPEARANCE_FIDELITY_GATE`;
- Evidence/Authority Ledger.

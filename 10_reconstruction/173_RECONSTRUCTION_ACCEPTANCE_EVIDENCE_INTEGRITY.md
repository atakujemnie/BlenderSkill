# Reconstruction Acceptance Evidence Integrity

## Purpose

Prevent a reconstruction agent from certifying its own visual success through narrative statements, unchecked `PASS` flags or downstream runtime success.

This module was added after the Lafar Wayfinding Pylon benchmark, where the final run reported `RECONSTRUCTION_COMPLETE = PASS` after substantial repair work, but the compact final report did not carry machine-checkable registered multi-view proof sufficient for a strict v0.8 acceptance gate.

## Core rule

```text
claim != evidence
```

The following are not acceptance evidence by themselves:
- `looks correct`;
- `matching the card`;
- `ortho checked`;
- object existence;
- correct overall dimensions;
- successful export;
- successful engine load;
- a bare `{status: PASS}` record.

## Proof-bearing record

Every reconstruction acceptance owner emits:

```yaml
owner: <view/feature/dimension/material>
status: PASS | FAIL | UNVERIFIED
evidence_kind: <typed validator evidence>
provenance_id: <artifact/report/registration id>
validator_id: <semantic skill/executor>
```

Optional metrics belong in the compact record, not raw dumps.

## Canonical view evidence

For a view with authoritative reference:

```yaml
owner: FRONT
status: PASS
evidence_kind: REGISTERED_OVERLAY
provenance_id: front_reg_003
validator_id: REFERENCE_OVERLAY_VALIDATE
metrics:
  iou: 0.97
  mean_contour_delta_px: 1.2
  max_contour_delta_px: 4.0
failing_rois: []
```

The registration itself must be valid:
- same projection class;
- same physical scale;
- same centerline/datum;
- same crop/aspect policy;
- QA scene isolation applied.

## Feature evidence

A visible MUST feature needs evidence appropriate to its failure mode:
- `FEATURE_ROI` for local shape/placement;
- `LAYER_STACK` for glass/content/recess ordering;
- `RAY_VISIBILITY` for occlusion/host burial;
- `LANDMARK_PROJECTION` for keypoint placement;
- `NUMERIC_MEASUREMENT` for explicit dimensions.

`OBJECT_EXISTS` is never sufficient for a visible MUST feature.

## Authority evidence

A hard deviation can close only as:

```text
RESOLVED
```

with a resolution evidence record, or:

```text
ACCEPTED_BY_AUTHORITY
```

with:
- `authority_source`;
- `authority_record_id`;
- affected contract fields.

The modeling agent is not automatically an authority merely because it can justify one interpretation.

## Separation of builder and acceptance logic

The same process may technically execute build and validation, but acceptance must be derived from independent validator outputs rather than from builder state.

Bad:

```python
build_finished = True
reconstruction_pass = True
```

Required:

```text
build artifact
-> registered validators
-> compact evidence records
-> fidelity gate aggregation
-> acceptance state
```

## Downstream proof does not back-propagate

```text
ENGINE_REGRESSION_TEST PASS
```

does not prove:
- reference fidelity;
- canonical silhouette;
- material segmentation;
- branding orientation;
- screen layer visibility.

Likewise reconstruction PASS does not prove Game-Ready or Pipeline Integrated.

## Final acceptance bundle

Before `RECONSTRUCTION_COMPLETE`, persist at minimum:

```yaml
reconstruction_acceptance:
  target_fidelity: L4_or_L5
  hard_dimensions: <proof-bearing record>
  canonical_views:
    FRONT: <proof-bearing record>
    SIDE: <proof-bearing record>
    TOP: <proof-bearing record>
    REAR: <proof-bearing record>
    BOTTOM: <proof-bearing record>
  landmarks_d0_d1: <proof-bearing record>
  must_features: [<proof-bearing records>]
  material_segmentation: <proof-bearing record when target >= L4>
  deviations: [<resolved/authority records>]
  fidelity_gate: PASS
```

## Anti-self-certification rule

If a final report contains only prose plus untyped PASS flags, downgrade the affected owners to `UNVERIFIED` before completion evaluation.

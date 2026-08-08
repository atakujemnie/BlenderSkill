# Reference Measurement Executor Pattern

## Purpose

This module defines a semantic executor contract for technical-sheet and concept-art measurement without flooding the language model with raw pixel arrays.

Skill ID:

```text
REFERENCE_MEASURE
```

Maturity:

```text
CONTRACT_READY
```

It becomes `EXECUTOR_READY` only after a concrete implementation has been tested in the current Blender/runtime integration.

## Design goal

The executor may perform thousands of pixel-level operations internally.

It must return only compact measurements, confidence, conflicts and requested diagnostics.

The language model must not inspect one record per image row/column unless a failing local ROI explicitly requires it.

## Inputs

```yaml
reference_measure:
  source_image: concept_art.png
  known_dimensions:
    height_mm: 1050
    main_body_diameter_mm: 140
    base_diameter_mm: 210
  requested_views:
    - FRONT
    - SIDE
    - TOP
    - REAR
    - BOTTOM
  expected_sheet_type: TECHNICAL_CONCEPT_SHEET
  output_detail: SUMMARY
```

Optional:
- pre-existing Reference Registry;
- explicit ROI list;
- expected view labels;
- known axis/datum;
- requested feature IDs.

## Executor stages

```text
LOAD IMAGE
-> DETECT / USE REGISTERED ROI
-> CLASSIFY VIEW
-> MASK ANNOTATION NOISE
-> CALIBRATE KNOWN DIMENSION
-> MEASURE SILHOUETTE / TRANSITIONS
-> CROSS-VIEW COMPARE
-> AGGREGATE
-> RETURN COMPACT RESULT
```

## Annotation exclusion

Technical sheets often contain dimension lines, arrows, labels and leaders near the asset silhouette.

The executor must not blindly threshold the whole crop and treat every dark pixel as geometry.

Use one or more of:
- registered object ROI narrower than annotation area;
- connected-component filtering;
- centerline/silhouette continuity;
- expected object-axis constraints;
- dimension-line morphology detection;
- explicit exclusion masks.

If annotation contamination remains ambiguous, return a localized warning rather than silently shifting the measured silhouette.

## Threshold strategy

Do not expose a long threshold-search trace to the language model.

Internally the implementation may test multiple thresholds, but it must select them using a deterministic score such as:
- silhouette continuity;
- expected axis symmetry;
- cross-row width stability;
- agreement with known dimensions;
- cross-view consistency.

If threshold confidence is low:

```yaml
status: NEEDS_LOCAL_REVIEW
roi: [x0, y0, x1, y1]
reason: ANNOTATION_OR_LOW_CONTRAST
```

## Compact output contract

Preferred output:

```yaml
reference_measurement:
  status: PASS
  source: concept_art.png
  views:
    FRONT:
      roi: [735, 165, 860, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      silhouette:
        body_width_px: 70
        body_width_variance_px: 1.1
      transitions:
        top_module_y_px: [207, 220]
        base_y_px: [604, 634]
    SIDE:
      projection: ORTHOGRAPHIC
      authority: HIGH
      silhouette:
        body_width_px: 68
        body_width_variance_px: 0.8
  calibration:
    height_mm:
      value: 1050
      source: EXPLICIT_DIMENSION
      confidence: LOCKED
  cross_view:
    front_side_width_difference_pct: 2.9
    status: CONSISTENT
  anomalies: []
```

Do not return:
- per-pixel arrays;
- all rows of a width profile;
- full masks;
- all threshold candidates;
- full image buffers;
- hundreds of unchanged samples.

## Drill-down mode

Detailed data is allowed only after a specific failure or ambiguity.

Example:

```yaml
reference_measure:
  mode: ROI_DIAGNOSTIC
  view: FRONT
  roi: [750, 202, 835, 226]
  reason: TOP_RING_BOUNDARY_AMBIGUOUS
```

Even in diagnostic mode, return a summarized result plus only the minimal samples required to explain the failure.

## Cross-view validation

For dimensions visible in multiple orthographic views:

```text
measure independently
-> normalize using trusted anchors
-> compare
-> report deviation
```

Do not ask the language model to visually compare hundreds of rows when a numeric aggregate can answer the question.

## Cache integration

Every successful result updates `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md` state.

The executor must use existing validated ROI/calibration from the cache when available instead of rediscovering them.

## Failure codes

```text
REF_NO_VIEW
REF_LOW_CONTRAST
REF_ANNOTATION_CONTAMINATION
REF_NO_SCALE_ANCHOR
REF_PERSPECTIVE_UNSAFE
REF_CROSS_VIEW_CONFLICT
REF_ROI_INVALID
REF_MEASUREMENT_LOW_CONFIDENCE
```

## Repair policy

After failure:
1. localize the failing ROI;
2. change one justified measurement strategy;
3. rerun only that ROI;
4. do not rescan the full sheet unless segmentation itself is invalid.

## Success gate

`PASS` requires:
- source and ROI provenance;
- projection classification;
- explicit or normalized calibration strategy;
- compact measurement table;
- confidence per measurement;
- cross-view conflicts reported;
- no raw diagnostic dump in normal output.

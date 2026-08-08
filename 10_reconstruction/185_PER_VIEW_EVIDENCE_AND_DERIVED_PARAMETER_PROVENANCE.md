# Per-View Evidence and Derived Parameter Provenance

## Problem

v0.10 allowed a node to list multiple views but asset specs often assigned one generic evidence requirement to all of them. That is wrong for mixed concept sheets.

```text
SIDE orthographic
HERO perspective
DETAIL_HEAD close-up
```

are not interchangeable instruments.

## Per-view contract

Each node declares evidence mode per view:

```yaml
view_contracts:
  SIDE:
    controls: [outer_profile, projection]
    allowed_evidence_kinds: [REGISTERED_OVERLAY]
  HERO:
    controls: [junction_interpretation]
    allowed_evidence_kinds: [PERSPECTIVE_INSPECTION]
  DETAIL_HEAD:
    controls: [sensor_boundary, trim_termination]
    allowed_evidence_kinds: [LOCAL_FEATURE_ROI]
```

Do not demand a globally registered orthographic overlay from a perspective hero crop.

## Derived parameters

A scalar in `lamp_spec.py` is not source truth merely because the builder uses it consistently.

For every derived radius, angle, station, width, path or material seed that matters to MUST fidelity persist:

```yaml
derived_parameter:
  id: ELBOW_RADIUS
  value: 70
  unit: mm
  value_range: [62, 78]
  method: ARC_FIT
  source_reference_id: SIDE
  source_roi: [x0, y0, x1, y1]
  confidence: 0.81
  residual_px: 2.7
  provenance_id: fit_elbow_003
  conflict_decision_id: null
```

If the source views conflict, `conflict_decision_id` is mandatory.

## Seed versus evidence

Material values inferred from rendered swatches are lookdev seeds unless independently calibrated.

```text
roughness = 0.28
anisotropy = 0.65
```

may initialize the shader but cannot themselves prove material fidelity. The proof is the controlled neutral-lookdev response against the reference.

## Canonical gate behavior

`RECONSTRUCTION_NODE_GATE` v0.3 validates per-view evidence kinds and derived-parameter provenance records.

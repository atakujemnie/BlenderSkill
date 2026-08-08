# Reference Analysis Cache

## Purpose

Reference analysis is expensive. Once a view, ROI, dimension anchor or authority decision has been validated, the agent must persist it and reuse it instead of repeatedly rediscovering the same information.

This cache is an asset-scoped analytical state, not a conversational summary.

## Core rule

```text
analyze once
-> validate
-> cache
-> reuse
```

Do not re-run broad image analysis unless the cached fact has been invalidated.

## Cache schema

```yaml
reference_analysis_cache:
  asset_id: SM_EXAMPLE
  source:
    file: concept_art.png
    width_px: 1122
    height_px: 1402
    fingerprint: OPTIONAL_HASH_OR_MTIME

  views:
    FRONT:
      roi: [735, 165, 860, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true
      crop_artifact: c_front_ortho.png
    SIDE:
      roi: [930, 165, 1030, 640]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true

  dimension_anchors:
    overall_height_mm:
      value: 1050
      source: EXPLICIT_DIMENSION
      confidence: LOCKED

  measurements: {}
  feature_rois: {}
  exclusions: {}
  conflicts: []
  unresolved: []
```

## What must be cached

Persist when validated:
- original source metadata;
- segmented view ROI coordinates;
- view classification;
- View Authority Matrix decisions;
- explicit dimensions and datum/origin information;
- pixel-to-world calibration anchors;
- feature-specific ROI;
- annotation exclusion masks/regions where needed;
- cross-view consistency results;
- unresolved conflicts;
- crop artifact paths if crops are generated.

## What must NOT be cached as truth

Do not promote to cache truth:
- temporary threshold guesses;
- failed measurement candidates;
- speculative hidden geometry;
- unvalidated perspective-derived dimensions;
- visual impressions such as "looks about right".

These may be logged as diagnostics but must not become authoritative measurements.

## Cache reuse

Before any reference-analysis call:

```text
1. check source identity
2. check requested view/feature
3. check cached validity
4. reuse valid facts
5. analyze only missing or invalid fields
```

If FRONT, SIDE, TOP and their calibration are already valid, a later seam investigation must request only the seam ROI, not segment and measure the entire sheet again.

## Invalidation

Invalidate only affected records when:
- the source image changes;
- a crop was found incorrect;
- a higher-authority source supersedes a measurement;
- a dimension conflict is resolved differently;
- an explicit user correction changes interpretation;
- the source fingerprint no longer matches.

Do not invalidate unrelated views or measurements.

## Scope

Cache scope is normally one asset/reference set.

A cache from another product may provide project conventions but must never supply geometry measurements for the current asset.

## Analysis completion snapshot

At the end of ANALYZE write a compact immutable snapshot:

```yaml
analysis_snapshot:
  status: PASS
  source_revision: ...
  locked_dimensions: {}
  view_authority: {}
  accepted_measurements: {}
  feature_rois: {}
  unresolved: []
```

Later states consume this snapshot.

## Re-entry rule

After `ANALYZE: PASS`, broad exploratory analysis is prohibited.

Return to reference analysis only through one of:
- `FEATURE_ROI_FAILURE(feature_id)`;
- `DIMENSION_CONFLICT(metric_id)`;
- `VIEW_CONFLICT(view_id)`;
- `USER_SOURCE_UPDATE`;
- `CACHE_INVALIDATED(record_id)`.

The re-entry request must identify the affected record/ROI.

## Token-efficiency requirement

The cache must contain compact structured values. It must not embed:
- full image pixels;
- per-row profiles;
- giant tool logs;
- duplicate crop images encoded as text;
- full source documents.

## Relationship to other modules

- `103_REFERENCE_INGESTION_PROTOCOL.md` creates the initial source/view entries.
- `104_CONCEPT_SHEET_SEGMENTATION.md` provides segmented ROIs.
- `106_VIEW_AUTHORITY_MATRIX.md` provides authority.
- `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md` writes compact measurements.
- `110_DIMENSION_GRAPH.md` consumes accepted dimensional relations.
- `145_FEATURE_ROI_VALIDATION.md` may request narrow re-analysis.

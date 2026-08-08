# Reference Conflict Arbitration

## Purpose

v0.11 turns multi-view conflict handling from narrative guidance into a decision artifact.

The Lafar Street Lamp benchmark exposed a characteristic failure: the SIDE drawing suggested a sloped top/head interpretation while the close head detail and hero design language supported a different local form. The model followed one view too literally.

## Property-level authority

Authority belongs to a property, not to an entire image or sheet.

A source may be authoritative for width and weak for local head profile.

Example:

```yaml
property_id: HEAD_TOP_PROFILE
candidates:
  - value: SLOPED
    source_reference_id: SIDE
    authority_kind: ORTHOGRAPHIC
    confidence: 0.74
  - value: STEPPED_COMPOUND
    source_reference_id: DETAIL_HEAD
    authority_kind: DETAIL_ORTHO
    confidence: 0.92
```

## Canonical authority kinds

Default precedence when the project has no explicit override:

```text
EXPLICIT_DIMENSION
EXPLICIT_TEXT_SPEC
DETAIL_ORTHO
ORTHOGRAPHIC
DETAIL_PERSPECTIVE
HERO_PERSPECTIVE
PIXEL_INFERENCE
GENERIC_STYLE_INFERENCE
```

This ordering is only a default. `106_VIEW_AUTHORITY_MATRIX` may override it per property.

## Conflict classes

- `DIMENSION_CONFLICT`
- `PROFILE_CONFLICT`
- `FEATURE_PRESENCE_CONFLICT`
- `MATERIAL_CONFLICT`
- `PROJECTION_CONFLICT`
- `CONCEPT_SHEET_INTERNAL_INCONSISTENCY`
- `STYLE_VS_TECHNICAL_CONFLICT`

## Rules

1. Never average incompatible geometric interpretations merely to reduce error.
2. Explicit dimensions control the dimension they name, not unrelated local shape.
3. Detail views dominate local construction when their intended region is unambiguous.
4. Orthographic views dominate global projection-derived silhouette where valid.
5. Hero views may resolve design intent and junction form but do not silently override locked dimensions.
6. Equal-authority conflicting candidates remain `BLOCKED` until another source or explicit decision exists.
7. Persist rejected alternatives and reason.

## Decision artifact

```yaml
status: PASS
validator_id: REFERENCE_CONFLICT_RESOLVER
property_id: HEAD_TOP_PROFILE
decision_id: conflict_head_004
selected_value: STEPPED_COMPOUND
selected_source_reference_id: DETAIL_HEAD
rejected:
  - source_reference_id: SIDE
    value: SLOPED
averaging_used: false
```

Nodes that depend on the property must reference `decision_id`.

## Canonical executor

`executors/reference_conflict_resolver.py`.

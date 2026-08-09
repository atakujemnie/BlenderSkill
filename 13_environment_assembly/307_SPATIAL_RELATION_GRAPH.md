# Spatial Relation Graph

## Purpose

Describe what inter-object placement means. This complements the asset-level Assembly Relation Contract.

## Canonical types

```text
INSIDE_ZONE
AGAINST_SURFACE
CENTERED_ON
ALIGNS_WITH
FACES_TARGET
ABOVE
BEHIND
ADJACENT
CLEARANCE
CONTAINS
PAIRED_WITH
```

Example:

```yaml
relation_id: BAR_BACKBAR
relation: BEHIND
a: BACKBAR
b: BAR_MAIN
must: true
satisfied: true
constraints:
  longitudinal_alignment_mm: 80
```

A generic `does not overlap` check cannot prove correct placement.

Canonical executor: `executors/spatial_relation_gate.py`.

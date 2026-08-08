# Edge Language System

## Purpose

Preserve the product's reference-specific hard-surface language.

Edge language is not generic cleanup and is not equivalent to `add bevel`.
It can decide whether a dimensionally correct model reads as the same product.

The Lafar Street Bench v0.9 benchmark showed the failure clearly: protected dimensions survived, but side supports and seat still read too soft/monolithic because reference edge families and plane transitions were not actually proven.

## Edge families

Identify at least:
- outer protective corners;
- structural shell corners;
- panel edges;
- metal trim edges;
- screen/insert edges;
- shadow-gap/lip edges;
- underside utilitarian edges.

Do not merge families only because their approximate radius is similar.

## Record

```yaml
edge_family:
  id: SIDE_OUTER_PROTECTIVE
  importance: MUST
  members: [...]
  host_shape_nodes: [...]
  source_reference_ids: [...]
  source_rois: {...}
  profile_type: FILLET | CHAMFER | STEP | LIP | SHADOW_GAP
  radius_or_width_samples_mm: [...]
  start_end_landmarks: [...]
  continuity: G0 | G1 | G2 | HARD_BREAK
  material_relation: ...
  required_views: [...]
```

## Plane hierarchy first

Before edge treatment validate the intended plane hierarchy:
- primary flat planes;
- secondary stepped planes;
- recesses;
- caps/trim;
- lips;
- shadow gaps.

An oversized radius can erase a real plane and turn an engineered housing into a soft slab while preserving the outside dimensions.

That is a reconstruction FAIL.

## Reference proof

RDL4 PASS requires more than protected-dimension survival.

For each MUST family validate:
1. location;
2. profile type;
3. radius/chamfer/step family;
4. start/end positions;
5. continuity around corners;
6. transition into adjacent family;
7. relation to part/material boundaries;
8. protected dimension regression.

Preferred evidence:
- `EDGE_FAMILY_VALIDATION`;
- registered FEATURE_ROI;
- section/profile numeric fit;
- registered overlay in authoritative view.

`modifier exists` is not proof.

## Consistency

If two elements belong to the same manufactured family, edge treatment should be consistent unless reference evidence says otherwise.

Consistency is evaluated against the reference family, not against whatever radius the builder happened to choose first.

## Large vs small radius

Classify semantic role before choosing radius:

```text
protective exterior corner
!=
panel softening
!=
trim highlight edge
!=
service-cover chamfer
```

Do not use one global bevel value across the asset.

## Trim interaction

Trim often owns a different edge family from the host shell.

Validate:
- visible trim width after edge treatment;
- wrapping continuity;
- no host/trim intersection;
- no bevel-induced boundary drift;
- no specular highlight falsely standing in for missing trim geometry.

## Acceptance record

```yaml
edge_language:
  status: PASS
  evidence_kind: EDGE_FAMILY_VALIDATION
  validator_id: APPEARANCE_REFERENCE_VALIDATE
  provenance_id: edge_report_...
  source_reference_ids: [...]
  families_total: 7
  must_families_pass: 7
  missing_must: 0
```

For target fidelity L4/L5 this record feeds `APPEARANCE_FIDELITY_GATE`.

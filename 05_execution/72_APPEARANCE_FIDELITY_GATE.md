# Appearance Fidelity Gate

## Purpose

Block runtime work when the model is dimensionally/silhouette-correct but still visibly not the same product.

This gate is introduced in v0.10 after the Lafar Street Bench v0.9 benchmark produced technically successful geometry/export but only a 6/10 reference match.

---

## Position in pipeline

```text
Shape Graph
-> RDL0..RDL3 structural proof
-> RDL4 edge-language proof
-> RDL5 surface/detail proof as required
-> APPEARANCE_FIDELITY_GATE
-> RECON_FIDELITY_GATE
-> runtime LOD/UV/bake/export
```

For target fidelity below L4 this gate may be NOT_REQUIRED by policy. For L4/L5 it is mandatory.

---

## Required owners

### L4 minimum
- part boundary graph;
- required trim paths;
- required junctions;
- edge families;
- material regions and material response;
- emissive/glass region behavior where present;
- matched/registered final views required by appearance authority.

### L5 additional
- detail coverage;
- branding/decal exactness;
- reference-significant microstructure/wear;
- zero missing MUST appearance owners.

---

## Strict proof record

Each owner record contains:

```yaml
status: PASS
evidence_kind: <typed appearance evidence>
validator_id: <canonical validator>
provenance_id: <report artifact>
source_reference_ids: [...]
```

Projected evidence additionally requires `registration_id`.

A builder-local gate or material/object existence check is not sufficient.

---

## Allowed evidence kinds

```text
PART_BOUNDARY_VALIDATION
TRIM_PATH_VALIDATION
JUNCTION_VALIDATION
EDGE_FAMILY_VALIDATION
MATERIAL_SEGMENTATION
MATERIAL_APPEARANCE_VALIDATION
EMISSIVE_REGION_VALIDATION
DETAIL_COVERAGE
BRANDING_VALIDATION
REGISTERED_OVERLAY
FEATURE_ROI
```

The executor validates proof class compatibility.

---

## Non-compensating MUST logic

Appearance categories do not average away MUST failures.

Example:

```text
part boundaries 10/10
materials 10/10
trim path FAIL
```

Result:

```text
APPEARANCE_FIDELITY_GATE = FAIL
```

A high global score is diagnostic only.

---

## Optional scorecard

For benchmark reporting compute separate scores:

```text
A0 composition/massing
A1 part architecture
A2 edge language
A3 material identity
A4 meso detail
A5 micro detail
```

Weighted total is useful for regression trends but cannot override blockers.

The Street Bench benchmark release target is `REFERENCE_FIDELITY_SCORE >= 8.5/10` plus zero required blockers.

---

## Final-view contract

At least one final proof bundle must validate the assembled model, not only isolated nodes.

Use:
- registered orthographic views for technical sheets;
- matched perspective for HERO when it controls style/continuity;
- neutral form render for part/edge architecture;
- calibrated material render for appearance.

This catches interactions that isolated node checks can miss.

---

## Runtime lock

The following do not unlock runtime when appearance is required:
- correct bounds;
- silhouette alpha PASS;
- triangle budgets;
- UV existence;
- glTF package readback;
- engine import.

Only:

```yaml
appearance_fidelity_gate:
  status: PASS
  can_advance_to_recon_fidelity: true
```

may satisfy the appearance owner of `RECON_FIDELITY_GATE`.

---

## Executor

`executors/appearance_fidelity_gate.py`

The executor aggregates compact records. It does not perform image analysis itself.

Image/geometry validators remain separate producers of evidence.
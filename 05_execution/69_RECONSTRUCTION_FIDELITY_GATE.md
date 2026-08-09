# Reconstruction Fidelity Gate

## Purpose

Provide the hard proof-bearing transition from reference reconstruction to runtime work.

v0.12 establishes that reference fidelity and physical geometric integrity are independent, non-compensating requirements.

```text
perfect dimensions / overlays / appearance
+ unintended interpenetration or silent geometry mutation failure
!=
RECONSTRUCTION_COMPLETE
```

## Canonical v0.12 gate order

```text
registered source set
-> hard dimensions
-> canonical global views/silhouettes
-> D0/D1 landmarks/proportions
-> MUST geometry/features
-> current Shape Node acceptance
-> current mutation-postcondition closure
-> current Assembly Relation closure
-> current topology/validator-control closure
-> GEOMETRIC_INTEGRITY_GATE
-> Appearance Contract closure when target >= L4
-> APPEARANCE_FIDELITY_GATE when target >= L4
-> authority/deviation closure
-> RECON_FIDELITY_GATE
-> only then runtime LOD/UV/bake/export
```

## Hard rule

For target L4/L5 `GEOMETRIC_INTEGRITY_GATE` is required and cannot be compensated by appearance score, source IoU, correct dimensions, triangle budgets or engine success.

## Proof-bearing PASS

Required proof records contain:

```yaml
status: PASS
evidence_kind: <allowed kind>
validator_id: <canonical validator>
provenance_id: <artifact/report id>
```

Reference-derived evidence additionally carries source reference ID(s). Projected evidence carries registration ID.

A bare `status: PASS` is `UNVERIFIED` in strict mode.

## Geometric integrity record

```yaml
geometric_integrity:
  status: PASS
  evidence_kind: GEOMETRIC_INTEGRITY_GATE
  validator_id: GEOMETRIC_INTEGRITY_GATE
  provenance_id: geometry_gate_asset_rev_012
```

It aggregates:
- mutation postconditions;
- Assembly Relation integrity;
- topology records;
- required validator negative controls;
- evidence freshness/revision closure.

## Appearance requirement for L4/L5

`APPEARANCE_FIDELITY_GATE` remains required for product-defining:
- part boundaries;
- trim paths;
- junction appearance;
- edge families;
- material response;
- emissive/branding;
- detail coverage;
- final matched views.

Assembly semantics and visible junction appearance are complementary: a gap can be physically correct but visually wrong, or visually plausible while surfaces interpenetrate.

## Canonical validator rule

Use canonical owners:

```text
view/silhouette/ROI       -> REFERENCE_OVERLAY_VALIDATE
appearance owner          -> APPEARANCE_REFERENCE_VALIDATE
mutation effect           -> MUTATION_POSTCONDITION_GATE
physical part relation    -> ASSEMBLY_INTEGRITY_GATE
mesh topology             -> MESH_VALIDATE
validator bite proof      -> VALIDATOR_NEGATIVE_CONTROL
physical aggregate        -> GEOMETRIC_INTEGRITY_GATE
node acceptance           -> RECONSTRUCTION_NODE_GATE
appearance aggregate      -> APPEARANCE_FIDELITY_GATE
final reconstruction      -> RECON_FIDELITY_GATE
```

Asset-local helpers may measure but may not replace canonical acceptance semantics.

## Canonical-view proof

For every required view:
- use one declared registration;
- preserve physical scale/projection/crop policy;
- no local warp/translation to improve score;
- clean technical-sheet annotations from product mask when needed;
- prove QA scene isolation;
- record compact metrics/blockers.

## Authority/deviations

`HARD`, `MUST`, `CANONICAL` deviations:
- `OPEN` blocks;
- close as `RESOLVED` or `ACCEPTED_BY_AUTHORITY`;
- authority acceptance carries authority source/record;
- repair that changes accepted geometry invalidates stale evidence before new final gate.

## Anti-gaming

Do not pass through:
- correct bounds with wrong internal architecture;
- high IoU contaminated by annotation lines;
- builder-local numeric gates derived from builder constants;
- object existence without feature visibility;
- material names without appearance proof;
- engine/package PASS with unresolved geometric integrity;
- a validator that has never failed a known-broken fixture;
- current report referencing `SUPERSEDED` proof.

## Executor

`executors/fidelity_gate.py`

The executor aggregates compact proof. It does not measure geometry itself.

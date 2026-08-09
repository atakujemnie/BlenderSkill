# Reconstruction Acceptance Evidence Integrity

## Purpose

Prevent reconstruction acceptance from being certified by narrative statements, unchecked PASS flags, circular builder tests, stale evidence or validators that do not actually detect the physical failure they claim to cover.

v0.12 adds a crucial lesson from the Lafar Street Lamp v0.11 benchmark: a fully green source/appearance chain can still certify physically invalid geometry when parts interpenetrate or a mutation silently does nothing.

## Core rule

```text
claim != evidence
PASS != trustworthy proof unless the validator can bite
current-looking proof != current proof after geometry revision
```

Not acceptance evidence by themselves:
- `looks correct` / `matching the card`;
- object existence;
- correct bounds;
- successful Python/operator return;
- applied Boolean modifier without geometry delta;
- generic overlap between junction participants;
- successful export/engine load;
- bare `{status: PASS}`;
- evidence attached to superseded node revision.

## Proof-bearing record

Every acceptance owner emits typed evidence:

```yaml
owner: <node/view/feature/relation/mutation/material>
status: PASS | FAIL | UNVERIFIED | SUPERSEDED
evidence_kind: <typed evidence>
validator_id: <canonical validator>
provenance_id: <artifact/report id>
node_revision: <when applicable>
source_reference_id: <when reference-derived>
registration_id: <when projected>
```

## Mutation evidence

Before a production node can become `BUILT_UNVERIFIED`:

```text
one authorized mutation
-> before/after metrics
-> MUTATION_POSTCONDITION_GATE
```

The record proves the requested effect, not merely execution lifecycle.

Example:

```yaml
operation_id: cut_head_channel
status: PASS
evidence_kind: MUTATION_POSTCONDITION
validator_id: MUTATION_POSTCONDITION_GATE
provenance_id: mutation:head_channel:007
checks:
  geometry_change: PASS
  volume_direction: PASS
  cutter_removed: PASS
  feature_probe: PASS
```

## Assembly evidence

A junction first declares semantic relation, then measured metrics are interpreted by `ASSEMBLY_INTEGRITY_GATE`.

```yaml
relation_id: J_SENSOR_ARM
relation_type: SHADOW_GAP
metrics:
  min_gap_mm: 3.0
  penetration_area_mm2: 0.0
status: PASS
evidence_kind: ASSEMBLY_INTEGRITY
validator_id: ASSEMBLY_INTEGRITY_GATE
provenance_id: assembly:J_SENSOR_ARM:008
```

Generic `overlap=True` cannot certify a junction without relation semantics.

## Canonical view evidence

For an authoritative reference view, use global registered proof with source/registration provenance. Technical-sheet annotations that contaminate product silhouette must be explicitly excluded/component-filtered and mask policy recorded.

No local candidate warp/translation is allowed to improve score.

## Feature evidence

Visible MUST feature uses evidence matching its failure mode, e.g.:
- `FEATURE_ROI`;
- `LAYER_STACK`;
- `LANDMARK_PROJECTION`;
- `NUMERIC_MEASUREMENT`;
- trim/boundary/edge/material-specific evidence;
- mutation postcondition for destructive feature creation.

`OBJECT_EXISTS` is never sufficient for a visible MUST feature.

## Validator trust evidence

A new validator used for MUST acceptance requires adversarial controls:

```text
KNOWN_GOOD -> PASS
KNOWN_BROKEN -> FAIL
```

Persist `VALIDATOR_NEGATIVE_CONTROL` proof. If known-broken returns PASS, current asset PASS from that validator is not trusted acceptance evidence.

The negative fixture must exercise the claimed failure property, not an artificial marker.

## Authority evidence

Hard deviation closes only as:
- `RESOLVED` with resolution evidence; or
- `ACCEPTED_BY_AUTHORITY` with authority source/record and affected fields.

The modeling agent is not authority merely because it can explain its choice.

## Separation of measurement, builder and acceptance

Canonical pattern:

```text
asset-local Blender adapter
-> compact measurement artifact
-> canonical decision executor
-> canonical gate
-> persistent evidence state
```

Bad:

```text
builder infers radius
-> builder creates radius
-> builder verifies same constant
-> PASS
```

Likewise an asset-local interpenetration helper may measure penetration but may not redefine whether overlap is correct. That belongs to the declared Assembly Relation + canonical gate.

## Evidence freshness / repair

After an accepted host changes:

```text
DEPENDENCY_INVALIDATOR
-> affected node revisions bump
-> dependent state DIRTY/BLOCKED
-> hosted Appearance Owners UNVERIFIED
-> old evidence SUPERSEDED
```

Final gates must reject references to stale/superseded evidence. Keep old records for traceability; do not delete them and do not silently reactivate them.

## Downstream proof does not back-propagate

Engine/runtime PASS does not prove reconstruction fidelity, mutation correctness, topology integrity or Assembly Relations.

## Final integrity bundle

Before `RECONSTRUCTION_COMPLETE`, persist at minimum:

```yaml
reconstruction_acceptance:
  graph_revision: sg_...
  appearance_revision: ac_...
  assembly_revision: assembly_...
  mutation_postconditions: [...]
  assembly_integrity: <proof-bearing aggregate>
  topology_records: [...]
  validator_negative_controls: [...]
  hard_dimensions: <proof>
  canonical_views: {...}
  landmarks_d0_d1: <proof>
  must_features: [...]
  geometric_integrity_gate:
    status: PASS
    evidence_kind: GEOMETRIC_INTEGRITY_GATE
    validator_id: GEOMETRIC_INTEGRITY_GATE
    provenance_id: geometry_gate_...
  appearance_fidelity_gate: <when required>
  reconstruction_fidelity_gate: <proof>
```

## Anti-self-certification rule

If final report contains prose/untyped PASS flags, toothless validator output, local acceptance semantics or stale revision evidence, downgrade affected owner to `UNVERIFIED` or `SUPERSEDED` before completion evaluation.

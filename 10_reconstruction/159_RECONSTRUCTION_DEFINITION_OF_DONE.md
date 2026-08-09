# Reconstruction Definition of Done

This module defines Level A `RECONSTRUCTION_COMPLETE`. It does not by itself prove Game-Ready or Pipeline Integrated.

A reconstruction is accepted only from current, proof-bearing evidence. Builder-local green flags, downstream export success and good-looking renders are insufficient.

## Evidence and authority

Required:
- all sources inventoried;
- conflicts/unknowns explicit;
- property-level authority assigned;
- HARD/MUST/CANONICAL deviations `RESOLVED` with evidence or `ACCEPTED_BY_AUTHORITY` with authority record;
- strict PASS records contain evidence kind, provenance and canonical validator;
- reference-derived proof names source reference IDs;
- projected proof names registration IDs;
- current acceptance bundle contains no stale/superseded proof.

## Shape understanding

Required:
- current Reconstruction Shape Graph;
- structural graph validator PASS;
- G0–G5 classification;
- parent/dependency relations;
- shape class/strategy for required nodes;
- authoritative views/properties;
- no unresolved required G0–G3 representation;
- concrete current graph revision.

## Appearance and assembly understanding

For 1:1/L4/L5:
- current Reference Appearance Contract;
- part boundaries, trim paths, visible junctions, edge families, material/emissive/branding/detail owners inventoried;
- owner source references/ROIs and host nodes;
- current Assembly Relation Contract for important multi-part junctions;
- each MUST relation declares semantics such as SHADOW_GAP/BUTT/RECESSED_INSERT/FLUSH/CLEARANCE/EMBEDDED rather than generic overlap.

## Coarse-to-fine execution

Required:
- `RDL0_BARRIER: PASS` with physical diagnostic geometry;
- all required G1/G2/G3 nodes `ACCEPTED` and corresponding RDL barriers PASS;
- required G4 edge work accepted;
- required G5 work completed for target fidelity;
- no child accepted on non-current/non-accepted parent revision;
- every production mutation was authorized and node-scoped.

## Mutation postconditions

For every required current production mutation:
- compact before/after record exists;
- `MUTATION_POSTCONDITION_GATE: PASS`;
- expected Boolean/transform/loft/material effect actually occurred;
- silent Boolean no-op = FAIL;
- mutation evidence is bound to current node revision.

`LOCAL_BUILDER: PASS` is not mutation proof.

## Canonical node proof

Each required node acceptance uses canonical `RECONSTRUCTION_NODE_GATE` and current proof for:
- source views/ROIs;
- numeric/section constraints;
- topology/regression as required;
- mutation postcondition;
- Assembly Relations touched by node.

## Geometry and physical assembly

Required:
- hard dimensions PASS;
- canonical source views/silhouettes PASS where authoritative;
- landmarks/proportions PASS;
- MUST geometry features PASS;
- multi-section/profile proof where representation requires it;
- final assembled views validated;
- all MUST Assembly Relations `PASS` through `ASSEMBLY_INTEGRITY_GATE`;
- zero unintended interpenetration for relations that forbid it;
- required gaps/clearances/contact/embedding lie inside contract tolerances.

## Topology integrity

Required mesh owners have explicit topology intent and `MESH_VALIDATE: PASS`.

For relevant closed solids and visible critical regions classify:
- manifold/boundary state;
- signed volume orientation;
- loose/duplicate/zero-area geometry;
- non-planar n-gons;
- concave/high-order n-gons according to policy.

N-gon existence alone is not an automatic failure. Unclassified risky topology is not a PASS either.

## Validator trust

Every validator used as new MUST acceptance authority for a failure class has current negative-control proof:

```text
KNOWN_GOOD -> PASS
KNOWN_BROKEN -> FAIL
```

A validator that returns PASS on its known-broken fixture cannot close that owner.

## Repair integrity

When accepted geometry changes:
- `DEPENDENCY_INVALIDATOR` ran before rebuild;
- changed/built dependent nodes became DIRTY as appropriate;
- unbuilt dependants became BLOCKED;
- affected Appearance Owners became UNVERIFIED;
- old revision evidence became SUPERSEDED;
- unrelated accepted branches remained reusable;
- repaired closure was revalidated on current revisions.

## Internal product architecture

For 1:1/L4/L5:
- part-boundary graph PASS;
- required trim paths PASS;
- visible junction appearance PASS;
- no missing MUST internal boundary;
- major gaps/steps/recesses match source evidence;
- rear/bottom/detail architecture is not replaced by generic covers when reference defines it.

Physical relation and appearance are separate: a junction can be physically valid yet visually wrong, or visually plausible while interpenetrating.

## Edge language

Required:
- edge-family profile/radius/chamfer proof;
- start/end/continuity;
- protected dimensions;
- hard-surface plane hierarchy preserved.

`dimensions survived bevel` alone is insufficient.

## Surface evidence

For L4+:
- material segmentation PASS;
- material appearance response PASS where source defines it;
- directional brushing/anisotropy when required;
- emissive/glass ownership;
- layer-stack/visibility proof for layered assemblies;
- calibrated lookdev evidence as appropriate.

For L5 additionally:
- complete MUST detail coverage or explicit authority waiver;
- zero silently missing MUST appearance/detail owners;
- branding/decal exactness;
- reference-significant microstructure.

## Reference-mask integrity

Technical-sheet overlays exclude dimension lines/leaders/text from product silhouette where they contaminate metrics. Mask policy/exclusions are recorded. No local candidate warp is allowed to improve fidelity score.

## Final QA/gates

Required:
- QA scene isolation;
- required Shape Nodes accepted;
- RDL barriers PASS;
- `GEOMETRIC_INTEGRITY_GATE: PASS`;
- `APPEARANCE_OWNER_COVERAGE: PASS` and `APPEARANCE_FIDELITY_GATE: PASS` for target >= L4;
- `RECON_FIDELITY_GATE: PASS`;
- no unauthorized deviations;
- final evidence bundle references current revisions only.

## Runtime boundary

```text
GEOMETRIC_INTEGRITY_GATE != PASS
or APPEARANCE_FIDELITY_GATE != PASS when required
or RECON_FIDELITY_GATE != PASS
-> LOD/UV/bake/export/runtime FORBIDDEN
```

Runtime/engine PASS never back-propagates to Level A.

## Documentation

Persist:
- reconstruction report;
- Shape Graph revision;
- Appearance Contract revision when required;
- Assembly Relation revision;
- node acceptance records;
- mutation postcondition records;
- assembly/topology/validator-control records;
- Appearance Owner records;
- RDL barriers;
- geometric/appearance/reconstruction gate reports;
- evidence/unknown/deviation lists;
- inferred geometry with provenance;
- known limitations;
- highest completion level separately.

## Required final record

```yaml
reconstruction_complete:
  status: PASS
  graph_revision: sg_...
  appearance_revision: ac_...
  assembly_revision: assembly_...
  geometric_integrity_gate:
    status: PASS
    evidence_kind: GEOMETRIC_INTEGRITY_GATE
    validator_id: GEOMETRIC_INTEGRITY_GATE
    provenance_id: geometry_gate_...
  appearance_fidelity_gate:
    status: PASS
    provenance_id: appearance_gate_...
  reconstruction_fidelity_gate:
    status: PASS
    evidence_kind: RECON_FIDELITY_GATE
    validator_id: RECON_FIDELITY_GATE
    provenance_id: recon_gate_...
  target_fidelity: L4_or_L5
  deviations: []
```

## Rule

Do not call reconstruction PASS because:
- builder says it looks correct;
- dimensions/silhouette are correct while internal product architecture is wrong;
- all visual gates are green while physical parts interpenetrate;
- a validator has never been proven to fail its own defect class;
- old green evidence belongs to a superseded geometry revision.

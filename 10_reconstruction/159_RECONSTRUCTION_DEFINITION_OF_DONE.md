# Reconstruction Definition of Done

This module defines **reference-reconstruction acceptance**, corresponding primarily to Level A `RECONSTRUCTION_COMPLETE`.

It does not by itself prove `GAME_READY_COMPLETE` or `PIPELINE_INTEGRATED`.
Use `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` for the full asset lifecycle.

Asset reconstruction is accepted only when final state is supported by proof-bearing evidence records, not by narrative self-certification or builder-local green checks.

## Evidence
- all sources inventoried;
- conflicts resolved or explicit;
- unknowns recorded;
- property-level authority assigned where sources disagree;
- HARD/MUST/CANONICAL deviations are `RESOLVED` with evidence or `ACCEPTED_BY_AUTHORITY` with authority record;
- bare `PASS` without evidence kind/provenance/validator does not close a strict gate;
- reference-derived evidence points to source reference IDs;
- projected evidence points to registration IDs.

## Shape understanding
- current `Reconstruction Shape Graph` exists;
- graph structural validator PASS;
- required forms classified G0–G5;
- required nodes have parent/dependency relations;
- required nodes have shape class and implementation strategy;
- authoritative views have explicit responsibilities per node;
- no `UNRESOLVED_REPRESENTATION` for required G0–G3 nodes;
- final acceptance references a concrete graph revision.

## Appearance understanding for 1:1 / L4 / L5
- current `Reference Appearance Contract` exists;
- appearance revision references same source-set revision as reconstruction;
- required part boundaries are inventoried;
- required trim paths are inventoried;
- required junctions are inventoried;
- required edge families are inventoried;
- material/emissive/branding regions are inventoried when visible;
- MUST meso/detail features are inventoried;
- every appearance owner links to source reference/ROI and host Shape Node(s).

A coarse Shape Node does not excuse missing internal product architecture.

## Coarse-to-fine execution
- `RDL0_BARRIER: PASS`;
- all required G1 nodes `ACCEPTED` and `RDL1_BARRIER: PASS`;
- all required G2 nodes `ACCEPTED` and `RDL2_BARRIER: PASS`;
- all required G3 nodes `ACCEPTED` and `RDL3_BARRIER: PASS`;
- required G4 edge-language work accepted through reference edge-family proof;
- G5 required by target fidelity completed or explicitly deferred only when completion boundary allows it;
- no child accepted on failed/unverified/superseded required parent revision.

## Canonical node proof
- each required node acceptance uses `RECONSTRUCTION_NODE_GATE` or compatible canonical validator path;
- required view records name canonical validator IDs;
- builder-local `Gate.accept()` cannot certify canonical node acceptance;
- derived geometry parameters have source-fit/measurement provenance in addition to builder-consistency checks.

## Geometry
- hard dimensions pass with numeric provenance;
- all canonical silhouettes/views pass via registered comparison where reference authority exists;
- all primary landmarks/proportions pass with validator evidence;
- all MUST geometry features pass with suitable ROI/numeric/visibility proof;
- multi-section/profile nodes have station/cross-section proof where representation requires it;
- final assembled views do not rely only on isolated-node success.

## Internal product architecture
For target 1:1/L4/L5:
- part-boundary graph PASS;
- required trim paths PASS;
- required junctions PASS;
- no missing MUST internal boundary;
- major shadow gaps/steps/recess boundaries match source evidence;
- rear/bottom architecture is not replaced by a generic flat cover when source defines structure.

## Edge language
- required edge families have explicit profile/radius/chamfer evidence;
- start/end and continuity are validated;
- protected dimensions survive edge treatment;
- `dimensions survived bevel` alone is not edge-language PASS;
- hard-surface plane hierarchy remains consistent with reference.

## Surface evidence
For L4+:
- material segmentation PASS;
- material appearance response PASS where source defines it;
- directional material evidence such as brushing/anisotropy is represented;
- emissive/glass geometry/material ownership defined;
- visible layered assemblies have layer-stack/visibility proof;
- calibrated neutral-light lookdev evidence exists for material comparison where needed.

A material slot/name assignment is not material appearance proof.

For L5 additionally:
- MUST detail coverage is complete or explicitly waived by authority;
- missing MUST appearance/detail owners = 0;
- branding/decal exactness closed;
- reference-significant microstructure completed.

Final runtime textures/bloom do not need to be finished for Level A if the authoring appearance evidence is otherwise sufficient, but they may not be claimed as complete downstream work.

## QA
- QA scene isolation proves no collision/export proxy contamination;
- each required Shape Node has canonical node acceptance record;
- multi-view gate PASS;
- regression gate PASS;
- RDL barriers PASS;
- `APPEARANCE_FIDELITY_GATE` PASS when target >= L4;
- `RECON_FIDELITY_GATE` PASS;
- no unauthorized deviations;
- lighting/material readability has not been used to justify unsupported geometry changes;
- final acceptance bundle contains typed evidence + provenance + validator IDs for required owners.

## Runtime boundary

Runtime work is downstream from reconstruction acceptance.

For target L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> LOD/UV/bake/export FORBIDDEN
```

Correct dimensions, triangle budgets, UVs or glTF readback do not override this lock.

For higher completion levels:
- Level B -> clean authoring model/UV/material segmentation;
- Level C -> LOD/collision/bake/package/export/runtime material closure;
- Level D -> project catalog/import integration.

Runtime/engine PASS never back-propagates to Level A.

## Documentation
- reconstruction report;
- Shape Graph + graph revision;
- Appearance Contract + appearance revision when required;
- node acceptance records;
- appearance owner records;
- RDL stage barrier records;
- appearance fidelity report when required;
- reconstruction acceptance evidence bundle;
- evidence/unknown list;
- inferred geometry list with derivation provenance;
- known limitations;
- highest completion level reported separately.

## Required final record

```yaml
reconstruction_complete:
  status: PASS
  evidence_kind: RECON_FIDELITY_GATE
  validator_id: RECON_FIDELITY_GATE
  provenance_id: recon_gate_report_...
  graph_revision: sg_...
  appearance_revision: ac_...
  rdl_barriers:
    RDL0: PASS
    RDL1: PASS
    RDL2: PASS
    RDL3: PASS
    RDL4: PASS
    RDL5: PASS_OR_NOT_REQUIRED
  appearance_fidelity_gate:
    status: PASS
    provenance_id: appearance_gate_...
  target_fidelity: L4_or_L5
  canonical_views: {...}
  must_features: [...]
  deviations: [...]
```

## Rule

Do not call the entire asset `DONE` merely because this reconstruction DoD passes.
Do not call reconstruction `PASS` because the builder says it looks correct.
Do not call reconstruction `PASS` when primary forms were not solved node-by-node.
Do not call reconstruction `PASS` when dimensions/silhouette pass but product-defining internal boundaries, edge families, material identity or MUST detail remain wrong/unverified.

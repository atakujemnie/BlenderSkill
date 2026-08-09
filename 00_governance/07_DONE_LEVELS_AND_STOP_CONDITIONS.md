# Asset Completion Levels and Stop Conditions

## Purpose

Agent never uses `DONE` without a named completion level and proof.

```text
A RECONSTRUCTION_COMPLETE
-> B MODELING_COMPLETE
-> C GAME_READY_COMPLETE
-> D PIPELINE_INTEGRATED
```

Higher levels require all lower levels.

## Level A — RECONSTRUCTION_COMPLETE

A reference-driven object is geometrically, physically and visually solved and proven.

Required:
- coherent Reference/Evidence Registry and property-level authority;
- current Shape Graph structural PASS;
- RDL0 diagnostic barrier PASS;
- all required G1/G2/G3 nodes `ACCEPTED` with their RDL barriers PASS;
- canonical node evidence rather than builder-local self-certification;
- hard dimensions, landmarks and required canonical views PASS;
- MUST feature owners source-anchored and PASS;
- HARD/MUST/CANONICAL deviations resolved/accepted with authority records;
- every production mutation required by current revisions has `MUTATION_POSTCONDITION_GATE: PASS`;
- every required multi-part junction has a declared Assembly Relation and `ASSEMBLY_INTEGRITY_GATE: PASS`;
- required topology records `MESH_VALIDATE: PASS`;
- required acceptance validators have current negative-control proof;
- no current report references `SUPERSEDED` evidence;
- `GEOMETRIC_INTEGRITY_GATE: PASS`;
- `RECON_FIDELITY_GATE: PASS`.

For explicit 1:1/L4/L5 additionally:
- current Reference Appearance Contract;
- required part boundaries/trim paths/junctions/edge families PASS;
- material segmentation + appearance response PASS where reference defines them;
- emissive/glass/branding owners PASS where present;
- final matched/registered appearance views PASS;
- `APPEARANCE_OWNER_COVERAGE: PASS`;
- `APPEARANCE_FIDELITY_GATE: PASS`;
- L5: zero silently missing MUST details unless authority explicitly waives them.

Not sufficient:
- `looks correct`;
- correct bounding box;
- outer silhouette alone;
- one hero render;
- builder-local tests against builder constants;
- correctly named material slots without appearance proof;
- all Shape Nodes green while physical parts interpenetrate;
- successful export or engine load.

## Level B — MODELING_COMPLETE

Requires Level A plus:
- final intended authoring geometry;
- topology intent per mesh;
- final mesh validation PASS;
- UV strategy complete;
- material segmentation complete;
- decals/branding represented by intended pipeline;
- transforms/pivot/naming PASS;
- editable authoring source saved;
- no temporary QA/helper contamination in production collection.

## Level C — GAME_READY_COMPLETE

Requires Level B plus:
- Game Asset Contract;
- active Engine/Profile or explicit neutral runtime contract;
- runtime LOD validation against active budget/authority;
- collision validation;
- material/draw-call implications validated;
- procedural effects have runtime disposition;
- required runtime texture outputs exist;
- emissive runtime handoff documented;
- package readback validates nodes/materials/images/required primitive attributes and transform policy;
- export + round-trip invariants PASS;
- protected Shape Graph/Appearance/Assembly contracts survive optimization;
- baked/runtime-material QA PASS.

Parseable glTF without required attributes or produced from unresolved Level A geometry is not Level C.

## Level D — PIPELINE_INTEGRATED

Requires Level C plus:
- stable project asset ID;
- canonical runtime path;
- catalog/registry integration where required;
- no unintended overwrite;
- target-engine production loader/import succeeds;
- instantiation/use or equivalent regression succeeds;
- trustworthy Test Oracle;
- integration report persisted.

Accepted runtime evidence kinds:

```text
ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
```

Blender glTF re-import is Level C round-trip evidence, not Level D.

## Stop conditions

Stop and report the earliest blocker when any required gate fails.

Examples:
- Shape Graph unresolved;
- mutation postcondition FAIL / Boolean no-op;
- forbidden assembly interpenetration or wrong junction relation;
- validator fails its negative control;
- stale/superseded evidence referenced after repair;
- RDL barrier FAIL;
- part boundary/trim/edge/material owner FAIL;
- `GEOMETRIC_INTEGRITY_GATE` FAIL/UNVERIFIED;
- `APPEARANCE_FIDELITY_GATE` FAIL/UNVERIFIED;
- `RECON_FIDELITY_GATE` FAIL/UNVERIFIED;
- unresolved authority conflict;
- runtime package/export/engine blocker at higher levels.

Do not silently downgrade the target.

## Runtime lock

For reconstruction work, and especially 1:1/L4/L5:

```text
GEOMETRIC_INTEGRITY_GATE != PASS
or
APPEARANCE_FIDELITY_GATE != PASS when required
or
RECON_FIDELITY_GATE != PASS
-> GAME_READY_FINISH must not start
```

Dimensions, triangle budgets, UVs or engine success cannot raise the completion level through this lock.

## Mandatory completion report

```yaml
asset_completion:
  target_level: GAME_READY_COMPLETE
  highest_passed_level: RECONSTRUCTION_COMPLETE
  levels:
    reconstruction: PASS
    modeling: FAIL
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED
  reconstruction_evidence:
    graph_revision: sg_012
    appearance_revision: ac_009
    assembly_revision: assembly_004
    geometric_integrity_gate:
      status: PASS
      evidence_kind: GEOMETRIC_INTEGRITY_GATE
      provenance_id: geometry_gate_004
    appearance_gate:
      status: PASS
      evidence_kind: APPEARANCE_FIDELITY_GATE
      provenance_id: appearance_gate_009
    fidelity_gate:
      status: PASS
      evidence_kind: RECON_FIDELITY_GATE
      provenance_id: recon_gate_012
  blockers:
    - PBR_BAKE_NOT_DONE
```

The first failing required level is the real completion state.

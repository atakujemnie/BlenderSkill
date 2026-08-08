# Asset Completion Levels and Stop Conditions

## Purpose

Agent nie używa `DONE` bez jawnego poziomu i dowodu.

Lifecycle:

```text
A RECONSTRUCTION_COMPLETE
-> B MODELING_COMPLETE
-> C GAME_READY_COMPLETE
-> D PIPELINE_INTEGRATED
```

Wyższy poziom wymaga wszystkich niższych.

---

# Level A — RECONSTRUCTION_COMPLETE

Reference-driven object jest geometrycznie i wizualnie rozwiązany **oraz udowodniony**.

Required v0.10:
- Reference/Evidence Registry and property-level authority are coherent;
- current `Reconstruction Shape Graph` structural PASS;
- required G0–G3 nodes have shape class, parent/dependencies, authoritative views and Node Contracts;
- RDL0 barrier PASS;
- required G1 primary nodes `ACCEPTED` + RDL1 barrier PASS;
- required G2 nodes `ACCEPTED` + RDL2 barrier PASS;
- required G3 nodes `ACCEPTED` + RDL3 barrier PASS;
- canonical node acceptance records use canonical validators rather than builder-local gates;
- hard dimensions PASS with source/numeric provenance;
- canonical silhouettes/views PASS through registered evidence where reference has authority;
- primary proportions/landmarks PASS;
- MUST features have owner + source-anchored visibility/ROI/numeric proof;
- branding/orientation correct or explicitly deferred only when target fidelity allows it;
- rear/bottom/hidden evidence handled according to authority;
- HARD/MUST/CANONICAL deviations are `RESOLVED` or `ACCEPTED_BY_AUTHORITY` with record;
- multi-view regression PASS;
- `RECON_FIDELITY_GATE` proof-bearing PASS for accepted graph revision.

For explicit 1:1/exact reconstruction or target fidelity L4/L5 additionally required:
- current `Reference Appearance Contract`;
- required part boundaries inventoried and PASS;
- required trim paths PASS;
- required junctions PASS;
- required edge families PASS with reference profile evidence;
- material segmentation PASS;
- material appearance response PASS where reference defines it;
- emissive/glass/branding appearance owners PASS where present;
- final matched/registered appearance views PASS;
- `APPEARANCE_FIDELITY_GATE: PASS`;
- L5: all MUST detail owners accounted for and `must_missing = 0` unless authority explicitly waives a feature.

Not required for Level A by itself:
- final runtime bake;
- runtime LOD/collision;
- engine integration.

Not sufficient:
- `looks correct`;
- correct overall bounding box;
- alpha outer silhouette PASS by itself;
- existing Blender objects;
- one hero render;
- builder-local numeric gates against builder constants;
- correctly named material slots without appearance proof;
- successful export/engine load.

---

# Level B — MODELING_COMPLETE

Requires Level A plus:
- final intended authoring geometry;
- topology intent per mesh;
- mesh validation PASS;
- UV strategy complete;
- material segmentation complete;
- decals/branding represented by intended pipeline;
- transforms/pivot/naming PASS;
- editable authoring source saved;
- no temporary QA/helper contamination of production collection.

Procedural Blender shader may still exist if runtime disposition is not yet required.

---

# Level C — GAME_READY_COMPLETE

Requires Level B plus:
- Game Asset Contract;
- active Engine/Profile or explicit neutral runtime contract;
- runtime LOD validation against active hard/authority-resolved budget;
- collision validation;
- material/draw-call implications validated;
- procedural effects have runtime disposition: BAKE / RECREATE / NATIVE_VERIFIED / REMOVE_BY_DESIGN;
- required BaseColor/Normal/ORM/Emissive or engine-specific outputs exist;
- runtime emissive handoff documented;
- package readback validates nodes/materials/images/required primitive attributes and transform policy;
- export validation PASS;
- export round-trip protected invariants PASS;
- protected Shape Graph, Appearance Contract and Feature Contract survive optimization;
- baked/runtime-material QA PASS.

Parseable glTF without required `TEXCOORD_0`, with forbidden node TRS, without required runtime textures, or derived from an unresolved Level A asset is not Level C.

---

# Level D — PIPELINE_INTEGRATED

Requires Level C plus:
- stable project asset ID;
- canonical runtime path;
- catalog/registry integration where required;
- no unintended overwrite;
- target engine loader/import succeeds;
- instantiation/use or equivalent engine regression succeeds;
- trustworthy test oracle;
- integration report persisted.

Accepted runtime evidence kinds:

```text
ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
```

Blender glTF re-import is Level C round-trip evidence, not Level D.

---

# User-requested stop level

Examples:
- model/reconstruction only -> A/B depending scope;
- game ready -> C;
- put into actual project catalog/runtime -> D.

For a game-production request `build the asset` defaults to Level C unless user scope clearly says otherwise.

A Level C target does not permit skipping Level A appearance proof.

---

# Stop conditions

Stop/report blocker when a required gate cannot pass.

Examples:
- Shape Graph unresolved for primary form;
- required G1 node FAIL in SIDE/TOP;
- builder tries to replace canonical node gate with local self-certification;
- RDL stage barrier FAIL;
- required part boundary/trim/junction FAIL;
- edge family unverified;
- material appearance unverified for L4/L5;
- `APPEARANCE_FIDELITY_GATE` FAIL/UNVERIFIED;
- hard authority conflict unresolved;
- missing runtime material/bake;
- collision contract unknown;
- exported package missing required attributes;
- catalog write or target-engine proof unavailable.

Do not silently downgrade target.

---

# Runtime lock

For 1:1/L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> GAME_READY_FINISH must not start
```

Correct dimensions, silhouette, triangle budgets, UVs or export success cannot raise the completion level through this lock.

---

# Mandatory completion report

```yaml
asset_completion:
  target_level: GAME_READY_COMPLETE
  highest_passed_level: MODELING_COMPLETE
  levels:
    reconstruction: PASS
    modeling: PASS
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED

  reconstruction_evidence:
    graph_revision: sg_010
    appearance_revision: ac_006
    rdl_barriers:
      RDL0: PASS
      RDL1: PASS
      RDL2: PASS
      RDL3: PASS
      RDL4: PASS
      RDL5: PASS
    appearance_gate:
      status: PASS
      evidence_kind: APPEARANCE_FIDELITY_GATE
      provenance_id: appearance_gate_006
    fidelity_gate:
      status: PASS
      evidence_kind: RECON_FIDELITY_GATE
      provenance_id: recon_gate_010

  blockers:
    - PBR_BAKE_NOT_DONE
  deliverables_present:
    blend: true
    runtime_mesh: true
    textures: false
```

First failing required level is the real completion state.

---

# Anti-pattern

Never report an asset as complete when the same report contains a required blocker.

Do not report Level A merely because a monolithic builder created all scene elements.

Do not report Level A merely because hard dimensions and global alpha silhouette pass while product-defining internal boundaries, edge/material families or MUST detail remain wrong/unverified.

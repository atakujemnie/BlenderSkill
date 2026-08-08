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

Required v0.9:
- Reference/Evidence Registry i authority są spójne;
- aktualny `Reconstruction Shape Graph` structural PASS;
- required G0–G3 nodes mają shape class, parent/dependencies, authoritative views i Node Contracts;
- RDL0 barrier PASS;
- required G1 primary nodes `ACCEPTED` + RDL1 barrier PASS;
- required G2 nodes `ACCEPTED` + RDL2 barrier PASS;
- required G3 nodes `ACCEPTED` + RDL3 barrier PASS;
- required RDL4 edge-language work PASS zgodnie z target fidelity;
- hard dimensions PASS z numeric provenance;
- canonical silhouettes/views PASS przez registered evidence, jeśli reference ma authority;
- primary proportions/landmarks PASS;
- MUST features mają owner + visibility/ROI/numeric proof;
- branding/orientation poprawne lub jawnie deferred do późniejszej powierzchni;
- rear/bottom/hidden evidence obsłużone wg authority;
- HARD/MUST/CANONICAL deviations są `RESOLVED` albo `ACCEPTED_BY_AUTHORITY` z recordem;
- multi-view regression PASS;
- `RECON_FIDELITY_GATE` proof-bearing PASS dla zaakceptowanego graph revision.

Nie jest wymagane:
- final runtime bake;
- runtime LOD/collision;
- engine integration.

Nie wystarcza:
- `looks correct`;
- poprawny overall bounding box;
- istniejące Blender objects;
- jeden hero render;
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

Procedural Blender shader może nadal istnieć.

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
- protected Shape Graph/Feature Contract survives optimization;
- baked/runtime-material QA PASS.

Parseable glTF bez required `TEXCOORD_0`, z niedozwolonym node TRS albo bez wymaganych runtime textures nie jest Level C.

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

---

# Stop conditions

Stop/report blocker when required gate cannot pass.

Examples:
- Shape Graph unresolved for primary form;
- required G1 node FAIL in SIDE/TOP;
- RDL stage barrier FAIL;
- hard authority conflict unresolved;
- missing runtime material/bake;
- collision contract unknown;
- exported package missing required attributes;
- catalog write or target-engine proof unavailable.

Do not silently downgrade target.

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
    graph_revision: sg_004
    rdl_barriers: {RDL0: PASS, RDL1: PASS, RDL2: PASS, RDL3: PASS, RDL4: PASS}
    fidelity_gate: {status: PASS, evidence_kind: RECON_FIDELITY_GATE, provenance_id: recon_gate_004}

  blockers:
    - PBR_BAKE_NOT_DONE
  deliverables_present:
    blend: true
    runtime_mesh: true
    textures: false
```

Pierwszy failing required level jest realnym completion state.

---

# Anti-pattern

Nigdy nie raportuj assetu jako ukończonego, jeśli ten sam raport zawiera required blocker.

Nie raportuj Level A tylko dlatego, że monolityczny builder stworzył wszystkie elementy sceny. v0.9 wymaga coarse-to-fine Shape Node evidence.

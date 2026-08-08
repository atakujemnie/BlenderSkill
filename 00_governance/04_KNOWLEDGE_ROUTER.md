# Knowledge Router

Agent nie ładuje całej biblioteki. Router wybiera najmniejszy Task Pack dla current state, failing evidence i Shape Node.

Canonical rule:

```text
intent/current state
-> Task Pack
-> semantic skill
-> executor/tool binding
-> compact evidence
```

## SESSION_PREFLIGHT

Load:
- Agent Charter;
- Semantic Skill Registry;
- Tool Discovery/Profile;
- Blender 5.1 Compatibility Matrix;
- Scene Inspection;
- matching Project Asset Pipeline Profile.

Persist Tool Registry, Blender version, project profile, runtime path context.

Nie rediscoveruj stable project facts per asset.

---

# Reference reconstruction v0.9

## 1. Technical-sheet analyze

Use `RECON_TECHNICAL_SHEET_ANALYZE`:
- Evidence Model;
- ingestion/view classification/authority;
- measurement/calibration;
- Reference Analysis Cache.

Preferred skills:
- `REFERENCE_MEASURE`;
- `REFERENCE_OVERLAY_VALIDATE` only after registration exists.

Po `ANALYZE: PASS` nie wracaj do broad exploration bez konkretnego conflict/ROI/source update.

## 2. Shape understanding — mandatory before production geometry

Use `RECON_SHAPE_GRAPH_PLAN`.

Load:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- prompt 68;
- script pattern 95.

Preferred skills:
- `SHAPE_GRAPH`;
- `SHAPE_CLASSIFY`.

Required persistent output:
- Shape Graph revision;
- G0–G5 hierarchy;
- RDL0–RDL5 assignment;
- node parent/dependencies;
- shape class;
- authoritative views + controlled properties;
- node validation contract.

`SHAPE_GRAPH != PASS` blocks production geometry except diagnostic RDL0.

## 3. RDL0 envelope

Use `RECON_RDL0`.

Only:
- global bounds;
- axes;
- ground/contact;
- minimal envelope carrier.

Validate FRONT/SIDE/TOP where authoritative.

No detail skills.

## 4. RDL1 primary forms

Use `RECON_NODE_BUILD` **one Shape Node at a time**.

Canonical loop:

```text
SHAPE_GRAPH ready node
-> choose representation skill
-> build/repair current node only
-> QA_SCENE_ISOLATE
-> registered required-view validation
-> numeric/section checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

After all required G1 nodes:
`SHAPE_GRAPH.evaluate_stage_barrier(RDL1)`.

Do not load G2–G5 skills on RDL1 FAIL.

## 5. Shape representation routing

```text
axisymmetric profile
-> AXISYMMETRIC_PROFILE

width/depth/corner treatment change across stations
-> SECTION_LOFT_HARD_SURFACE

structural transition between two sections
-> SECTION_LOFT_HARD_SURFACE

stable 2D profile + depth
-> EXTRUDED_PROFILE / direct mesh strategy

path-driven profile
-> PROFILE_SWEEP / curves

smooth compound freeform without stable sections
-> SUBD_TOPOLOGY_CONTROL
```

### Box-abuse trigger

If primary form changes width + depth + corner treatment along an axis:

```text
PARAMETRIC_BOX + BEVEL
-> not default
-> SHAPE_CLASSIFY
-> MULTI_SECTION_LOFT or SUBD_FREEFORM candidate
```

## 6. RDL2 secondary structural forms

Same node-by-node loop.

Typical:
- side frames;
- display housing;
- utility modules;
- large service panels;
- major trims.

Required G2 stage barrier before RDL3.

## 7. RDL3 structural features

Leaf skills become available only on `ACCEPTED` hosts:

```text
narrow seam/groove -> HS_PANEL_LINE
recess -> boolean/direct recess playbook
layered glass/content -> LAYER_STACK_VALIDATE
radial holes/fasteners -> RADIAL_REPEAT
```

No host acceptance -> feature `BLOCKED`.

## 8. RDL4 edge language

Load edge/bevel/continuity/SubD support modules only now.

Rule:
`shape first -> edge treatment second`.

Bevel cannot repair wrong primary section.

## 9. RDL5 surface/detail

Load branding, materials, decals, emissive, civic finish only after structural barriers.

## 10. Reconstruction final gate

Use:
- `QA_SCENE_ISOLATE`;
- `REFERENCE_OVERLAY_VALIDATE`;
- `RECONSTRUCTION_NODE_GATE` records;
- RDL barriers;
- `RECON_FIDELITY_GATE`.

Runtime is forbidden while final gate is FAIL/UNVERIFIED.

---

# Existing specialized routes

## Panel line
`HS_PANEL_LINE`; add SubD skill only if evaluated cage/flow requires it.

## SubD topology
`SUBD_TOPOLOGY_CONTROL` + topology/normals rules.

## Mesh validation
`MESH_VALIDATE`. Every mesh declares topology intent.

## Civic material finish
`MATERIAL_FINISH_CIVIC`; no uniform global grunge.

## Emissive
`EMISSIVE_HANDOFF`; authored emitter and engine bloom are separate gates.

## UV atlas / runtime bake
`UV_ATLAS_CONTRACT` -> `BAKE_RUNTIME_TEXTURES` -> `BAKE_VALIDATE`.

Use stable semantic part IDs. Missing atlas assignment = FAIL.

## QA/bake contamination
`QA_SCENE_ISOLATE`. `hide_viewport` is not render proof.

## Stale external image in Blender
`IMAGE_CACHE_COHERENCE` before rebake/UV changes.

## Local repair after accepted runtime stages
`PIPELINE_DAG_PLAN` before replaying build/bake/export. Execute dirty dependency closure only.

---

# Game-ready finishing

Use `GAME_READY_FINISH` only after `RECON_FIDELITY_GATE: PASS`.

Preferred skills:
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `ASSET_COMPLETION`.

Order:

```text
runtime path
-> LOD/collision
-> UV contract
-> dirty bake stages
-> bake validation/cache coherence
-> runtime material
-> export/package readback
-> round-trip invariants
-> baked runtime QA
-> completion gate
```

Runtime LOD is downstream from RDL and must not be used as reconstruction progression state.

---

# Pipeline integration

Use `PIPELINE_INTEGRATION` only when target is Level D.

Load verified Project Profile, runtime-root, package, catalog, Engine Smoke Test, Test Oracle.

For current RPG profile reuse:
- `<repo>/Assets/GameAssets`;
- one glTF multi-node LOD packaging;
- current MIRROR_X contract while valid;
- `Source/Engine/AssetCatalog.cpp`;
- `Engine::Model::Load`;
- `Tests/ModelTests.cpp`;
- `Build/windows-debug` / `ModelTests`;
- direct executable exit status.

Blender glTF import = Level C round-trip evidence, not Level D.

---

# Failure routing principles

```text
looks wrong in one view
-> registration/parameters/shape representation

FRONT pass + SIDE/TOP compound-form fail
-> SHAPE_CLASSIFY before random parameter tweaking

child feature fails because host contour wrong
-> parent Shape Node owner

correct source geometry + exported dimension fail
-> EXPORT_ROUNDTRIP_VALIDATE

parseable glTF + missing TEXCOORD_0
-> RUNTIME_PACKAGE_VALIDATE

ambiguous test success
-> TEST_ORACLE
```

After one corrected retry of same strategy, second proven failure requires re-inspection + strategy switch.

---

# Output budget

Use:

```text
compute locally
-> compact node/stage report
-> decision
```

Do not return raw arrays/full logs/full generated scripts unless diagnostic need requires them.

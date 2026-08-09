# Knowledge Router

Agent loads the smallest Task Pack needed for current state, failing evidence and Shape/Appearance owner.

Canonical rule:

```text
intent/current state
-> Task Pack
-> semantic skill
-> executor/tool binding
-> compact evidence
-> decision
```

## v0.12 canonical reconstruction route

This route has precedence over older execution sequences.

```text
runtime pin
-> reference ingest / calibration / conflict arbitration
-> Shape Graph + Appearance Contract + Assembly Relation Contract
-> eligible Shape Node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> mutate exactly one node
-> MUTATION_POSTCONDITION_GATE
-> PASS: persist BUILT_UNVERIFIED
-> source-anchored per-view QA
-> ASSEMBLY_INTEGRITY_GATE for touched relations
-> topology / section / layer checks as required
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> RDL stage barrier
```

After all required reconstruction nodes close:

```text
GEOMETRIC_INTEGRITY_GATE
-> APPEARANCE_FIDELITY_GATE when target requires it
-> RECON_FIDELITY_GATE
-> runtime
```

Hard laws:
- no authorization -> no production geometry mutation;
- builder returned normally -> not proof that geometry changed correctly;
- `BUILT_UNVERIFIED` -> no child unlock;
- assembly semantics must be declared before overlap/gap/contact is judged;
- validator that cannot reject its known-broken fixture cannot own MUST acceptance;
- accepted host repair -> `DEPENDENCY_INVALIDATOR` before further work;
- stale revision evidence becomes `SUPERSEDED`;
- final reference fidelity cannot override failed physical geometry.

## SESSION_PREFLIGHT

Load:
- Agent Charter;
- State Machine;
- Semantic Skill Registry;
- Tool Discovery/Profile;
- Blender 5.1 Compatibility Matrix;
- Scene Inspection;
- matching Project Asset Pipeline Profile.

Run `CANONICAL_SKILL_RUNTIME_PIN` and persist Blender version, project profile, runtime path context, source root and commit.

Do not rediscover stable project facts per asset.

## 1. Technical sheet / concept analysis

Use reference ingestion/classification/authority/measurement modules.

Preferred skills:
- `REFERENCE_MEASURE`;
- `REFERENCE_CONFLICT_RESOLVER` for incompatible property interpretations;
- `REFERENCE_OVERLAY_VALIDATE` only after registration exists.

Required outputs:
- source-set revision and reference IDs;
- calibrated canonical views;
- property-level authority decisions;
- conflicts/unknowns;
- annotation/exclusion policy for technical-sheet masks.

If dimension lines/leaders contaminate a silhouette, route through `191_REFERENCE_MASK_CONTAMINATION_AND_ANNOTATION_EXCLUSION.md`; do not compensate by moving or locally warping the candidate.

## 2. Shape understanding before geometry

Use:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`.

Preferred skills:
- `SHAPE_GRAPH`;
- `SHAPE_CLASSIFY`.

Persistent output:
- G0–G5 Shape Graph revision;
- parent/dependencies;
- RDL0–RDL5 assignment;
- mathematical shape class;
- authoritative views/properties;
- validation contract.

`SHAPE_GRAPH != PASS` blocks production geometry except diagnostic RDL0.

## 3. Appearance and assembly understanding

For target 1:1/L4/L5 build a Reference Appearance Contract before product detail work.

Use:
- `180_REFERENCE_APPEARANCE_CONTRACT.md`;
- `181_ANTI_CIRCULAR_VISUAL_VALIDATION.md`;
- `182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md`;
- `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`;
- `189_ASSEMBLY_RELATION_AND_INTERPENETRATION_CONTRACT.md`.

Required outputs:
- MUST/SHOULD appearance owners;
- part boundaries and trim paths;
- junction owners;
- edge families;
- material/emissive/branding regions;
- detail inventory;
- source reference/ROI per owner;
- semantic assembly relation for important part pairs.

Example:

```text
J_SENSOR_ARM
-> relation = SHADOW_GAP
-> expected gap/tolerance
-> penetration forbidden
```

Do not encode `junction = parts overlap` unless reference/manufacturing evidence explicitly calls for an overlap relation.

## 4. RDL0 diagnostic geometry

Only:
- global envelope;
- ground/contact datum;
- axes;
- major negative space.

Neutral shading only. Validate authoritative FRONT/SIDE/TOP. No detail/lookdev.

## 5. RDL1–RDL3 node loop

For every Shape Node:

```text
SHAPE_GRAPH eligible
-> choose representation skill
-> EXECUTION_AUTHORIZATION_GATE
-> READY_TO_BUILD persisted
-> capture mutation-before snapshot
-> build/repair current node only
-> capture mutation-after snapshot
-> MUTATION_POSTCONDITION_GATE
-> PASS -> BUILT_UNVERIFIED
-> QA_SCENE_ISOLATE
-> source/reference validation
-> ASSEMBLY_INTEGRITY_GATE for every touched MUST relation
-> MESH_VALIDATE / section / layer proof where applicable
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL | UNVERIFIED
```

A failed postcondition returns to the current mutation owner before reference QA. Do not try to hide a silent Boolean no-op with later detail.

### Shape representation routing

```text
axisymmetric profile -> AXISYMMETRIC_PROFILE
width/depth/corner changes across stations -> SECTION_LOFT_HARD_SURFACE
structural transition -> SECTION_LOFT_HARD_SURFACE
stable 2D profile + depth -> EXTRUDED_PROFILE / direct mesh
path-driven profile -> PROFILE_SWEEP / curves
smooth freeform without stable sections -> SUBD_TOPOLOGY_CONTROL
```

Compound primary forms do not default to `PARAMETRIC_BOX + BEVEL`.

### RDL2 product architecture

Major panels, housings, trims and junctions instantiate their Appearance/Assembly owners here. Outer silhouette PASS does not close internal product architecture.

### RDL3 leaf features

Leaf skills run only on accepted hosts:
- seam/groove -> `HS_PANEL_LINE`;
- recess -> Boolean/direct recess + `MUTATION_POSTCONDITION_GATE`;
- layered glass/content -> `LAYER_STACK_VALIDATE`;
- radial holes/fasteners -> `RADIAL_REPEAT`.

## 6. RDL4 edge language

Shape first, then reference edge-family contract, then implementation, then source proof.

Use:
- `164_EDGE_LANGUAGE_SYSTEM.md`;
- `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`;
- `MESH_VALIDATE` after destructive edge/Boolean work.

RDL4 does not pass merely because global dimensions survived bevel.

## 7. RDL5 surface/detail

After structural barriers:
- materials;
- branding;
- decals;
- emissive;
- micro/meso detail required by the contract.

Use `APPEARANCE_OWNER_COVERAGE`. Material segmentation alone is not material appearance proof.

Material-only mutation should preserve geometry signature; otherwise route back to geometry owner.

## 8. Validator trust route

Before a new validator provides MUST evidence:

```text
validator implementation
-> known-good fixture
-> known-broken fixture representing claimed failure class
-> VALIDATOR_NEGATIVE_CONTROL
-> PASS
```

If the broken fixture passes, the validator is toothless. Rework the measurement/algorithm before using its green output.

Use `190_ADVERSARIAL_VALIDATION_AND_NEGATIVE_CONTROLS.md`.

## 9. Repair after acceptance

When accepted geometry changes:

```text
change/repair intent
-> DEPENDENCY_INVALIDATOR
-> changed node DIRTY + revision bump
-> dependent built nodes DIRTY
-> dependent unbuilt nodes BLOCKED
-> hosted Appearance Owners UNVERIFIED
-> revision-bound evidence SUPERSEDED
-> rebuild only affected closure
```

Unrelated accepted branches remain reusable.

Do not manually keep a child green because it still looks plausible after host repair.

## 10. Topology integrity route

Use `MESH_VALIDATE` with explicit topology intent.

For closed solids inspect:
- manifold/boundary state;
- signed volume orientation;
- zero-area/duplicate/loose geometry;
- high-order n-gons;
- non-planar n-gons;
- concave n-gons according to policy.

N-gon existence alone is not failure. Non-planarity, unstable triangulation/shading or contract-specific risk is.

Assembly interpenetration is owned by `ASSEMBLY_INTEGRITY_GATE`, not by generic mesh topology validation.

## 11. Geometric, appearance and final reconstruction gates

Before Level A closure aggregate current physical proof:

```text
current mutation postconditions
+ current Assembly Relation closure
+ current topology records
+ required validator negative controls
+ zero stale evidence
-> GEOMETRIC_INTEGRITY_GATE
```

Then for target >= L4:

```text
GEOMETRIC_INTEGRITY_GATE PASS
+ APPEARANCE_OWNER_COVERAGE
+ APPEARANCE_FIDELITY_GATE
+ all required Shape Nodes ACCEPTED
+ no stale/superseded proof referenced by current revisions
-> RECON_FIDELITY_GATE
```

MUST categories are non-compensating. A high visual score cannot override physical integrity failure.

## 12. Runtime/game-ready route

Start only after reconstruction closure.

Preferred order:

```text
runtime path
-> LOD/collision
-> UV contract
-> bake stages
-> bake validation/cache coherence
-> runtime material
-> export/package readback
-> round-trip invariants
-> target-engine proof if Level D
-> completion gate
```

Preferred skills:
- `RUNTIME_PATH_RESOLVE`;
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `TEST_ORACLE`;
- `ASSET_COMPLETION`.

Blender glTF re-import remains Level C evidence, not Level D engine proof.

## Failure routing

```text
builder runs but recess/feature absent
-> MUTATION_POSTCONDITION_GATE

parts visually fight / z-fight / pierce each other
-> ASSEMBLY_RELATION contract + ASSEMBLY_INTEGRITY_GATE

validator says PASS on obvious known defect
-> VALIDATOR_NEGATIVE_CONTROL

repair changes accepted host
-> DEPENDENCY_INVALIDATOR before rebuild

outer silhouette passes but product reads wrong
-> Appearance Contract / internal architecture

FRONT pass + SIDE/TOP compound form fail
-> SHAPE_CLASSIFY before parameter thrashing

technical-sheet contour polluted by leaders/text
-> reference mask contamination route

correct Blender geometry + exported dimension fail
-> EXPORT_ROUNDTRIP_VALIDATE

parseable glTF + missing TEXCOORD_0
-> RUNTIME_PACKAGE_VALIDATE

ambiguous automated test success
-> TEST_ORACLE / bite test
```

After one corrected retry of the same strategy, a second proven failure requires re-inspection and strategy switch.

## Output budget

```text
compute locally
-> compact node/assembly/appearance/stage report
-> decision
```

Do not dump raw mesh arrays/full logs/scripts into reasoning unless required for a concrete diagnostic.

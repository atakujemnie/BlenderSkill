# Reconstruction Layer Index and Controller v0.9

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D z concept sheet, blueprintów, rzutów, zdjęć, renderów, wymiarów i opisów.

Nie jest to warstwa inspiracji. Celem jest evidence-constrained reconstruction z kontrolowaną niepewnością.

## Fundamental rule

```text
UNDERSTAND FORM
-> BUILD COARSE
-> PROVE
-> ADD DETAIL
```

Nie:

```text
reference -> one large Blender script -> inspect finished scene
```

Model z poprawnym detalem, ale błędną primary form jest nieudaną rekonstrukcją.

---

## v0.9 controller pipeline

```text
INGEST
-> CLASSIFY EVIDENCE
-> AUTHORITY
-> REGISTER
-> CONSTRAIN
-> DECOMPOSE
-> SHAPE GRAPH
-> RDL0 ENVELOPE
-> RDL1 PRIMARY FORMS node-by-node
-> RDL2 SECONDARY STRUCTURAL FORMS node-by-node
-> RDL3 STRUCTURAL FEATURES node-by-node
-> RDL4 EDGE LANGUAGE
-> RDL5 SURFACE/DETAIL
-> MULTIVIEW + RECON_FIDELITY_GATE
-> TOPOLOGY/RUNTIME
-> EXPORT/ENGINE
```

Detailed state: `149_RECONSTRUCTION_STATE_MACHINE.md`.

---

# Knowledge groups

## Evidence / authority
100–109.

Important:
- Evidence Model;
- ingestion/segmentation/classification;
- View Authority Matrix;
- conflict resolution;
- uncertainty/provenance.

## Geometric constraints
110–123.

Important:
- Dimension Graph;
- landmark/keypoint system;
- coordinate registration/calibration;
- silhouette constraints;
- negative space;
- cross-section/profile/curvature inference;
- thickness/gaps/panel lines.

## Surface evidence
124–127.

## Form decomposition and construction
128–140 plus v0.9:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `129_FEATURE_TO_MODELING_STRATEGY_MAP.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`;
- `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`.

## Validation
141–148 + v0.8 fidelity/evidence modules.

## Governance
149–159.

## Specialized modes
160–173.

---

# 1. Reference analysis

Before geometry identify:
- projection/view class;
- known dimensions/datums;
- principal axes;
- global silhouette;
- major landmarks;
- negative spaces;
- primary planes/profiles/curves;
- repeated structures;
- material boundaries;
- hidden/uncertain geometry;
- conflicts between prompt/card/views.

Do not convert uncertain pixels into fake metric precision.

---

# 2. Registration before deformation

When a screen-space mismatch exists diagnose:

```text
projection class
-> calibration
-> camera/ortho scale
-> shift/rotation
-> object orientation
-> only then geometry
```

QA cameras are evidence instruments. Once registered, do not move them to hide geometry error.

---

# 3. Shape Graph before production geometry

After constraints, decompose asset into:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

Build `Reconstruction Shape Graph`.

Each required node records:
- role;
- parent/dependencies;
- G-level + RDL;
- shape class;
- feature ownership;
- authoritative views;
- controlled properties per view;
- numeric/relationship constraints;
- validation contract;
- implementation skill.

Graph structural PASS is required before production modeling.

---

# 4. Representation-first construction

Do not select Blender operators before the shape class.

Canonical classes:
- primitive;
- extruded profile;
- revolved profile;
- profile sweep;
- multi-section loft/transition;
- SubD freeform;
- recess/panel-line/layered assembly;
- hybrid assembly.

Example:

```text
width changes with Z
+ depth changes with Z
+ corner treatment changes with Z
=> do not default to cube + bevel
=> classify as MULTI_SECTION_LOFT / SUBD_FREEFORM candidate
```

Use `177` and `129`.

---

# 5. RDL coarse-to-fine

Reconstruction Detail Levels:

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

`RDL != runtime LOD`.

Runtime LOD starts only after reconstruction fidelity PASS.

---

# 6. Node-by-node build loop

For each ready Shape Node:

```text
validate dependencies
-> select representation skill
-> build current node only
-> mark BUILT_UNVERIFIED
-> QA scene isolation
-> render required canonical views
-> registered local/global comparison
-> numeric/section checks
-> regression outside expected-change region
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

Accepted node unlocks dependent children.

A required child is blocked when its required parent/dependency is not accepted.

---

# 7. Stage barriers

After each RDL:

```text
all required nodes accepted
+ protected earlier invariants pass
=> RDL barrier PASS
```

No RDL2 before RDL1 barrier.
No structural features before accepted hosts.
No edge language before structural form.
No surface finish before geometry acceptance.

---

# 8. Multi-view responsibilities

Multiple views constrain one 3D object.

Typical:

```text
FRONT -> width/height/front contour
SIDE -> depth/height/profile
TOP -> width/depth/corner plan
REAR -> rear form/features
BOTTOM -> underside/contact/service geometry
HERO -> supporting spatial/edge/material interpretation
```

Every node states exactly what each required view controls.

Do not accept `looks okay`.

---

# 9. Cross-section and loft logic

For forms varying along an axis define semantic section stations.

Validate:
- station positions;
- width/depth;
- corner/chamfer/profile family;
- common point correspondence;
- no unintended twist;
- continuity intent;
- FRONT/SIDE/TOP projection.

Preferred skill for supported forms:
`SECTION_LOFT_HARD_SURFACE`.

---

# 10. Detail skills are leaf skills

Only after host acceptance:
- narrow seam -> `HS_PANEL_LINE`;
- SubD cage/flow -> `SUBD_TOPOLOGY_CONTROL`;
- radial patterns -> `RADIAL_REPEAT`;
- recess -> boolean/direct recess strategy;
- layered display -> `LAYER_STACK_VALIDATE`;
- branding/decals/materials -> RDL5.

A leaf skill never substitutes for primary-form understanding.

---

# 11. Validation hierarchy

```text
node numeric/silhouette
-> node neutral/matcap
-> RDL stage barrier
-> whole-asset registered multiview
-> material/surface evidence
-> final RECON_FIDELITY_GATE
```

Required proof is typed and has provenance. Bare `PASS` is `UNVERIFIED` where strict evidence is required.

QA isolation is mandatory; collision/export/LOD proxies cannot stand in for the asset.

---

# 12. Repair priority

When validation fails:

```text
registration
-> scale/constraints
-> shape representation
-> primary form parameters
-> secondary form
-> structural feature
-> edge treatment
-> surface
```

After one corrected retry, second proven failure of the same strategy requires re-inspection and possible representation switch.

Do not perform endless visual tweaking.

---

# 13. Final reconstruction gate

Before runtime:
- Shape Graph current and valid;
- required G0–G3 nodes accepted;
- required RDL barriers PASS;
- hard dimensions PASS;
- canonical registered views PASS;
- primary landmarks/proportions PASS;
- MUST feature evidence PASS;
- material segmentation PASS when target fidelity requires it;
- authority conflicts/deviations closed;
- final `RECON_FIDELITY_GATE: PASS`.

Only then route to topology/UV/runtime LOD/bake/export.

---

# 14. Single-image mode

When only one image exists:
- solve visible silhouette/landmarks;
- infer depth conservatively;
- separate observed/derived/inferred;
- keep hidden geometry minimal;
- Shape Graph may contain LOW/UNKNOWN-confidence nodes;
- do not claim fully determined literal 1:1 in unobserved regions.

---

# 15. Persistent outputs

```text
Reference Registry
Evidence Ledger
View Authority Matrix
Dimension Graph
Feature Contract
Shape Graph + revision
Node Contracts
Node Acceptance Records
RDL Stage Barrier Records
Reconstruction Fidelity Report
```

Conversation history is not the execution database.

---

# Final rule

Agent must answer these questions before detail:

```text
What is the global form?
What are the primary forms?
What depends on what?
Which views define each form?
What mathematical representation fits each form?
How will each form be proven before children are added?
```

Dopiero potem wykonuje Blender operations.

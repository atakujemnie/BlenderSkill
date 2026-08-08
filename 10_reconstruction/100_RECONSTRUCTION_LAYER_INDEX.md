# Reconstruction Layer Index and Controller v0.10

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D z concept sheet, blueprintów, rzutów, zdjęć, renderów, wymiarów i opisów.

Nie jest to warstwa inspiracji. Celem jest evidence-constrained reconstruction z kontrolowaną niepewnością.

v0.10 adds a second reconstruction model alongside Shape Graph:

```text
Shape Graph
= what forms exist and how they depend on each other

Reference Appearance Contract
= which visible boundaries, trims, junctions, edge/material/detail families make this the same product
```

## Fundamental rule

```text
UNDERSTAND FORM
-> UNDERSTAND VISIBLE PRODUCT ARCHITECTURE
-> BUILD COARSE
-> PROVE FROM SOURCE
-> ADD DETAIL
-> PROVE APPEARANCE
```

Not:

```text
reference -> one large Blender script -> builder-local PASS -> runtime
```

A model with correct dimensions and outer silhouette but wrong internal architecture is a failed reconstruction.

---

## v0.10 controller pipeline

```text
INGEST
-> CLASSIFY EVIDENCE
-> PROPERTY-LEVEL AUTHORITY
-> REGISTER
-> CONSTRAIN
-> DECOMPOSE
-> SHAPE GRAPH
-> APPEARANCE CONTRACT for 1:1/L4/L5
-> RDL0 ENVELOPE
-> RDL1 PRIMARY FORMS node-by-node
-> RDL2 SECONDARY STRUCTURAL FORMS + major boundaries/trim/junctions
-> RDL3 STRUCTURAL FEATURES
-> RDL4 EDGE FAMILY FIDELITY
-> RDL5 MATERIAL/DETAIL FIDELITY
-> APPEARANCE_FIDELITY_GATE when required
-> RECON_FIDELITY_GATE
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
- uncertainty/provenance;
- property-level source ownership.

## Geometric constraints
110–123.

Important:
- Dimension Graph;
- landmarks/keypoints;
- registration/calibration;
- silhouette;
- negative space;
- cross-sections/profiles/curvature;
- thickness/gaps/panel lines.

## Surface evidence
124–127 plus `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`.

## Form decomposition and construction
128–140 plus:
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`;
- `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`.

## Appearance fidelity v0.10
- `180_REFERENCE_APPEARANCE_CONTRACT.md`;
- `181_ANTI_CIRCULAR_VISUAL_VALIDATION.md`;
- `182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md`;
- `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`.

## Validation
141–148 + proof-integrity modules + appearance gate.

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
- visible part/material boundaries;
- trim paths;
- junctions;
- edge families;
- hidden/uncertain geometry;
- conflicts between prompt/card/views.

Do not convert uncertain pixels into fake metric precision.

---

# 2. Property-level authority

Do not assign one source blanket authority over every property.

Example:

```text
overall width -> PRINTED_DIMENSION
side outer contour -> SIDE_ORTHO
trim path -> SIDE + HERO + DETAIL
rear panel architecture -> REAR
brush direction -> MATERIAL DETAIL / HERO
```

Resolve conflicts per property and persist provenance.

---

# 3. Registration before deformation

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

# 4. Shape Graph before production geometry

After constraints, decompose asset into:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

Each required node records role, dependencies, RDL, shape class, authoritative views, constraints, validation contract and implementation skill.

Graph structural PASS is required before production modeling.

---

# 5. Appearance Contract for 1:1 / L4 / L5

Inventory visible owners before they can silently disappear:

```text
PART_BOUNDARY
TRIM_PATH
JUNCTION
EDGE_FAMILY
MATERIAL_REGION
MATERIAL_RESPONSE
EMISSIVE_REGION
BRANDING_REGION
DETAIL_FEATURE
DETAIL_DENSITY_REGION
NEGATIVE_SPACE
```

Each owner records:
- host Shape Node(s);
- source reference IDs;
- source ROIs;
- required views;
- importance;
- validation methods.

A single Shape Node may contain many appearance owners.

---

# 6. Representation-first construction

Do not select Blender operators before shape class.

Canonical classes:
- primitive;
- extruded profile;
- revolved profile;
- profile sweep;
- multi-section loft/transition;
- SubD freeform;
- recess/panel-line/layered assembly;
- hybrid assembly.

If width, depth and corner treatment change across an axis, do not default to box + bevel.

---

# 7. RDL coarse-to-fine

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms / major product architecture
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

`RDL != runtime LOD`.

Runtime LOD starts only after final reconstruction gates PASS.

---

# 8. Canonical node-by-node build loop

For each ready Shape Node:

```text
validate dependencies
-> select representation skill
-> build current node only
-> mark BUILT_UNVERIFIED
-> QA scene isolation
-> render required canonical views
-> registered source comparison
-> numeric/section checks
-> regression outside expected-change region
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL | UNVERIFIED
```

Strict reference-derived PASS requires canonical validator ID, provenance, source reference and registration for projected evidence.

A builder-local `Gate.accept()` cannot substitute for the canonical gate.

---

# 9. Anti-circular proof

This proves implementation consistency only:

```text
infer parameter P
-> build P
-> test geometry == P
```

Reference fidelity additionally requires:

```text
source evidence
-> source-fit / registered comparison
-> candidate artifact
-> canonical validator
```

Persist derivation records for inferred radii, angles, stations and paths.

---

# 10. Stage barriers

After each RDL:

```text
all required nodes accepted
+ protected earlier invariants pass
=> RDL barrier PASS
```

No RDL2 before RDL1 barrier.
No structural feature on failed host.
No edge/material fidelity claim before structural acceptance.

---

# 11. Internal product architecture

Outer silhouette does not validate internal visible architecture.

For MUST regions validate:
- part boundaries;
- panel transitions;
- trim centerline/width/termination;
- junction participants/order;
- shadow gaps;
- plinth splits;
- rear service bands;
- seat/support and backrest/endcap relationships.

Use `182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md` and `APPEARANCE_REFERENCE_VALIDATE`.

---

# 12. RDL4 edge-family fidelity

For every MUST edge family validate:
- profile type;
- radius/chamfer/step family;
- start/end;
- continuity;
- relation to part/material boundary;
- protected dimension survival.

`bevel did not change bounds` is not enough.

Validate neutral/clay plane hierarchy so excessive smoothing cannot hide missing hard-surface planes.

---

# 13. RDL5 material and detail fidelity

Separate:

```text
material segmentation
!=
material appearance
```

For L4/L5 validate as evidence requires:
- metallic/dielectric identity;
- roughness hierarchy;
- brushing/anisotropy direction;
- micro-normal scale;
- glass/emissive response;
- visible material boundaries;
- controlled wear hierarchy.

For L5, all MUST meso/detail features must be accounted for. Silent omission is forbidden.

---

# 14. Appearance Fidelity Gate

For target >= L4 aggregate:
- part boundaries;
- trim paths;
- junctions;
- edge families;
- material response;
- final matched views;
- emissive/branding where present;
- detail coverage for L5.

MUST categories are non-compensating.

A high global score cannot erase a failed design-defining owner.

---

# 15. Final reconstruction gate

Before runtime require:
- current valid Shape Graph;
- current Appearance Contract when required;
- required G0–G3 nodes accepted;
- required RDL barriers PASS;
- hard dimensions PASS;
- canonical registered views PASS;
- primary landmarks/proportions PASS;
- MUST geometry/features PASS;
- internal architecture owners PASS;
- edge/material/detail evidence according to target;
- `APPEARANCE_FIDELITY_GATE: PASS` for L4/L5;
- authority conflicts/deviations closed;
- `RECON_FIDELITY_GATE: PASS`.

Only then route to topology/UV/runtime LOD/bake/export.

---

# 16. Runtime lock

For L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> runtime forbidden
```

Correct dimensions, alpha silhouette, triangle budgets, UVs, package readback or engine import cannot override this lock.

---

# 17. Repair priority

When validation fails:

```text
registration
-> authority/constraints
-> shape representation
-> primary form
-> internal product architecture
-> secondary form
-> structural feature
-> edge family
-> material/detail
```

After one corrected retry, second proven failure of same strategy requires re-inspection and possible representation switch.

Do not perform endless visual tweaking.

---

# 18. Persistent outputs

```text
Reference Registry
Evidence Ledger
Property Authority Map
Dimension Graph
Feature Contract
Shape Graph + revision
Reference Appearance Contract + revision
Part Boundary / Trim / Junction Graph
Node Contracts
Node Acceptance Records
Appearance Owner Records
RDL Stage Barrier Records
Appearance Fidelity Report
Reconstruction Fidelity Report
```

Conversation history is not the execution database.

---

# Single-image mode

When only one image exists:
- solve visible silhouette/landmarks;
- infer depth conservatively;
- separate observed/derived/inferred;
- keep hidden geometry minimal;
- use LOW/UNKNOWN confidence where appropriate;
- do not claim fully determined literal 1:1 in unobserved regions.

---

# Final rule

Before detail the agent must answer:

```text
What is the global form?
What are the primary forms?
What depends on what?
Which views define each form?
What mathematical representation fits each form?
Which visible boundaries/trims/junctions make it this exact product?
Which source proves each of them?
How will validation remain independent of builder assumptions?
```

Dopiero potem wykonuje Blender operations i claimuje fidelity.

# Node-by-Node Multi-View Validation

## v0.11 validation amendment

Before the loop begins, one eligible node must receive `EXECUTION_AUTHORIZATION_GATE` and persisted `READY_TO_BUILD`. After mutation persist `BUILT_UNVERIFIED` and stop until the canonical node gate closes.

Evidence mode is per view: ORTHO/NEAR_ORTHO -> registered overlay; HERO -> supporting `PERSPECTIVE_INSPECTION`; DETAIL -> `LOCAL_FEATURE_ROI`. Significant derived parameters require value/method/source/confidence/provenance and a conflict decision when needed. Builder consistency against its own constants never replaces source proof.

---

## Purpose

Validate one form immediately after it is built, before the scene is densified with dependent geometry.

v0.10 additionally prevents a node from certifying itself through builder-local checks.

Do not wait for the final asset render to discover a primary-form error.

---

## Core loop

For every `READY_TO_BUILD` Shape Node:

```text
isolate accepted ancestors + current node
-> build/repair current node only
-> persist BUILT_UNVERIFIED artifact/revision
-> render required canonical views
-> registered comparison per view/ROI
-> numeric/section checks
-> canonical RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL | UNVERIFIED
```

Only `ACCEPTED` unlocks dependent children.

---

## Canonical acceptance rule

Strict node acceptance is derived from validator artifacts, not builder state.

Required records name:
- `validator_id`;
- `provenance_id`;
- `source_reference_id(s)` for reference-derived evidence;
- `registration_id` for projected evidence.

For required view proof use canonical registered validators such as:
- `REFERENCE_OVERLAY_VALIDATE`;
- `APPEARANCE_REFERENCE_VALIDATE` where internal appearance owner is being checked.

A builder-local helper may produce measurements. It may not substitute for `RECONSTRUCTION_NODE_GATE`.

Invalid:

```text
builder chooses radius 165
-> builder makes radius 165
-> local Gate verifies radius 165
-> node ACCEPTED
```

Valid:

```text
source ROI / explicit dimension
-> source-fit or registered validator artifact
-> candidate artifact
-> RECONSTRUCTION_NODE_GATE
```

---

## View responsibility contract

Each node defines what each view controls.

Example:

```yaml
BASE_PLINTH:
  FRONT:
    controls: [width, height, shoulder_contour]
  SIDE:
    controls: [depth, height, front_rear_profile]
  TOP:
    controls: [width, depth, corner_plan]
  HERO:
    controls: [transition_interpretation]
```

Do not require views that add no evidence. Do not omit a REQUIRED view.

For product/civic hard-surface, view responsibilities may include internal boundaries, not only outer contour.

Example:

```yaml
SIDE_MODULE_R:
  SIDE:
    controls:
      - outer_profile
      - composite_panel_boundary
      - trim_path
      - utility_panel_junction
```

---

## Isolation rule

Node QA render contains only:
- accepted ancestor/host geometry required for context;
- current node;
- required QA rig.

Do not render:
- runtime collision;
- LOD proxies;
- future RDL nodes;
- helper shells;
- export copies;
- unrelated scene geometry.

Use `QA_SCENE_ISOLATE`.

`isolation_status != PASS` means node is `UNVERIFIED` even if visual metrics look good.

---

## Registered comparison

For authoritative orthographic/near-orthographic evidence:
- one global registration per view;
- same crop/aspect/physical scale;
- no local translation/warp of current node;
- ROI may restrict evaluation area but must not change global registration;
- record source reference ID and registration ID.

Preferred skill:
`REFERENCE_OVERLAY_VALIDATE`.

For internal boundary/trim/junction owners:
`APPEARANCE_REFERENCE_VALIDATE`.

---

## Outer silhouette vs internal architecture

A node may affect:
- `GLOBAL_SILHOUETTE`;
- `LOCAL_BOUNDARY`;
- `INTERNAL_FEATURE`;
- `MATERIAL_BOUNDARY`;
- `TRIM_PATH`;
- `JUNCTION`;
- `NO_SILHOUETTE`.

### Global silhouette node
After repair validate:
1. node ROI;
2. global canonical silhouette regression.

### Internal architecture node
Validate:
1. source-registered owner ROI;
2. boundary/path/junction metrics;
3. parent protected-region regression.

Do not use global silhouette IoU as proof of an internal boundary.

---

## Numeric responsibilities

Depending on shape class validate:
- bounds;
- centerline;
- station heights;
- width/depth per station;
- profile landmarks;
- recess depth;
- contact plane;
- layer order;
- symmetry/asymmetry;
- cross-section sample contract.

Image overlay does not replace locked numeric dimensions.

Builder-consistency numeric checks do not replace source anchoring for derived parameters.

---

## Derived-parameter proof

If a node uses an inferred radius/angle/station/path, persist derivation evidence:

```yaml
derived_parameter:
  id: SIDE_FRONT_RADIUS
  value_mm: 165
  method: ARC_FIT
  source_reference_id: side_ref_v2
  source_roi: [...]
  confidence: 0.84
  residual_px: 2.9
```

Then node validation may contain both:
- geometry == derived parameter consistency;
- source-fit/registered projected evidence.

The first without the second is insufficient for reference acceptance.

---

## Cross-section validation

For `MULTI_SECTION_LOFT` / `MULTI_SECTION_TRANSITION` require station report.

Example:

```yaml
sections:
  - station: BASE_BOTTOM
    z_mm: 0
    width_mm: 600
    depth_mm: 300
    source_fit_id: section_fit_bottom_003
    status: PASS
  - station: BASE_UPPER
    z_mm: 95
    width_mm: 570
    depth_mm: 282
    source_fit_id: section_fit_upper_003
    status: PASS
```

Additionally validate:
- monotonic ordering along loft axis;
- common vertex correspondence;
- no unintended twist;
- expected corner/chamfer family;
- transition continuity;
- source-backed station geometry when sections are derived from reference.

---

## Appearance-owner interaction

A Shape Node can be geometrically accepted while appearance owners over its surface remain open.

Example:

```text
SIDE_MODULE_R geometry ACCEPTED
SIDE_TRIM_PATH_R appearance FAIL
```

Result:
- dependent geometry children may follow Shape Graph rules if their host geometry is accepted;
- RDL4/L4 final appearance cannot pass;
- runtime remains locked through `APPEARANCE_FIDELITY_GATE`.

If the failed appearance owner reveals that host geometry itself is wrong, route failure back to the host Shape Node and mark affected descendants DIRTY.

---

## Node acceptance minimum

```yaml
node_gate:
  node_id: LOWER_SHOULDER
  graph_revision: sg_006
  node_revision: node_009
  parent_status: PASS
  isolation:
    status: PASS
    evidence_kind: QA_SCENE_ISOLATION
    validator_id: QA_SCENE_ISOLATE
    provenance_id: iso_009
  required_views:
    FRONT:
      status: PASS
      evidence_kind: REGISTERED_OVERLAY
      validator_id: REFERENCE_OVERLAY_VALIDATE
      provenance_id: front_009
      source_reference_id: front_ref_v3
      registration_id: front_reg_v3
    SIDE:
      status: PASS
      evidence_kind: REGISTERED_OVERLAY
      validator_id: REFERENCE_OVERLAY_VALIDATE
      provenance_id: side_009
      source_reference_id: side_ref_v3
      registration_id: side_reg_v3
  numeric_constraints:
    status: PASS
    evidence_kind: NUMERIC_MEASUREMENT
    validator_id: REFERENCE_MEASURE
    provenance_id: num_009
  section_contract:
    status: PASS
    evidence_kind: NUMERIC_MEASUREMENT
    validator_id: SECTION_LOFT_HARD_SURFACE
    provenance_id: sections_009
  regression:
    status: PASS
    evidence_kind: REGRESSION_DIFF
    validator_id: REFERENCE_OVERLAY_VALIDATE
    provenance_id: regression_009
  status: ACCEPTED
```

All strict PASS fields are proof-bearing.

---

## Failure routing

If FRONT/SIDE/TOP indicate different failure classes, assign failure to:
- registration;
- parameters;
- representation;
- parent relation;
- internal appearance owner;
- material/edge stage.

Example:

```text
FRONT width PASS
SIDE outer depth PASS
SIDE trim path FAIL
TOP corner plan PASS
```

Do not randomly alter depth. The likely owner is trim/part architecture, not global envelope.

Example:

```text
FRONT width PASS
SIDE depth FAIL
TOP corner-plan FAIL
```

often indicates a wrong 3D representation rather than one scalar parameter.

---

## Stop rule

`MUST Shape Node + FAIL`:
- stop that Shape Graph branch;
- do not build children;
- do not advance RDL;
- repair or switch representation.

`MUST Appearance Owner + FAIL`:
- stop the appearance stage that depends on it;
- do not claim L4/L5;
- do not enter runtime;
- route to owner/host repair.

Do not save either case as a cosmetic TODO for the end.

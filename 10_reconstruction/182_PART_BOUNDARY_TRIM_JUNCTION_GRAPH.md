# Part Boundary, Trim and Junction Graph

## Purpose

Represent the internal visible architecture of a hard-surface product.

Outer silhouette answers:

```text
where does the object end?
```

This graph answers:

```text
where do its manufactured parts, materials and transitions begin and end?
```

The distinction is mandatory for products whose identity depends on panel architecture, trim and junctions.

---

## Why this exists

The Lafar Street Bench v0.9 result kept the global 2000 x 550 x 820 envelope and passed outer silhouette checks while losing much of the Astera design language.

The failure was concentrated inside the silhouette:
- side trim width/path;
- side panel boundary;
- plinth separation;
- shoulder/end-cap transition;
- rear service bands;
- seat/support shadow gap.

Therefore internal visible contours must be first-class reconstruction evidence.

---

## Graph entities

### Part region
A visible manufactured region with stable identity.

```yaml
part_region:
  id: SIDE_COMPOSITE_R
  host_shape_node: SIDE_MODULE_R
  material_family: DARK_COMPOSITE
```

### Boundary
A visible contour between two regions.

```yaml
boundary:
  id: B_SIDE_TRIM_COMPOSITE_R
  a: SIDE_TRIM_R
  b: SIDE_COMPOSITE_R
  importance: MUST
  required_views: [FRONT, SIDE, HERO]
```

### Junction
A multi-part transition where simple two-region boundary is insufficient.

```yaml
junction:
  id: J_SIDE_BACKREST_R
  participants: [SIDE_COMPOSITE_R, SIDE_TRIM_R, BACKREST, ENDCAP_R]
  importance: MUST
  required_views: [SIDE, HERO, REAR]
```

### Trim path
A design-defining elongated part or material strip.

```yaml
trim:
  id: T_SIDE_ALU_R
  host: SIDE_MODULE_R
  centerline_landmarks: [...]
  width_samples: [...]
  wraps_corner: true
  termination: BACKREST_ENDCAP
```

---

## Boundary classes

```text
GEOMETRIC_STEP
SHADOW_GAP
SEAM
MATERIAL_BORDER
TRIM_EDGE
RECESS_EDGE
OVERLAP_EDGE
CONTACT_EDGE
OPENING_EDGE
```

A boundary may have multiple classes only when evidence supports the combination.

---

## Required data

For every MUST boundary:
- stable boundary ID;
- adjacent regions;
- source reference IDs;
- source ROIs per authoritative view;
- path landmarks or sampled contour;
- expected boundary class;
- expected relative depth/order if visible;
- validation methods;
- owner revision.

For every MUST junction:
- participants;
- contact/order relation;
- supporting views;
- expected continuity or discontinuity;
- protected negative space if any.

---

## Boundary validation

Preferred evidence:
- registered edge/contour overlay;
- landmark projection;
- feature ROI mask;
- layer/depth ordering;
- numeric gap/offset where explicitly defined.

Metrics may include:

```yaml
boundary_metrics:
  mean_normal_distance_px: 1.8
  p95_normal_distance_px: 4.2
  endpoint_error_px: 2.1
  width_error_pct: 3.4
  missing_length_pct: 0.0
```

Global silhouette IoU is not a boundary metric.

---

## Trim validation

For design-defining trim compare:
1. path centerline;
2. visible width at semantic stations;
3. start/end/termination;
4. corner wrapping;
5. adjacency to host regions;
6. material identity;
7. continuity across connected parts.

A trim object that exists but follows a different path is FAIL.

A lighting highlight that visually resembles trim in one render is not trim evidence.

---

## Junction validation

Junctions often determine whether the object reads as engineered or improvised.

Check:
- part order;
- contact gaps;
- tangent/normal continuity;
- step height;
- overlap logic;
- edge-family transition;
- local negative space.

Example Street Bench right shoulder:

```text
side shell
-> aluminium cap
-> dark shoulder insert
-> backrest shell
```

Replacing the sequence with one broad wedge is not equivalent even if the outside contour is similar.

---

## Graph relation to Shape Graph

Part-boundary graph is a view/appearance graph over accepted shape nodes.

```text
Shape Node revision changes
-> affected part regions DIRTY
-> connected boundaries DIRTY
-> junctions DIRTY
-> appearance gate invalidated
```

A G1/G2 shape node may own multiple part regions.

This is expected and prevents one coarse node from hiding product-defining subdivisions.

---

## Stage use

### RDL1
Declare primary region boundaries that affect form understanding.

### RDL2
Build/validate major trim, panels and junctions.

### RDL3
Add service seams/recess boundaries.

### RDL4
Validate edge-family transitions along boundaries.

### RDL5
Validate material borders and surface behavior.

Do not wait until RDL5 to discover that a major metallic cap follows the wrong path.

---

## Acceptance minimum

For target fidelity L4/L5:

```yaml
part_boundary_graph:
  revision: pbg_004
  must_boundaries_total: 18
  must_boundaries_pass: 18
  must_junctions_total: 6
  must_junctions_pass: 6
  missing_must: 0
  status: PASS
```

Any missing MUST boundary or junction is a blocker unless explicitly waived by authority.
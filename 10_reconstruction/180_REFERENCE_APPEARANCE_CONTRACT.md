# Reference Appearance Contract

## Purpose

Shape Graph answers **what forms exist** and how they depend on each other.

Reference Appearance Contract answers **what must be visibly true for the reconstructed object to read as the same designed product**.

The contract is mandatory for reference-driven assets when:
- target fidelity >= L4;
- the user asks for 1:1 / exact / faithful reconstruction;
- the reference contains product-defining material, trim, panel, junction or edge-language information;
- a benchmark is evaluated visually against concept art.

It exists because a model can have correct global dimensions and outer silhouette while remaining a poor reconstruction.

---

## Appearance owners

Each reference-defining visible property belongs to one explicit owner.

Canonical owner classes:

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

An owner is not automatically a Blender object.

Example:

```yaml
owner_id: SIDE_TRIM_PATH_R
class: TRIM_PATH
host_nodes: [SIDE_SHELL_R, BACKREST_ENDCAP_R]
importance: MUST
required_views: [FRONT, SIDE, HERO]
source_reference_ids: [sheet_tech_v1, sheet_hero_v1]
source_rois:
  SIDE: [x0, y0, x1, y1]
  HERO: [x0, y0, x1, y1]
properties:
  - path_centerline
  - visible_width
  - corner_wrap
  - continuity
  - material_boundary
validation:
  - REGISTERED_OVERLAY
  - FEATURE_ROI
  - LANDMARK_PROJECTION
```

---

## Property-level authority

Authority is assigned per visible property, not once for the whole asset.

Example:

```text
overall width       -> PRINTED_DIMENSION
side outer contour  -> SIDE_ORTHO
trim path           -> HERO + SIDE + DETAIL
rear service bands  -> REAR
brushed direction   -> MATERIAL_DETAIL + HERO
utility placement   -> SIDE + printed offsets
```

Do not collapse this into a global statement such as `the card wins`.

A printed dimension can override a conflicting inferred width without becoming authority for:
- material boundaries;
- trim path;
- edge profile;
- panel subdivision;
- surface finish.

---

## Required inventory before RDL4/RDL5

For target L4/L5 create an `appearance_contract` containing:

```yaml
appearance_contract:
  revision: ac_003
  source_set_revision: refset_004
  owners:
    - owner_id: ...
      class: ...
      importance: MUST | SHOULD | MAY
      source_reference_ids: [...]
      required_views: [...]
      validation_methods: [...]
      status: DECLARED
```

At minimum inventory:
- visible material-region boundaries;
- major trim paths;
- major junctions between primary/secondary forms;
- edge families that change the product character;
- branding/info-screen regions;
- emissive regions;
- visible meso-scale panel/service details;
- distinctive negative spaces.

---

## Appearance hierarchy

Use the following hierarchy to avoid treating all detail as equivalent:

### A0 — composition / massing
- global silhouette;
- primary negative space;
- major mass ratios.

### A1 — internal product architecture
- part boundaries;
- large panel transitions;
- trim paths;
- major junctions.

### A2 — edge language
- protective radii;
- chamfers;
- stepped lips;
- shadow gaps;
- continuity between materials.

### A3 — material identity
- dark/light region placement;
- metallic/dielectric distinction;
- roughness hierarchy;
- directionality / anisotropy;
- glass/emissive response.

### A4 — meso detail
- service seams;
- utility recesses;
- fastener groups;
- underside panel layout;
- local trim terminations.

### A5 — micro detail / wear
- brushing scratches;
- micro-normal;
- fingerprints/touch zones;
- weathering/dust/rain traces.

A high A0 score does not compensate for failed A1/A2 on a design where those layers are MUST.

---

## Part-boundary requirement

Outer silhouette validates only the external contour.

A faithful hard-surface product often depends more on internal contours such as:
- metal/composite boundary;
- removable panel perimeter;
- side-shell/backrest shoulder;
- seat/support shadow gap;
- rear cover/service band;
- lower plinth split.

Every MUST boundary receives:
- stable ID;
- owner class;
- source ROI;
- host relation;
- expected path/landmarks;
- validation evidence.

---

## Trim path contract

For a design-defining trim, record:

```yaml
trim_path:
  centerline_landmarks: [...]
  visible_width_samples: [...]
  host_adjacency: [...]
  wraps_corners: true
  termination_type: ...
  material_family: ...
```

Validation must detect:
- correct start/end;
- correct path;
- correct width family;
- continuity;
- wrong host placement;
- flattening a wrapping trim into a decal/highlight-like strip.

Object existence is not sufficient.

---

## Material appearance contract

For each visible material region define:
- region boundary owner;
- base color family;
- metallic/dielectric behavior;
- roughness range/order relative to neighboring materials;
- directional response if present;
- micro-normal scale family;
- calibrated neutral-light appearance requirement.

Example:

```yaml
material_region:
  id: SIDE_ALUMINIUM_R
  family: BRUSHED_ALUMINIUM
  metallic: 1.0
  roughness: [0.25, 0.38]
  directionality: REQUIRED
  region_boundary: SIDE_TRIM_PATH_R
  importance: MUST
```

A material name assigned to a mesh does not satisfy this contract.

---

## Detail coverage

Every visible reference feature classified MUST is accounted for as one of:

```text
PASS
NOT_REQUIRED_BY_AUTHORITY
BLOCKING_DEVIATION
```

It may not silently disappear because the builder never created a node for it.

Report:

```yaml
detail_coverage:
  must_total: 28
  must_pass: 27
  must_not_required: 1
  must_missing: 0
  weighted_coverage: 1.0
```

For L5:
- `must_missing` must be zero;
- weighted MUST coverage must be 1.0 unless authority explicitly waives a feature.

---

## Matched-camera appearance review

At final reconstruction state use source-matched views appropriate to evidence:
- orthographic registered comparisons for technical views;
- solved/matched perspective for hero when it controls product appearance;
- neutral form render for geometry boundaries;
- calibrated material render for surface response.

Do not compare a random beauty camera to a reference hero and call the difference subjective.

---

## Relationship to Shape Graph

```text
Shape Graph
= form/dependency/representation model

Appearance Contract
= visible-boundary/style/material/detail proof model
```

Both refer to the same source set and revisions.

Required cross-links:

```yaml
appearance_owner:
  host_shape_nodes: [...]
  source_reference_ids: [...]
  graph_revision: sg_...
  appearance_revision: ac_...
```

If a Shape Node changes and invalidates an appearance owner, that owner becomes DIRTY.

---

## Acceptance rule

For target fidelity L4/L5:

```text
Shape Graph PASS
and
required node gates PASS
and
Appearance Contract required owners PASS
and
APPEARANCE_FIDELITY_GATE PASS
```

Only then can final `RECON_FIDELITY_GATE` unlock runtime.
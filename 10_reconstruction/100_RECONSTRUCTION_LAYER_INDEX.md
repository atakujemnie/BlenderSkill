# Reconstruction Layer Index and Reference Reconstruction Controller

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D na podstawie:
- concept sheet,
- blueprintów,
- rzutów ortograficznych,
- zdjęć,
- renderów,
- detail close-upów,
- wymiarów,
- opisów funkcjonalnych i materiałowych.

Nie jest to warstwa "inspiracji".
Celem jest maksymalnie wierna rekonstrukcja przy jawnej obsłudze niepewności.

Ten plik jest również **wysokopoziomowym controllerem rekonstrukcji z obrazu**. Nie powiela szczegółowych algorytmów z pozostałych modułów; ustala kolejność pracy i routuje agent do właściwych kompetencji.

---

## 1. Fundamental rule

**Reconstruct shape and proportion before detail.**

Model z perfekcyjnymi rowkami, śrubami i materiałami, ale błędną sylwetką lub proporcjami, jest nieudaną rekonstrukcją.

Nie używaj detalu do maskowania błędów bryły.

---

## 2. Task-facing reconstruction priority

Dla rekonstrukcji z reference images agent optymalizuje wynik w tej kolejności:

```text
CAMERA
-> SCALE
-> BOUNDING BOX
-> SILHOUETTE
-> PRIMARY MASSES
-> PROPORTIONS
-> SECONDARY MASSES
-> MAJOR CUTOUTS / STRUCTURAL TRANSITIONS
-> EDGE TREATMENT
-> PANEL LINES / GROOVES / VENTS / SEAMS
-> MICRODETAIL
-> MATERIALS / TEXTURING
-> RUNTIME
```

Ta kolejność jest warstwą kontrolną. Szczegółowy stan procesu znajduje się w `149_RECONSTRUCTION_STATE_MACHINE.md`.

---

## 3. Full reconstruction pipeline

`INGEST -> SEGMENT -> CLASSIFY -> AUTHORITY -> REGISTER -> CONSTRAIN -> DECOMPOSE -> PLAN -> BLOCKOUT -> MATCH -> DETAIL -> SHADE -> MULTIVIEW_QA -> RUNTIME`

### Mapping controller -> pipeline

- `CAMERA` -> CLASSIFY / REGISTER
- `SCALE + BOUNDING BOX` -> CONSTRAIN
- `SILHOUETTE + PRIMARY MASSES` -> BLOCKOUT / MATCH
- `PROPORTIONS` -> CONSTRAIN / MATCH
- `SECONDARY MASSES` -> DETAIL
- `SURFACE` -> SHADE
- `VALIDATION` -> MULTIVIEW_QA
- `GAME READY` -> RUNTIME

---

## 4. Packages of knowledge

### Evidence
100–109

Key modules:
- `102_EVIDENCE_MODEL.md`
- `103_REFERENCE_INGESTION_PROTOCOL.md`
- `104_CONCEPT_SHEET_SEGMENTATION.md`
- `105_VIEW_CLASSIFICATION.md`
- `106_VIEW_AUTHORITY_MATRIX.md`
- `107_MULTI_VIEW_CONFLICT_RESOLUTION.md`
- `108_UNCERTAINTY_AND_CONFIDENCE_LEDGER.md`

### Geometry constraints
110–123

Key modules:
- `110_DIMENSION_GRAPH.md`
- `111_DIMENSION_LOCKING_AND_TOLERANCES.md`
- `112_LANDMARK_AND_KEYPOINT_SYSTEM.md`
- `113_REFERENCE_COORDINATE_REGISTRATION.md`
- `114_ORTHOGRAPHIC_REFERENCE_CALIBRATION.md`
- `115_PERSPECTIVE_CAMERA_SOLVING.md`
- `116_SILHOUETTE_CONSTRAINT_SYSTEM.md`
- `117_NEGATIVE_SPACE_AND_CLEARANCE.md`
- `119_HIDDEN_AND_OCCLUDED_GEOMETRY_POLICY.md`

### Surface/material evidence
124–127

### Construction planning
128–140

### Validation
141–148

### Governance
149–159

### Specialized reconstruction
160–169

---

## 5. Reference input contract

The controller should receive as much of the following as available:

```yaml
reference_set:
  asset_id: bench_01
  target_scale_unit: METERS
  known_dimensions:
    - id: WIDTH
      value_m: 1.80
      confidence: LOCKED

  images:
    - id: front
      type: ORTHOGRAPHIC_OR_APPROX_FRONT
      path: /references/bench_front.png

    - id: side
      type: ORTHOGRAPHIC_OR_APPROX_SIDE
      path: /references/bench_side.png

    - id: perspective
      type: PERSPECTIVE
      path: /references/bench_perspective.png
```

If only one image exists, continue only with explicit uncertainty tracking. Do not manufacture unsupported depth or hidden detail.

---

## 6. Reference analysis before modeling

Before geometry creation the agent must identify:

```text
REFERENCE
|
+-- object bounding box
+-- principal axes / orientation
+-- projection class
+-- symmetry evidence
+-- outer silhouette
+-- internal silhouette breaks / negative spaces
+-- major landmarks
+-- dominant planes / curves
+-- repeated structures
+-- depth / perspective cues
+-- material boundaries
+-- hidden or uncertain geometry
```

The authoritative data model for these observations is the Evidence/Constraint/Feature system defined by the detailed reconstruction modules.

---

## 7. Camera-first mismatch rule

The agent must never deform geometry merely because a perspective reference does not line up.

When a screen-space mismatch is detected, diagnose in this order:

```text
1. projection class
2. reference calibration
3. focal length / ortho scale
4. camera rotation and shift
5. object/reference orientation
6. only then geometry
```

Detailed camera behavior belongs to:
- `01_analysis/15_CAMERA_REFERENCE_MATCHING.md`
- `114_ORTHOGRAPHIC_REFERENCE_CALIBRATION.md`
- `115_PERSPECTIVE_CAMERA_SOLVING.md`
- `141_RECONSTRUCTION_QA_CAMERA_RIG.md`

QA cameras are evidence instruments, not artistic cameras. Once calibrated they must not be moved to hide geometric error.

---

## 8. Bounding volume and normalized proportion model

Before detailed modeling, create a proportion model from known dimensions and calibrated views.

Use normalized ratios when exact metric data is incomplete:

```text
object width  = 1.000
object height = 0.540
object depth  = 0.430
seat height   = 0.287
seat depth    = 0.438
```

If one dimension is known, resolve derived dimensions from ratios only when the relevant view/calibration supports that inference.

Do not convert an uncertain pixel estimate into fake metric precision.

The canonical implementation is the Dimension Graph plus the confidence/evidence ledger.

---

## 9. Landmark system

Use semantic landmarks to constrain reconstruction, such as:
- extreme corners;
- seat/front/back junctions;
- major panel corners;
- centers of circular features;
- armrest peaks;
- attachment points;
- dominant transition edges.

Landmarks should use normalized image coordinates where practical and remain semantically stable across topology changes.

Do not use transient vertex indices as landmark identity.

Detailed representation and projection rules are defined in `112_LANDMARK_AND_KEYPOINT_SYSTEM.md` and the QA scripts.

---

## 10. Silhouette-first blockout

The first real geometry must solve:
- world-scale bounds;
- primary silhouette;
- negative spaces;
- primary landmarks;
- primary mass relationships.

Preferred blockout primitives:
- cube/box;
- plane/extruded profile;
- cylinder;
- sphere only when appropriate;
- Mirror;
- Array for actual repetition.

Forbidden as a substitute for unresolved primary form:
- panel lines;
- vents;
- screws;
- decorative booleans;
- micro-bevels;
- final UV/textures.

The blockout gate is controlled by `131_DIMENSION_LOCKED_BLOCKOUT.md` and `146_MULTI_VIEW_CONSISTENCY_GATE.md`.

---

## 11. Primitive/part decomposition

Before topology refinement, decompose the asset into semantic masses.

Example:

```text
BENCH
+-- seat shell
+-- back shell
+-- left structural housing
+-- right structural housing
+-- base / feet
+-- utility insert
+-- trim / lighting / branding
```

For each part record:
- semantic role;
- primitive/profile class;
- symmetry relationship;
- feature ownership;
- likely modeling strategy.

Use `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md` and `129_FEATURE_TO_MODELING_STRATEGY_MAP.md` for the canonical data model.

---

## 12. Symmetry controller rule

Classify the asset as:
- `FULL_SYMMETRY`
- `PARTIAL_SYMMETRY`
- `ASYMMETRIC`

Use Mirror for the symmetric core when evidence supports it.

Do not mirror asymmetric utility panels, branding, wear, ports, or reference-specific detail merely because the base shell is symmetric.

The canonical policy is `120_SYMMETRY_AND_ASYMMETRY_POLICY.md`.

---

## 13. Multi-view consistency

Multiple views constrain one 3D object.

Typical authority:

```text
FRONT -> width, height
SIDE  -> depth, height, profile
TOP   -> width, depth
REAR  -> rear features/material boundaries
BOTTOM -> underside/service geometry
HERO  -> material/edge language and spatial confirmation
```

Do not silently average contradictory drawings.

Conflicts must be recorded and resolved using the Evidence Model and View Authority Matrix.

---

## 14. Confidence-aware reconstruction

Use the canonical confidence vocabulary from `108_UNCERTAINTY_AND_CONFIDENCE_LEDGER.md`:

- `LOCKED`
- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

When helpful, evidence provenance may separately classify a value as observed/derived/inferred.

For low-confidence hidden geometry:

**Use the simplest continuous solution compatible with all visible evidence.**

Do not add speculative decorative detail to increase perceived sophistication.

---

## 15. Screen-space validation loop

At each accepted stage:

```text
matched QA camera
-> deterministic render/mask
-> compare against reference
-> measure error
-> identify highest-level cause
-> repair
-> revalidate
```

Minimum categories:
- bounding box;
- silhouette;
- landmarks;
- negative spaces;
- major internal feature boundaries.

Prefer measurements over statements such as "looks close".

Use:
- `142_ORTHOGRAPHIC_OVERLAY_VALIDATION.md`
- `143_SILHOUETTE_DIFF_PROTOCOL.md`
- `144_NUMERIC_AND_LANDMARK_VALIDATION.md`
- `145_FEATURE_ROI_VALIDATION.md`
- `146_MULTI_VIEW_CONSISTENCY_GATE.md`

---

## 16. Quality-gate defaults

Project contracts and explicit dimensions always override generic defaults.

For image-derived reconstruction, the following can be used as **starting heuristics**, not universal truth:

### Blockout gate
- bounding-box error < 3%
- major landmark error < 5%

### Primary geometry gate
- silhouette mean error < 2%
- major landmark mean error < 2%

### Final image-reconstruction gate
- silhouette mean error < 1%
- major landmark mean error < 1.5%

These thresholds must be tightened or relaxed according to:
- reference resolution;
- projection confidence;
- asset importance;
- explicit project tolerances;
- whether the input is a real technical drawing or stylized concept art.

Hard numeric dimensions use the tolerance rules in `111` and `148`, not these image-space heuristics.

---

## 17. Repair priority

When validation fails, repair the highest-level error first:

```text
1. camera/reference registration
2. metric scale / bounding box
3. silhouette
4. primary masses
5. primary landmarks / proportions
6. secondary geometry
7. edge treatment
8. detail
9. materials
```

Never repair a panel line while the primary silhouette is still failing.

---

## 18. Detail routing after primary pass

Only after primary geometry passes should the controller route work to specialized skills.

Examples:

```text
structural/cosmetic narrow seam
-> blender-agent-procedural-hard-surface-panel-lines.md

SubD topology / support-loop problem
-> blender-agent-subdivision-topology-control.md

reusable structural texture band
-> 03_modeling/40_TRIM_SHEETS.md

logo / unique marking
-> 03_modeling/41_DECALS_AND_FLOATING_DETAILS.md

high-to-low detail
-> 03_modeling/38_HIGH_LOW_POLY_WORKFLOW.md
-> 03_modeling/39_BAKING_PIPELINE.md
```

This controller orchestrates. Specialized skills execute.

---

## 19. Single-image mode

When only one image exists:

1. classify projection;
2. estimate/match camera;
3. extract visible silhouette and landmarks;
4. solve known dimensions or normalized proportions;
5. infer depth conservatively;
6. explicitly separate observed, derived and inferred information;
7. assign confidence;
8. keep hidden geometry minimal;
9. do not claim literal full 1:1 certainty in unobserved regions.

A single-view result may be an evidence-constrained 3D interpretation rather than a fully determined reconstruction.

---

## 20. Output contract

A controller pass should be able to emit:

```yaml
reconstruction_result:
  asset: bench_01
  stage: PRIMARY_GEOMETRY
  status: PASS

  dimensions:
    width_error_pct: 0.8
    height_error_pct: 1.1
    depth_error_pct: 1.4

  silhouette:
    mean_error_pct: 0.9
    max_error_pct: 2.8

  landmarks:
    mean_error_pct: 1.2
    max_error_pct: 2.1

  unresolved_geometry:
    - underside_rear_shell
```

The detailed final report schema is defined in `152_RECONSTRUCTION_REPORT_SCHEMA.md`.

---

## 21. Controller completion criteria

Before routing to final detail/material/runtime, verify:

```text
[ ] reference projection/classification is resolved sufficiently
[ ] camera/reference registration is validated
[ ] known scale/dimensions are respected
[ ] bounding volume is within tolerance
[ ] primary silhouette passes required views
[ ] major negative spaces pass
[ ] primary landmarks pass
[ ] multi-view conflicts are resolved or explicitly documented
[ ] low-confidence regions are identified
[ ] primary object decomposition is stable
[ ] no lower-level detail contradicts the accepted primary form
```

The full asset is complete only when `159_RECONSTRUCTION_DEFINITION_OF_DONE.md` also passes.

---

## 22. Final rule

Reconstruction 1:1 does not mean "one render looks similar".

It means:
- known dimensions are respected;
- canonical views are simultaneously consistent;
- silhouette and proportions are controlled;
- features do not disappear;
- uncertainty is explicit;
- hidden geometry is not hallucinated;
- detail is added only after the primary form is proven;
- every accepted stage can be validated and regressed.

The controller's permanent priority is:

`CAMERA -> SCALE -> BOUNDING BOX -> SILHOUETTE -> PRIMARY MASSES -> PROPORTIONS -> SECONDARY MASSES -> DETAIL -> MATERIALS -> RUNTIME`.
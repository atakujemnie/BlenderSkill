# 504 — Visual Fidelity and Feature Completion

## Scope

This contract defines BlenderSkill v0.22 behavior after the Lafar Public Service Terminal blind test showed that a dimensionally correct, fully `APPROVED` structural asset can still be a poor reconstruction of its reference.

The governing invariant is:

> **Correct envelope + successful executor + trusted structural receipts != visually faithful asset.**

v0.22 makes visible reference features explicit, measurable and independently reviewable before final approval.

## 1. Feature Contract is production data

For every reference-critical component, the planner records a `feature_contract`. Features use three priorities:

- `MUST` — missing/incorrect blocks the component or final fidelity review;
- `SHOULD` — deviation is reported but may proceed;
- `OPTIONAL` — documented but never allowed to hide a missing MUST feature.

A feature record may contain:

```yaml
feature_id: SERVICE_PANEL_VENTS
priority: MUST
owner_component_id: SERVICE_PANEL
required_operations: [CAPSULE_PRISM, ARRAY, BOOLEAN_CUT]
forbidden_operations: []
expected_count: 8
requires_reference_evidence: true
evidence_ids: [EV-DETAIL-B]
require_scene_proof: true
required_proof_types: [REPEAT, BOOLEAN_EFFECT]
expected_measurements:
  repeat_count: {value: 8}
  pitch_mm: {value: 36, tolerance_mm: 0.5}
  material_removed_mm3: {min: 1}
visual_required: true
qa_views: [FRONT, DETAIL_B]
```

The Feature Contract supplements — and does not replace — the component tree, dimensional graph, assembly relations and representation contract.

## 2. Reference features cannot disappear because the brief omitted their names

The reference remains authoritative for visible shape/features according to the existing authority and conflict-resolution rules.

If an independent reviewer sees a reference-critical detail that is not represented in the Feature Contract, it records that detail in `discovered_unmapped_features`. Final fidelity review fails until the contract and model are updated.

This prevents the terminal-test failure where obvious panel screws, sensor housing rings and top-cap profile transitions disappeared simply because the numerical brief did not enumerate them.

## 3. Recipe intent requires scene proof

`FEATURE_CONTRACT_GATE` verifies both authoring intent and measured result.

Recipe-level proof may include:

- required/forbidden operations;
- repeat count;
- explicit feature ownership.

Scene proof is emitted by deterministic executors and carried through `SCENE_COMPONENT_SNAPSHOT` as compact `feature_ids` / `feature_proofs`.

Typical proof types:

- `GEOMETRY_OUTPUT`
- `BOOLEAN_EFFECT`
- `REPEAT`
- `BEVEL`
- `INSTANCE`
- `MATERIAL_BINDING`

A MUST feature is not accepted solely because its operation name appears in a recipe.

## 4. Boolean material-removal proof

`BLENDER_HARD_SURFACE_BUILDER` measures evaluated signed volume before and after `BOOLEAN_CUT` / `BOOLEAN_UNION`.

The operation fails when its expected direction produces no material effect above epsilon.

For `BOOLEAN_CUT` the proof contains at least:

- `volume_before_mm3`
- `volume_after_mm3`
- `boolean_effect_mm3`
- `material_removed_mm3`

This is the direct regression for the v0.21 blind-test failure where a modifier existed and received trusted PASS receipts despite no cavity being produced.

## 5. Detail primitives are semantic tools, not decoration

v0.22 adds first-class deterministic primitives:

- `CYLINDER` — sensor lenses, bores/cutters, screws/fasteners;
- `RING` — sensor bezels, camera housing rings;
- `CAPSULE_PRISM` — rounded ventilation slots and elongated recessed features.

`PROFILE_PRISM`, explicit `BEVEL`, booleans, arrays and instances remain the preferred construction methods for non-box hard-surface language.

A generic box is not an acceptable substitute when the Feature Contract requires a more specific representation.

## 6. Edge profiles are part of design fidelity

A single global bevel is not a design system.

Components may carry `edge_profiles` and feature-level bevel requirements. Task packs preserve these records. Builders/reviewers must distinguish, for example:

- main body corner radius;
- front transition radius;
- display bezel outer/inner edge;
- service panel edge;
- top-cap outer edge;
- top-cap undercut/chamfer;
- LED channel termination.

When an edge profile is a MUST visual feature, it requires both deterministic geometry proof where measurable and visual QA in an appropriate view.

## 7. Structural acceptance is not final acceptance

Component acceptance has an `acceptance_level`:

`NONE < BLOCKOUT < STRUCTURAL < DETAILS < MATERIALS < GAME_READY < FIDELITY < FINAL`

`APPROVED` task status updates a component to the acceptance level corresponding to the task stage. A structural task cannot silently grant later-stage completion.

Stage transition requirements are evaluated when leaving each production stage:

- enter `DETAILS` only after structural acceptance;
- enter `MATERIALS` only after details acceptance;
- enter `GAME_READY` only after materials acceptance;
- enter `FIDELITY_AUDIT` only after game-ready acceptance;
- enter final `APPROVED` only after fidelity acceptance and a current independent visual review.

This intentionally makes the terminal-test statement “asset complete” invalid while the asset is only at `STRUCTURAL_GEOMETRY`.

## 8. Independent multi-view visual reviewer

Visual fidelity is not reduced to pixel equality or one scalar similarity score.

The builder and reviewer are separate roles. `VISUAL_FIDELITY_REVIEW_GATE` requires:

- exact asset revision;
- exact scene revision;
- exact reference revision;
- independent reviewer identity/role;
- QA render artifact(s);
- reference evidence IDs for every QA view;
- per-MUST-feature review results.

Recommended QA views are registered/calibrated to the reference using the existing camera/reference protocols:

- FRONT
- REAR
- LEFT/RIGHT or SIDE
- TOP where relevant
- PERSPECTIVE
- DETAIL crops for critical features

Review focuses on:

- silhouette;
- major/secondary edges;
- negative spaces and recesses;
- feature location/orientation;
- relative proportions;
- material region boundaries;
- profile/edge character;
- visible feature completeness.

A global score may be reported, but **cannot override a failed or missing MUST feature**.

## 9. Revision binding

Fidelity reviews are persisted separately in `FIDELITY_REVIEW_REPOSITORY`.

A PASS review is valid only for the exact:

`asset_revision + scene_revision + reference_revision`

Any mutation or reference change invalidates its use for final approval.

## 10. Task-pack constraints remain component scoped

Feature contracts, visual feature maps, QA view requirements and edge profiles are carried into the component-scoped task pack. The runtime still forbids routine full-library/full-history context.

Target budgets remain:

- REPAIR <= 4k estimated input tokens;
- BUILD <= 8k;
- asset planning <= 15k.

Visual evidence should be delivered as materialized ROI/view attachments, not repeated as verbose text descriptions.

## 11. Failure behavior

The runtime must fail or block rather than silently simplify when:

- a MUST feature is missing;
- required repeat count is wrong;
- a boolean has no measured material effect;
- a required proof type is absent;
- visual reviewer marks a MUST feature FAIL/NOT_VISIBLE;
- reviewer discovers an unmapped reference-critical feature;
- a stale fidelity review is reused;
- a later production stage is entered before the previous acceptance level is complete;
- final approval is requested without a current independent visual fidelity review.

## 12. Release regression

Canonical v0.22 regression:

`07_examples/92_LAFAR_SERVICE_TERMINAL_VISUAL_FIDELITY_V022_REGRESSION_BENCHMARK.md`

The benchmark intentionally encodes the human-visible failures from the blind terminal run: flat sensor dots, missing panel fasteners, generic top-cap profile, wrong LED interpretation, ineffective booleans, structural-success/final-success confusion and stale or incomplete visual review.

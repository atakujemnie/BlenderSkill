# Benchmark 92 — Lafar Public Service Terminal Visual Fidelity (v0.22)

## Purpose

Benchmark 92 is the release gate created from the blind end-to-end production test of `LAFAR-SERVICE-TERMINAL-BLIND-001`.

The v0.21 run proved that dimensional correctness, trusted receipts and successful executor calls are not enough to guarantee a visually faithful asset. The human result was approximately 3/10: the envelope and major parts were correct, but reference-critical detail was lost or simplified.

v0.22 must therefore prove **feature completion and visual fidelity**, not only outer geometry.

## Known-broken cases that MUST fail

1. Three sensor locations exist but each is only a flat cylinder/dot; visible housing ring/depth structure is absent.
2. Service panel has eight slots but the four visible corner fasteners from the reference are omitted.
3. A `BOOLEAN_CUT` operation exists in the recipe but evaluated geometry shows no material removal.
4. LED count and symmetry are mathematically correct but the independent visual reviewer reports wrong surface/orientation relative to the side/detail reference.
5. `TOP_CAP` has the correct bounding box but its stepped/undercut profile is replaced by a generic rounded box.
6. A high global visual similarity score attempts to hide one missing MUST feature.
7. The reviewer discovers a reference-critical feature that was never entered into the Feature Contract.
8. All structural component tasks are `APPROVED`, but the asset is still at `STRUCTURAL_GEOMETRY`; this may not be declared final.
9. A stale visual review is reused after the asset, scene, or reference revision changes.

## Required v0.22 behavior

### Feature Contract

Every reference-critical visible detail is represented as a feature record with:

- `feature_id`
- `priority` (`MUST`, `SHOULD`, `OPTIONAL`)
- owning component
- reference evidence
- required/forbidden representation operations when applicable
- measurable expectations such as count, pitch, diameter, recess depth, material removal or bevel width
- QA view(s)

Missing MUST features block acceptance.

### Measured execution proof

`BOOLEAN_CUT` is not accepted merely because the modifier exists. The Blender executor measures evaluated solid volume before and after the operation and emits `BOOLEAN_EFFECT` proof. A cut with no observed material removal fails execution.

Repeated detail such as eight vent slots emits `REPEAT` proof with count/pitch. Detail primitives such as `CYLINDER`, `RING` and `CAPSULE_PRISM` provide explicit representation for cameras, fasteners and rounded slots.

### Independent visual review

The final fidelity review is performed independently of the builder and is bound to exact:

- asset revision
- scene revision
- reference revision
- QA render artifacts
- reference evidence IDs

Every visual MUST feature is reviewed separately. A global score is secondary and cannot override a missing MUST feature.

If the reviewer notices an important reference feature absent from the Feature Contract, `discovered_unmapped_features` blocks final approval until the contract/model is corrected.

### Stage semantics

`STRUCTURAL_GEOMETRY` means structural acceptance only. The asset cannot advance through `DETAILS`, `MATERIALS`, `GAME_READY`, `FIDELITY_AUDIT`, and finally `APPROVED` unless each production component proves the required acceptance level.

`APPROVED` additionally requires a current PASS visual fidelity review.

## Canonical terminal regression features

The benchmark uses the blind-test failure classes, not the original production files:

- service-panel vent slots: 8, rounded slot representation, repeated deterministically
- service-panel fasteners: 4 visible fasteners
- sensor cluster: 3 sensors with separate housing/ring/lens semantics
- display: physical recess rather than a surface patch
- top cap: explicit profile/undercut feature
- side LED: feature must be visually reviewed in side/detail QA views

## Acceptance

Benchmark 92 passes only if known-broken recipes/reviews are rejected and the complete feature/review contracts are accepted. Real Blender runtime tests separately prove the new primitives and boolean material-removal evidence.

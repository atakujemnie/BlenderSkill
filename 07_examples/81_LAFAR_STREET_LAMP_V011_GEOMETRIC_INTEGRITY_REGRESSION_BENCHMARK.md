# Benchmark 81 — Lafar Street Lamp v0.11 Geometric Integrity Regression

## Purpose

Canonical regression driver for BlenderSkill v0.12.0.

Source asset: Astera Civic Systems / LAFAR 3470 Civic Lighting Module.

v0.11 delivered the strongest process discipline so far: runtime pinning, conflict arbitration, persistent node state, authorized one-node mutation, `BUILT_UNVERIFIED` branch stops, source-anchored node QA, 23/23 Shape Nodes accepted, 32/32 Appearance Owners accounted, and final appearance/reconstruction gates passed.

Human review still found a severe geometric defect after the green pipeline: the sensor housing and arm interpenetrated and the head lost visible detail.

## Critical finding

A fully green evidence chain can still be wrong if the validators test the wrong physical property.

The broken head had approximately coincident/interpenetrating skins. Initial containment-style checking returned PASS because the defect was not one object fully buried in another; it was surface interpenetration. The first guard therefore did not bite.

After repair:
- arm tip ended at approximately Y=482 mm;
- sensor housing began at approximately Y=485 mm;
- the intended shadow-gap junction was restored;
- unintended interpenetration findings dropped to zero.

The old junction validator then failed because it had encoded the wrong semantic rule: it expected overlap. It had to be rewritten to validate a shadow gap plus housing lip instead.

## Failure classes protected by v0.12

### V12-01 — assembly interpenetration blind spot
Separate parts can physically intersect while node/view/fidelity gates remain green.

### V12-02 — wrong junction semantics
A validator can reward the defect if it checks generic overlap instead of the declared assembly relation.

### V12-03 — silent Boolean no-op
Modifier application is not proof that the target mesh changed.

### V12-04 — transform/context hazard
Active object, selected objects and evaluated transforms can diverge from builder assumptions.

### V12-05 — inverted volume/orientation hazard
A loft can render plausibly but carry a wrong closed-volume orientation that breaks downstream operations.

### V12-06 — toothless validator
The first containment probe returned PASS on the known-broken fixture. A validator that cannot reject the defect is not acceptance evidence.

### V12-07 — topology classification gap
The repaired `SensorShell` still contained three n-gons with more than six vertices. N-gons are not automatically wrong, but planarity/concavity/shading risk must be classified.

### V12-08 — contaminated reference mask
Dimension lines/leaders on the concept sheet changed contour metrics materially. Product and annotation masks must be separated.

### V12-09 — stale evidence after repair
`ACCEPTED -> DIRTY` exists, but downstream Shape/Appearance/Evidence invalidation must be automatic and revision-aware.

### V12-10 — asset-local integrity validator invention
Interpenetration logic was invented only after the human found the defect. Assembly integrity belongs in the canonical executor layer.

## v0.12 regression fixtures

```text
BROKEN_SENSOR_ASSEMBLY
-> ASSEMBLY_INTEGRITY_GATE FAIL

FIXED_SENSOR_ASSEMBLY
-> ASSEMBLY_INTEGRITY_GATE PASS

BOOLEAN_TARGET_UNCHANGED
-> MUTATION_POSTCONDITION_GATE FAIL

TOOTHLESS_NEGATIVE_CONTROL
-> VALIDATOR_NEGATIVE_CONTROL FAIL

ARM_REPAIR
-> descendants DIRTY/BLOCKED
-> affected Appearance Owners UNVERIFIED
-> stale evidence SUPERSEDED
```

## Acceptance target

```text
zero unauthorized mutations
zero silent mutation no-ops
zero undefined MUST assembly relations
zero unintended interpenetrations on forbidden relations
zero stale green evidence after repair
100% MUST integrity validators proven by negative control
0 non-manifold closed solids
no unclassified non-planar high-order n-gons in MUST visible regions
```

Reference/appearance fidelity remains required; geometric integrity is non-compensating and cannot be averaged away by a good visual score.

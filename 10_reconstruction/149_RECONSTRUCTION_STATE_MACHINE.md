# Reconstruction State Machine

## v0.12 integrity amendment

Every production-node mutation now has two independent closure layers:

```text
execution permission
-> actual mutation postcondition
-> reference/assembly/topology proof
```

A node cannot reach `BUILT_UNVERIFIED` unless `MUTATION_POSTCONDITION_GATE` proves the intended geometry change actually occurred. A node cannot reach `ACCEPTED` unless required source evidence and Assembly Relations are valid. Final Level A also requires `GEOMETRIC_INTEGRITY_GATE`.

Repairing accepted geometry first routes through `DEPENDENCY_INVALIDATOR` so descendants, Appearance Owners and old evidence cannot remain falsely green.

## R0 — INGEST

Register sources/segments and stable source IDs.

## R1 — CLASSIFY EVIDENCE

Classify projection/view/material/detail/text/annotation evidence.

For technical sheets distinguish product pixels from dimension lines/leaders/text when they contaminate QA.

## R2 — AUTHORITY

Resolve property-level authority and conflicts. Do not use one global `card wins` rule for unrelated properties.

## R3 — REGISTER

Physical scale, axes, datums, image planes/cameras, global registrations. No local candidate warp for acceptance.

## R4 — CONSTRAIN

Dimension Graph, landmarks, Feature Contract, derived-parameter provenance.

## R5 — DECOMPOSE + SHAPE / APPEARANCE / ASSEMBLY CONTRACTS

Required:
- decompose G0–G5 forms;
- build Reconstruction Shape Graph;
- assign parents/dependencies/RDL/shape representation;
- assign authoritative views/properties;
- define node validation contracts;
- for L4/L5 build Reference Appearance Contract;
- define semantic Assembly Relations for important multi-part junctions.

Shape Graph must structurally PASS before production geometry.

## R6 — RDL0 ENVELOPE

Create actual neutral diagnostic geometry for envelope/contact datum/axes.

Proof:
- numeric bounds;
- registered FRONT/SIDE/TOP as authoritative;
- QA isolation;
- `RDL0_BARRIER: PASS`.

## R7 — RDL1 PRIMARY FORMS

For each eligible G1 node:

```text
EXECUTION_AUTHORIZATION_GATE
-> READY_TO_BUILD
-> before snapshot
-> mutate node only
-> after snapshot
-> MUTATION_POSTCONDITION_GATE
-> BUILT_UNVERIFIED
-> required source QA + topology/assembly proof
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL | UNVERIFIED
```

Includes primary shell/body, base/plinth, structural transitions and primary negative spaces.

All required G1 accepted -> `RDL1_STAGE_BARRIER`.

## R8 — RDL2 SECONDARY STRUCTURAL FORMS

Build frames, housings, service assemblies, major trims/inserts and design-defining junction participants one node at a time.

Instantiate/validate relevant Appearance Owners and Assembly Relations. Outer silhouette alone does not close this state.

All required G2 accepted -> `RDL2_STAGE_BARRIER`.

## R9 — RDL3 STRUCTURAL FEATURES

Panels, openings, recesses, vents, grooves, light channels, handles, layered assemblies.

Leaf skill only on ACCEPTED host.

Destructive Boolean/recess operation must prove mutation bite before source QA. Feature proof may include ROI, depth/position, layer stack, panel path and outside-region regression.

All required G3 accepted -> `RDL3_STAGE_BARRIER`.

## R10 — RDL4 EDGE LANGUAGE

Bevel/fillet/chamfer/corner radius/tangency/SubD support only after accepted form.

Validate:
- source edge family;
- protected dimensions;
- silhouette/boundaries;
- topology risk after destructive edge work.

`RDL4_STAGE_BARRIER` before surface finish.

## R11 — RDL5 SURFACE / DETAIL

Branding, decals, materials, texture direction, weathering, emissive finish and required micro/meso detail.

For material-only operations geometry signature should remain stable. L4/L5 requires material appearance/segmentation evidence and Appearance Owner closure.

## R12 — GEOMETRIC INTEGRITY + MULTIVIEW / APPEARANCE FIDELITY

First physical closure:

```text
current node revisions
-> all required mutation postconditions PASS
-> all MUST Assembly Relations PASS
-> required topology records PASS
-> required validator negative controls PASS
-> zero stale/superseded evidence in current bundle
-> GEOMETRIC_INTEGRITY_GATE
```

Then source/appearance closure:

```text
Shape Graph revision validation
-> all required node gates accepted
-> RDL barriers
-> QA_SCENE_ISOLATE
-> registered canonical views
-> hard dimensions / landmarks
-> MUST features
-> Appearance Contract closure for L4/L5
-> APPEARANCE_FIDELITY_GATE for L4/L5
-> authority/deviation closure
-> RECON_FIDELITY_GATE
```

A perfect overlay cannot compensate for invalid physical geometry.

## R13 — TOPOLOGY / RUNTIME PREP

Only after required reconstruction gates PASS:
- production topology cleanup/freeze;
- UV;
- runtime LOD;
- collision;
- bake;
- runtime material closure.

## R14 — EXPORT VALIDATION

Validate package/readback, primitive attributes, node transform policy, export round-trip dimensions/contact and target-engine evidence for Level D.

## Repair/backtracking

Every FAIL routes to earliest owner.

If accepted geometry changes:

```text
change intent
-> DEPENDENCY_INVALIDATOR
-> affected node revisions/states updated
-> Appearance Owners UNVERIFIED
-> old evidence SUPERSEDED
-> rebuild affected closure
```

Examples:

```text
Boolean modifier applied but recess absent
-> current node mutation / MUTATION_POSTCONDITION_GATE

sensor housing pierces arm despite good side overlay
-> J_SENSOR_ARM / ASSEMBLY_INTEGRITY_GATE

validator passes known-broken overlap fixture
-> VALIDATOR_NEGATIVE_CONTROL / validator implementation

SIDE primary contour second FAIL
-> SHAPE_CLASSIFY representation review

technical-sheet leader pollutes contour
-> reference mask annotation exclusion, not candidate warp

missing TEXCOORD_0 after export
-> runtime package/UV owner
```

## Monolithic-build prohibition

Forbidden:

```text
analyze -> build G1..G5 -> one QA -> accept
```

Canonical:

```text
understand hierarchy/relations
-> authorize one form
-> prove mutation
-> prove source + physical integrity
-> accept current revision
-> continue coarse-to-fine
```

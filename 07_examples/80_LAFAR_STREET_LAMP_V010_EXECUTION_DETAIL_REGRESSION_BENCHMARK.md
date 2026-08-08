# Benchmark 80 — Lafar Street Lamp v0.10 Execution and Detail Regression

## Purpose

Canonical regression driver for BlenderSkill v0.11.0.

Source asset: Astera Civic Systems / LAFAR 3470 Civic Lighting Module.

The v0.10 run is the strongest reconstruction result so far, but it exposed the next architectural gap.

## Result

Human assessment: approximately **7.5/10** overall reference fidelity.

Strengths:
- correct product identity;
- strong global proportions and envelope;
- much better Shape Graph decomposition than earlier assets;
- base/pole/head treated as designed assemblies rather than generic boxes;
- improved trim, junction and edge-family awareness;
- technically coherent QA, materials and emissive implementation.

Remaining visible failures:
- head module too simplified;
- missing/weak upper shell cuts and break lines;
- sensor housing interpretation too generic;
- local detail density below concept art;
- some material response still reads as procedural Blender lookdev rather than exact product finish;
- concept-sheet conflict at the head/top profile was resolved too literally from the SIDE view instead of reconciling SIDE with DETAIL_HEAD/HERO design intent.

## Critical process regression

The Shape Graph validator reported no authorized ready node, yet the asset builder invoked the full asset in one `main()`:

```text
RDL0
-> all RDL1 nodes
-> all RDL2 nodes
-> all RDL3 nodes
-> RDL4
-> RDL5
```

The functions were named node-by-node, but acceptance did not occur between mutations.

This proves:

```text
node-by-node code organization
!=
node-by-node reconstruction execution
```

## Failure classes protected by v0.11

### V11-01 — advisory state machine
`ready_nodes=[]` did not prevent mutation.

### V11-02 — BUILT_UNVERIFIED was only a label
Children were built immediately after an unverified host.

### V11-03 — no persistent node revision state
One scene reset + one full builder run encouraged monolithic reconstruction.

### V11-04 — RDL0 was not falsifiable geometry
Envelope existed as a report dictionary instead of a grey diagnostic blockout.

### V11-05 — production lookdev too early
Full materials were initialized before geometric stages closed.

### V11-06 — mixed report namespaces
Shape Nodes and Appearance Owners could be written into the same generic report namespace.

### V11-07 — Appearance Contract inventory not executable enough
Declared MUST owners could still be absent from actual geometry while RDL5 code ran.

### V11-08 — per-view evidence mismatch
Ortho, hero perspective and local detail crops require different proof modes.

### V11-09 — derived numbers became hard too early
Values such as inferred radii/angles were stored as single constants without always carrying range, confidence and source-fit residual.

### V11-10 — reference conflict arbitration insufficient
The head/top profile conflict showed that printed dimensions and one orthographic view do not globally determine local design form.

### V11-11 — duplicate BlenderSkill roots
A canonical checkout and project-local executor copy can silently diverge unless version/commit/source root is pinned.

### V11-12 — analysis helper proliferation
Many one-off card-scan helpers indicate missing reusable analysis primitives.

## v0.11 acceptance criteria

A future lamp regression must show:

```text
eligible node
-> canonical authorization
-> READY_TO_BUILD persisted
-> one node mutation
-> BUILT_UNVERIFIED persisted
-> source-anchored QA
-> ACCEPTED
-> only then next dependent node
```

Additionally:
- RDL0 diagnostic render exists before RDL1;
- head profile conflict has a decision artifact;
- all MUST Appearance Owners are accounted;
- Shape/Appearance/Evidence namespaces are separate;
- runtime source pin PASS;
- no LOD/UV/export before appearance/reconstruction gates.

## Regression target

For comparable industrial civic hard-surface concept sheets:

```text
human reference-fidelity target >= 8.5/10
zero MUST owner blockers
zero unauthorized geometry mutations
zero child builds on BUILT_UNVERIFIED/FAIL/UNVERIFIED hosts
```

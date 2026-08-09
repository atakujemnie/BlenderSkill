# Task Pack Protocol

## Purpose

A `Task Pack` is the smallest knowledge set for the current state and failing owner. In reference reconstruction it is scoped to the current Shape Node, Appearance Owner or Assembly Relation.

```text
state + RDL + current owner + measured failure
-> Task Pack
-> execute one bounded transaction
-> canonical validate
-> persist revisions/evidence
-> advance through barrier/gate
```

## SESSION_PREFLIGHT

Load Agent Charter, State Machine, Semantic Skill Registry, Blender/runtime compatibility, Scene Inspection and matching Project Profile.

Run `CANONICAL_SKILL_RUNTIME_PIN`. Persist Blender version, project profile, runtime path context, canonical skill source/version/commit.

## RECON_TECHNICAL_SHEET_ANALYZE

Load Evidence Model, ingestion/classification, View Authority Matrix, measurement/calibration, conflict arbitration, Reference Analysis Cache and mask-contamination policy.

Preferred:
- `REFERENCE_MEASURE`;
- `REFERENCE_CONFLICT_RESOLVER`;
- `REFERENCE_OVERLAY_VALIDATE` only after registration.

Output:
- Reference Registry/source revision;
- Evidence Ledger;
- hard dimensions and derived provenance;
- property-level authority/conflicts;
- canonical registrations;
- annotation/product mask policy.

No production geometry/UV/LOD/export.

## RECON_SHAPE_GRAPH_PLAN

Mandatory before production geometry.

Load `128`, `129`, `174`–`177`, prompt 68 and validator pattern 95.

Preferred: `SHAPE_GRAPH`, `SHAPE_CLASSIFY`.

Persist G0–G5 hierarchy, RDL, Node Contracts, parents/dependencies, representation and per-view responsibilities.

Gate: `shape_graph_validation.status == PASS`.

## RECON_APPEARANCE_AND_ASSEMBLY_PLAN

Mandatory for explicit 1:1/L4/L5 and industrial/product assemblies where internal architecture defines identity.

Load:
- `180_REFERENCE_APPEARANCE_CONTRACT.md`;
- `181_ANTI_CIRCULAR_VISUAL_VALIDATION.md`;
- `182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md`;
- `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`;
- `189_ASSEMBLY_RELATION_AND_INTERPENETRATION_CONTRACT.md`.

Output:
- Appearance Contract revision;
- boundary/trim/junction/edge/material/emissive/branding/detail owners;
- source IDs/ROIs;
- Assembly Relation revision;
- relation type + gap/contact/embedding/interpenetration constraints for important part pairs.

Do not infer `connected = overlap`.

## RECON_RDL0

Build physical neutral diagnostic envelope/contact datum/axes.

Validate numeric bounds and authoritative FRONT/SIDE/TOP.

Gate: `RDL0_BARRIER: PASS`.

## RECON_NODE_BUILD

Input: exactly one eligible Shape Node plus current revisions.

Required modules:
- Node Contract;
- Shape Classification;
- Node Execution Protocol;
- Execution Authorization;
- Mutation Postcondition;
- QA isolation;
- canonical reference validators;
- Assembly Relation contract for touched junctions;
- topology/section/layer validator only when relevant.

Canonical loop:

```text
eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> capture before metrics
-> mutate current node only
-> capture after metrics
-> MUTATION_POSTCONDITION_GATE
-> PASS: persist BUILT_UNVERIFIED
-> isolate
-> source-registered view/numeric/section proof
-> ASSEMBLY_INTEGRITY_GATE for touched relations
-> MESH_VALIDATE / layer proof as required
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
```

A builder-local gate may produce measurements, never canonical acceptance.

Representation routes include:

```text
REVOLVED_PROFILE -> AXISYMMETRIC_PROFILE
MULTI_SECTION_LOFT/TRANSITION -> SECTION_LOFT_HARD_SURFACE
PANEL_LINE -> HS_PANEL_LINE
SUBD_FREEFORM -> SUBD_TOPOLOGY_CONTROL
LAYERED_ASSEMBLY -> LAYER_STACK_VALIDATE
```

Forbidden:
- sibling/future-RDL bulk creation;
- production lookdev while primary form is unresolved;
- silent Boolean no-op accepted as build success;
- child build on non-ACCEPTED host;
- self-certification from builder constants.

## RECON_MUTATION_FAILURE

Route here when builder completed but geometry postcondition failed.

Load `76_MUTATION_POSTCONDITION_GATE.md`, relevant modeling skill and operation-specific Blender API rules.

Diagnose:
- topology/signature delta;
- volume/signed-volume direction;
- transform/depsgraph state;
- modifier/cutter lifecycle;
- predeclared feature probe.

Do not proceed to source QA until postcondition PASS.

## RECON_ASSEMBLY_INTEGRITY

Input: one or more touched Assembly Relations with measured metrics.

Preferred: `ASSEMBLY_INTEGRITY_GATE`.

Validate relation semantics, not generic overlap:
- SHADOW_GAP/CLEARANCE -> penetration forbidden, gap bounded;
- RECESSED_INSERT/EMBEDDED -> embedding required and bounded;
- FLUSH/BUTT -> contact/gap/penetration tolerance;
- OVERLAP_ALLOWED/WELDED -> explicit bounded policy.

Failed MUST relation blocks node acceptance.

## VALIDATOR_BITE_TEST

Use before a new validator can own MUST acceptance.

```text
known-good fixture -> validator -> PASS
known-broken fixture representing claimed defect -> validator -> FAIL
-> VALIDATOR_NEGATIVE_CONTROL
```

If known-broken returns PASS, fix validator before trusting current asset PASS.

## RECON_APPEARANCE_OWNER_VALIDATE

Input: one Appearance Owner plus current host revision.

Preferred: `APPEARANCE_REFERENCE_VALIDATE`.

Use source-anchored evidence for part boundaries, trim paths, junction appearance, edge families, materials/emissive/branding/detail coverage. Host revisions must be current.

## RECON_RDL_STAGE_GATE

Use `SHAPE_GRAPH.evaluate_stage_barrier()` after required nodes at each RDL.

```text
RDL0 -> RDL1 -> RDL2 -> RDL3 -> RDL4 -> RDL5
```

No bypass because downstream work is easy.

## RECON_RDL2_PRODUCT_ARCHITECTURE

After G1 acceptance, build major secondary housings, frames, trims, service assemblies and junction participants. Close associated Appearance/Assembly owners as they become testable.

## RECON_RDL3_DETAIL

Only on ACCEPTED structural hosts. Load the minimum leaf skills for recesses, panel lines, radial repeats, layered assemblies, fasteners, curves/sweeps.

Destructive recess/Boolean work always routes through mutation postconditions.

## RECON_RDL4_EDGE

Load `164_EDGE_LANGUAGE_SYSTEM.md`, `183_EDGE_MATERIAL_DETAIL_FIDELITY.md` and implementation-specific bevel/SubD modules.

Validate edge family profile/placement/start/end/continuity and protected dimensions. Run `MESH_VALIDATE` after destructive topology change.

## SURFACE_FINISH / RDL5

Load material/branding/decal/emissive only after structural barriers.

Material-only mutations should preserve geometry signature. For L4/L5 prove material appearance, not only segmentation/name. Use `APPEARANCE_OWNER_COVERAGE`.

## REPAIR_ACCEPTED_GEOMETRY

Before changing an accepted host:

```text
change intent
-> DEPENDENCY_INVALIDATOR
-> persist DIRTY/BLOCKED descendants
-> Appearance Owners UNVERIFIED
-> evidence SUPERSEDED
-> rebuild affected closure node-by-node
```

Unrelated accepted branches remain reusable.

## RECON_GEOMETRIC_INTEGRITY

Before final fidelity aggregate current physical proof:
- all required mutation postconditions;
- Assembly Relation closure;
- topology records;
- required validator negative controls;
- zero stale evidence references;
- zero unresolved MUST relations.

Gate: `GEOMETRIC_INTEGRITY_GATE == PASS`.

## RECON_APPEARANCE_FIDELITY

Mandatory for target >= L4 after relevant Appearance Owners close.

Gate: `APPEARANCE_FIDELITY_GATE == PASS`.

MUST categories are non-compensating.

## RECON_FINAL_FIDELITY

Requires:
- accepted/current Shape Graph revision;
- Appearance/Assembly revisions when required;
- all required node records/RDL barriers;
- QA isolation and canonical registered views;
- hard dimensions/landmarks/MUST features;
- `GEOMETRIC_INTEGRITY_GATE: PASS`;
- `APPEARANCE_FIDELITY_GATE: PASS` when required;
- authority/deviation closure;
- `RECON_FIDELITY_GATE: PASS`.

Only PASS opens runtime.

## GAME_READY_FINISH

Precondition:

```text
GEOMETRIC_INTEGRITY_GATE == PASS
and RECON_FIDELITY_GATE == PASS
and, for L4/L5, APPEARANCE_FIDELITY_GATE == PASS
```

Then runtime path -> LOD/collision -> UV -> dirty DAG -> bake/validate/cache -> runtime material -> package/readback -> round-trip -> engine proof as required -> completion.

Runtime LOD is downstream from RDL.

## PIPELINE_INTEGRATION

Level D only. Blender round-trip remains Level C. Level D requires target-engine production loader/regression/instantiation evidence.

## Persistent state

Persist compact:
- Tool/Project/Runtime Pin;
- Reference Registry/Evidence/Authority/Conflicts;
- Shape Graph revision;
- Appearance Contract revision;
- Assembly Relation revision;
- Node/Appearance/Assembly evidence;
- mutation postconditions;
- validator-control records;
- RDL barriers;
- geometric/appearance/reconstruction fidelity reports;
- runtime/completion state.

Do not rely on conversation history as execution state.

## Retry

First proven failure: diagnose + one corrected retry. Second proven same-strategy failure: re-inspect and switch representation/strategy/validator as appropriate.

## Final rule

```text
understand form
-> understand visible architecture and physical relations
-> build one node
-> prove mutation happened
-> prove reference fit and assembly integrity
-> accept node
-> deepen detail
-> prove final physical + visual fidelity
-> runtime
```

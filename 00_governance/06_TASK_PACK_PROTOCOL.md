# Task Pack Protocol

## Purpose

A `Task Pack` is the smallest knowledge set for the current state. In v0.9 reconstruction it is also scoped to one `Shape Node` whenever geometry is being built.

```text
state + RDL + Shape Node + measured failure
-> Task Pack
-> execute
-> validate
-> persist compact state
-> advance through barrier
```

## SESSION_PREFLIGHT

Load Agent Charter, Semantic Skill Registry, tool/runtime compatibility, Scene Inspection and matching Project Profile.

Persist Tool Registry, Blender version, project profile and runtime path context.

## RECON_TECHNICAL_SHEET_ANALYZE

Load Evidence Model, reference ingestion/classification, View Authority Matrix, measurement/calibration and Reference Analysis Cache.

Preferred skill: `REFERENCE_MEASURE`.

Output: Reference Registry, Evidence Ledger, locked dimensions, authority/conflicts.

Production geometry, UV, LOD and export are forbidden here.

## RECON_SHAPE_GRAPH_PLAN

Mandatory before production geometry.

Load:
- `128_RECONSTRUCTION_OBJECT_DECOMPOSITION.md`;
- `129_FEATURE_TO_MODELING_STRATEGY_MAP.md`;
- `174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- prompt 68;
- validator pattern 95.

Preferred skills: `SHAPE_GRAPH`, `SHAPE_CLASSIFY`.

Persist G0-G5 hierarchy, RDL assignments, Node Contracts, parent/dependencies, representation decisions and view responsibilities.

Gate: `shape_graph_validation.status == PASS`.

Do not write a monolithic production builder in this pack.

## RECON_RDL0

Build only total envelope, contact datum, axes and centerline.

Validate numeric bounds and authoritative FRONT/SIDE/TOP. No detail skills.

Gate: `RDL0_BARRIER: PASS`.

## RECON_NODE_BUILD

Canonical v0.9 construction pack. Input is exactly one Shape Node plus graph revision.

Required:
- Node Contract;
- Shape Classification;
- Node-by-Node Multi-View Validation;
- Node Execution Protocol;
- only the representation skill needed by the current node;
- QA scene isolation and registered validators.

Loop:

```text
resolve ready node
-> build/repair node only
-> BUILT_UNVERIFIED
-> isolate
-> validate required views
-> numeric/section/regression checks
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL
```

Representation routes:

```text
REVOLVED_PROFILE -> AXISYMMETRIC_PROFILE
MULTI_SECTION_LOFT / TRANSITION -> SECTION_LOFT_HARD_SURFACE
PANEL_LINE -> HS_PANEL_LINE
SUBD_FREEFORM -> SUBD_TOPOLOGY_CONTROL
LAYERED_ASSEMBLY -> LAYER_STACK_VALIDATE
```

Forbidden:
- unrelated sibling/future-RDL geometry;
- logo/materials while solving primary form;
- a `build_all()` that bypasses node gates.

## RECON_RDL_STAGE_GATE

Load Reconstruction Detail Levels, Stage Barrier and node acceptance records.

Preferred: `SHAPE_GRAPH.evaluate_stage_barrier()`.

```text
RDL0 PASS -> RDL1
RDL1 PASS -> RDL2
RDL2 PASS -> RDL3
RDL3 PASS -> RDL4
RDL4 PASS -> RDL5
```

No bypass for later detail.

## RECON_RDL3_DETAIL

Use only on ACCEPTED structural hosts. Load only applicable leaf skills: panel lines, recesses, radial repeats, layered display, curves/sweeps, fasteners.

Host failure routes backward.

## RECON_RDL4_EDGE

Load Edge Language, bevel/radius, Surface Continuity and SubD only after structural form acceptance. Revalidate protected dimensions/silhouette after changes.

## SURFACE_FINISH / RDL5

Load material/branding/decal/emissive modules only after structural barriers. Material cannot compensate geometry error.

## RECON_FINAL_FIDELITY

Requires accepted Shape Graph revision, required node records, RDL barriers, QA isolation, registered canonical views, hard dimensions/landmarks, MUST features, authority closure and `RECON_FIDELITY_GATE`.

Only PASS opens runtime.

## GAME_READY_FINISH

Precondition: `RECON_FIDELITY_GATE == PASS`.

Preferred skills:
- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `ASSET_COMPLETION`.

Order:

```text
runtime path
-> LOD/collision
-> UV contract
-> DAG dirty plan
-> bake/validate/cache
-> runtime material
-> package/readback
-> round-trip
-> runtime QA
-> completion
```

Runtime LOD is downstream from RDL and is not a reconstruction state.

## PIPELINE_INTEGRATION

Only for Level D. Load Project Profile, runtime path/package, catalog integration, Engine Smoke Test and Test Oracle.

Blender round-trip is Level C evidence. Target engine loader/instantiation is Level D evidence.

## Persistent state

Persist compact records:
- Tool Registry / Project Profile;
- Reference Registry / Evidence Ledger / Authority;
- Dimension Graph / Feature Contract;
- Shape Graph + revision;
- Node Contracts / Node Acceptance Records;
- RDL Stage Barrier Records;
- material/UV/bake/package state;
- Completion Report.

Do not rely on conversation history as execution state.

## Pack expansion

Load a module only when current state/RDL requires it, current Shape Node maps to it, or measured failure routes to it.

## Retry

After first proven failure: diagnose and one corrected retry. After second: re-inspect and strategy/representation switch.

## Final rule

```text
understand -> Shape Graph -> coarse form -> prove node -> deepen detail
```

not:

```text
one big script -> build everything -> inspect at the end
```

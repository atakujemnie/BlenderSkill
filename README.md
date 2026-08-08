# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.11.0 — enforced reconstruction execution, conflict arbitration and detail closure.**

v0.11 is driven by the Lafar Street Lamp v0.10 benchmark. v0.10 produced the strongest reconstruction so far, but the run exposed that the state machine was still advisory: `ready_nodes=[]` did not prevent a monolithic RDL0→RDL5 builder, `BUILT_UNVERIFIED` did not stop dependent geometry, and a local SIDE/detail conflict could be resolved too literally.

The v0.11 invariant is executable:

```text
eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> build exactly one node
-> persist BUILT_UNVERIFIED
-> source-anchored per-view QA
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> only ACCEPTED unlocks dependants
```

Additional v0.11 closure:
- persistent node/checkpoint state;
- per-property `REFERENCE_CONFLICT_RESOLVER`;
- per-view evidence contracts for ortho / hero / detail;
- source provenance for significant derived parameters;
- `APPEARANCE_OWNER_COVERAGE` with separate Shape/Appearance/Evidence namespaces;
- RDL0 diagnostic geometry and neutral RDL0–RDL3 shading;
- canonical BlenderSkill version/commit/source-root pinning;
- benchmark 80 for the Lafar Street Lamp.

Runtime remains downstream of `APPEARANCE_FIDELITY_GATE` and `RECON_FIDELITY_GATE`.

## Core v0.11 concepts

### 1. Reconstruction Shape Graph

Every reference-driven asset is decomposed into stable design forms:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

A Shape Node stores:
- semantic role;
- parent/dependencies;
- importance;
- mathematical shape class;
- authoritative views and properties controlled by each view;
- numeric/relationship constraints;
- validation contract;
- implementation skill.

`Shape Graph != Blender Object hierarchy`.

### 2. Reference Appearance Contract

For 1:1 reconstruction or target fidelity L4/L5, Shape Graph is necessary but insufficient.

The Appearance Contract inventories what must be visibly true for the model to read as the same designed product.

Canonical appearance-owner classes:

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

Each owner links to:
- host Shape Nodes;
- source reference IDs;
- source ROIs;
- required views;
- importance;
- validation method.

This prevents a coarse node such as `SIDE_MODULE` from hiding wrong trim, panel boundaries or shoulder transitions inside a correct outer silhouette.

### 3. Appearance hierarchy A0–A5

```text
A0 composition / massing
A1 internal product architecture
A2 edge language
A3 material identity
A4 meso detail
A5 micro detail / wear
```

A high A0 score does not compensate for failed A1/A2 when those owners are MUST.

### 4. Reconstruction Detail Levels

RDL remains separate from runtime LOD:

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms / major product architecture
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

Runtime `LOD0..LOD3` is generated only after reconstruction acceptance.

### 5. Canonical node-by-node execution

```text
one READY node
-> build/repair only that node
-> BUILT_UNVERIFIED
-> QA isolation
-> registered required views
-> numeric/section/regression checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL | UNVERIFIED
```

Required children remain blocked until their host/parent is accepted.

### 6. Anti-circular validation

v0.10 closes a concrete loophole exposed by the Street Bench run.

This is not reference proof:

```text
builder infers R165
-> builder constructs R165
-> builder-local Gate checks R165
-> PASS
```

It proves only internal consistency.

Strict reference-derived acceptance now requires:
- canonical `validator_id`;
- `provenance_id`;
- `source_reference_id` / `source_reference_ids`;
- `registration_id` for projected evidence.

A local helper may produce a measurement artifact. It cannot replace the canonical acceptance validator.

### 7. Representation before Blender operator

The agent still classifies geometry before implementation:

```text
PARAMETRIC_PRIMITIVE
EXTRUDED_PROFILE
REVOLVED_PROFILE
PROFILE_SWEEP
MULTI_SECTION_LOFT
MULTI_SECTION_TRANSITION
SUBD_FREEFORM
BOOLEAN_RECESS
PANEL_LINE
LAYERED_ASSEMBLY
HYBRID_ASSEMBLY
```

Compound hard-surface forms must not default to `cube + bevel` when width, depth and corner behavior vary across stations.

### 8. Part Boundary / Trim / Junction Graph

Outer silhouette answers where the object ends.

The new graph captures where its manufactured regions begin and end:
- metal/composite boundaries;
- panel perimeters;
- shadow gaps;
- trim centerlines and widths;
- trim terminations;
- multi-part junctions;
- rear service bands;
- plinth splits.

For major trim, validation covers:
- path;
- visible width;
- start/end;
- corner wrapping;
- host adjacency;
- continuity;
- material identity.

Object existence is not sufficient.

### 9. RDL4 edge-language proof

v0.10 treats edge language as reference geometry, not generic cleanup.

For every MUST edge family validate:
- profile type;
- radius/chamfer/step family;
- start/end landmarks;
- continuity;
- relation to part/material boundaries;
- protected-dimension survival.

`dimensions survived bevel` alone no longer passes RDL4.

### 10. Material segmentation != material appearance

For target L4/L5 the system distinguishes:

```text
which region uses which material
```

from:

```text
does that region respond like the reference material?
```

Appearance evidence can include:
- metallic/dielectric identity;
- roughness hierarchy;
- brushed directionality / anisotropy;
- micro-normal scale;
- glass response;
- emissive recession/intensity;
- controlled wear hierarchy.

A correctly named Principled material slot is not material appearance proof.

### 11. Detail coverage

Visible structural meso detail is not treated as optional microdetail.

Examples:
- service-panel perimeter;
- rear service bands;
- plinth split;
- utility recess;
- major fastener groups;
- trim terminations;
- underside service-cover layout.

For L5, all MUST reference features must be accounted for as:

```text
PASS
NOT_REQUIRED_BY_AUTHORITY
BLOCKING_DEVIATION
```

Silent omission is forbidden.

### 12. Appearance Fidelity Gate

For target L4/L5:

```text
part boundaries
+ trim paths
+ junctions
+ edge families
+ material response
+ final matched views
+ emissive/branding when present
+ detail coverage for L5
-> APPEARANCE_FIDELITY_GATE
```

MUST categories are non-compensating.

A failed trim path cannot be averaged away by perfect dimensions.

### 13. Final runtime lock

For L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> LOD / UV / bake / export / runtime FORBIDDEN
```

Correct dimensions, triangle budgets, UV attributes, glTF readback or engine import do not override this lock.

## v0.9 foundation retained

v0.10 keeps the Shape Graph/coarse-to-fine architecture introduced in v0.9:
- mandatory form hierarchy;
- RDL0–RDL5;
- representation-first modeling;
- one-node transactions;
- stage barriers;
- multi-section hard-surface loft support.

The distinction is now:

```text
v0.8 -> proof-bearing reconstruction fidelity
v0.9 -> understand and build the right forms in the right order
v0.10 -> prove the same visible product architecture, style and finish without self-certification
```

## New v0.10 semantic skills

- `APPEARANCE_REFERENCE_VALIDATE`;
- `APPEARANCE_FIDELITY_GATE`.

Strengthened:
- `RECONSTRUCTION_NODE_GATE`;
- `RECON_FIDELITY_GATE`;
- `QA_REFERENCE`;
- edge/material reconstruction routing.

New executor:

```text
executors/appearance_fidelity_gate.py
```

`MESH_VALIDATE` remains the currently proven `EXECUTOR_READY` library executor. New appearance executors remain `CONTRACT_READY` until a real Blender 5.1 end-to-end v0.10 benchmark proves runtime execution maturity.

## Existing runtime pipeline retained

The runtime infrastructure remains active:
- image datablock cache coherence;
- Pipeline DAG / dirty-stage reuse;
- canonical runtime path context;
- post-export round-trip invariants;
- trustworthy test oracle;
- Level C vs Level D evidence separation.

For the verified RPG project profile:

```text
engine asset directory = <repo>/Assets
game asset root       = <repo>/Assets/GameAssets
forbidden lookalike   = <repo>/GameAssets
```

## Completion model

```text
RECONSTRUCTION_COMPLETE
-> MODELING_COMPLETE
-> GAME_READY_COMPLETE
-> PIPELINE_INTEGRATED
```

### Level A for L4/L5 now requires
- valid Shape Graph revision;
- valid Appearance Contract revision;
- required Shape Nodes accepted by canonical gates;
- required RDL barriers passed;
- internal part/trim/junction owners closed;
- edge/material appearance proof;
- `APPEARANCE_FIDELITY_GATE: PASS`;
- `RECON_FIDELITY_GATE: PASS`.

### Level C
Requires runtime LOD/collision/material/bake/package/export closure and round-trip invariants after Level A is proven.

### Level D
Requires actual target-engine proof such as production loader, engine regression test or instantiation. Blender glTF re-import remains Level C evidence only.

## Repository structure

- `00_governance` — state/routing/skills/task packs/completion
- `01_analysis` — briefs/references/features/measurements
- `02_blender_api` — Blender 5.1 API/runtime compatibility/cache
- `03_modeling` — hard-surface/topology/UV/procedural modeling
- `04_game_ready` — runtime LOD/collision/bake/export contracts
- `05_execution` — node/appearance/fidelity gates, QA, DAG, completion proof
- `06_prompts` — system/planner/reviewer/repair prompts
- `07_examples` — real benchmark/post-mortem runs
- `08_scripts` — reusable validation patterns
- `09_engine` — project/runtime profiles and integration proof
- `10_reconstruction` — evidence-driven 1:1 reconstruction, Shape Graph and Appearance Contract
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executors/candidates
- `99_sources` — technical sources

## Canonical source

Modular Markdown files listed in `MANIFEST.json` are canonical.

`_FULL_LIBRARY.md` is generated from the manifest and should not be edited manually.

## v0.10 benchmark

Canonical release regression benchmark:

`07_examples/79_LAFAR_STREET_BENCH_V09_APPEARANCE_FAILURE_REGRESSION_BENCHMARK.md`

It protects against:
- dimensions/global silhouette being mistaken for full fidelity;
- builder-local circular acceptance gates;
- coarse Shape Nodes hiding wrong internal product architecture;
- incorrect aluminium trim path/width/continuity;
- weak rear panel architecture;
- generic/oversoft edge language;
- placeholder material response;
- missing meso detail;
- runtime work before appearance fidelity is locked.

Benchmark release target:

```text
REFERENCE_FIDELITY_SCORE >= 8.5/10
and
zero MUST visual blockers
```

The score is a regression oracle, not a replacement for objective evidence.

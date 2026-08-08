# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Current release

**v0.9.0 — Shape Graph, coarse-to-fine reconstruction and node-by-node geometric proof.**

v0.9 addresses a failure exposed by the Lafar Wayfinding Pylon: the agent could possess good Blender skills and strong final QA, yet still interpret a complex object too loosely, build many parts at once and represent a compound hard-surface form as stacked boxes/bevels before proving its primary geometry.

The central change is:

```text
reference
-> understand form hierarchy
-> Shape Graph
-> classify mathematical representation
-> RDL coarse-to-fine build
-> validate one Shape Node at a time
-> final reconstruction fidelity proof
-> runtime
```

not:

```text
reference
-> one large build script
-> 20 objects appear
-> quick visual check
```

## Core v0.9 concepts

### Reconstruction Shape Graph

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
- authoritative views and the properties each view controls;
- numeric/relationship constraints;
- validation contract;
- implementation skill.

`Shape Graph != Blender Object hierarchy`.

### Reconstruction Detail Levels

RDL is separate from runtime LOD:

```text
RDL0 envelope
RDL1 primary forms
RDL2 secondary structural forms
RDL3 structural features
RDL4 edge language
RDL5 surface/detail
```

Runtime `LOD0..LOD3` is generated only after reconstruction is accepted.

### Node-by-node execution

Canonical transaction:

```text
one READY node
-> build/repair only that node
-> BUILT_UNVERIFIED
-> QA isolation
-> required registered views
-> numeric/section/regression checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | FAIL
```

Required children remain blocked until their host/parent is accepted.

### RDL stage barriers

A later detail level cannot start because it is convenient.

```text
RDL0 PASS
-> RDL1 nodes + barrier
-> RDL2 nodes + barrier
-> RDL3 nodes + barrier
-> RDL4
-> RDL5
-> final RECON_FIDELITY_GATE
```

### Representation before Blender operator

The agent classifies the form before selecting implementation:

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

A complex base that changes width, depth and corner treatment along Z should not default to `cube + bevel`.

### Multi-section hard-surface loft

v0.9 adds `SECTION_LOFT_HARD_SURFACE` and `executors/section_loft.py` for deterministic station-based hard-surface geometry.

Typical use:
- plinth/base widening toward the ground;
- structural shoulder between narrow body and wide base;
- shells with changing width/depth/corner plan.

The executor keeps section point correspondence deterministic and exposes pure geometry validation plus an explicit Blender creation entry point.

## New v0.9 semantic skills

- `SHAPE_GRAPH`;
- `SHAPE_CLASSIFY`;
- `RECONSTRUCTION_NODE_GATE`;
- `SECTION_LOFT_HARD_SURFACE`.

New executors:

```text
executors/shape_graph.py
executors/reconstruction_node_gate.py
executors/section_loft.py
```

They are `CONTRACT_READY` until a real Blender 5.1 benchmark exercises the v0.9 contracts end-to-end.

`MESH_VALIDATE` remains the currently proven `EXECUTOR_READY` library executor.

## v0.8 foundation retained

v0.9 keeps the v0.8 proof-integrity layer:
- registered reference overlay validation;
- chroma-aware reference masks;
- layer-stack visibility validation;
- proof-bearing `RECON_FIDELITY_GATE`;
- no narrative `PASS` without provenance;
- package checks for primitive attributes such as `TEXCOORD_0` and node-transform policy.

The distinction is:

```text
v0.8: prove whether reconstruction is correct
v0.9: structure the work so the agent understands and solves the right forms before detail
```

## Existing runtime pipeline retained

v0.7 infrastructure remains active:
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

### Level A now additionally requires
- valid Shape Graph revision;
- required Shape Nodes accepted;
- required RDL barriers passed;
- proof-bearing final reconstruction fidelity gate.

### Level C
Still requires runtime LOD/collision/material/bake/package/export closure and round-trip invariants.

### Level D
Requires actual target-engine proof such as production loader, engine regression test or instantiation. Blender glTF re-import remains Level C evidence only.

## Repository structure

- `00_governance` — state/routing/skills/task packs/completion
- `01_analysis` — briefs/references/features/measurements
- `02_blender_api` — Blender 5.1 API/runtime compatibility/cache
- `03_modeling` — hard-surface/topology/UV/procedural modeling
- `04_game_ready` — runtime LOD/collision/bake/export contracts
- `05_execution` — node execution, stage barriers, QA, DAG, completion proof
- `06_prompts` — system/planner/reviewer/repair prompts
- `07_examples` — real benchmark/post-mortem runs
- `08_scripts` — reusable validation patterns
- `09_engine` — project/runtime profiles and integration proof
- `10_reconstruction` — evidence-driven 1:1 reconstruction + Shape Graph/RDL layer
- `11_playbooks` — asset-class production playbooks
- `executors` — reusable Python executors/candidates
- `99_sources` — technical sources

## Canonical source

Modular Markdown files listed in `MANIFEST.json` are canonical.

`_FULL_LIBRARY.md` is generated from the manifest and should not be edited manually.

## v0.9 benchmark

Canonical new regression benchmark:

`07_examples/78_LAFAR_WAYFINDING_PYLON_SHAPE_GRAPH_REGRESSION_BENCHMARK.md`

It protects against:
- production geometry before Shape Graph;
- monolithic multi-RDL builds;
- child geometry on failed parent;
- primary nodes without per-view proof;
- box abuse for multi-section forms;
- detail skills before host acceptance;
- RDL barrier bypass;
- runtime work before reconstruction fidelity PASS.

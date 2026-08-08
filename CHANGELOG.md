# Changelog

## 0.10.0

v0.10.0 is the **reference appearance fidelity + anti-self-certification** release.

It is driven by the Lafar Street Bench v0.9 benchmark. That run was technically strong: hard dimensions, outer silhouettes, LOD budgets and glTF package checks passed. The user still rated the reconstruction only **6/10** because the side housings, aluminium trim, rear assembly, edge language, material response and meso detail did not faithfully reproduce the concept art.

The release closes the gap between:

```text
technically coherent asset
```

and:

```text
visibly the same designed product
```

### Reference Appearance Contract
- added `10_reconstruction/180_REFERENCE_APPEARANCE_CONTRACT.md`;
- 1:1/L4/L5 reconstruction now inventories visible appearance owners in addition to Shape Nodes;
- owner classes include part boundaries, trim paths, junctions, edge families, material/emissive/branding regions, detail features and negative spaces;
- source authority is resolved per visible property rather than through one global `card wins` decision;
- A0–A5 appearance hierarchy separates massing, product architecture, edge language, materials, meso detail and micro detail.

### Anti-circular validation
- added `10_reconstruction/181_ANTI_CIRCULAR_VISUAL_VALIDATION.md`;
- a builder can no longer prove reference fidelity only by checking geometry against constants it inferred itself;
- strict reference-derived evidence requires canonical `validator_id`, provenance and source reference;
- projected evidence additionally requires registration;
- canonical validators cannot be replaced by a builder-local `Gate.accept()`.

### Part Boundary / Trim / Junction Graph
- added `10_reconstruction/182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md`;
- internal visible architecture is now first-class evidence instead of being hidden behind a correct outer silhouette;
- major panel/material boundaries, trim paths and multi-part junctions receive stable IDs, source ROIs and validation ownership;
- trim validation checks path, width, start/end, corner wrapping, host adjacency and continuity.

### Edge, material and detail fidelity
- added `10_reconstruction/183_EDGE_MATERIAL_DETAIL_FIDELITY.md`;
- strengthened `164_EDGE_LANGUAGE_SYSTEM.md`;
- strengthened `124_MATERIAL_EVIDENCE_RECONSTRUCTION.md`;
- RDL4 cannot pass only because bevel preserves protected dimensions;
- edge families now require reference profile/radius/start-end/continuity evidence;
- material segmentation is explicitly separated from material appearance;
- brushed/directional material response, roughness hierarchy, neutral lookdev, emissive recession and detail coverage become evidence owners;
- L5 requires zero silently missing MUST details unless authority explicitly waives them.

### Appearance Fidelity Gate
- added `05_execution/72_APPEARANCE_FIDELITY_GATE.md`;
- added `executors/appearance_fidelity_gate.py`;
- L4/L5 categories are non-compensating: a failed MUST trim path cannot be averaged away by perfect dimensions or materials;
- optional benchmark score remains diagnostic, with Street Bench regression target `>= 8.5/10` plus zero MUST blockers.

### Canonical proof hardening
- `executors/reconstruction_node_gate.py` upgraded to v0.2.0;
- required view proof names canonical validators;
- reference-derived proof requires source reference IDs;
- projected proof requires registration IDs;
- local builder gates are rejected as canonical view acceptance.

### Final reconstruction gate hardening
- `executors/fidelity_gate.py` upgraded to v0.3.0;
- target L4/L5 requires `APPEARANCE_FIDELITY_GATE` before runtime;
- final gate validates canonical validator identity and source anchoring;
- correct dimensions, silhouette, UVs, triangle budgets, package readback or engine load cannot compensate for failed appearance fidelity.

### Runtime lock

For L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> LOD / UV / bake / export / runtime FORBIDDEN
```

This prevents spending large runtime effort on a visually unresolved reconstruction.

### Benchmark
- added `07_examples/79_LAFAR_STREET_BENCH_V09_APPEARANCE_FAILURE_REGRESSION_BENCHMARK.md`;
- records the v0.9 Street Bench result as a reconstruction regression despite technical pipeline success;
- separates `TECHNICAL_PIPELINE_SCORE` from `REFERENCE_FIDELITY_SCORE`;
- protects against outer-silhouette-only acceptance, local circular gates, coarse side-module decomposition, wrong trim paths, weak rear architecture, generic edge language, placeholder materials and silent detail omission.

### Validator pattern / tests
- added `08_scripts/96_REFERENCE_ANCHORED_APPEARANCE_VALIDATOR_PATTERN.md`;
- added `tools/test_v010_reference_fidelity.py`;
- CI preserves v0.9 Shape Graph regression tests and adds v0.10 tests for source anchoring, registration, local-gate rejection, appearance blocking and final runtime lock.

Canonical manifest version: **0.10.0**.
Canonical module count: **222**.
Canonical benchmark: **79 — Lafar Street Bench v0.9 Appearance-Fidelity Failure**.

## 0.9.0

v0.9.0 is the **Shape Graph + coarse-to-fine geometric reasoning** release.

It is based on the second Lafar Wayfinding Pylon post-mortem: after v0.8 hardened proof-bearing visual fidelity, the remaining failure was earlier in the process. The agent still lacked a mandatory internal model of what the object is made of, could create many unrelated parts in one build transaction and could represent a compound base/transition as stacked boxes plus bevels before proving its primary form.

### Reconstruction Shape Graph
- added `10_reconstruction/174_RECONSTRUCTION_SHAPE_GRAPH.md`;
- design hierarchy is now explicit: G0 envelope, G1 primary form, G2 secondary structural form, G3 structural feature, G4 edge language, G5 surface detail;
- Shape Nodes carry parent/dependencies, role, shape class, authoritative views, constraints and validation ownership;
- Shape Graph is a design/evidence model, not Blender object hierarchy.

### Reconstruction Detail Levels
- added `175_RECONSTRUCTION_DETAIL_LEVELS.md`;
- RDL0–RDL5 enforce coarse-to-fine construction;
- RDL is explicitly separated from runtime LOD;
- runtime LOD work starts only after reconstruction fidelity acceptance.

### Node contracts and execution
- added `176_RECONSTRUCTION_NODE_CONTRACT.md`;
- added `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`;
- added `05_execution/70_RECONSTRUCTION_NODE_EXECUTION_PROTOCOL.md`;
- one Shape Node is now the default geometry transaction;
- node must be built -> isolated -> validated in required views -> accepted before dependent children unlock;
- monolithic multi-RDL `build_all()` is a v0.9 regression unless it internally preserves node gates.

### Stage barriers
- added `05_execution/71_RECONSTRUCTION_STAGE_BARRIER.md`;
- each RDL has a hard transition barrier;
- detail cannot advance because it is easy to implement;
- later changes dirty earlier barriers when protected form regresses.

### Shape classification before Blender operators
- added `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md`;
- updated object decomposition and Feature-to-Modeling Strategy Map;
- canonical representation classes now include extruded/revolved/swept profile, multi-section loft/transition, SubD freeform and layered assembly;
- box-abuse detector prevents `cube + bevel` from being the default for compound primary forms.

### Multi-section hard-surface loft
- added `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`;
- added playbook `11_playbooks/118_COMPLEX_HARD_SURFACE_BASE_AND_TRANSITION.md`;
- added `executors/section_loft.py` candidate;
- deterministic section rings, point correspondence and quad bridging are reusable rather than asset-specific;
- complex plinth/shoulder geometry can be represented by semantic section stations.

### Executable graph/gate layer
- added `executors/shape_graph.py`;
- added `executors/reconstruction_node_gate.py`;
- Shape Graph executor validates DAG structure, level/RDL consistency, readiness and stage barriers;
- node gate requires proof-bearing isolation/view/numeric/regression evidence;
- all three v0.9 executors were locally syntax/smoke tested; they remain `CONTRACT_READY` pending a real Blender 5.1 end-to-end benchmark.

### Routing / prompts
- Semantic Skill Registry adds `SHAPE_GRAPH`, `SHAPE_CLASSIFY`, `RECONSTRUCTION_NODE_GATE`, `SECTION_LOFT_HARD_SURFACE`;
- Knowledge Router and Task Packs now route through Shape Graph planning and one-node construction;
- System Prompt rewritten around representation-first, node-by-node RDL execution;
- Shape Graph Planner Prompt added.

### Benchmark
- added `07_examples/78_LAFAR_WAYFINDING_PYLON_SHAPE_GRAPH_REGRESSION_BENCHMARK.md`;
- protects against pre-graph geometry, multi-RDL monolithic build, child-on-failed-parent, missing per-view primary proof, box abuse, premature leaf skills and runtime-before-fidelity.

Canonical manifest version: **0.9.0**.
Canonical module count: **215**.

## 0.8.0

v0.8.0 is the **proof-bearing reconstruction fidelity** release based on the ~67k-token Lafar Wayfinding Pylon run.

Key changes:
- `RECON_FIDELITY_GATE` before runtime;
- registered reference overlay/silhouette/ROI validator;
- chroma-aware reference mask model for bright materials/emissive;
- layer-stack visibility/order validator for glass/content/recess assemblies;
- reconstruction acceptance requires typed evidence + provenance;
- HARD/MUST/CANONICAL deviations require explicit authority closure;
- glTF package validation extended to required primitive attributes such as `TEXCOORD_0` and node-transform policy;
- engine dimension proof distinguishes local vertex geometry from node transform policy;
- benchmark `77_LAFAR_WAYFINDING_PYLON_VISUAL_FIDELITY_REGRESSION_BENCHMARK.md`.

## 0.7.0

v0.7.0 is the **runtime-proof integrity + project infrastructure reuse** release.

Key changes:
- image datablock cache coherence;
- executable Pipeline DAG / dirty-stage reuse;
- post-export invariant validation;
- canonical runtime root/path contract;
- verified RPG project pipeline profile;
- target-engine integration smoke-test contract;
- trustworthy test oracle and bite-test rules;
- completion gate distinguishes Blender round-trip from Level D engine proof;
- benchmark `76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`.

Canonical module count at v0.7: 198.

## 0.6.0

Deterministic bake/runtime closure:
- bake execution/channel semantics;
- stable UV atlas/LOD contract;
- semantic baked-map validation;
- dirty-stage cache and long-running job protocol;
- import-safe build/bake/export patterns;
- runtime package validation;
- benchmark `75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`.

## 0.5.0

First benchmark-driven agent execution/completion release:
- explicit completion levels A–D;
- Blender 5.1 runtime compatibility preflight;
- reusable reference/profile/radial/mesh/runtime/QA/completion executors;
- game-ready bake gate;
- material/emissive runtime boundaries;
- asset catalog integration contract;
- benchmark `74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`.

## 0.3.0

Full Reconstruction Layer:
- evidence/provenance model;
- concept-sheet segmentation;
- authority/conflict system;
- Dimension Graph and locks;
- landmark/calibration system;
- geometry inference rules;
- material/branding reconstruction;
- multi-view QA/regression gates;
- blueprint/photo/stylized modes;
- Lafar Street Bench benchmark.

## 0.2.0

Production layer:
- camera/reference matching;
- Visual Feature Map;
- high/low-poly workflow;
- baking/trim/decal/curve/Geometry Nodes workflows;
- texture packing/mip safety;
- automated visual diff;
- reference fidelity levels;
- engine profile/adapter;
- deterministic QA render/diff patterns.

Architecture retained across releases:
- modular MD files are canonical;
- `_FULL_LIBRARY.md` is generated from `MANIFEST.json`.

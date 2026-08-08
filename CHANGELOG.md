# Changelog

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

## 0.19.0 — Production Studio Runtime

- Promoted persistent asset/component production state and relational parameter graph to release executors.
- Added versioned design-system repository with reverse usage and impact reporting.
- Added persistent dependency-aware production task queues and approval lifecycle.
- Added compact scene/component snapshots, structural diffs and mutation-scope enforcement.
- Routed component/feature reference evidence into token-bounded task packs.
- Added Production Iteration Gate and standalone Asset Production Studio GUI.
- Added canonical Benchmark 89 for the Lafar street-bench production workflow.

# Changelog

## 0.18.0

v0.18.0 is the **Runtime Verification & Contract Convergence** release.

Key changes:
- introduced one canonical provider state protocol and one canonical JSON provider registry;
- removed duplicate provider metadata from active executors and retained the old catalog only as a registry-backed compatibility facade;
- made Blender add-on discovery non-executing and preserved unknown providers as `UNKNOWN`;
- added explicit capability-probe adapters and real cleanup validation;
- changed Geometry Nodes discovery from implied PASS to `PROBE_REQUIRED` until a real Blender probe succeeds;
- added dependency-free provider version constraints and a complete auditable decision pipeline;
- added contract/executor/test parity validation, pytest/ruff structure and v0.17 compatibility fixtures;
- introduced `MANIFEST` schema v2 and deterministic `_RUNTIME_INDEX.json`;
- consolidated active Router/Registry/System Prompt semantics instead of stacking historical overrides;
- split read-only normal CI, pinned Blender runtime CI and the only write-enabled release workflow;
- removed the v0.17 metadata-upgrade chain from active CI/release;
- added Benchmark 87 and real Blender runtime discovery/Geometry Nodes/cleanup tests.

Canonical benchmark: **87 — Lafar Runtime Capability Probe v0.18 Regression**.

## 0.17.0

v0.17.0 is the **Runtime Provider Discovery + Capability Inventory + Selection Transparency** release.

Key changes:
- added Blender-side discovery of enabled/discoverable add-ons/extensions plus registered Asset Libraries;
- separated ready Asset Libraries from procedural generators, external generators, utilities and built-in backends;
- added normalized identity/classification for Sapling, IvyGen, A.N.T. Landscape, Sverchok, MPFB, Meshy, Geo Nodes Guide and MCP;
- added `EXPECTED_PROVIDER_GATE`: user/project-declared installed providers cannot silently disappear from discovery;
- added explicit discovery/probe/domain/quality/selection state separation;
- added mandatory `PROVIDER_SELECTION_REPORT` showing relevant rejected providers and reasons;
- added vegetation routing that keeps Sapling/IvyGen/Sverchok visible even when no ready vegetation library exists;
- changed NodeToPython policy to optional reference/development tool rather than BlenderSkill 5.1 runtime dependency;
- added Benchmark 86 and adversarial provider-discovery regression tests.

Canonical benchmark: **86 — Lafar Provider Discovery v0.17 Regression**.

## 0.16.0

v0.16.0 is the **Persistent Location Design System + Reusable Visual Language** release.

Key changes:
- operationalized the thin v0.15 design-system gate as a persistent source-side layer under `14_design_system/`;
- added find-or-create `LOCATION_DESIGN_SYSTEM_RESOLVE` returning canonical MD/JSON/material/branding/component/Asset-Library paths;
- added machine-readable design-system manifest readiness validation;
- added deterministic Universe/Location/Organization/Family/Asset inheritance with locked-token protection and provenance;
- added hash-deduplicated promotion of reusable logos, textures, decals, profiles and source resources;
- separated source design-system root from the v0.14 runtime location material library;
- added canonical material, branding, component/nodegroup, form/edge/detail, weathering and lighting languages;
- added Blender Asset Library packaging contract for API-driven reuse through `.blend` libraries;
- added asset consumption protocol and non-compensating `DESIGN_SYSTEM_CONFORMANCE_GATE`;
- added design-system version/change propagation semantics;
- fixed the v0.15 CI import-path failure so the location-assembly regression runs from GitHub Actions;
- added Benchmark 85 and pure-Python v0.16 regression tests.

Canonical benchmark: **85 — Lafar Location Design System v0.16 Regression**.

## 0.15.0

v0.15.0 is the **Location Reconstruction + Environment Assembly** release, driven by the failed v0.14 Lafar Restaurant full-location build.

Key changes:
- added `13_environment_assembly/` as the hierarchy above single-asset reconstruction;
- added persistent Location Scene Graph (`LOCATION -> ZONE -> SYSTEM -> ASSET -> INSTANCE`);
- added exhaustive Location Asset Manifest with explicit `MISSING/PROXY/BUILDING/ACCEPTED/INSTANCED` state and 100% required HERO closure;
- made Location Design System mandatory before asset proliferation, reusing the v0.14 persistent material-language library;
- added architecture-first assembly, zoning, placement anchors, HERO composition and furniture-cluster grammar;
- added semantic Spatial Relation Graph and explicit circulation/clearance validation;
- added non-compensating location interpenetration, reference-composition and completeness gates;
- added location completion levels and runtime partitioning/instancing boundary;
- upgraded `06_prompts/60_SYSTEM_PROMPT.md` to v0.15 and added the dedicated location planner prompt;
- added pure-Python decision validators and adversarial v0.15 regression tests;
- added Benchmark 84 — Lafar Restaurant Full Location Reconstruction.

Canonical benchmark: **84 — Lafar Restaurant v0.15 Full Location Reconstruction Regression**.

## 0.14.0

v0.14.0 is the **visual-quality + library-first + persistent location-material-language + context-efficiency** release, driven by human review of the v0.13 Lafar planter benchmark.

Key changes:
- runtime provider compatibility is separated from visual quality tier and usage suitability;
- final vegetation is library-first: project/licensed quality sources outrank generic procedural fallback when compatible;
- planting composition now owns masses, height layers, rhythm, negative space, periodicity and clone visibility in addition to physical root/stem/container fit;
- reference-driven planting gains compact occupancy/height/mass composition fidelity;
- every location resolves or bootstraps one persistent material-language library and returns its exact path for subsequent prompts;
- material authoring reuses/adapts location families before generating new textures and adds semantic wetness/dirt/contact/wear breakup;
- early visual-quality barrier blocks expensive runtime finishing for visually unresolved assets;
- context-budget gate targets <=30k tokens for the three-planter regression (stretch <=20k) and promotes repeated helpers into canonical executors;
- fixed `PROCEDURAL_GENERATOR_PROVIDER` to emit its canonical `validator_id` directly;
- added benchmark 83 and v0.14 regression tests.

Canonical benchmark: **83 — Lafar Planter v0.14 Visual Quality and Efficiency Regression**.

## 0.13.0

v0.13.0 is the **deterministic procedural vegetation + generator-provider + planter-composition** release. It is intentionally narrower than a generic environment-generator release: the next real Blender 5.1 benchmark is a Lafar planter containing hard-surface container geometry and procedural vegetation.

The release follows a critical separation:

```text
procedural geometry generation
!= botanical/structural acceptance
!= deterministic reproducibility
!= game-ready vegetation
```

### Procedural Generator Provider
- added `00_governance/08_PROCEDURAL_GENERATION_EXTENSION.md` and new `12_procedural_generation/` domain;
- added `PROCEDURAL_GENERATOR_PROVIDER` so third-party tools remain adapters behind stable semantic specs;
- provider records Blender compatibility, execution type, background/UI requirements, deterministic seed support, capabilities, license boundary and isolated runtime probe;
- documentation compatibility is discovery evidence only; active Blender 5.1 probe owns runtime availability;
- added curated provider catalog with executable, probe-required, version-blocked and source-only roles.

### Node graph compilation
- added `NODEGRAPH_TO_PYTHON` contract and `executors/nodegraph_codegen_gate.py`;
- preferred workflow is vetted node graph -> compiler probe -> generated import-safe Python -> clean-scene graph reconstruction -> structural round-trip proof;
- NodeToPython is the preferred compiler candidate when installed and probed;
- generated code should normally remove the compiler add-on as a runtime dependency;
- `geonodes` is tracked as an optional Python-first Geometry Nodes authoring route.

### Botanical grammar and generation
- added `VEGETATION_BOTANICAL_GRAMMAR` with stem/branch hierarchy, internodes, phyllotaxis, crown envelope/density, apical dominance, tropism, age/season and root/contact semantics;
- form classes include tree, shrub, herbaceous, grass, rosette, reed, vine, ground cover and alien branching;
- added `VEGETATION_GENERATION_GATE` requiring provider proof, botanical proof, semantic parts, generation metadata and a fixed-seed reproduction probe;
- procedural assets persist provider/version, seed, parameter hash, geometry signature and semantic part IDs.

### Vegetation placement and composition
- added deterministic `VEGETATION_SCATTER` over pre-sampled candidates with slope, biome weight, exclusion and minimum-spacing constraints;
- morphology seed and placement seed are separated by policy;
- added `PLANTER_VEGETATION_COMPOSITION` to validate rootball/soil/wall/stem relationships;
- initial composition validator supports rectangular and circular usable soil footprints;
- host/container repair remains compatible with v0.12 dependency invalidation semantics.

### Vegetation runtime preparation
- added `VEGETATION_RUNTIME_PREP` as a separate gate from generation;
- runtime planning covers LOD budgets, leaf-card/impostor recommendation, semantic-part preservation, material-slot limits, instancing and wind attributes;
- benchmark MID defaults begin at 30k / 14k / 5k / 1.2k triangles for LOD0–LOD3 unless project profile overrides them;
- raw high-poly generator success can never claim game-ready completion.

### Tool policy
- built-in Blender 5.1 Geometry Nodes is the primary runtime-safe backend;
- Sapling Tree Gen, IvyGen, A.N.T. Landscape, Archimesh, Sverchok and engon/botaniq are optional providers after local capability/license probe;
- Infinigen, ProcFunc and BlenderProc are treated primarily as architecture/algorithm sources for this release rather than mandatory in-process dependencies;
- The Grove remains version-blocked for BlenderSkill 5.1 until compatible runtime evidence replaces the currently documented Blender 4.2–4.4 range.

### Benchmark and tests
- added `07_examples/82_LAFAR_PLANTER_VEGETATION_V013_BENCHMARK.md`;
- added `11_playbooks/121_LAFAR_PLANTER_AND_VEGETATION.md`;
- added `08_scripts/100_PROCEDURAL_PROVIDER_AND_VEGETATION_VALIDATION_PATTERN.md`;
- added eight v0.13 pure-Python decision/catalog executors;
- added `tools/test_v013_procedural_vegetation.py` and wired it into CI;
- v0.9, v0.10, v0.11 and v0.12 regression suites remain active.

Canonical manifest version: **0.13.0**.
Canonical module count: **263**.
Canonical benchmark: **82 — Lafar Planter + Vegetation v0.13**.

## 0.12.0

v0.12.0 is the **geometric integrity + mutation postcondition + adversarial validation** release, driven by the Lafar Street Lamp v0.11 repair benchmark.

v0.11 enforced the intended reconstruction process and produced a fully green evidence chain, but human review still found a severe `ARM` / `SENSOR_MODULE` interpenetration that erased head detail. The initial containment guard also returned PASS on the known-broken geometry. The release therefore closes the gap between `correct process/evidence` and `physically correct geometry`.

### Mutation postconditions
- added `05_execution/76_MUTATION_POSTCONDITION_GATE.md` and `executors/mutation_postcondition_gate.py`;
- `LOCAL_BUILDER: PASS` no longer authorizes `BUILT_UNVERIFIED` by itself;
- risky mutations record before/after topology, volume/signature, transform and helper lifecycle;
- silent Boolean no-op, wrong volume direction, unapplied transform and failed feature probes block the node;
- `NODE_STATE_STORE` v0.2 requires canonical mutation-postcondition proof for `READY_TO_BUILD -> BUILT_UNVERIFIED`.

### Assembly integrity
- added `10_reconstruction/189_ASSEMBLY_RELATION_AND_INTERPENETRATION_CONTRACT.md`;
- added `executors/assembly_integrity_gate.py`;
- junctions declare semantics such as `SHADOW_GAP`, `BUTT_JOINT`, `RECESSED_INSERT`, `FLUSH_MATE`, `CLEARANCE`, `EMBEDDED` and `WELDED` before validation;
- measured gap/contact/embedding/interpenetration is evaluated against the declared relation;
- generic overlap can no longer prove that two product parts are correctly joined.

### Adversarial validation
- added `10_reconstruction/190_ADVERSARIAL_VALIDATION_AND_NEGATIVE_CONTROLS.md` and `executors/validator_negative_control.py`;
- MUST validators require a known-good PASS and known-broken FAIL fixture before they can be trusted as acceptance evidence;
- a validator that returns PASS on its own defect class is explicitly rejected as toothless.

### Repair invalidation
- added `05_execution/77_REPAIR_INVALIDATION_AND_EVIDENCE_SUPERSESSION.md` and `executors/dependency_invalidator.py`;
- repairing an accepted host dirties/blocks dependent Shape Nodes, invalidates hosted Appearance Owners and marks old revision evidence `SUPERSEDED`;
- unrelated accepted branches remain reusable;
- stale green evidence cannot survive a geometry revision.

### Topology and reference-mask hardening
- `MESH_VALIDATE` now reports high-order, non-planar and concave n-gons plus signed closed volume;
- non-planar n-gons and inverted closed volumes fail while planarity/concavity are classified rather than blanket-rejecting all n-gons;
- `REFERENCE_OVERLAY_VALIDATE` v0.2 supports annotation exclusions and connected-component selection so dimension lines/leaders do not contaminate product silhouette evidence;
- added `191_REFERENCE_MASK_CONTAMINATION_AND_ANNOTATION_EXCLUSION.md`.

### Execution integration
- `RECONSTRUCTION_NODE_GATE` v0.4 requires canonical mutation postcondition and assembly-integrity evidence for authorized production mutations;
- state-machine precedence is now mutation -> postcondition -> `BUILT_UNVERIFIED` -> source QA/integrity -> canonical node gate;
- added `08_scripts/99_GEOMETRIC_INTEGRITY_VALIDATION_PATTERN.md` and `11_playbooks/120_INDUSTRIAL_ASSEMBLY_INTEGRITY.md`.

### Benchmark and tests
- added benchmark `81_LAFAR_STREET_LAMP_V011_GEOMETRIC_INTEGRITY_REGRESSION_BENCHMARK.md`;
- added `tools/test_v012_geometric_integrity.py`;
- regression covers broken-vs-fixed sensor/arm relation, silent Boolean no-op, toothless validator rejection, state-store postcondition enforcement and repair invalidation;
- v0.9, v0.10 and v0.11 regression suites remain active.

Canonical manifest version: **0.12.0**.
Canonical module count: **242**.
Canonical benchmark: **81 — Lafar Street Lamp v0.11 Geometric Integrity Regression**.

## 0.11.0

v0.11.0 is the **enforced reconstruction execution + reference-conflict closure** release, driven by the Lafar Street Lamp v0.10 benchmark.

The lamp was the best reconstruction so far (human assessment about 7.5/10), proving that v0.10 improved form and appearance understanding. It also exposed the next gap: the agent could still organize code node-by-node while executing the whole RDL0→RDL5 asset in one monolithic run, despite `ready_nodes=[]` and without acceptance between nodes.

### Hard execution authorization
- added `05_execution/73_EXECUTION_AUTHORIZATION_GATE.md` and `executors/execution_authorization_gate.py`;
- `CONSTRAINED` is eligibility, not permission to build;
- production mutation requires persisted `READY_TO_BUILD` plus canonical authorization;
- parent/dependency acceptance and previous RDL barriers are rechecked immediately before mutation.

### Persistent node state
- added `05_execution/74_PERSISTENT_NODE_STATE_AND_CHECKPOINTS.md` and `executors/node_state_store.py`;
- `BUILT_UNVERIFIED` is a hard branch stop;
- only `RECONSTRUCTION_NODE_GATE` can transition a built node to `ACCEPTED`;
- checkpoints separate `shape_nodes`, `appearance_owners`, `evidence` and `conflicts`.

### Node-scoped orchestration
- added `05_execution/75_NODE_SCOPED_ORCHESTRATION.md`;
- code organization into `node_*()` functions no longer counts as node-by-node execution;
- deterministic replay is allowed, but cannot mint new acceptance evidence.

### Conflict arbitration and per-view proof
- added `184_REFERENCE_CONFLICT_ARBITRATION.md` and `executors/reference_conflict_resolver.py`;
- added `185_PER_VIEW_EVIDENCE_AND_DERIVED_PARAMETER_PROVENANCE.md`;
- explicit dimensions own named dimensions, not unrelated local form;
- detail/hero/ortho evidence uses different proof modes;
- equal-authority contradictory interpretations remain BLOCKED instead of being averaged or silently selected.

### Appearance-owner closure
- added `186_APPEARANCE_OWNER_COVERAGE_AND_REPORT_NAMESPACES.md` and `executors/appearance_owner_coverage.py`;
- `APPEARANCE_FIDELITY_GATE` v0.2 requires canonical MUST-owner inventory closure for strict L4/L5;
- missing or unverified MUST owners block appearance acceptance.

### Diagnostic form before finish
- added `187_RDL_DIAGNOSTIC_GEOMETRY_AND_NEUTRAL_SHADING.md`;
- RDL0 must create falsifiable grey diagnostic geometry;
- RDL0–RDL3 source-fit QA defaults to neutral diagnostic shading;
- production material response belongs to RDL5.

### Runtime source integrity and reuse
- added `188_CANONICAL_SKILL_RUNTIME_PINNING_AND_ANALYSIS_REUSE.md` and `executors/runtime_source_pin.py`;
- benchmark runs require version/commit/source-root pinning and one active executor root;
- repeated one-off analysis helpers trigger canonical executor reuse/migration review.

### Benchmark and playbook
- added benchmark `80_LAFAR_STREET_LAMP_V010_EXECUTION_DETAIL_REGRESSION_BENCHMARK.md`;
- added `119_CIVIC_STREET_LAMP.md`;
- regression target: human reference fidelity >= 8.5/10, zero unauthorized mutations, zero children built on unaccepted hosts, zero missing MUST appearance owners.

### Tests
- added `tools/test_v011_execution_enforcement.py`;
- v0.9 and v0.10 regression suites remain active and were updated for the stricter v0.11 contracts.

Canonical manifest version: **0.11.0**.
Canonical module count: **234**.
Canonical benchmark: **80 — Lafar Street Lamp v0.10 Execution and Detail Regression**.

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

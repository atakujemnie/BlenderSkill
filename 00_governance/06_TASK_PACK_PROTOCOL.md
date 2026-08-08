# Task Pack Protocol

## Purpose

A Blender agent must not load every relevant document for the whole asset lifecycle at once.

A `Task Pack` is the smallest bounded set of knowledge required for the current state and task subtype.

```text
current state + task subtype
-> one Task Pack
-> only required modules
-> execute / validate
-> persist compact state
-> unload non-required context
-> advance state
```

The Knowledge Router selects the pack. The pack does not replace the State Machine or Semantic Skill Registry.

## Required fields

```yaml
task_pack:
  id: RECON_TECHNICAL_SHEET_ANALYZE
  state: ANALYZE
  purpose: segment and measure a technical concept sheet
  required_modules: []
  optional_modules: []
  forbidden_until_later: []
  persistent_outputs: []
  context_budget_tokens: 8000
```

`context_budget_tokens` is a planning ceiling. When approaching it, summarize persistent state and unload non-required material before loading more documents.

---

# Canonical packs

## `SESSION_PREFLIGHT`

Use once before first production scene mutation.

Required:
- Agent Charter;
- Semantic Skill Registry;
- Tool Discovery and Registry;
- Tool Call and Token Efficiency;
- Agent Tool API Profile;
- Blender 5.1 Runtime Compatibility Matrix.

Preferred semantic skill:
- `RUNTIME_COMPAT`.

Persistent output:
- Tool Registry;
- capability bindings;
- Blender version;
- available render engines;
- relevant version-sensitive API facts;
- stable project-root source;
- whether the blend is currently saved.

Do not repeat compatibility discovery before every feature unless the runtime changes.

---

## `RECON_TECHNICAL_SHEET_ANALYZE`

Required:
- Agent Charter;
- Reconstruction Controller;
- Evidence Model;
- Reference Ingestion;
- View Authority Matrix;
- Reference Measurement Protocol;
- Blueprint/Technical Drawing Mode;
- Reference Analysis Cache;
- Reference Measurement Executor Pattern.

Persistent output:
- Reference Registry;
- Analysis Cache;
- Evidence Summary;
- locked dimensions;
- View Authority Matrix;
- unresolved conflicts.

Forbidden until later unless required to resolve an ANALYZE blocker:
- UV authoring;
- materials/shaders;
- LOD generation;
- collision;
- export;
- microdetail modeling;
- decorative detailing.

---

## `RECON_BLOCKOUT`

Required:
- Reconstruction Controller;
- Dimension Graph;
- dimension locks/tolerances;
- landmark system;
- silhouette constraints;
- object decomposition;
- dimension-locked blockout;
- Build Plan;
- Execution Protocol.

For a rotational primary form, route to `AXISYMMETRIC_PROFILE` rather than writing a new revolve helper.

Do not load material/UV/LOD modules.

---

## `RECON_DETAIL`

Load only after camera/scale/silhouette/primary-form gates pass.

Required:
- current Feature Contract subset;
- feature-to-modeling strategy map;
- only semantic skills required by current Feature IDs;
- checkpoint/visual QA.

Examples:
- narrow seam -> `HS_PANEL_LINE`;
- curved SubD support flow -> `SUBD_TOPOLOGY_CONTROL`;
- radial anchors -> `RADIAL_REPEAT`;
- additive logo/graphic -> decal workflow.

---

## `SURFACE_FINISH`

Load after material segmentation is accepted.

Required only as applicable:
- Material Evidence Reconstruction;
- Lighting vs Material Disentanglement;
- Procedural Material Authoring;
- Brushed Metal + Dark Composite playbook;
- Integrated Light Strip playbook;
- Emissive Runtime Handoff.

Preferred skills:
- `MATERIAL_FINISH_CIVIC` for maintained civic props;
- `EMISSIVE_HANDOFF` for guidance/accent emitters.

Persistent outputs:
- material family decisions;
- macro/meso/micro breakup contract;
- wear/dirt masks or strategy;
- emissive authoring status;
- runtime disposition per procedural effect.

Do not start generic grunge iteration before material identity is correct.

---

## `GAME_READY_FINISH`

Load only after reconstruction/modeling acceptance.

### Required knowledge

- Game Asset Contract;
- Completion Levels;
- Polycount/LOD/Collision;
- Pivots/Transforms/Naming;
- Texture/Material Runtime;
- Game-Ready Bake Gate;
- Runtime Bake Execution and Channel Semantics;
- UV Atlas and LOD Stability Contract;
- Bake Output Validation Pattern;
- Incremental Dirty-Stage Cache;
- Long-Running Job and Poll Protocol for expensive operations;
- Emissive Runtime Handoff if applicable;
- active Engine Profile;
- active Project Asset Pipeline Profile;
- Runtime Module Packaging Contract;
- export module;
- Final Validation;
- Mesh Contract Validator;
- Reference-to-Runtime Completeness Report;
- Import-Safe Python Module Pattern when scripts call/reuse one another.

### Preferred skills

- `MESH_VALIDATE`;
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_VALIDATE`;
- `ASSET_COMPLETION`.

### Preferred candidate executors

```text
executors/mesh_validate.py
executors/uv_atlas_contract.py
executors/bake_runtime_textures.py
executors/bake_validate.py
executors/qa_scene_isolation.py
executors/gltf_package_validate.py
executors/completion_gate.py
```

Do not write replacement generic helpers before checking these files.

### Internal stage order

```text
GAME_READY_PREFLIGHT
-> LOD_COLLISION_VALIDATE
-> UV_CONTRACT
-> BAKE_PLAN_DIRTY_GRAPH
-> BAKE_CHANNELS
-> BAKE_VALIDATE
-> RUNTIME_MATERIAL_BIND
-> PACKAGE_EXPORT
-> PACKAGE_READBACK
-> BAKED_RUNTIME_QA
-> ASSET_COMPLETION
```

Do not jump from successful bake files directly to Level C.

### Bake rules

- Bake operator must return `FINISHED`.
- Every contributing material must have the correct selected+active target image node.
- AO/ray-dependent pass must isolate unrelated render-visible geometry.
- BaseColor/Metallic/Emissive use explicit channel semantics.
- Structural bake must not absorb unrelated decal/dynamic-display UV owners.
- Bake source and consuming runtime LODs must share a validated UV contract.
- A channel repair dirties only dependent channels/artifacts.
- Timeout triggers job/artifact inspection, not duplicate full bake.

### Persistent outputs

- LOD report;
- collision report;
- `UV_CONTRACT_ID` + part assignments;
- dirty-stage artifact cache;
- per-channel bake reports;
- semantic bake validation;
- runtime material disposition;
- runtime package/readback report;
- baked-runtime QA result;
- completion report.

### Efficiency target

For a standard hard-surface prop starting from accepted geometry, plan this pack to fit roughly within a 15k-token operational budget when possible.

This is a benchmark target, not a universal hard limit. Complexity may justify more, but solved infrastructure must not be rediscovered.

Level C cannot pass while required Blender-only material effects remain without a runtime strategy or while baked runtime QA/package readback is failing.

---

## `PIPELINE_INTEGRATION`

Load only when target is `PIPELINE_INTEGRATED`.

Required:
- Completion Levels;
- Project Asset Pipeline Profile;
- Engine Adapter Protocol;
- Runtime Module Packaging Contract;
- Asset Catalog Integration Protocol;
- Authoring to Runtime Handoff;
- Reference-to-Runtime Completeness Report.

Preferred skill:
- `ASSET_CATALOG_INTEGRATE`.

Persistent outputs:
- stable asset ID;
- verified packaging profile;
- previous conflicting catalog entry if any;
- registration/update result;
- readback verification;
- importer/instantiation smoke-test result.

If catalog write capability is unavailable, emit a Level D blocker. Do not silently finish at Level C while calling the whole task complete.

---

# Persistent-state rule

Task Pack changes must not discard validated facts.

Persist compact structured records, not full conversation/tool history:

```text
Tool Registry
Compatibility Snapshot
Reference Registry
Reference Analysis Cache
Evidence Ledger
Dimension Graph
View Authority Matrix
Feature Contract
Build Plan
Code Artifact Registry
Checkpoint results
Material Runtime Disposition
UV Contract
Dirty-Stage Artifact Cache
Bake Channel Reports
Runtime Package Profile
Completion Report
```

---

# No duplicate loading

If a module was already loaded and its relevant rules are represented in persistent structured state, do not re-read it merely because the next step mentions the same concept.

Re-read only when:
- conflict requires exact source wording;
- entering a section not represented in persistent state;
- module changed during the session;
- validator explicitly requests it.

---

# Pack expansion rule

Do not load a new module because it might become useful.

Expand only when:
1. current state requires it;
2. measured failure routes to it;
3. current feature maps to it in Semantic Skill Registry.

---

# Analysis completion gate

Before ANALYZE -> CONTRACT/PLAN emit:

```yaml
analysis_complete:
  locked_dimensions: {}
  high_confidence_relations: {}
  view_authority: {}
  feature_ids: []
  unresolved: []
  analysis_cache_valid: true
  status: PASS
```

Once `ANALYZE: PASS`, do not continue broad reference exploration. Later investigation must target a specific unresolved item, feature ID or failed ROI validator.

---

# Final completion gate

Before ending the task:
1. evaluate `TARGET_COMPLETION_LEVEL`;
2. run `ASSET_COMPLETION` contract;
3. emit `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md`;
4. only use unconditional `DONE` if the requested target level passes.

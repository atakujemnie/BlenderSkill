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

Required:
- Game Asset Contract;
- completion levels;
- polycount/LOD/collision;
- transforms/pivots/naming;
- Texture/Material Runtime;
- Game-Ready Bake Gate;
- Emissive Runtime Handoff if applicable;
- active Engine Profile;
- active Project Asset Pipeline Profile;
- export module;
- Final Validation;
- Mesh Contract Validator;
- Reference-to-Runtime Completeness Report.

Preferred skills:
- `MESH_VALIDATE`;
- `BAKE_RUNTIME_TEXTURES` when bake/runtime texture closure is required;
- `EXPORT_VALIDATE`;
- `ASSET_COMPLETION`.

Persistent outputs:
- LOD report;
- collision report;
- texture/bake report;
- runtime material disposition;
- export validation;
- completion report.

Level C cannot pass while required Blender-only material effects remain without a runtime strategy.

---

## `PIPELINE_INTEGRATION`

Load only when target is `PIPELINE_INTEGRATED`.

Required:
- Completion Levels;
- Project Asset Pipeline Profile;
- Engine Adapter Protocol;
- Asset Catalog Integration Protocol;
- Authoring to Runtime Handoff;
- Reference-to-Runtime Completeness Report.

Preferred skill:
- `ASSET_CATALOG_INTEGRATE`.

Persistent outputs:
- stable asset ID;
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

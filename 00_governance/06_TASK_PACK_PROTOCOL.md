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

If a matching validated project profile exists, load it here.

Preferred semantic skills:
- `RUNTIME_COMPAT`;
- `RUNTIME_PATH_RESOLVE` when external runtime paths will be written later.

Persistent output:
- Tool Registry;
- capability bindings;
- Blender version;
- available render engines;
- relevant version-sensitive API facts;
- stable project root;
- active Project Asset Pipeline Profile ID if matched;
- canonical engine-visible runtime asset root if known;
- whether the blend is currently saved.

Do not repeat compatibility/path/build discovery before every feature unless the runtime/profile changes.

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
- `MATERIAL_FINISH_CIVIC`;
- `EMISSIVE_HANDOFF`.

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
- Blender Image Datablock Cache Coherence;
- Bake Output Validation Pattern;
- Incremental Dirty-Stage Cache;
- Pipeline DAG Executor and Stage Reuse;
- Long-Running Job and Poll Protocol for expensive operations;
- Emissive Runtime Handoff if applicable;
- active Engine Profile;
- active Project Asset Pipeline Profile;
- Runtime Asset Root and Path Contract before external writes;
- Runtime Module Packaging Contract;
- Post-Export Invariant and Round-Trip Validation;
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
- `IMAGE_CACHE_COHERENCE`;
- `PIPELINE_DAG_PLAN`;
- `RUNTIME_PATH_RESOLVE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `EXPORT_ROUNDTRIP_VALIDATE`;
- `EXPORT_VALIDATE`;
- `ASSET_COMPLETION`.

### Preferred candidate executors

```text
executors/mesh_validate.py
executors/uv_atlas_contract.py
executors/bake_runtime_textures.py
executors/bake_validate.py
executors/image_cache_coherence.py
executors/pipeline_dag.py
executors/runtime_path_resolver.py
executors/qa_scene_isolation.py
executors/gltf_package_validate.py
executors/export_roundtrip_validate.py
executors/completion_gate.py
```

Do not write replacement generic helpers before checking these files.

### Internal stage order

```text
GAME_READY_PREFLIGHT
-> RUNTIME_PATH_PREFLIGHT
-> LOD_COLLISION_VALIDATE
-> UV_CONTRACT
-> PIPELINE_DAG_PLAN
-> BAKE_DIRTY_CHANNELS
-> BAKE_VALIDATE
-> DISK/BLENDER_IMAGE_COHERENCE
-> RUNTIME_MATERIAL_BIND
-> PACKAGE_EXPORT
-> PACKAGE_READBACK
-> EXPORT_ROUNDTRIP_INVARIANTS
-> BAKED_RUNTIME_QA
-> ASSET_COMPLETION
```

Do not jump from successful bake files directly to Level C.

### Bake/cache rules

- Bake operator must return `FINISHED`.
- Every contributing material must have the correct selected+active target image node.
- AO/ray-dependent pass must isolate unrelated render-visible geometry.
- BaseColor/Metallic/Emissive use explicit channel semantics.
- Structural bake must not absorb unrelated decal/dynamic-display UV owners.
- Bake source and consuming runtime LODs must share a validated UV contract.
- A channel repair dirties only dependent channels/artifacts.
- Timeout triggers job/artifact inspection, not duplicate full bake.
- Correct external PNG does not prove Blender's current image datablock is fresh.
- Disk-authoritative baked images must be synchronized/reloaded before runtime-material QA.
- A stale image datablock normally dirties binding/QA, not texture content.

### Stage-reuse rule

Before rerunning `build -> decals -> bake -> export`, use `PIPELINE_DAG_PLAN`.

A local geometry repair may dirty AO/Normal/export while leaving a separate decal atlas or unrelated material channels clean.

Manual full-chain replay is a benchmark regression unless the dependency graph proves every stage dirty.

### Post-export invariant rule

Hard dimensions and datums must be measured on the final exported/re-imported artifact.

Source geometry PASS is insufficient because bevels, export copies and coordinate conversion can change final bounds.

Persist separate results for:
- package metadata readback;
- Blender/neutral round-trip invariants;
- target-engine proof, which belongs to Level D.

### Persistent outputs

- canonical Runtime Path Context;
- LOD report;
- collision report;
- `UV_CONTRACT_ID` + part assignments;
- Pipeline DAG plan;
- dirty-stage artifact cache;
- per-channel bake reports;
- semantic bake validation;
- external-image/cache coherence report;
- runtime material disposition;
- runtime package/readback report;
- export round-trip invariant report;
- baked-runtime QA result;
- completion report.

### Efficiency target

For a standard hard-surface prop starting from accepted geometry, plan this pack to fit roughly within a 15k-token operational budget when possible.

This is a benchmark target, not a universal hard limit. Complexity may justify more, but solved infrastructure must not be rediscovered.

Level C cannot pass while required Blender-only material effects remain without a runtime strategy, while runtime asset destination is unverified, or while exported round-trip invariants/baked-runtime QA are failing.

---

## `PIPELINE_INTEGRATION`

Load only when target is `PIPELINE_INTEGRATED`.

### Required

- Completion Levels;
- active Project Asset Pipeline Profile;
- Engine Adapter Protocol;
- Runtime Asset Root and Path Contract;
- Runtime Module Packaging Contract;
- Asset Catalog Integration Protocol;
- Engine Integration Smoke-Test Contract;
- Test Oracle, Exit Code and Bite-Test Integrity;
- Authoring to Runtime Handoff;
- Reference-to-Runtime Completeness Report.

### Preferred skills

- `RUNTIME_PATH_RESOLVE`;
- `ASSET_CATALOG_INTEGRATE`;
- `TEST_ORACLE`;
- `ENGINE_INTEGRATION_PROOF`;
- `ASSET_COMPLETION`.

### Preferred executors

```text
executors/runtime_path_resolver.py
executors/test_oracle.py
executors/completion_gate.py
```

### Internal stage order

```text
VERIFY_CANONICAL_RUNTIME_ROOT
-> VERIFY_LEVEL_C_EXPORT_ROUNDTRIP_PASS
-> CATALOG_REGISTER_AND_READBACK
-> BUILD_NARROW_ENGINE_TEST_TARGET_IF_REQUIRED
-> TARGET_ENGINE_LOADER_TEST
-> OPTIONAL_CONTROLLED_BITE_TEST_FOR_NEW_ASSERTION
-> FINAL_ENGINE_TEST_GREEN
-> ASSET_COMPLETION
```

### Level D evidence rule

A Blender glTF import is **not** target-engine evidence.

`runtime_import_or_instantiation` must provide one of:

```text
ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
```

The v0.7 `completion_gate.py` rejects a bare string `PASS` for this Level D requirement.

### Test-oracle rule

Do not report test success from:

```bash
./test 2>&1 | tail ...
echo $?
```

unless the executable status is actually preserved with a verified mechanism such as `pipefail`.

Prefer direct process execution/capture.

When a new regression assertion is added, perform one safe bite test when practical and verify the intended assertion message, not merely a non-zero/crash.

### Project-profile reuse

If a matching project profile already contains:
- runtime root;
- catalog source;
- build directory;
- narrow model/import test target;
- test binary;
- production loader;

use those facts directly. Do not spend multiple shell calls rediscovering them.

### Persistent outputs

- stable asset ID;
- verified runtime root/profile ID;
- previous conflicting catalog entry if any;
- registration/update result;
- catalog readback verification;
- engine loader/test result with trustworthy executable exit code;
- bite-test evidence when applicable;
- completion report.

If catalog write capability or target-engine proof is unavailable, Level D is BLOCKED. Do not silently finish at Level C while calling the whole task complete.

Preferred integration-stage efficiency target for an already `GAME_READY_COMPLETE` asset: roughly <=10k operational tokens where project profile/test infrastructure is already known.

---

# Persistent-state rule

Task Pack changes must not discard validated facts.

Persist compact structured records, not full conversation/tool history:

```text
Tool Registry
Compatibility Snapshot
Project Profile ID
Runtime Path Context
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
Pipeline DAG
Dirty-Stage Artifact Cache
Bake Channel Reports
Image Cache Coherence Report
Runtime Package Profile
Export Round-Trip Report
Engine Test Oracle Report
Completion Report
```

---

# No duplicate loading

If a module was already loaded and its relevant rules are represented in persistent structured state, do not re-read it merely because the next step mentions the same concept.

Re-read only when:
- conflict requires exact source wording;
- entering a section not represented in persistent state;
- module/profile changed during the session;
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
2. run Final Validation;
3. run `ASSET_COMPLETION` contract;
4. emit `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md`;
5. only use unconditional `DONE` if the requested target level passes with the required evidence class.
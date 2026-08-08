# Knowledge Router

Agent nie powinien ładować całej biblioteki do każdego zadania.

Przed wyborem modułów stosuj `00_governance/06_TASK_PACK_PROTOCOL.md`.
Knowledge Router wybiera najmniejszy wymagany pakiet dla bieżącego STATE i task subtype.

## Session startup / first scene mutation
Load Task Pack `SESSION_PREFLIGHT`:
- `00_governance/00_AGENT_CHARTER.md`
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `02_blender_api/19_TOOL_DISCOVERY_AND_REGISTRY.md`
- `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`
- `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`
- `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`
- `02_blender_api/23_SCENE_INSPECTION.md`

Route runtime/API discovery to `RUNTIME_COMPAT` before version-sensitive generated code.
Before production mutation, bind connected tools to required semantic capabilities.

## Nowy asset hard-surface
Load:
- Agent Charter
- State Machine
- Semantic Skill Registry
- Asset Brief Schema
- Reference Decomposition
- Feature Contract
- Modeling Decision Tree
- Hard Surface Workflow
- Game Asset Contract
- `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`
- Build Plan
- Execution Protocol
- Code Artifact and Patch Protocol when generating non-trivial Python
- Retry Budget and Strategy Switching
- Visual QA

Set `TARGET_COMPLETION_LEVEL` during CONTRACT/PLAN.
Do not preload UV/material/LOD/export modules before their state is reached.

## Axisymmetric / rotational hard-surface asset

Typical triggers:
- bollard/post;
- round base/collar/cap;
- cylindrical housing;
- stacked radial profile where most primary geometry shares one axis.

Load:
- Semantic Skill Registry
- `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`
- `11_playbooks/110_HARD_SURFACE_CIVIC_FURNITURE.md` for civic props
- Code Artifact and Patch Protocol
- Game Asset Contract
- Feature Contract

Route rotational master geometry to `AXISYMMETRIC_PROFILE` before writing another local `lathe()`/profile-revolve helper.
For repeated radial fasteners/anchors route placement/annulus checks to `RADIAL_REPEAT`.
Keep asymmetric service panels, decals, local emitters and similar features as separate feature owners.

## Poprawka istniejącego assetu
Load:
- Agent Charter
- Semantic Skill Registry
- Feature Contract
- Scene Inspection
- API Strategy
- Blender 5.1 Compatibility Matrix when runtime/API is involved
- Idempotency/Recovery
- Code Artifact and Patch Protocol if a build/QA script is being patched
- Retry Budget and Strategy Switching
- Visual QA
- Failure Recovery
- Repair Prompt

## Problem z Blender API
Load:
- API Strategy
- Blender 5.1 Compatibility Matrix
- Tool Discovery and Registry
- Agent Tool API Profile
- bpy.data vs bpy.ops vs BMesh
- Context/Mode/Selection
- Scene Inspection
- Tool Call Efficiency
- Retry Budget and Strategy Switching

Route capability enumeration, render-engine selection and stable root discovery to `RUNTIME_COMPAT` where possible.

## Procedural panel line / narrow groove
Load:
- Semantic Skill Registry
- `blender-agent-procedural-hard-surface-panel-lines.md`
- Agent Tool API Profile
- Retry Budget and Strategy Switching

If the host is SubD-controlled or pinching/topology flow matters, additionally load `blender-agent-subdivision-topology-control.md`.
Do not route wide/deep recesses or silhouette-changing features to `HS_PANEL_LINE`.

## Subdivision topology problem
Load:
- Semantic Skill Registry
- `blender-agent-subdivision-topology-control.md`
- Topology/Normals/Shading
- bpy.data/BMesh
- Retry Budget

## Mesh / topology validation
Route to `MESH_VALIDATE`.
Load:
- `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`
- Mesh Validation Snippets
- active Game Asset Contract

Every mesh declares topology intent before general PASS/FAIL:
- CLOSED_SOLID;
- OPEN_ASSEMBLY_PART;
- SURFACE_DETAIL;
- COLLISION.

`MESH_VALIDATE` is `EXECUTOR_READY` after successful Blender 5.1 use in the Lafar Civic Bollard benchmark. It still becomes `RUNTIME_BOUND` only after the current integration can invoke/import it.

## Civic material looks too clean / procedural
Route to `MATERIAL_FINISH_CIVIC`.
Load:
- `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md`
- Procedural Material Authoring
- Lighting vs Material Disentanglement
- Material Evidence Reconstruction when reference-driven

Do not add generic grunge. Build macro/meso/micro variation with manufacturing/exposure logic.

## Integrated emissive / neon guidance feature
Route to `EMISSIVE_HANDOFF`.
Load:
- `11_playbooks/115_INTEGRATED_LIGHT_STRIP.md`
- `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`
- active Engine Profile if runtime glow must be verified

Keep asset emitter correctness separate from bloom/exposure/tone-mapping behavior.

## UV atlas shared by bake source and LODs
Route to `UV_ATLAS_CONTRACT`.
Load:
- `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`
- UV/Texel Density/Materials
- active Feature/Object registry

Use semantic part IDs rather than transient Blender object names such as `.001`.
Missing atlas assignment is a hard FAIL.
Do not apply the atlas only to the temporary bake source while exported LODs keep another UV layout.

## High -> low / procedural -> runtime bake
Route runtime texture closure to `BAKE_RUNTIME_TEXTURES`.
Load:
- High-Poly / Low-Poly Workflow when geometric transfer is required
- Baking Pipeline
- `04_game_ready/50_GAME_READY_BAKE_GATE.md`
- `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`
- `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`
- `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`
- `05_execution/64_LONG_RUNNING_JOB_AND_POLL_PROTOCOL.md`
- `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`
- UV/Texel Density/Materials
- Texture Packing and Mip Safety
- active Engine Profile

Preferred executors:
- `executors/bake_runtime_textures.py`;
- `executors/uv_atlas_contract.py`;
- `executors/bake_validate.py`;
- `executors/qa_scene_isolation.py` for AO/ray-dependent passes.

A separate high-poly source is not mandatory for every procedural-to-texture bake.
Do not write a new generic multi-material bake helper before checking these executors.
Do not rerun every channel after a local repair; consult the dirty-stage cache.
A tool timeout triggers job/artifact inspection, not immediate duplicate bake.

## Bake failure diagnostics

Route by measured failure:

```text
bpy bake returns CANCELLED / active image warning
-> BAKE_RUNTIME_TEXTURES target-binding diagnostics

AO nearly black / unexpected global occlusion
-> QA_SCENE_ISOLATE + AO diagnostics

metal BaseColor black after bake
-> BaseColor channel semantics, not lighting iteration

metallic = 1 across atlas
-> scalar channel extraction + region validator

emissive white/full atlas or clipped hue
-> emissive color*strength normalization + approved-region validator

textures correct but runtime model samples wrong regions
-> UV_ATLAS_CONTRACT

export file exists but nodes/material/images wrong
-> RUNTIME_PACKAGE_VALIDATE / EXPORT_VALIDATE
```

Do not restart the entire bake pipeline when one scoped channel/contract fails.

## Game-ready finishing
Use Task Pack `GAME_READY_FINISH` only after modeling/reconstruction acceptance.
Load:
- Game Asset Contract
- Polycount/LOD/Collision
- Pivots/Transforms
- Texture/Material Runtime
- Bake Gate
- Bake Execution and Channel Semantics
- UV Atlas/LOD Stability Contract
- Bake Output Validation
- Incremental Dirty-Stage Cache
- Long-Running Job Protocol for expensive passes
- Emissive Runtime Handoff if applicable
- active Engine Profile
- active Project Asset Pipeline Profile
- Runtime Module Packaging Contract
- glTF/export module
- Final Validation
- `MESH_VALIDATE`
- Completion Levels
- Completeness Report

Preferred skills:
- `UV_ATLAS_CONTRACT`;
- `BAKE_RUNTIME_TEXTURES`;
- `BAKE_VALIDATE`;
- `RUNTIME_PACKAGE_VALIDATE`;
- `ASSET_COMPLETION`.

Before claiming Level C route final status through `ASSET_COMPLETION`.
The final surface check must use the baked runtime material on a runtime LOD mesh, not only the procedural authoring shader.

## Runtime module packaging / export readback
Route to `RUNTIME_PACKAGE_VALIDATE` and/or `EXPORT_VALIDATE`.
Load:
- `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`
- active Engine Profile
- active Project Asset Pipeline Profile
- glTF Export
- Export Validation Snippets

Persist project facts such as:
- one-file multi-node vs separate LOD files;
- node suffix pattern;
- collision packaging;
- handedness/mirror compensation;
- material/image URI expectations.

Do not inspect long sibling exporter scripts again if the active project profile already contains these verified facts.

## Python module/helper reused by another stage
Load:
- Code Artifact and Patch Protocol
- `08_scripts/94_IMPORT_SAFE_PYTHON_MODULE_PATTERN.md`

Reusable modules must be import-safe and scratch collections must have explicit ownership.
Do not let helper import/exec trigger production export/bake as a top-level side effect.

## Project/asset catalog integration
Use Task Pack `PIPELINE_INTEGRATION` only when target is Level D.
Load:
- Asset Catalog Integration Protocol
- Engine Adapter Protocol
- Project Asset Pipeline Profile
- Authoring to Runtime Handoff
- Completeness Report

Route catalog work to `ASSET_CATALOG_INTEGRATE`.
If catalog write capability is missing, Level D is BLOCKED rather than silently skipped.

## Asset modularny
Dodatkowo:
- Modularity/Instancing
- Modular Architecture Example

## Animowany asset
Dodatkowo:
- Animation and Rigging

## Reviewer
Load:
- Feature Contract
- Visual QA
- Final Validation
- Completion Levels
- Completeness Report
- Reviewer Prompt

## Token budget rule

Jeżeli agent potrzebuje jednej informacji, nie ładuj całego folderu.
Najpierw Task Pack, potem router, potem najwęższy moduł.

Zawsze stosuj Tool Call and Token Efficiency:
- obliczaj lokalnie;
- agreguj;
- nie wysyłaj raw arrays/profiles bez diagnostic need;
- nie echoj pełnych wygenerowanych skryptów/patchy, jeśli kod jest już artefaktem na dysku.

Dla kodu używaj Code Artifact and Patch Protocol.
Dla bake/export używaj dirty-stage cache, aby poprawka jednego kanału nie uruchamiała sześciu zaakceptowanych etapów.

## Retry budget rule

Po pierwszej porażce agent diagnozuje i może wykonać tylko jedną poprawioną próbę tej samej strategii.
Po drugiej porażce: re-inspection + strategy switch/blocker.

Dla operacji długotrwałych timeout nie liczy się jako udowodniona porażka. Najpierw sprawdź job/artifact state.

## Trim-sheet UV texturing
Load:
- Semantic Skill Registry
- Trim Sheets
- UV/Texel Density/Materials
- Texture/Material Runtime
- Texture Packing and Mip Safety

If unique local graphics exist, additionally load Decals and Floating Details.

## Procedural / repeated asset
Load:
- Geometry Nodes Authoring
- Curves for Assets, jeśli dotyczy
- Modularity/Instancing
- Asset Variants and Randomization
- Draw Calls/Instancing/Batching

## Reference reconstruction
Load first:
- Semantic Skill Registry
- Task Pack Protocol
- Reconstruction Controller

Then load only the modules required by current/failing stage.
Do not load detail/modeling skills before camera, scale, silhouette and primary-form gates pass.

## Technical concept sheet / blueprint ANALYZE
Use Task Pack `RECON_TECHNICAL_SHEET_ANALYZE`.

Required core:
- Evidence Model
- Reference Ingestion
- View Authority Matrix
- Reference Measurement Protocol
- Blueprint/Technical Drawing Mode
- Reference Analysis Cache
- Reference Measurement Executor Pattern
- Concept Sheet Ingest Prompt

Route measurement to `REFERENCE_MEASURE`.
After segmentation/calibration pass, reuse cached ROI/authority/dimensions and do not rescan the full sheet.

## Runtime integration
Load:
- Agent Tool API Profile
- Blender 5.1 Compatibility Matrix
- Game Asset Contract
- Engine Profile Schema
- Engine Adapter Protocol
- Project Asset Pipeline Profile Schema
- Runtime Module Packaging Contract
- Asset Catalog Integration Protocol when Level D is required
- Authoring to Runtime Handoff
- właściwy format eksportu

## Full 1:1 reconstruction

Load core:
- Semantic Skill Registry
- Task Pack Protocol
- Reconstruction Controller
- Definition of 1:1
- Reconstruction State Machine
- Reconstruction Knowledge Routing
- Completion Levels

Then load only current Task Pack/stage pack.

### Concept sheet ingest
- 102–109
- 160
- 168
- 170
- script 91
- prompt 67

### Geometry solve
- 110–123
- 128–134
- appropriate playbooks
- `AXISYMMETRIC_PROFILE` when primary form is rotationally symmetric
- `RADIAL_REPEAT` for circular repeated details

### Rear/bottom
- 119
- 135
- playbook 113

### Surface
- 124–127
- 140
- material playbook 114 where applicable
- integrated light playbook 115 where applicable

### Reconstruction QA
- 141–148
- scripts 81, 83, 86–90, 92
- prompt 65

### Benchmarks
- `07_examples/73_LAFAR_STREET_BENCH_RECONSTRUCTION_BENCHMARK.md`
- `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`
- `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`

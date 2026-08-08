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
- `02_blender_api/23_SCENE_INSPECTION.md`

Before production mutation, bind the current connected tools to the semantic capabilities required by the selected skill.
Do not assume that knowledge about Blender implies that the current integration can execute it.

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
- Build Plan
- Execution Protocol
- Code Artifact and Patch Protocol when generating non-trivial Python
- Retry Budget and Strategy Switching
- Visual QA

Do not preload UV/material/LOD/export modules before their state is reached.

## Axisymmetric / rotational hard-surface asset

Typical triggers:
- bollard/post;
- round base/collar/cap;
- cylindrical housing;
- stacked radial profile where most primary geometry shares one axis.

Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`
- `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`
- Game Asset Contract
- Feature Contract

Route rotational master geometry to `AXISYMMETRIC_PROFILE` before writing another local `lathe()`/profile-revolve helper.

Keep asymmetric service panels, decals, local emitters and similar features as separate feature owners.

## Poprawka istniejącego assetu
Load:
- Agent Charter
- Semantic Skill Registry
- Feature Contract
- Scene Inspection
- API Strategy
- Idempotency/Recovery
- Code Artifact and Patch Protocol if a build/QA script is being patched
- Retry Budget and Strategy Switching
- Visual QA
- Failure Recovery
- Repair Prompt

## Problem z Blender API
Load:
- API Strategy
- Tool Discovery and Registry
- Agent Tool API Profile
- bpy.data vs bpy.ops vs BMesh
- Context/Mode/Selection
- Scene Inspection
- Tool Call Efficiency
- Retry Budget and Strategy Switching

## Procedural panel line / narrow groove
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `blender-agent-procedural-hard-surface-panel-lines.md`
- `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`
- `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`

If the host surface is SubD-controlled or pinching/topology flow becomes relevant, additionally load:
- `blender-agent-subdivision-topology-control.md`

Do not route wide/deep recesses or silhouette-changing features to `HS_PANEL_LINE`.

## Subdivision topology problem
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `blender-agent-subdivision-topology-control.md`
- `03_modeling/33_TOPOLOGY_NORMALS_SHADING.md`
- `02_blender_api/21_BPY_DATA_OPS_BMESH.md`
- `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`

Typical triggers:
- support loops bunching around corners;
- curved-surface pinching;
- local density that should terminate;
- cylindrical recess/protrusion on curved SubD surface;
- branch junction cleanup;
- pole-safe sphere requirement.

## Mesh / topology validation

Route to semantic skill `MESH_VALIDATE`.

Load:
- `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`
- `08_scripts/81_MESH_VALIDATION_SNIPPETS.md`
- active Game Asset Contract

Every mesh must declare topology intent before general PASS/FAIL:
- CLOSED_SOLID;
- OPEN_ASSEMBLY_PART;
- SURFACE_DETAIL;
- COLLISION.

Do not treat boundary edges as harmless unless the object's contract explicitly allows them.

## Optymalizacja do gry
Load Task Pack `GAME_READY`:
- Game Asset Contract
- Polycount/LOD/Collision
- Pivots/Transforms
- Texture/Material Runtime
- active Engine Profile
- active Project Asset Pipeline Profile
- glTF Export
- Final Validation
- `MESH_VALIDATE`

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
- Reviewer Prompt

## Token budget rule

Jeżeli agent potrzebuje jednej informacji, nie ładuj całego folderu.
Najpierw użyj Task Pack, potem routera, potem najwęższego modułu.

Zawsze stosuj `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`:
- obliczaj lokalnie;
- agreguj;
- nie wysyłaj raw arrays/profiles do LLM bez konkretnego diagnostic need;
- nie echoj pełnych wygenerowanych skryptów/patchy, jeśli kod jest już artefaktem na dysku.

Dla kodu używaj `05_execution/62_CODE_ARTIFACT_AND_PATCH_PROTOCOL.md`.

## Retry budget rule

Po pierwszej porażce agent diagnozuje i może wykonać tylko jedną poprawioną próbę tej samej strategii.
Po drugiej porażce tej samej strategii musi załadować `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md`, przeprowadzić re-inspection i zmienić strategię albo zatrzymać zadanie jako blocker.

## High -> low + bake
Load:
- High-Poly / Low-Poly Workflow
- Baking Pipeline
- UV/Texel Density/Materials
- Texture Packing and Mip Safety
- Automated Visual Diff
- Authoring to Runtime Handoff

## Trim-sheet UV texturing
Load:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `03_modeling/40_TRIM_SHEETS.md`
- `03_modeling/34_UV_TEXEL_DENSITY_MATERIALS.md`
- `04_game_ready/43_TEXTURE_MATERIAL_RUNTIME.md`
- `04_game_ready/47_TEXTURE_PACKING_AND_MIP_SAFETY.md`

If unique local graphics are present, additionally load:
- `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md`

If runtime material/draw-call cost is part of the task, additionally load:
- `04_game_ready/46_DRAW_CALLS_INSTANCING_AND_BATCHING.md`
- the active Engine Profile.

## Procedural / repeated asset
Load:
- Geometry Nodes Authoring
- Curves for Assets, jeśli dotyczy
- Modularity/Instancing
- Asset Variants and Randomization
- Draw Calls/Instancing/Batching

## Reference reconstruction
Load first:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `00_governance/06_TASK_PACK_PROTOCOL.md`
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`

Then load only the modules required by the current/failing reconstruction stage.

Do not load detail/modeling skills before the controller has passed camera, scale, silhouette and primary-form gates.

When a validated detail feature is reached, route it through the Semantic Skill Registry rather than improvising a modeling technique.

## Technical concept sheet / blueprint ANALYZE

Use Task Pack `RECON_TECHNICAL_SHEET_ANALYZE`.

Required core:
- `10_reconstruction/102_EVIDENCE_MODEL.md`
- `10_reconstruction/103_REFERENCE_INGESTION_PROTOCOL.md`
- `10_reconstruction/106_VIEW_AUTHORITY_MATRIX.md`
- `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md`
- `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`
- `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`
- `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`
- `06_prompts/67_CONCEPT_SHEET_INGEST_PROMPT.md`

Route technical image measurement to semantic skill `REFERENCE_MEASURE`.

After segmentation and calibration are validated:
- reuse cached ROI/view authority/dimensions;
- do not rescan the full sheet;
- re-enter analysis only for a specific failing ROI, metric, feature or source update.

Do not read unrelated sibling build scripts for project conventions if an active `PROJECT_ASSET_PIPELINE_PROFILE.md` is available.
If no profile exists, inspect the smallest relevant range and persist the discovered convention according to `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md`.

## Runtime integration
Load:
- Agent Tool API Profile
- Game Asset Contract
- Engine Profile Schema
- Engine Adapter Protocol
- Project Asset Pipeline Profile Schema
- Authoring to Runtime Handoff
- właściwy format eksportu

## Full 1:1 reconstruction

Load core:
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `00_governance/06_TASK_PACK_PROTOCOL.md`
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`
- `10_reconstruction/101_DEFINITION_OF_1_TO_1.md`
- `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`
- `10_reconstruction/155_RECONSTRUCTION_KNOWLEDGE_ROUTING.md`

Then load only the current Task Pack/stage pack.

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
- appropriate `11_playbooks`
- `AXISYMMETRIC_PROFILE` when the primary form is rotationally symmetric

### Rear/bottom
- 119
- 135
- playbook 113

### Surface
- 124–127
- 140
- appropriate material playbook

### Reconstruction QA
- 141–148
- scripts 81, 83, 86–90, 92
- prompt 65

### Lafar bench benchmark
- example 73
- playbooks 110, 111, 112, 113, 114, 115, 116, 117

# Knowledge Router

Agent nie powinien ładować całej biblioteki do każdego zadania.

## Nowy asset hard-surface
Load:
- Agent Charter
- State Machine
- Asset Brief Schema
- Reference Decomposition
- Feature Contract
- Modeling Decision Tree
- Hard Surface Workflow
- Game Asset Contract
- Build Plan
- Execution Protocol
- Visual QA

## Poprawka istniejącego assetu
Load:
- Agent Charter
- Feature Contract
- Scene Inspection
- API Strategy
- Idempotency/Recovery
- Visual QA
- Failure Recovery
- Repair Prompt

## Problem z Blender API
Load:
- API Strategy
- bpy.data vs bpy.ops vs BMesh
- Context/Mode/Selection
- Scene Inspection
- Tool Call Efficiency

## Optymalizacja do gry
Load:
- Game Asset Contract
- Polycount/LOD/Collision
- Pivots/Transforms
- Texture/Material Runtime
- glTF Export
- Final Validation

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
Najpierw użyj routera, potem najwęższego modułu.

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
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`

Then load only the modules required by the failing or current reconstruction stage:
- Reference Decomposition
- Reference Measurement Protocol
- Camera and Reference Matching
- Visual Feature Map
- Reference Fidelity Protocol
- Automated Visual Diff

Do not load detail/modeling skills before the controller has passed camera, scale, silhouette and primary-form gates.

## Runtime integration
Load:
- Game Asset Contract
- Engine Profile Schema
- Engine Adapter Protocol
- Authoring to Runtime Handoff
- właściwy format eksportu

## Full 1:1 reconstruction

Load core:
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`
- `10_reconstruction/101_DEFINITION_OF_1_TO_1.md`
- `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`
- `10_reconstruction/155_RECONSTRUCTION_KNOWLEDGE_ROUTING.md`

Then load only the current stage pack.

### Concept sheet ingest
- 102–109
- 168
- prompt 67

### Geometry solve
- 110–123
- 128–134
- appropriate `11_playbooks`

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
- scripts 86–90
- prompt 65

### Lafar bench benchmark
- example 73
- playbooks 110, 111, 112, 113, 114, 115, 116, 117

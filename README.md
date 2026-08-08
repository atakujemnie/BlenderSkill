# BlenderSkill

Canonical knowledge repository for the Blender AI Agent Library.

## Purpose

The repository contains modular Markdown skills for an AI agent that plans, builds, reconstructs, validates and prepares Blender assets for game/VFX pipelines.

The canonical source is the modular library stored in the numbered directories. `_FULL_LIBRARY.md` is generated automatically from the modules listed in `MANIFEST.json` and should not be edited manually.

## Main areas

- `00_governance` — agent rules, routing and state machines
- `01_analysis` — briefs, references, features and measurements
- `02_blender_api` — `bpy`, BMesh, context and automation strategy
- `03_modeling` — hard-surface, topology, UV, trim sheets and authoring workflows
- `04_game_ready` — runtime optimization, materials, LOD, export constraints
- `05_execution` — execution, validation, QA, regression and repair
- `06_prompts` — planner/reviewer/repair prompts
- `07_examples` — examples and benchmarks
- `08_scripts` — reusable audit/validation patterns
- `09_engine` — engine profile and adapter contracts
- `10_reconstruction` — evidence-driven 1:1 reconstruction system
- `11_playbooks` — asset-class production playbooks
- `99_sources` — technical sources

## Repository rules

1. Prefer updating an existing canonical module over creating a parallel skill with duplicated responsibility.
2. Add a new skill only when it introduces a distinct responsibility or reusable primitive.
3. Keep semantic intent separate from temporary Blender indices, UI state and one-off operator sequences.
4. Validate changes against existing modules before merging them into the library.
5. `MANIFEST.json` defines the modules compiled into `_FULL_LIBRARY.md`.
6. GitHub Actions regenerates `_FULL_LIBRARY.md` after canonical Markdown changes.

## Current target

- Blender 5.1.x
- Python automation through Blender API/BMesh where practical
- reconstruction-first and game-asset production workflows
- glTF/GLB as a neutral runtime baseline unless an engine profile overrides it

# Changelog

## Unreleased

No canonical changes after the v0.5.0 release baseline yet.

## 0.5.0

v0.5.0 is the first benchmark-driven **agent execution + completion** release. It incorporates lessons from the real Lafar Civic Bollard run (~60k-token baseline, final human visual assessment 9/10) and converts them into routing, reusable executors, runtime gates and truthful completion states.

### Completion and runtime closure
- added `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md` with explicit levels: `RECONSTRUCTION_COMPLETE`, `MODELING_COMPLETE`, `GAME_READY_COMPLETE`, `PIPELINE_INTEGRATED`;
- added `05_execution/63_REFERENCE_TO_RUNTIME_COMPLETENESS_REPORT.md` so exported-but-unbaked/unintegrated assets cannot be reported as unconditionally DONE;
- expanded Game Asset Contract and Final Validation with completion target, bake/runtime material state, emissive state and catalog integration;
- clarified `10_reconstruction/159_RECONSTRUCTION_DEFINITION_OF_DONE.md` as reconstruction acceptance rather than full game-asset completion.

### Blender 5.1 compatibility
- added `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md` based on observed runtime traps;
- added `executors/runtime_compat.py` for render-engine/property/path discovery;
- captured unsaved `.blend` path risk, viewport-vs-render visibility, import-time builder side effects and mutable default capture;
- updated API strategy and session preflight to discover version-sensitive behavior instead of guessing it.

### Execution acceleration
- retained/registered candidate executors for reference measurement, axisymmetric profile generation and mesh validation;
- added `executors/radial_repeat.py` for radial fastener placement and annulus containment;
- added `executors/qa_scene_isolation.py` for non-destructive render isolation;
- added `executors/completion_gate.py` for machine-readable completion evaluation;
- expanded Semantic Skill Registry with `RADIAL_REPEAT`, `RUNTIME_COMPAT`, `QA_SCENE_ISOLATE`, `MATERIAL_FINISH_CIVIC`, `EMISSIVE_HANDOFF`, `BAKE_RUNTIME_TEXTURES`, `ASSET_COMPLETION`, `ASSET_CATALOG_INTEGRATE`;
- candidate executors remain `CONTRACT_READY` until individually benchmarked in the active runtime.

### Surface and material finish
- substantially expanded `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md` with macro/meso/micro breakup, channel separation, restrained civic wear and exposure/manufacturing logic;
- material target is maintained/used/not-sterile, not generic global grunge;
- expanded civic hard-surface playbook with structural subtype routing and dedicated axisymmetric fast path.

### Emissive/runtime separation
- added `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md`;
- expanded Integrated Light Strip playbook;
- separated emitter geometry/mask/color/export from engine bloom/exposure/tone mapping;
- final runtime neon/glow may remain `UNVERIFIED` even when Blender emitter authoring passes.

### Bake gate
- added `04_game_ready/50_GAME_READY_BAKE_GATE.md`;
- corrected the assumption that every bake requires a separate high-poly mesh;
- procedural-to-texture bake can use authoring geometry, while high-to-low detail transfer requires an appropriate high-detail source;
- Level C cannot pass while Blender-only procedural effects have no runtime disposition.

### Floating detail and decal hardening
- expanded `03_modeling/41_DECALS_AND_FLOATING_DETAILS.md` with the explicit rule that floating geometry adds surfaces but cannot cut negative depth from the host;
- visible floating panels/emitters require visibility/occlusion proof;
- authoritative logo/branding sources must be used when supplied instead of guessed geometry/font approximations;
- LOD/export rebuilds must not delete decal owners through import-time side effects.

### Pipeline integration
- added `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` for stable asset IDs, conflict classification, registration readback and importer smoke tests;
- Level D is BLOCKED when project catalog write capability is missing rather than silently downgraded.

### Task packs and routing
- expanded Task Pack Protocol with `SURFACE_FINISH`, `GAME_READY_FINISH` and `PIPELINE_INTEGRATION`;
- Knowledge Router now routes compatibility, radial repetition, civic material finish, emissive handoff, bake closure and final completion explicitly;
- System Prompt now requires target completion level and truthful end-state reporting.

### Benchmarking
- added `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md` as the first real end-to-end B7 benchmark;
- baseline: ~60k tokens, final geometry 210×210×1050 mm, LOD0/1/2/3 = 2716/1152/480/128 tris, collision = 88 tris;
- records real detected failures: loose/duplicate geometry, dimension overshoot, fastener annulus overflow, hidden emitter, destructive builder import, material exposure issue;
- target for equivalent v0.5 run: no quality regression and at least 35% token reduction, preferred <=35k total;
- expanded Agent Evaluation Harness with B7 end-to-end completion and efficiency metrics.

### Previous v0.5 development passes folded into release
- production-grade Trim Sheet semantic skill integration;
- reconstruction controller integration without duplicate parallel skills;
- Semantic Skill Registry and Agent Tool API Profile;
- Retry Budget and Strategy Switch;
- Tool Output Budget and Task Packs;
- Reference Analysis Cache and measurement executor pattern;
- Project Asset Pipeline Profile schema;
- Code Artifact and Patch Protocol;
- `AXISYMMETRIC_PROFILE` semantic primitive;
- `MESH_VALIDATE` topology-intent-aware validation;
- canonical panel-line and SubD topology skills.

Canonical module count: **182**.

## 0.3.0

Added full Reconstruction Layer:
- 70 reconstruction modules/playbooks/scripts/prompts/benchmark elements,
- evidence/provenance model,
- concept-sheet segmentation,
- authority/conflict system,
- dimension graph and locks,
- landmark and calibration system,
- geometry inference rules,
- exact feature/material/branding handling,
- parametric reconstruction workflow,
- multi-view QA and regression gates,
- specialized modes for blueprint/photo/stylized references,
- Lafar Street Bench reconstruction benchmark.

## 0.2.0

Added production layer:
- camera/reference matching,
- Visual Feature Map,
- high/low-poly workflow,
- baking pipeline,
- trim sheets,
- decals/floating details,
- curve authoring,
- Geometry Nodes authoring,
- procedural material authoring,
- texture packing/mip safety,
- asset variants/randomization,
- automated visual diff,
- reference fidelity levels,
- authoring-to-runtime handoff,
- engine profile schema,
- engine adapter protocol,
- deterministic QA render pattern,
- visual diff script pattern.

Architecture decision:
- modular MD files are canonical,
- `_FULL_LIBRARY.md` is generated from them.

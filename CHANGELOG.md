# Changelog

## Unreleased

Integrated two reviewed production skills without creating redundant parallel modules:
- expanded `03_modeling/40_TRIM_SHEETS.md` into a full semantic trim-sheet UV texturing skill;
- integrated the reference-image proportion/silhouette workflow into `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` as the high-level reconstruction controller;
- added explicit trim-sheet routing and controller-first reference routing to the Knowledge Router.

Important integration corrections:
- texel density is now unit-explicit (`px_per_m`) instead of a bare numeric value;
- intentional trim-sheet UV reuse is distinguished from accidental overlap;
- trim-sheet reuse is not treated as an automatic draw-call reduction;
- persistent surface identity should not rely only on transient polygon indices;
- reconstruction confidence vocabulary is aligned with the existing `LOCKED/HIGH/MEDIUM/LOW/UNKNOWN` ledger;
- image-space quality thresholds are defined as overridable heuristics, not universal hard limits.

Agent-runtime readiness pass:
- added `00_governance/05_SEMANTIC_SKILL_REGISTRY.md` as the stable intent -> skill -> capability -> validation routing layer;
- added `02_blender_api/28_AGENT_TOOL_API_PROFILE.md` with required runtime capabilities, discovery/binding states and preflight rules;
- added `05_execution/61_RETRY_BUDGET_AND_STRATEGY_SWITCH.md` to stop blind repeated API/tool attempts;
- registered `HS_PANEL_LINE` and `SUBD_TOPOLOGY_CONTROL` as canonical skills;
- added the existing panel-line and SubD skill files to `MANIFEST.json`, so they are now included in `_FULL_LIBRARY.md`;
- expanded the Knowledge Router with session preflight, panel-line routing, SubD routing and retry-budget loading;
- updated the system prompt to require capability binding, semantic skill selection and a strategy switch after repeated failure;
- canonical module count increased from 163 to 168.

Reference-analysis efficiency pass based on the first real technical-sheet reconstruction test:
- added `00_governance/06_TASK_PACK_PROTOCOL.md` to bound active knowledge by state/task subtype and prevent loading later-stage modules too early;
- expanded `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md` with a strict Tool Output Budget and `SUMMARY -> DIAGNOSTIC -> RAW` progressive disclosure policy;
- added `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md` and registered semantic skill `REFERENCE_MEASURE` for local pixel/NumPy measurement with compact aggregate outputs;
- added `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md` so validated view ROIs, dimensions, calibration and authority decisions are reused instead of repeatedly rediscovered;
- added `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md` to separate project naming/material/decal/path conventions from sibling asset geometry scripts;
- updated technical-sheet authority to `explicit numeric dimensions/datum > orthographic views > sections > details > perspective hero > approximate prose > visual inference`;
- updated ingest and measurement protocols to reject raw pixel/profile dumps during normal operation and localize diagnostics to failing ROIs;
- updated system prompt and Knowledge Router to require task packs, cache reuse and output aggregation;
- canonical module count increased from 168 to 172.

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

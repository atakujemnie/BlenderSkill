# Task Pack Protocol

## Purpose

A Blender agent must not load every relevant document for the whole asset lifecycle at once.

A `Task Pack` is the smallest bounded set of knowledge required for the current state and task subtype.

The goal is to reduce context growth, repeated document reads and cross-stage interference while preserving required constraints.

## Core rule

```text
current state + task subtype
-> one Task Pack
-> only required modules
-> execute / validate
-> discard non-persistent context
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

`context_budget_tokens` is a planning ceiling, not a guarantee from the runtime. If the pack approaches the ceiling, summarize persistent state and unload non-required material before loading more documents.

## Canonical packs

### `SESSION_PREFLIGHT`

Use once before the first production scene mutation.

Required:
- `00_governance/00_AGENT_CHARTER.md`
- `00_governance/05_SEMANTIC_SKILL_REGISTRY.md`
- `02_blender_api/19_TOOL_DISCOVERY_AND_REGISTRY.md`
- `02_blender_api/25_TOOL_CALL_AND_TOKEN_EFFICIENCY.md`
- `02_blender_api/28_AGENT_TOOL_API_PROFILE.md`

Persistent output:
- Tool Registry;
- capability bindings;
- Blender/runtime version facts.

### `RECON_TECHNICAL_SHEET_ANALYZE`

Required:
- `00_governance/00_AGENT_CHARTER.md`
- `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md`
- `10_reconstruction/102_EVIDENCE_MODEL.md`
- `10_reconstruction/103_REFERENCE_INGESTION_PROTOCOL.md`
- `10_reconstruction/106_VIEW_AUTHORITY_MATRIX.md`
- `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md`
- `10_reconstruction/160_BLUEPRINT_AND_TECHNICAL_DRAWING_MODE.md`
- `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`
- `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`

Persistent output:
- Reference Registry;
- Analysis Cache;
- Evidence Summary;
- locked dimensions;
- View Authority Matrix;
- unresolved conflicts.

Forbidden until later unless directly needed to resolve an ANALYZE blocker:
- UV authoring;
- materials/shaders;
- LOD generation;
- collision;
- export;
- microdetail modeling;
- decorative detailing skills.

### `RECON_BLOCKOUT`

Required:
- reconstruction controller;
- Dimension Graph;
- dimension locks/tolerances;
- landmark system;
- silhouette constraints;
- object decomposition;
- dimension-locked blockout;
- Build Plan;
- Execution Protocol.

Do not load material/UV/LOD modules.

### `RECON_DETAIL`

Load only after camera/scale/silhouette/primary-form gates pass.

Required:
- current Feature Contract subset;
- feature-to-modeling strategy map;
- only semantic skills required by current feature IDs;
- checkpoint/visual QA.

Example: load `HS_PANEL_LINE` only when the current accepted feature is actually a narrow seam/path.

### `GAME_READY`

Load only after geometry/reconstruction acceptance.

Required:
- Game Asset Contract;
- polycount/LOD/collision;
- transforms/pivots/naming;
- texture/material runtime;
- active Engine Profile;
- active Project Asset Pipeline Profile;
- export/final validation as needed.

## Persistent-state rule

Task Pack changes must not discard facts that have already been validated.

Persist compact structured records, not full conversational history:

```text
Tool Registry
Reference Registry
Reference Analysis Cache
Evidence Ledger
Dimension Graph
View Authority Matrix
Feature Contract
Build Plan
Checkpoint results
```

## No duplicate loading

If a module was already loaded and its relevant rules are represented in persistent structured state, do not re-read it merely because the next step mentions the same concept.

Re-read only when:
- a conflict requires exact source wording;
- the task enters a section not represented in persistent state;
- the module changed during the session;
- an explicit validator requests it.

## Pack expansion rule

Do not load a new module because it might become useful.

Expand the Task Pack only when:
1. the current state requires it;
2. a measured failure routes to it;
3. a current feature maps to it in the Semantic Skill Registry.

## Completion gate

Before advancing from ANALYZE to CONTRACT/PLAN, emit a compact `Evidence Summary` containing at minimum:

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

Once `ANALYZE: PASS`, do not continue broad reference exploration. Later investigation must be scoped to a specific unresolved item, feature ID or failed ROI validator.

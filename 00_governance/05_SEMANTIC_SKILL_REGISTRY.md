# Semantic Skill Registry

## Purpose

This registry is the stable routing layer between user intent, knowledge modules, executable primitives, Blender capabilities and validation.

The agent must not jump directly from a natural-language request to ad-hoc `bpy`, shell or project code when a registered semantic skill already covers the operation.

## Execution maturity

Every semantic skill has one maturity state:

- `KNOWLEDGE_ONLY` — guidance exists, but no stable execution contract.
- `CONTRACT_READY` — stable semantic inputs/outputs, validation and fallback rules exist.
- `EXECUTOR_READY` — a tested implementation is callable through a stable API.
- `RUNTIME_BOUND` — executor is mapped to the tools available in the current agent/runtime integration.

Never claim a skill is `EXECUTOR_READY` or `RUNTIME_BOUND` without evidence.

## Canonical registry

| Skill ID | Purpose | Canonical knowledge | Current maturity | Required capabilities | Validation |
|---|---|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | camera/scale/silhouette/proportion-first reconstruction | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` + stage modules | CONTRACT_READY | scene inspect, image/reference access, camera/render | multi-view, silhouette, landmarks, dimensions |
| `REFERENCE_MEASURE` | compact technical-sheet/reference measurement and cross-view aggregation | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md` + `01_analysis/14_REFERENCE_MEASUREMENT_PROTOCOL.md`; `executors/reference_measure.py` | CONTRACT_READY | reference image access, Python/NumPy or equivalent image analysis | provenance, calibration, confidence, cross-view deviation, output budget |
| `AXISYMMETRIC_PROFILE` | deterministic profile-revolved geometry for rotationally symmetric hard-surface parts | `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`; `executors/axisymmetric_profile.py` | CONTRACT_READY | Python, BMesh | radius/axis bounds, continuity, topology intent, UV, triangle budget |
| `RADIAL_REPEAT` | repeated anchors/fasteners around a known axis | `11_playbooks/110_HARD_SURFACE_CIVIC_FURNITURE.md`; `executors/radial_repeat.py` | CONTRACT_READY | Python; geometry mutation by caller | count, phase, annulus containment, triangle estimate |
| `HS_PANEL_LINE` | narrow hard-surface seam/groove | `blender-agent-procedural-hard-surface-panel-lines.md` | CONTRACT_READY | Python, BMesh, modifiers, evaluated mesh | path continuity, topology, profile, modifier order |
| `SUBD_TOPOLOGY_CONTROL` | SubD cage design and topology repair | `blender-agent-subdivision-topology-control.md` | CONTRACT_READY | Python/BMesh, Subdivision evaluation | evaluated surface, pinching, density, continuity |
| `TRIM_SHEET_UV` | trim-sheet classification and deterministic UV assignment | `03_modeling/40_TRIM_SHEETS.md` | CONTRACT_READY | mesh UV access, materials | region bounds, density, orientation, intentional overlap |
| `UV_ATLAS_CONTRACT` | stable semantic atlas ownership across bake source and LODs | `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`; `executors/uv_atlas_contract.py` | CONTRACT_READY | mesh UV access, semantic part registry | part IDs, rect ownership, LOD consistency, missing assignments |
| `MESH_VALIDATE` | contract-aware mesh/topology audit with compact output | `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`; `executors/mesh_validate.py` | EXECUTOR_READY | scene inspect, Python/BMesh | topology intent, boundaries, non-manifold, duplicates, loose/zero-area geometry, UV, tris |
| `RUNTIME_COMPAT` | discover Blender/runtime API facts before version-sensitive code | `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`; `executors/runtime_compat.py` | CONTRACT_READY | Python/RNA | enums/properties/paths discovered, no guessed API |
| `QA_SCENE_ISOLATE` | non-destructive QA/bake scene isolation | `08_scripts/83_QA_RENDER_SCRIPT_PATTERN.md`; `executors/qa_scene_isolation.py` | CONTRACT_READY | scene access | render state restored, unrelated objects not deleted |
| `MATERIAL_FINISH_CIVIC` | non-sterile maintained civic material breakup | `11_playbooks/114_BRUSHED_METAL_AND_DARK_COMPOSITE.md` | CONTRACT_READY | material authoring, texture/bake access | macro/meso/micro breakup, material identity, runtime disposition |
| `EMISSIVE_HANDOFF` | separate emitter authoring from engine glow/bloom | `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md` + playbook 115 | CONTRACT_READY | material/export; engine profile for runtime proof | emitter visibility, exported emissive, runtime status |
| `BAKE_RUNTIME_TEXTURES` | deterministic closure of Blender material state into runtime textures | `04_game_ready/50_GAME_READY_BAKE_GATE.md` + `04_game_ready/51_BAKE_EXECUTION_AND_CHANNEL_SEMANTICS.md`; `executors/bake_runtime_textures.py` | CONTRACT_READY | UV, material nodes, Cycles bake, image write | operator result, target binding, channel semantics, dirty-stage cache |
| `BAKE_VALIDATE` | semantic validation of baked maps/regions | `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`; `executors/bake_validate.py` | CONTRACT_READY | image access, NumPy or equivalent | degeneracy, ranges, material regions, emissive containment, clipping |
| `IMAGE_CACHE_COHERENCE` | synchronize accepted external texture artifacts with Blender image datablocks | `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`; `executors/image_cache_coherence.py` | CONTRACT_READY | Blender image/data API, external file access | canonical path, reload/load action, dimensions, colorspace, binding |
| `PIPELINE_DAG_PLAN` | compute minimal dirty execution closure and reuse accepted stages | `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`; `executors/pipeline_dag.py` | CONTRACT_READY | Python | acyclic graph, execute/reuse closure, invalidation reasons |
| `RUNTIME_PACKAGE_VALIDATE` | validate exported module nodes/materials/images against packaging profile | `09_engine/94_RUNTIME_MODULE_PACKAGING_CONTRACT.md`; `executors/gltf_package_validate.py` | CONTRACT_READY | exported-file read | LOD nodes, materials, image URIs, project packaging contract |
| `EXPORT_ROUNDTRIP_VALIDATE` | re-import exported asset and re-check hard invariants | `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`; `executors/export_roundtrip_validate.py` | CONTRACT_READY | Blender import/scratch context, mesh bounds | dimensions, ground datum, LOD family, runtime material availability |
| `RUNTIME_PATH_RESOLVE` | resolve engine-visible runtime asset root from project authority | `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`; `executors/runtime_path_resolver.py` | CONTRACT_READY | filesystem/project profile/build facts | canonical root, containment, forbidden lookalike roots |
| `TEST_ORACLE` | trustworthy process exit status and regression bite-test proof | `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`; `executors/test_oracle.py` | CONTRACT_READY | subprocess/shell/test runner | direct exit code, expected failing marker, restored green run |
| `ENGINE_INTEGRATION_PROOF` | prove Level D with target engine loader/instantiation | `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md` | CONTRACT_READY | project build/test/engine loader | engine-visible path, loader success, asset invariants, trustworthy test oracle |
| `QA_REFERENCE` | visual/numeric reconstruction QA | `10_reconstruction/141_RECONSTRUCTION_QA_CAMERA_RIG.md` through `148_ACCEPTANCE_THRESHOLDS_AND_ERROR_BUDGETS.md` | CONTRACT_READY | camera/render/screenshot, geometry metrics | stage-specific gates |
| `ASSET_COMPLETION` | determine true completion level and blockers | `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`; `executors/completion_gate.py` | CONTRACT_READY | compact validation state | Reconstruction/Modeling/Game-ready/Pipeline gates + Level D evidence kind |
| `ASSET_CATALOG_INTEGRATE` | register a game-ready asset in a project catalog/registry | `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` | KNOWLEDGE_ONLY | project catalog read/write | readback, unique ID, file associations, import smoke test |
| `EXPORT_VALIDATE` | export and post-export checks | `04_game_ready/45_GLTF_EXPORT.md`, `05_execution/53_FINAL_VALIDATION.md`, engine profile | KNOWLEDGE_ONLY | save/export/file inspect | runtime contract |

## Runtime evidence

### `MESH_VALIDATE` is `EXECUTOR_READY`

The Lafar Civic Bollard production benchmark imported `executors/mesh_validate.py` in Blender 5.1.

Observed evidence:
- invalid custom topology intent vocabulary was rejected;
- corrected canonical intents were accepted;
- nine asset parts were checked;
- duplicate/loose/zero-area/topology metrics were returned;
- collection status passed after contract correction.

This is sufficient for `EXECUTOR_READY` library status.

It is **not automatically `RUNTIME_BOUND`** in every future session. The current integration must still prove it can import/invoke the executor.

### Completion gate runtime evidence

The final Bollard continuation exercised `executors/completion_gate.py` twice:
- it correctly blocked `PIPELINE_INTEGRATED` while runtime import remained `UNVERIFIED`;
- it passed after the target engine loader regression test was green.

v0.7 additionally hardens the executor so `runtime_import_or_instantiation` must carry an engine evidence kind:

```text
ENGINE_PRODUCTION_LOADER
ENGINE_REGRESSION_TEST
ENGINE_INSTANTIATION
```

Because this evidence-kind extension is new in v0.7, `ASSET_COMPLETION` remains `CONTRACT_READY` until the next benchmark exercises the new API.

## Packaged executor status

```text
REFERENCE_MEASURE          -> executors/reference_measure.py          CONTRACT_READY
AXISYMMETRIC_PROFILE       -> executors/axisymmetric_profile.py       CONTRACT_READY
RADIAL_REPEAT              -> executors/radial_repeat.py              CONTRACT_READY
MESH_VALIDATE              -> executors/mesh_validate.py              EXECUTOR_READY
RUNTIME_COMPAT             -> executors/runtime_compat.py             CONTRACT_READY
QA_SCENE_ISOLATE           -> executors/qa_scene_isolation.py         CONTRACT_READY
ASSET_COMPLETION           -> executors/completion_gate.py            CONTRACT_READY
UV_ATLAS_CONTRACT          -> executors/uv_atlas_contract.py          CONTRACT_READY
BAKE_RUNTIME_TEXTURES      -> executors/bake_runtime_textures.py      CONTRACT_READY
BAKE_VALIDATE              -> executors/bake_validate.py              CONTRACT_READY
IMAGE_CACHE_COHERENCE      -> executors/image_cache_coherence.py      CONTRACT_READY
PIPELINE_DAG_PLAN          -> executors/pipeline_dag.py                CONTRACT_READY
RUNTIME_PACKAGE_VALIDATE   -> executors/gltf_package_validate.py      CONTRACT_READY
EXPORT_ROUNDTRIP_VALIDATE  -> executors/export_roundtrip_validate.py  CONTRACT_READY
RUNTIME_PATH_RESOLVE       -> executors/runtime_path_resolver.py      CONTRACT_READY
TEST_ORACLE                -> executors/test_oracle.py                 CONTRACT_READY
```

New v0.7 executors remain `CONTRACT_READY` until a later real benchmark validates their contracts in the target runtime.

## Registered SubD sub-operations

`SUBD_TOPOLOGY_CONTROL` exposes:

```text
SUBD_REDIRECT_CORNER_SUPPORT
SUBD_BUILD_SUPPORT_BEVEL
SUBD_REPAIR_CURVED_PINCHING
SUBD_TERMINATE_LOCAL_DENSITY
SUBD_CURVED_CYLINDER_RECESS
SUBD_BUILD_POLE_SAFE_SPHERE
SUBD_REPAIR_BRANCH_JUNCTION
SUBD_CURVED_CYLINDER_PROTRUSION
SUBD_TOPOLOGY_AUDIT
```

## Routing precedence

When multiple skills could solve a feature/problem, route by design intent and failing evidence:

```text
technical-sheet/reference measurement
-> REFERENCE_MEASURE

rotationally symmetric stacked radius/height form
-> AXISYMMETRIC_PROFILE

radially repeated anchor/fastener/vent pattern
-> RADIAL_REPEAT

narrow seam represented as a path
-> HS_PANEL_LINE

smooth control cage under Catmull-Clark
-> SUBD_TOPOLOGY_CONTROL

shared baked atlas across LODs
-> UV_ATLAS_CONTRACT

mesh/topology acceptance gate
-> MESH_VALIDATE

maintained civic material looks sterile/uniform
-> MATERIAL_FINISH_CIVIC

emitter authored but final glow/runtime behavior unresolved
-> EMISSIVE_HANDOFF

Blender procedural material must become runtime data
-> BAKE_RUNTIME_TEXTURES

baked map exists but correctness is unknown
-> BAKE_VALIDATE

disk map is correct but Blender runtime material shows old/wrong pixels
-> IMAGE_CACHE_COHERENCE before rebake/UV changes

local repair should not rerun independent accepted stages
-> PIPELINE_DAG_PLAN

exported glTF/module exists but package contents are unknown
-> RUNTIME_PACKAGE_VALIDATE

exported package exists but dimensions/contact/material survival are unproven
-> EXPORT_ROUNDTRIP_VALIDATE

runtime/output root is ambiguous or multiple GameAssets-like trees exist
-> RUNTIME_PATH_RESOLVE

test is green but shell pipeline/exit status is ambiguous
-> TEST_ORACLE

claiming target-engine integration
-> ENGINE_INTEGRATION_PROOF

claiming final completion
-> ASSET_COMPLETION
```

A lower-level skill must not override a higher-level reconstruction/runtime constraint.

## Skill invocation contract

Before execution the agent records:

```yaml
skill_call:
  skill_id: RUNTIME_PATH_RESOLVE
  feature_id: RUNTIME_OUTPUT_ROOT
  maturity: CONTRACT_READY
  inputs_verified: true
  required_capabilities:
    - filesystem_read
    - project_profile_read
  runtime_bindings_verified: false
```

If `runtime_bindings_verified=false`, run Agent Tool API Profile preflight before mutation.

## Contract-ready is not executor-ready

A semantic skill can define excellent behavior without having a proven executor.

In that case the agent may still implement the operation through available tools, but it must:
1. follow the skill contract;
2. keep implementation local and transactional;
3. validate against postconditions;
4. not present ad-hoc code as a proven library executor;
5. record failed calls and repair iterations;
6. respect Tool Output Budget;
7. follow Code Artifact and Patch Protocol;
8. use the pipeline DAG/dirty-stage cache for expensive bake/export stages;
9. keep Blender round-trip and target-engine proof as separate evidence classes.

## Reuse before generation

Before generating helpers for common operations, search registry and `executors/`.

Do not rewrite compatible local copies of:
- reference measurement;
- profile revolution/lathe helpers;
- radial placement/annulus math;
- contract-aware mesh validation;
- runtime compatibility discovery;
- non-destructive QA scene isolation;
- completion-level evaluation;
- multi-material bake target/channel helpers;
- semantic UV atlas ownership/remapping;
- bake image statistics/emissive containment checks;
- Blender external-image reload/cache-coherence helpers;
- dependency/dirty-stage planning;
- glTF node/material/image readback validation;
- exported-mesh bound/contact checks;
- runtime-root containment validation;
- direct-process test exit-code capture.

## Registry update rule

Whenever a new specialized skill is added:
1. assign a stable Skill ID;
2. add its canonical file here;
3. define maturity;
4. define required runtime capabilities;
5. define validation ownership;
6. add routing in Knowledge Router if needed;
7. include canonical MD in `MANIFEST.json`.

The registry, Knowledge Router and Manifest must never disagree about the existence of a production skill.
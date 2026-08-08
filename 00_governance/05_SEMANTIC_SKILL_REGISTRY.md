# Semantic Skill Registry

## v0.11 registry additions and precedence

The following skills are canonical additions. They have precedence over any v0.10 routing sequence later in this document where the rules conflict.

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `REFERENCE_CONFLICT_RESOLVER` | per-property multi-view arbitration | `184_REFERENCE_CONFLICT_ARBITRATION.md`; `executors/reference_conflict_resolver.py` | CONTRACT_READY |
| `EXECUTION_AUTHORIZATION_GATE` | hard permission for one geometry mutation | `05_execution/73`; `executors/execution_authorization_gate.py` | CONTRACT_READY |
| `NODE_STATE_STORE` | persistent transition/checkpoint validation | `05_execution/74`; `executors/node_state_store.py` | CONTRACT_READY |
| `APPEARANCE_OWNER_COVERAGE` | MUST-owner inventory and namespace closure | `186`; `executors/appearance_owner_coverage.py` | CONTRACT_READY |
| `CANONICAL_SKILL_RUNTIME_PIN` | version/commit/single-root preflight | `188`; `executors/runtime_source_pin.py` | CONTRACT_READY |

Canonical v0.11 order: eligible node -> authorization -> persisted READY_TO_BUILD -> one-node mutation -> BUILT_UNVERIFIED stop -> canonical node proof -> ACCEPTED. Local builders cannot self-authorize or self-accept.

---

## Purpose

Stable routing layer between user intent, reconstruction semantics, knowledge modules, executors and validation.

Agent nie przechodzi bezpośrednio z natural-language request do ad-hoc `bpy`, jeśli zarejestrowany skill już opisuje operację.

## Execution maturity

- `KNOWLEDGE_ONLY` — guidance exists, no stable execution contract.
- `CONTRACT_READY` — stable inputs/outputs/validation exist.
- `EXECUTOR_READY` — tested implementation callable through stable API.
- `RUNTIME_BOUND` — executor mapped to current runtime tools.

Nie claimuj wyższego maturity bez evidence.

## Canonical registry

| Skill ID | Purpose | Canonical knowledge | Maturity | Validation |
|---|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | end-to-end reference reconstruction controller | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` | CONTRACT_READY | evidence, Shape Graph, Appearance Contract, RDL barriers, fidelity gates |
| `REFERENCE_MEASURE` | compact reference measurement | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`; `executors/reference_measure.py` | CONTRACT_READY | provenance, calibration, confidence |
| `REFERENCE_OVERLAY_VALIDATE` | registered reference-vs-candidate silhouette/ROI comparison | `142`, `143`, `171`; `executors/reference_overlay_validate.py` | CONTRACT_READY | IoU, contour delta, MUST ROI |
| `APPEARANCE_REFERENCE_VALIDATE` | reference-anchored internal boundary/trim/edge/material/detail validation | `180_REFERENCE_APPEARANCE_CONTRACT.md`, `181_ANTI_CIRCULAR_VISUAL_VALIDATION.md`, `182_PART_BOUNDARY_TRIM_JUNCTION_GRAPH.md`, `183_EDGE_MATERIAL_DETAIL_FIDELITY.md`, script pattern 96 | CONTRACT_READY | source reference + registration + owner-class metrics |
| `SHAPE_GRAPH` | validate hierarchy/dependencies/readiness of design forms | `174_RECONSTRUCTION_SHAPE_GRAPH.md`, `95_SHAPE_GRAPH_VALIDATOR_PATTERN.md`; `executors/shape_graph.py` | CONTRACT_READY | DAG, levels, RDL, parent/dependency readiness, stage barrier |
| `SHAPE_CLASSIFY` | choose mathematical representation before Blender technique | `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md` | CONTRACT_READY | evidence-backed shape class, rejected alternatives |
| `RECONSTRUCTION_NODE_GATE` | proof-bearing acceptance of one Shape Node | `176_RECONSTRUCTION_NODE_CONTRACT.md`, `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`, `181`; `executors/reconstruction_node_gate.py` | CONTRACT_READY | parent/dependency, canonical validator IDs, source/registration, isolation, per-view evidence, numeric/section/regression |
| `SECTION_LOFT_HARD_SURFACE` | deterministic multi-section base/shell/transition construction | `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`, playbook 118; `executors/section_loft.py` | CONTRACT_READY | station ordering, sample correspondence, mesh data, multi-view/section proof |
| `LAYER_STACK_VALIDATE` | visibility/order validation for layered assemblies | `172_VISIBLE_LAYER_STACK_CONTRACT.md`; `executors/layer_stack_validate.py` | CONTRACT_READY | front-to-back order, burial, facing |
| `APPEARANCE_FIDELITY_GATE` | non-compensating L4/L5 appearance transition gate | `05_execution/72_APPEARANCE_FIDELITY_GATE.md`; `executors/appearance_fidelity_gate.py` | CONTRACT_READY | part boundaries, trim, junctions, edge families, material response, detail coverage, final matched views |
| `RECON_FIDELITY_GATE` | final proof-bearing Level A transition gate | `05_execution/69_RECONSTRUCTION_FIDELITY_GATE.md`, `173`, `180`–`183`; `executors/fidelity_gate.py` | CONTRACT_READY | typed source-anchored evidence, canonical views, MUST features, appearance gate, authority closure |
| `AXISYMMETRIC_PROFILE` | revolved hard-surface profile | `03_modeling/45_AXISYMMETRIC_PROFILE_ASSET_PRIMITIVE.md`; `executors/axisymmetric_profile.py` | CONTRACT_READY | bounds, continuity, topology |
| `RADIAL_REPEAT` | repeated radial details | playbook 110; `executors/radial_repeat.py` | CONTRACT_READY | count, phase, annulus |
| `HS_PANEL_LINE` | narrow seam/groove | `blender-agent-procedural-hard-surface-panel-lines.md` | CONTRACT_READY | path/profile/topology |
| `SUBD_TOPOLOGY_CONTROL` | Catmull-Clark cage design/repair | `blender-agent-subdivision-topology-control.md` | CONTRACT_READY | evaluated surface, pinching, continuity |
| `TRIM_SHEET_UV` | trim-sheet UV strategy | `03_modeling/40_TRIM_SHEETS.md` | CONTRACT_READY | region/density/orientation |
| `UV_ATLAS_CONTRACT` | stable atlas ownership across LODs | `04_game_ready/52_UV_ATLAS_LOD_STABILITY_CONTRACT.md`; `executors/uv_atlas_contract.py` | CONTRACT_READY | semantic part IDs, LOD consistency |
| `MESH_VALIDATE` | contract-aware mesh audit | `08_scripts/92_MESH_CONTRACT_VALIDATOR_PATTERN.md`; `executors/mesh_validate.py` | EXECUTOR_READY | topology intent, manifold/boundaries/UV/tris |
| `RUNTIME_COMPAT` | Blender/runtime API discovery | `02_blender_api/29_BLENDER_5_1_COMPATIBILITY_MATRIX.md`; `executors/runtime_compat.py` | CONTRACT_READY | discovered enums/properties/paths |
| `QA_SCENE_ISOLATE` | non-destructive QA/bake scene isolation | `08_scripts/83_QA_RENDER_SCRIPT_PATTERN.md`; `executors/qa_scene_isolation.py` | CONTRACT_READY | render state restored, contamination prevented |
| `MATERIAL_FINISH_CIVIC` | maintained civic material finish | playbook 114 | CONTRACT_READY | macro/meso/micro breakup |
| `EMISSIVE_HANDOFF` | separate authored emitter from runtime glow | `04_game_ready/49_EMISSIVE_RUNTIME_HANDOFF.md` | CONTRACT_READY | emitter/export/runtime status |
| `BAKE_RUNTIME_TEXTURES` | deterministic runtime texture bake | `04_game_ready/50`, `51`; `executors/bake_runtime_textures.py` | CONTRACT_READY | bake result/channel semantics |
| `BAKE_VALIDATE` | semantic baked-map validation | `08_scripts/93_BAKE_OUTPUT_VALIDATION_PATTERN.md`; `executors/bake_validate.py` | CONTRACT_READY | ranges/regions/degeneracy |
| `IMAGE_CACHE_COHERENCE` | synchronize disk texture and Blender datablock | `02_blender_api/30_IMAGE_DATABLOCK_CACHE_COHERENCE.md`; `executors/image_cache_coherence.py` | CONTRACT_READY | path/reload/colorspace/binding |
| `PIPELINE_DAG_PLAN` | minimal dirty execution closure | `05_execution/68_PIPELINE_DAG_EXECUTOR_AND_STAGE_REUSE.md`; `executors/pipeline_dag.py` | CONTRACT_READY | DAG/execute/reuse plan |
| `RUNTIME_PACKAGE_VALIDATE` | validate glTF package/attributes/transforms | `09_engine/94`, `96`; `executors/gltf_package_validate.py` | CONTRACT_READY | nodes/materials/images/TEXCOORD/TRS |
| `EXPORT_ROUNDTRIP_VALIDATE` | re-import export and check invariants | `05_execution/67_POST_EXPORT_INVARIANT_AND_ROUNDTRIP_VALIDATION.md`; `executors/export_roundtrip_validate.py` | CONTRACT_READY | dimensions/contact/material survival |
| `RUNTIME_PATH_RESOLVE` | resolve engine-visible runtime root | `09_engine/95_RUNTIME_ASSET_ROOT_AND_PATH_CONTRACT.md`; `executors/runtime_path_resolver.py` | CONTRACT_READY | canonical root/containment |
| `TEST_ORACLE` | trustworthy process exit/bite test | `05_execution/66_TEST_ORACLE_EXIT_CODE_AND_BITE_TEST.md`; `executors/test_oracle.py` | CONTRACT_READY | direct status/intended assertion |
| `ENGINE_INTEGRATION_PROOF` | Level D target-engine proof | `09_engine/96_ENGINE_INTEGRATION_SMOKE_TEST_CONTRACT.md` | CONTRACT_READY | loader/instantiation + oracle |
| `QA_REFERENCE` | reconstruction visual/numeric QA | `141`–`148`, `178`, `180`–`183` | CONTRACT_READY | node/stage/final evidence, appearance owners |
| `ASSET_COMPLETION` | determine true completion level | `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`; `executors/completion_gate.py` | CONTRACT_READY | A/B/C/D gate hierarchy |
| `ASSET_CATALOG_INTEGRATE` | project catalog registration | `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` | KNOWLEDGE_ONLY | readback/unique ID/import |
| `EXPORT_VALIDATE` | export and post-export checks | `04_game_ready/45_GLTF_EXPORT.md`, `05_execution/53_FINAL_VALIDATION.md` | KNOWLEDGE_ONLY | runtime contract |

## v0.10 reconstruction routing precedence

```text
reference ingest/measurement
-> REFERENCE_MEASURE

before production geometry
-> SHAPE_GRAPH + SHAPE_CLASSIFY

for 1:1 or target L4/L5
-> REFERENCE_APPEARANCE_CONTRACT + PART_BOUNDARY/TRIM/JUNCTION owners

one node ready to build/repair
-> node's representation skill
-> canonical registered view validator
-> RECONSTRUCTION_NODE_GATE

internal boundary/trim/edge/material owner
-> APPEARANCE_REFERENCE_VALIDATE

end of each RDL
-> SHAPE_GRAPH stage barrier

end of RDL4/RDL5 when appearance required
-> APPEARANCE_FIDELITY_GATE

claiming Level A / entering runtime
-> RECON_FIDELITY_GATE
```

## Anti-circular validation precedence

A canonical acceptance owner cannot be certified by an ad-hoc local substitute.

```text
local helper measurement
-> may produce artifact
-> canonical validator consumes artifact + source evidence
-> canonical gate accepts/rejects
```

Forbidden as acceptance:

```text
builder-local Gate.accept()
-> Shape Node ACCEPTED
```

when `RECONSTRUCTION_NODE_GATE` exists.

Strict reference-derived records require:
- `validator_id`;
- `provenance_id`;
- `source_reference_id` or `source_reference_ids`;
- `registration_id` for projected evidence.

## Host-before-leaf rule

Leaf skills nie mogą pełnić roli shape-understanding layer.

Examples:
- `HS_PANEL_LINE` only after host `ACCEPTED`;
- bevel/edge implementation only RDL4;
- decals/materials only after structural acceptance;
- `SECTION_LOFT_HARD_SURFACE` may be a primary-form skill;
- appearance owners may be declared earlier but cannot PASS before the host revision they validate exists.

## Runtime lock v0.10

For target fidelity L4/L5:

```text
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> runtime LOD/UV/bake/export FORBIDDEN
```

Correct dimensions, triangle budgets, UVs or glTF readback never override this lock.

## Box-abuse route

If a primary node changes width/depth/corner treatment along an axis:

```text
PARAMETRIC_BOX + BEVEL
-> do not default
-> SHAPE_CLASSIFY
-> likely SECTION_LOFT_HARD_SURFACE or SUBD_FREEFORM
```

## Packaged executor status

```text
REFERENCE_MEASURE           -> executors/reference_measure.py               CONTRACT_READY
REFERENCE_OVERLAY_VALIDATE  -> executors/reference_overlay_validate.py      CONTRACT_READY
SHAPE_GRAPH                 -> executors/shape_graph.py                     CONTRACT_READY
RECONSTRUCTION_NODE_GATE    -> executors/reconstruction_node_gate.py        CONTRACT_READY
SECTION_LOFT_HARD_SURFACE   -> executors/section_loft.py                    CONTRACT_READY
LAYER_STACK_VALIDATE        -> executors/layer_stack_validate.py            CONTRACT_READY
APPEARANCE_FIDELITY_GATE    -> executors/appearance_fidelity_gate.py        CONTRACT_READY
RECON_FIDELITY_GATE         -> executors/fidelity_gate.py                   CONTRACT_READY
AXISYMMETRIC_PROFILE        -> executors/axisymmetric_profile.py            CONTRACT_READY
RADIAL_REPEAT               -> executors/radial_repeat.py                   CONTRACT_READY
MESH_VALIDATE               -> executors/mesh_validate.py                   EXECUTOR_READY
RUNTIME_COMPAT              -> executors/runtime_compat.py                  CONTRACT_READY
QA_SCENE_ISOLATE            -> executors/qa_scene_isolation.py             CONTRACT_READY
ASSET_COMPLETION            -> executors/completion_gate.py                 CONTRACT_READY
UV_ATLAS_CONTRACT           -> executors/uv_atlas_contract.py               CONTRACT_READY
BAKE_RUNTIME_TEXTURES       -> executors/bake_runtime_textures.py           CONTRACT_READY
BAKE_VALIDATE               -> executors/bake_validate.py                   CONTRACT_READY
IMAGE_CACHE_COHERENCE       -> executors/image_cache_coherence.py           CONTRACT_READY
PIPELINE_DAG_PLAN           -> executors/pipeline_dag.py                    CONTRACT_READY
RUNTIME_PACKAGE_VALIDATE    -> executors/gltf_package_validate.py           CONTRACT_READY
EXPORT_ROUNDTRIP_VALIDATE   -> executors/export_roundtrip_validate.py       CONTRACT_READY
RUNTIME_PATH_RESOLVE        -> executors/runtime_path_resolver.py           CONTRACT_READY
TEST_ORACLE                 -> executors/test_oracle.py                     CONTRACT_READY
```

## Contract-ready is not executor-ready

A CONTRACT_READY skill may be implemented through current tools, but agent must:
1. follow semantic contract;
2. keep mutation local/idempotent;
3. validate postconditions;
4. not describe it as proven executor;
5. respect retry/strategy-switch rules;
6. persist compact state/evidence;
7. never replace proof with narrative PASS;
8. never replace a registered canonical validator with a builder-local acceptance gate.

## Reuse before generation

Before generating helpers search this registry and `executors/`.

Do not locally rewrite compatible implementations of:
- Shape Graph validation/readiness/stage barriers;
- node acceptance aggregation;
- appearance fidelity aggregation;
- reconstruction fidelity aggregation;
- reference measurement/overlay;
- layered visibility validation;
- multi-section loft ring/bridge generation;
- mesh/bake/cache/package/path/test validators.

## Registry update rule

New production skill requires:
1. stable Skill ID;
2. canonical knowledge path;
3. maturity;
4. capabilities;
5. validation owner;
6. Knowledge Router route;
7. MANIFEST inclusion for canonical MD.

Registry, Router, Task Packs and Manifest must agree.

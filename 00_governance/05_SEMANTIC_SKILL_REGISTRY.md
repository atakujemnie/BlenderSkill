# Semantic Skill Registry

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
| `RECONSTRUCT_REFERENCE` | end-to-end reference reconstruction controller | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` | CONTRACT_READY | evidence, Shape Graph, RDL barriers, fidelity gate |
| `REFERENCE_MEASURE` | compact reference measurement | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`; `executors/reference_measure.py` | CONTRACT_READY | provenance, calibration, confidence |
| `REFERENCE_OVERLAY_VALIDATE` | registered reference-vs-candidate silhouette/ROI comparison | `142`, `143`, `171`; `executors/reference_overlay_validate.py` | CONTRACT_READY | IoU, contour delta, MUST ROI |
| `SHAPE_GRAPH` | validate hierarchy/dependencies/readiness of design forms | `174_RECONSTRUCTION_SHAPE_GRAPH.md`, `95_SHAPE_GRAPH_VALIDATOR_PATTERN.md`; `executors/shape_graph.py` | CONTRACT_READY | DAG, levels, RDL, parent/dependency readiness, stage barrier |
| `SHAPE_CLASSIFY` | choose mathematical representation before Blender technique | `177_SHAPE_CLASSIFICATION_AND_REPRESENTATION.md` | CONTRACT_READY | evidence-backed shape class, rejected alternatives |
| `RECONSTRUCTION_NODE_GATE` | proof-bearing acceptance of one Shape Node | `176_RECONSTRUCTION_NODE_CONTRACT.md`, `178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md`; `executors/reconstruction_node_gate.py` | CONTRACT_READY | parent/dependency, isolation, per-view evidence, numeric/section/regression |
| `SECTION_LOFT_HARD_SURFACE` | deterministic multi-section base/shell/transition construction | `179_MULTI_SECTION_LOFT_AND_PROFILE_CAGE.md`, playbook 118; `executors/section_loft.py` | CONTRACT_READY | station ordering, sample correspondence, mesh data, multi-view/section proof |
| `LAYER_STACK_VALIDATE` | visibility/order validation for layered assemblies | `172_VISIBLE_LAYER_STACK_CONTRACT.md`; `executors/layer_stack_validate.py` | CONTRACT_READY | front-to-back order, burial, facing |
| `RECON_FIDELITY_GATE` | final proof-bearing Level A transition gate | `05_execution/69_RECONSTRUCTION_FIDELITY_GATE.md`, `173`; `executors/fidelity_gate.py` | CONTRACT_READY | typed evidence, canonical views, MUST features, authority closure |
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
| `QA_REFERENCE` | reconstruction visual/numeric QA | `141`–`148` + v0.8/v0.9 validation modules | CONTRACT_READY | node/stage/final evidence |
| `ASSET_COMPLETION` | determine true completion level | `00_governance/07_DONE_LEVELS_AND_STOP_CONDITIONS.md`; `executors/completion_gate.py` | CONTRACT_READY | A/B/C/D gate hierarchy |
| `ASSET_CATALOG_INTEGRATE` | project catalog registration | `09_engine/93_ASSET_CATALOG_INTEGRATION_PROTOCOL.md` | KNOWLEDGE_ONLY | readback/unique ID/import |
| `EXPORT_VALIDATE` | export and post-export checks | `04_game_ready/45_GLTF_EXPORT.md`, `05_execution/53_FINAL_VALIDATION.md` | KNOWLEDGE_ONLY | runtime contract |

## v0.9 reconstruction routing precedence

```text
reference ingest/measurement
-> REFERENCE_MEASURE

before production geometry
-> SHAPE_GRAPH + SHAPE_CLASSIFY

one node ready to build/repair
-> node's representation skill
-> RECONSTRUCTION_NODE_GATE

width/depth/corner profile changes across stations
-> SECTION_LOFT_HARD_SURFACE

axisymmetric profile
-> AXISYMMETRIC_PROFILE

narrow seam on ACCEPTED host
-> HS_PANEL_LINE

SubD/freeform cage on ACCEPTED structural node
-> SUBD_TOPOLOGY_CONTROL

layered visible assembly
-> LAYER_STACK_VALIDATE

registered view comparison
-> REFERENCE_OVERLAY_VALIDATE

end of each RDL
-> SHAPE_GRAPH stage barrier

claiming Level A / entering runtime
-> RECON_FIDELITY_GATE
```

## Host-before-leaf rule

Leaf skills nie mogą pełnić roli shape-understanding layer.

Przykłady:
- `HS_PANEL_LINE` dopiero po host node `ACCEPTED`;
- bevel/edge work dopiero RDL4;
- decals/materials dopiero po structural acceptance;
- `SECTION_LOFT_HARD_SURFACE` może być primary-form skill, bo reprezentuje samą formę, nie detal.

## Box-abuse route

Jeżeli primary node zmienia jednocześnie width/depth/corner treatment wzdłuż osi:

```text
PARAMETRIC_BOX + BEVEL
-> do not default
-> SHAPE_CLASSIFY
-> likely SECTION_LOFT_HARD_SURFACE or SUBD_FREEFORM
```

## Runtime evidence retained from earlier releases

`MESH_VALIDATE` pozostaje `EXECUTOR_READY` dzięki realnemu Blender 5.1 benchmarkowi bollarda.

Nowe executory v0.8/v0.9 pozostają `CONTRACT_READY`, dopóki kolejny realny benchmark nie wykona ich kontraktów w docelowym środowisku.

## Packaged executor status

```text
REFERENCE_MEASURE          -> executors/reference_measure.py              CONTRACT_READY
REFERENCE_OVERLAY_VALIDATE -> executors/reference_overlay_validate.py     CONTRACT_READY
SHAPE_GRAPH                -> executors/shape_graph.py                     CONTRACT_READY
RECONSTRUCTION_NODE_GATE   -> executors/reconstruction_node_gate.py        CONTRACT_READY
SECTION_LOFT_HARD_SURFACE  -> executors/section_loft.py                    CONTRACT_READY
LAYER_STACK_VALIDATE       -> executors/layer_stack_validate.py            CONTRACT_READY
RECON_FIDELITY_GATE        -> executors/fidelity_gate.py                   CONTRACT_READY
AXISYMMETRIC_PROFILE       -> executors/axisymmetric_profile.py            CONTRACT_READY
RADIAL_REPEAT              -> executors/radial_repeat.py                   CONTRACT_READY
MESH_VALIDATE              -> executors/mesh_validate.py                   EXECUTOR_READY
RUNTIME_COMPAT             -> executors/runtime_compat.py                  CONTRACT_READY
QA_SCENE_ISOLATE           -> executors/qa_scene_isolation.py             CONTRACT_READY
ASSET_COMPLETION           -> executors/completion_gate.py                 CONTRACT_READY
UV_ATLAS_CONTRACT          -> executors/uv_atlas_contract.py               CONTRACT_READY
BAKE_RUNTIME_TEXTURES      -> executors/bake_runtime_textures.py           CONTRACT_READY
BAKE_VALIDATE              -> executors/bake_validate.py                   CONTRACT_READY
IMAGE_CACHE_COHERENCE      -> executors/image_cache_coherence.py           CONTRACT_READY
PIPELINE_DAG_PLAN          -> executors/pipeline_dag.py                     CONTRACT_READY
RUNTIME_PACKAGE_VALIDATE   -> executors/gltf_package_validate.py           CONTRACT_READY
EXPORT_ROUNDTRIP_VALIDATE  -> executors/export_roundtrip_validate.py       CONTRACT_READY
RUNTIME_PATH_RESOLVE       -> executors/runtime_path_resolver.py           CONTRACT_READY
TEST_ORACLE                -> executors/test_oracle.py                      CONTRACT_READY
```

## Skill invocation contract

```yaml
skill_call:
  skill_id: SECTION_LOFT_HARD_SURFACE
  shape_node_id: BASE_PLINTH
  graph_revision: sg_004
  maturity: CONTRACT_READY
  inputs_verified: true
  parent_dependencies_accepted: true
  required_capabilities: [python, blender_mesh_create]
  runtime_bindings_verified: false
```

If runtime binding is required and unverified, perform capability preflight before mutation.

## Contract-ready is not executor-ready

A CONTRACT_READY skill may be implemented through current tools, but agent must:
1. follow semantic contract;
2. keep mutation local/idempotent;
3. validate postconditions;
4. not describe it as proven executor;
5. respect retry/strategy-switch rules;
6. persist compact state/evidence;
7. never replace proof with narrative PASS.

## Reuse before generation

Before generating helpers search this registry and `executors/`.

Do not locally rewrite compatible implementations of:
- Shape Graph validation/readiness/stage barriers;
- node acceptance aggregation;
- multi-section loft ring/bridge generation;
- reference measurement/overlay;
- layered visibility validation;
- reconstruction fidelity aggregation;
- axisymmetric profile/radial repeat;
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

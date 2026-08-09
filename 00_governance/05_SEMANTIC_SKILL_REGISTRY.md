# Semantic Skill Registry

## Execution maturity

- `KNOWLEDGE_ONLY` — guidance exists, no stable execution contract.
- `CONTRACT_READY` — stable inputs/outputs/validation exist.
- `EXECUTOR_READY` — tested implementation callable through stable API.
- `RUNTIME_BOUND` — executor mapped to current runtime tools.

Do not claim higher maturity without evidence.

## v0.12 registry additions and precedence

These skills have precedence over weaker v0.11/v0.10 execution routes:

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `MUTATION_POSTCONDITION_GATE` | prove an authorized geometry mutation actually produced its intended postcondition | `05_execution/76`; `executors/mutation_postcondition_gate.py` | CONTRACT_READY |
| `ASSEMBLY_INTEGRITY_GATE` | relation-aware gap/contact/embedding/interpenetration validation | `189_ASSEMBLY_RELATION_AND_INTERPENETRATION_CONTRACT.md`; `executors/assembly_integrity_gate.py` | CONTRACT_READY |
| `DEPENDENCY_INVALIDATOR` | propagate repair impact across Shape/Appearance/Evidence revisions | `05_execution/77`; `executors/dependency_invalidator.py` | CONTRACT_READY |
| `VALIDATOR_NEGATIVE_CONTROL` | prove that a MUST validator rejects its known-broken failure fixture | `190_ADVERSARIAL_VALIDATION_AND_NEGATIVE_CONTROLS.md`; `executors/validator_negative_control.py` | CONTRACT_READY |
| `GEOMETRIC_INTEGRITY_GATE` | final non-compensating physical-geometry closure before fidelity/runtime | `05_execution/78`; `executors/geometric_integrity_gate.py` | CONTRACT_READY |

Strengthened in v0.12:
- `NODE_STATE_STORE` — requires mutation-postcondition proof before `BUILT_UNVERIFIED`;
- `RECONSTRUCTION_NODE_GATE` — requires geometric integrity evidence for authorized production nodes;
- `MESH_VALIDATE` — classifies non-planar/concave/high-order n-gons and signed closed volume;
- `REFERENCE_OVERLAY_VALIDATE` — supports annotation exclusion/component filtering;
- `RECON_FIDELITY_GATE` and `ASSET_COMPLETION` — require final geometric-integrity proof for L4/L5/Level A closure.

Canonical production order:

```text
eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> NODE_STATE_STORE: READY_TO_BUILD
-> one-node mutation
-> MUTATION_POSTCONDITION_GATE
-> NODE_STATE_STORE: BUILT_UNVERIFIED
-> source QA
-> ASSEMBLY_INTEGRITY_GATE for touched relations
-> MESH_VALIDATE / section/layer evidence as required
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED
```

Before final fidelity/runtime:

```text
all required nodes/relations current
-> GEOMETRIC_INTEGRITY_GATE
-> APPEARANCE_FIDELITY_GATE when required
-> RECON_FIDELITY_GATE
-> runtime
```

Repair of accepted geometry routes first through `DEPENDENCY_INVALIDATOR`. MUST acceptance validators must have `VALIDATOR_NEGATIVE_CONTROL` proof before promotion to `EXECUTOR_READY`.

## Canonical registry

| Skill ID | Purpose | Canonical knowledge | Maturity | Validation |
|---|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | end-to-end reference reconstruction controller | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` | CONTRACT_READY | evidence, Shape Graph, Appearance Contract, integrity, RDL barriers, fidelity gates |
| `REFERENCE_MEASURE` | compact reference measurement | `08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`; `executors/reference_measure.py` | CONTRACT_READY | provenance, calibration, confidence |
| `REFERENCE_OVERLAY_VALIDATE` | registered source-vs-candidate silhouette/ROI comparison | `142`, `143`, `171`, `191`; `executors/reference_overlay_validate.py` | CONTRACT_READY | IoU, contour delta, MUST ROI, annotation-clean product mask |
| `REFERENCE_CONFLICT_RESOLVER` | per-property multi-view arbitration | `184`; `executors/reference_conflict_resolver.py` | CONTRACT_READY | property authority, no silent averaging |
| `SHAPE_GRAPH` | validate design hierarchy/dependencies/readiness/stage barriers | `174`; `executors/shape_graph.py` | CONTRACT_READY | DAG, levels, RDL, readiness |
| `SHAPE_CLASSIFY` | choose mathematical representation before Blender technique | `177` | CONTRACT_READY | evidence-backed shape class, rejected alternatives |
| `EXECUTION_AUTHORIZATION_GATE` | hard permission for exactly one geometry mutation | `05_execution/73`; `executors/execution_authorization_gate.py` | CONTRACT_READY | graph/node revision, dependencies, prior RDL |
| `NODE_STATE_STORE` | persistent transition/checkpoint validation | `05_execution/74`; `executors/node_state_store.py` | CONTRACT_READY | canonical transitions, namespaces, mutation postcondition |
| `MUTATION_POSTCONDITION_GATE` | validate actual effect of one mutation | `05_execution/76`; `executors/mutation_postcondition_gate.py` | CONTRACT_READY | before/after geometry, Boolean bite, transforms, volume, feature probe |
| `ASSEMBLY_INTEGRITY_GATE` | physical relation integrity between product parts | `189`; `executors/assembly_integrity_gate.py` | CONTRACT_READY | semantic relation + gap/contact/embedding/interpenetration metrics |
| `DEPENDENCY_INVALIDATOR` | invalidate downstream state/evidence after repair | `05_execution/77`; `executors/dependency_invalidator.py` | CONTRACT_READY | descendants, owners, revisions, supersession |
| `VALIDATOR_NEGATIVE_CONTROL` | adversarial bite test for validators | `190`; `executors/validator_negative_control.py` | CONTRACT_READY | known-good PASS + known-broken FAIL |
| `GEOMETRIC_INTEGRITY_GATE` | aggregate mutation/assembly/topology/control freshness before final fidelity | `05_execution/78`; `executors/geometric_integrity_gate.py` | CONTRACT_READY | postconditions, relations, topology, negative controls, stale evidence |
| `RECONSTRUCTION_NODE_GATE` | proof-bearing acceptance of one Shape Node | `176`, `178`, `181`, `189`, `190`; `executors/reconstruction_node_gate.py` | CONTRACT_READY | parent/dependency, authorization, postcondition, assembly integrity, source proof |
| `APPEARANCE_REFERENCE_VALIDATE` | internal boundary/trim/edge/material/detail validation | `180`–`183` | CONTRACT_READY | source reference + registration + owner-class metrics |
| `APPEARANCE_OWNER_COVERAGE` | MUST Appearance Owner inventory closure | `186`; `executors/appearance_owner_coverage.py` | CONTRACT_READY | no missing/unverified MUST owners |
| `SECTION_LOFT_HARD_SURFACE` | deterministic multi-section hard-surface construction | `179`; `executors/section_loft.py` | CONTRACT_READY | station order, correspondence, section proof |
| `LAYER_STACK_VALIDATE` | layered assembly visibility/order | `172`; `executors/layer_stack_validate.py` | CONTRACT_READY | front-to-back order, burial, facing |
| `APPEARANCE_FIDELITY_GATE` | non-compensating L4/L5 visible-product gate | `05_execution/72`; `executors/appearance_fidelity_gate.py` | CONTRACT_READY | boundaries, trim, junction, edge, material, detail |
| `RECON_FIDELITY_GATE` | final proof-bearing Level A reconstruction gate | `05_execution/69`; `executors/fidelity_gate.py` | CONTRACT_READY | source-anchored evidence, canonical views, MUST features, geometric integrity |
| `AXISYMMETRIC_PROFILE` | revolved hard-surface profile | `03_modeling/45`; `executors/axisymmetric_profile.py` | CONTRACT_READY | bounds, continuity, topology |
| `RADIAL_REPEAT` | repeated radial details | playbook 110; `executors/radial_repeat.py` | CONTRACT_READY | count, phase, annulus |
| `HS_PANEL_LINE` | narrow seam/groove | `blender-agent-procedural-hard-surface-panel-lines.md` | CONTRACT_READY | path/profile/topology |
| `SUBD_TOPOLOGY_CONTROL` | Catmull-Clark cage design/repair | `blender-agent-subdivision-topology-control.md` | CONTRACT_READY | evaluated surface, pinching, continuity |
| `MESH_VALIDATE` | contract-aware mesh/topology integrity audit | `08_scripts/92`; `executors/mesh_validate.py` | EXECUTOR_READY | manifold, volume orientation, n-gon risk, UV/tris |
| `QA_SCENE_ISOLATE` | non-destructive QA/bake isolation | `08_scripts/83`; `executors/qa_scene_isolation.py` | CONTRACT_READY | state restoration, contamination prevention |
| `CANONICAL_SKILL_RUNTIME_PIN` | version/commit/single-root preflight | `188`; `executors/runtime_source_pin.py` | CONTRACT_READY | exact runtime source |
| `MATERIAL_FINISH_CIVIC` | civic product material finish | playbook 114 | CONTRACT_READY | macro/meso/micro response |
| `EMISSIVE_HANDOFF` | authored emitter vs runtime glow | `04_game_ready/49` | CONTRACT_READY | emitter/export/runtime status |
| `UV_ATLAS_CONTRACT` | stable atlas ownership across LODs | `04_game_ready/52`; `executors/uv_atlas_contract.py` | CONTRACT_READY | semantic IDs, LOD stability |
| `BAKE_RUNTIME_TEXTURES` | deterministic runtime texture bake | `04_game_ready/50`, `51`; `executors/bake_runtime_textures.py` | CONTRACT_READY | bake result/channel semantics |
| `BAKE_VALIDATE` | semantic baked-map validation | `08_scripts/93`; `executors/bake_validate.py` | CONTRACT_READY | range/region/degeneracy |
| `IMAGE_CACHE_COHERENCE` | disk/Blender image synchronization | `02_blender_api/30`; `executors/image_cache_coherence.py` | CONTRACT_READY | path/reload/colorspace/binding |
| `PIPELINE_DAG_PLAN` | minimal dirty runtime-stage closure | `05_execution/68`; `executors/pipeline_dag.py` | CONTRACT_READY | DAG execute/reuse plan |
| `RUNTIME_PATH_RESOLVE` | canonical engine-visible asset root | `09_engine/95`; `executors/runtime_path_resolver.py` | CONTRACT_READY | root/containment |
| `RUNTIME_PACKAGE_VALIDATE` | glTF nodes/materials/attributes/transforms | `09_engine/94`, `96`; `executors/gltf_package_validate.py` | CONTRACT_READY | package/TEXCOORD/TRS |
| `EXPORT_ROUNDTRIP_VALIDATE` | re-import export and compare invariants | `05_execution/67`; `executors/export_roundtrip_validate.py` | CONTRACT_READY | dimensions/contact/material survival |
| `TEST_ORACLE` | trustworthy exit status and bite tests | `05_execution/66`; `executors/test_oracle.py` | CONTRACT_READY | direct assertion/negative mutation |
| `ENGINE_INTEGRATION_PROOF` | Level D target-engine proof | `09_engine/96` | CONTRACT_READY | production loader/instantiation |
| `ASSET_COMPLETION` | determine true A/B/C/D completion | `00_governance/07`; `executors/completion_gate.py` | CONTRACT_READY | hierarchical completion gates including geometric integrity |

## Routing laws

### Representation before operator

```text
reference evidence
-> Shape Graph
-> Shape Class
-> semantic construction skill
-> Blender implementation
```

Do not default compound primary forms to `cube + bevel` when width/depth/corner behavior varies across stations.

### Host-before-leaf

Leaf/detail skills only run on accepted hosts. A host changing during repair invalidates dependent leaves before they can remain green.

### Anti-circular validation

```text
local measurement adapter
-> compact artifact
-> canonical validator
-> canonical gate
```

A local builder/helper may measure. It may not redefine acceptance semantics.

### Validator bite law

For MUST acceptance, a new validator requires a negative-control fixture representing the same failure class. A test that only passes known-good input is insufficient.

### Runtime lock

For L4/L5:

```text
GEOMETRIC_INTEGRITY_GATE != PASS
or
APPEARANCE_FIDELITY_GATE != PASS
or
RECON_FIDELITY_GATE != PASS
-> runtime LOD/UV/bake/export FORBIDDEN
```

## Registry update rule

A new production skill requires:
1. stable Skill ID;
2. canonical knowledge path;
3. maturity;
4. capabilities;
5. validation owner;
6. Knowledge Router route;
7. MANIFEST inclusion when canonical Markdown is added.

Registry, Router, State Machine and Manifest must agree.

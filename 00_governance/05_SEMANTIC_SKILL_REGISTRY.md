# Semantic Skill Registry v0.11

## Maturity
`KNOWLEDGE_ONLY`, `CONTRACT_READY`, `EXECUTOR_READY`, `RUNTIME_BOUND`.

## Reconstruction core

| Skill ID | Purpose | Canonical knowledge | Maturity |
|---|---|---|---|
| `RECONSTRUCT_REFERENCE` | end-to-end controller | `10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md` | CONTRACT_READY |
| `REFERENCE_MEASURE` | calibrated source measurement | `executors/reference_measure.py` | CONTRACT_READY |
| `REFERENCE_OVERLAY_VALIDATE` | registered silhouette/ROI proof | `executors/reference_overlay_validate.py` | CONTRACT_READY |
| `APPEARANCE_REFERENCE_VALIDATE` | boundaries/trim/junction/material/detail proof | `180`–`183` | CONTRACT_READY |
| `REFERENCE_CONFLICT_RESOLVER` | per-property multi-view arbitration | `184_REFERENCE_CONFLICT_ARBITRATION.md`; `executors/reference_conflict_resolver.py` | CONTRACT_READY |
| `SHAPE_GRAPH` | graph structure, eligibility, readiness, barriers | `174`; `executors/shape_graph.py` | CONTRACT_READY |
| `SHAPE_CLASSIFY` | mathematical representation selection | `177` | CONTRACT_READY |
| `EXECUTION_AUTHORIZATION_GATE` | hard permission for one geometry mutation | `05_execution/73`; `executors/execution_authorization_gate.py` | CONTRACT_READY |
| `NODE_STATE_STORE` | canonical transition/checkpoint validator | `05_execution/74`; `executors/node_state_store.py` | CONTRACT_READY |
| `RECONSTRUCTION_NODE_GATE` | proof-bearing one-node acceptance | `176`, `178`, `185`; `executors/reconstruction_node_gate.py` | CONTRACT_READY |
| `SECTION_LOFT_HARD_SURFACE` | multi-section construction | `179`; `executors/section_loft.py` | CONTRACT_READY |
| `LAYER_STACK_VALIDATE` | layered visibility/order | `172`; `executors/layer_stack_validate.py` | CONTRACT_READY |
| `APPEARANCE_OWNER_COVERAGE` | MUST-owner inventory + namespace closure | `186`; `executors/appearance_owner_coverage.py` | CONTRACT_READY |
| `APPEARANCE_FIDELITY_GATE` | non-compensating L4/L5 appearance gate | `05_execution/72`; `executors/appearance_fidelity_gate.py` | CONTRACT_READY |
| `RECON_FIDELITY_GATE` | final Level A proof gate | `05_execution/69`; `executors/fidelity_gate.py` | CONTRACT_READY |
| `CANONICAL_SKILL_RUNTIME_PIN` | version/commit/single active root preflight | `188`; `executors/runtime_source_pin.py` | CONTRACT_READY |

## Modeling/runtime skills retained
`AXISYMMETRIC_PROFILE`, `RADIAL_REPEAT`, `HS_PANEL_LINE`, `SUBD_TOPOLOGY_CONTROL`, `TRIM_SHEET_UV`, `UV_ATLAS_CONTRACT`, `MESH_VALIDATE`, `RUNTIME_COMPAT`, `QA_SCENE_ISOLATE`, `MATERIAL_FINISH_CIVIC`, `EMISSIVE_HANDOFF`, `BAKE_RUNTIME_TEXTURES`, `BAKE_VALIDATE`, `IMAGE_CACHE_COHERENCE`, `PIPELINE_DAG_PLAN`, `RUNTIME_PACKAGE_VALIDATE`, `EXPORT_ROUNDTRIP_VALIDATE`, `RUNTIME_PATH_RESOLVE`, `TEST_ORACLE`, `ENGINE_INTEGRATION_PROOF`, `ASSET_COMPLETION`.

## v0.11 precedence

```text
runtime pin
-> reference evidence
-> conflict arbitration where needed
-> Shape Graph + Appearance Contract
-> eligible node
-> execution authorization
-> persist READY_TO_BUILD
-> one-node mutation
-> BUILT_UNVERIFIED hard stop
-> source proof + node gate
-> ACCEPTED
-> stage barrier
-> appearance owner coverage
-> appearance gate
-> recon gate
-> runtime
```

## Anti-bypass rules
- a local builder may not emit canonical authorization;
- a local builder may not move itself to ACCEPTED;
- `CONSTRAINED` is not build permission;
- `BUILT_UNVERIFIED` is not parent acceptance;
- a generic `REPORT['nodes']` may not mix Shape Nodes and Appearance Owners;
- one view's interpretation may not silently become global authority;
- local helper proliferation should trigger reuse/migration review.

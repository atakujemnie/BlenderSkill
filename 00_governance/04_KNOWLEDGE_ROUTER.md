# Knowledge Router v0.11

Load the smallest task pack for the current state, Shape Node, Appearance Owner or failing evidence.

## Preflight

Use:
- `CANONICAL_SKILL_RUNTIME_PIN`;
- Blender/runtime compatibility;
- project pipeline profile;
- scene inspection.

Do not execute a benchmark with two active BlenderSkill roots or a stale embedded copy.

## Reference analysis

Route to `REFERENCE_MEASURE`, registration/calibration, source registry and cache. If views disagree on one property, route immediately to `REFERENCE_CONFLICT_RESOLVER`; do not silently choose one view or average values.

## Shape/appearance planning

Before production geometry:
- `SHAPE_GRAPH`;
- `SHAPE_CLASSIFY`;
- per-view validation contracts;
- `REFERENCE_APPEARANCE_CONTRACT` for L4/L5;
- derived parameter provenance.

## Execution routing v0.11

```text
SHAPE_GRAPH eligible node
-> EXECUTION_AUTHORIZATION_GATE.issue_authorization
-> NODE_STATE_STORE persist READY_TO_BUILD
-> EXECUTION_AUTHORIZATION_GATE.can_mutate
-> build exactly one node
-> NODE_STATE_STORE persist BUILT_UNVERIFIED
-> QA_SCENE_ISOLATE
-> per-view canonical evidence
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
```

If `ready_nodes=[]`, geometry mutation is forbidden.

## Per-view evidence

- ORTHO / NEAR_ORTHO -> `REGISTERED_OVERLAY` / numeric/landmark proof;
- HERO perspective -> `PERSPECTIVE_INSPECTION` as supporting design-intent evidence;
- DETAIL crop -> `LOCAL_FEATURE_ROI` / appearance-owner validation.

Never assign one generic evidence kind to all views of a node.

## RDL routing

RDL0: diagnostic grey geometry only.

RDL1: primary forms; no production materials.

RDL2: secondary structural forms and major product architecture.

RDL3: recesses, seams, hatches, emitters and other structural features on ACCEPTED hosts.

RDL4: edge language.

RDL5: materials, branding, detail and lookdev.

Every RDL transition requires the canonical stage barrier.

## Appearance closure

Before `APPEARANCE_FIDELITY_GATE` run `APPEARANCE_OWNER_COVERAGE` against the declared contract. Missing or UNVERIFIED MUST owners block L4/L5.

## Runtime lock

`APPEARANCE_FIDELITY_GATE != PASS` or `RECON_FIDELITY_GATE != PASS` -> no runtime LOD/UV/bake/export.

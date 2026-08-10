# Fidelity Enforcement and Deterministic Assembly

Status: v0.21.0 implementation contract

## Purpose

v0.21 closes the gap exposed by the Lafar Standard Sidewalk blind end-to-end test: a production workflow may not report success merely because repositories, task queues and Blender executors ran without exceptions. `APPROVED` must mean that the component was placed where the asset state says it belongs, represented with the required geometric features, measured from the current Blender scene and accepted by trusted validators bound to the exact asset/scene revision.

The release invariant is:

```text
EXECUTOR_RAN_SUCCESSFULLY != ASSET_IS_CORRECT
WORKER_SAYS_PASS != TRUSTED_VALIDATION_PASS
METADATA_BINDING != BLENDER_MATERIAL
DECLARED_PLACEMENT != EXECUTED_PLACEMENT
CALLER_REQUESTS_AUTHORIZATION != AUTHORIZATION_PASS
```

## Blind-test failures fixed by this contract

The v0.20 blind test exposed these failure classes:

1. component placement such as `center_offset` could disappear between asset state and Blender recipe;
2. a geometry task could be created for a stage ahead of the persisted asset stage;
3. a component could remain `CONSTRAINED` while its task reached `APPROVED`;
4. a worker-supplied `validation_status: PASS` could satisfy approval;
5. semantic representations such as tactile grids or slotted drainage grates could collapse into generic boxes;
6. reference ROI records did not guarantee a concrete worker attachment;
7. design bindings could remain Blender custom properties without a real material slot;
8. immediately sampled Blender transforms could observe stale dependency-graph state;
9. footprint/seam contradictions could survive manifest validation;
10. Studio startup contained a demo-specific selected component and could silently display the demo asset after a live error.

## Canonical component transform

Every component task pack carries one normalized transform:

```yaml
transform:
  location_mm: [x, y, z]
  rotation_deg: [rx, ry, rz]
  scale: [sx, sy, sz]
  coordinate_space: ASSET_LOCAL | PARENT_LOCAL
  explicit: true | false
  source: TRANSFORM | LEGACY_LOCATION_MM | LEGACY_CENTER_OFFSET | IMPLICIT_ORIGIN
```

`COMPONENT_TRANSFORM` converts legacy placement records to this schema. A component marked `placement_required: true` cannot be executed when placement is implicit.

`component.origin.type` remains independent from transform. The transform locates the declared component origin. Blender primitive construction and envelope validation must therefore honor origins such as:

- `CENTER`;
- `CENTER_BOTTOM` / `CENTER_XY_BOTTOM_Z`;
- `FRONT_EDGE_CENTER_BOTTOM`;
- `REAR_EDGE_CENTER_BOTTOM`;
- `LEFT_EDGE_CENTER_BOTTOM`;
- `RIGHT_EDGE_CENTER_BOTTOM`.

Local recipe offsets are added only after canonical component placement is resolved.

## Asset envelope and seams

`ASSET_ENVELOPE_GATE` evaluates resolved component dimensions, origin semantics and canonical transforms against the root envelope.

When `enforce_asset_envelope: true`:

- child extents outside the nominal asset envelope are blockers unless explicitly allowed;
- `seam_constraints` compare declared and mathematically measured gaps;
- relational dimensions are resolved before bounds are evaluated;
- inconsistent values cannot be accepted independently merely because each is individually plausible.

Example negative control from the blind sidewalk test:

```text
centres = -500 mm / +500 mm
slab widths = 996 mm / 996 mm
measured gap = 4 mm
specified gap = 6 mm +/- 0.5 mm
=> FAIL: SEAM_GAP_MISMATCH
```

## Representation contract

`REPRESENTATION_CONTRACT_GATE` validates what a recipe actually builds, not only whether recipe syntax is valid.

Default fail-closed representation requirements include:

```text
PROFILE_PRISM          -> PROFILE_PRISM
TACTILE_GRID_PANEL     -> ARRAY or INSTANCE
SLOTTED_GRATE_PLATE    -> ARRAY or BOOLEAN_CUT
RECESSED_CHANNEL       -> BOOLEAN_CUT
RECESSED_HOUSING       -> BOOLEAN_CUT
EMISSIVE_STRIP         -> ASSIGN_BINDING
```

Components may additionally declare:

```yaml
representation_contract:
  required_operations: []
  required_any_operations: []
  forbidden_operations: []
  required_feature_ids: []
  minimum_repeat_count: 0
```

A weaker representation must return `BLOCKED`, not silently fall back to a box.

## Component execution authorization

Geometry mutation is split into two barriers:

```text
persistent component constraints/dependencies
-> ASSET_EXECUTION_AUTHORIZATION_GATE
-> component.state = READY_TO_BUILD
-> component-scoped task
-> COMPONENT_EXECUTION_GATE
-> Blender mutation
```

Authorization is system-derived. The UI/API may request authorization and provide actor/reason metadata, but caller-provided `status`, `validator_id` or confidence cannot create PASS evidence. `ASSET_EXECUTION_AUTHORIZATION_GATE` derives the verdict from persisted state, including:

- current asset stage is buildable;
- component state is authorizable;
- declared component dependencies are already `ACCEPTED`;
- no open HARD/CANONICAL correction targets the component.

For Studio-created geometry tasks:

- the requested task stage cannot be ahead of `asset.stage`;
- `BUILD` requires `component.state == READY_TO_BUILD`;
- mutation scope and recipe component ID must match the task pack;
- the representation contract must pass before Blender is called.

This makes the prior `RECONSTRUCTION_MANIFEST -> STRUCTURAL_GEOMETRY task` bypass illegal.

## Trusted validation receipts

Workers may propose task results. They do not own approval.

A trusted validation receipt is persistent evidence with at least:

```yaml
receipt_id:
validator_id:
validator_version:
asset_id:
asset_revision:
component_id:
scene_revision:
status: PASS | FAIL | BLOCKED
source: SYSTEM
```

`VALIDATION_RECEIPT_REPOSITORY` stores immutable receipt revisions separately from task results.

`SCENE_COMPONENT_VALIDATION` evaluates current component-scoped scene evidence against the exact task-pack asset revision and canonical placement. When requested by the component validation contract it also enforces dimensions and resolved material resources.

`COMPONENT_VALIDATION_RUNNER` executes the deterministic `REPRESENTATION_CONTRACT_GATE` and `SCENE_COMPONENT_VALIDATION`, then persists their PASS/FAIL receipts. This is the normal receipt-production path; workers do not manufacture receipt payloads.

Strict geometry tasks declare `required_validation_ids`. Approval requires one current `PASS` receipt for every required validator, matching exactly:

```text
asset_id
asset_revision
component_id
scene_revision
validator_id
source == SYSTEM
```

Therefore:

```text
worker result: {validation_status: PASS}
without trusted receipts
=> APPROVED forbidden
```

The task stores the receipt IDs used for approval. Service-level direct receipt publication is additionally constrained to the currently persisted asset revision and current scene revision and is not exposed as an arbitrary browser route.

## Component/task convergence

After a strict task is successfully approved, Production Studio persists:

```text
task.status = APPROVED
component.state = ACCEPTED
asset.revision += 1
```

The previous split-brain state where all tasks were approved while components remained `CONSTRAINED` is not a valid v0.21 completion state.

## Reference evidence materialization

Reference routing remains component/feature scoped, but metadata alone is insufficient for a multimodal worker.

`REFERENCE_EVIDENCE_MATERIALIZER` resolves evidence `artifact_id` records through an explicit local artifact catalog and produces attachment descriptors containing:

```text
path
media_type
roi
view
authority
feature_ids
```

Paths are resolved locally and can be confined to an allowed root. Task-pack token budgets remain unchanged because image attachments are not expanded into repeated textual scene descriptions.

## Blender design-resource materialization

`ASSIGN_BINDING` remains the recipe-level semantic operation, but `COMPONENT_EXECUTION_GATE` now follows successful geometry execution with `BLENDER_DESIGN_RESOURCE_ADAPTER`.

For `MATERIAL` resources the adapter creates/reuses a real `bpy.data.materials` datablock and assigns it to the object material slot. Supported runtime fields include:

- Base Color;
- Metallic;
- Roughness;
- Emission Color / Strength.

A binding custom property may remain as provenance, but it is no longer treated as proof that the Blender material exists.

## Blender runtime coherence

`BLENDER_HARD_SURFACE_BUILDER` updates the active view layer before returning. A snapshot taken immediately after execution therefore observes the current transform/dependency-graph state rather than relying on a later UI refresh.

## Studio UI invariant

The live Studio UI is asset-generic:

- no demo component ID is selected by default;
- a component removed or renamed between requests causes a retry without the stale component selector;
- a live API failure remains visibly a live API failure;
- the client does not silently substitute a bundled demo asset;
- `REVIEW -> APPROVED` is sent as an intent and the server remains authoritative for trusted validation requirements.

## v0.21 execution chain

```text
reference source
-> scoped evidence + concrete attachment
-> persistent asset/component state
-> canonical component transform + origin
-> asset envelope / seam constraints
-> system-derived component authorization
-> component task pack
-> compact recipe
-> representation contract gate
-> deterministic Blender mutation
-> real design-resource materialization
-> view-layer update
-> compact scene snapshot
-> deterministic scene + representation validation
-> trusted validation receipts
-> REVIEW
-> APPROVED
-> component ACCEPTED
```

## Token policy

v0.20 limits remain mandatory:

```text
REPAIR <= 4k estimated input tokens
BUILD <= 8k
ASSET PLANNING <= 15k
```

v0.21 optimizes correctness before further context reduction. Passing token budgets never compensates for a failed representation, envelope, placement or validation gate.

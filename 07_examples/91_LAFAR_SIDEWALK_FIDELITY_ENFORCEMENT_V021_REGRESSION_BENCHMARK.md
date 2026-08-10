# Benchmark 91 — Lafar Sidewalk Fidelity Enforcement v0.21 Regression

Status: canonical v0.21 release benchmark

## Origin

This benchmark is derived from the first blind end-to-end Production Studio test performed after v0.20. The test used a new Lafar Standard Sidewalk Module rather than the known Lafar bench fixture. The orchestration stack reported successful task execution and ultimately approved nineteen build tasks, while the resulting Blender asset was visually and structurally inconsistent with the supplied concept.

The benchmark exists to prevent that class of false success.

## Asset target

Canonical module family:

```text
LAFAR STANDARD SIDEWALK MODULE
Astera Civic Systems
nominal envelope: 2000 x 2000 x 160 mm
```

Reference-critical physical features include:

- four primary sidewalk slabs;
- controlled slab seams;
- tactile / anti-slip band with repeated raised detail;
- brushed aluminium curb trim;
- recessed linear drainage channel;
- drainage grate with repeated slots;
- two recessed guidance LED emitters rather than one continuous neon;
- graphite structural base body;
- consistent modular footprint and height.

The benchmark does not require production textures for every negative-control test. It does require the runtime to reject representations that cannot physically encode the declared feature.

## Blind-test failure signature

The known-broken v0.20 pattern was:

```text
manifest PASS
parameter graph PASS
task pack PASS
recipe validation PASS
Blender executor PASS
scene snapshot PASS
task lifecycle 19/19 APPROVED

human/reference result: FAIL
```

v0.21 must instead make every `APPROVED` traceable to current geometry and trusted validation evidence.

## Required negative controls

### 1. Placement preservation

A component with an explicit asset-local location must carry the same canonical transform into its task pack and Blender execution.

Known failure:

```text
manifest.center_offset = [500, -500]
-> field omitted from task pack
-> builder default location = [0, 0, 0]
```

Required v0.21 result: impossible when `placement_required: true`.

### 2. Seam mathematics

Two slabs centered at `x=-500` and `x=+500`, each `996 mm` wide, measure a `4 mm` gap.

If the declared constraint is:

```text
expected_gap_mm = 6
Tolerance = 0.5 mm
```

`ASSET_ENVELOPE_GATE` must return `FAIL / SEAM_GAP_MISMATCH`.

A consistent `994 mm + 994 mm` pair at the same centers measures `6 mm` and may pass.

### 3. Footprint escape

A component whose measured AABB extends beyond the 2000 x 2000 mm root footprint must fail unless the component explicitly permits an envelope exception.

### 4. Tactile representation

A component declared `TACTILE_GRID_PANEL` cannot pass with a recipe containing only one generic `BOX` or `ROUNDED_BOX`.

It must demonstrate repeated geometry/instances or a stronger explicit representation contract.

### 5. Drain grate representation

A component declared `SLOTTED_GRATE_PLATE` cannot pass as one unmodified rounded box. The representation must include repeated/removed slot structure according to its contract.

### 6. Recess representation

`RECESSED_CHANNEL` and `RECESSED_HOUSING` must contain a physical recess operation. A dark material or flat overlay is insufficient.

### 7. Stage bypass

When:

```text
asset.stage = RECONSTRUCTION_MANIFEST
requested task.stage = STRUCTURAL_GEOMETRY
```

Production Studio must return `BLOCKED / TASK_STAGE_NOT_AUTHORIZED`.

### 8. Build authorization

A geometry `BUILD` task for a component not in `READY_TO_BUILD` must return `BLOCKED / COMPONENT_BUILD_NOT_AUTHORIZED`.

### 9. Worker self-certification

A worker task result containing:

```json
{"validation_status":"PASS","scene_revision":1}
```

must not be enough to transition a strict geometry task from `REVIEW` to `APPROVED`.

Without all required trusted receipts, expected result:

```text
FAIL / TRUSTED_VALIDATION_RECEIPTS_REQUIRED
```

### 10. Revision-bound trusted approval

Required validation receipts must match the task's exact:

```text
asset_id
asset_revision
component_id
scene_revision
validator_id
```

and must have `source=SYSTEM`, `status=PASS`.

Stale scene receipts, stale asset receipts or worker-originated receipts must not authorize approval.

### 11. Component/task state convergence

After trusted approval:

```text
task.status == APPROVED
component.state == ACCEPTED
```

must both be persisted. The v0.20 state split (`APPROVED` task + `CONSTRAINED` component) is a regression failure.

### 12. Real Blender material

A recipe `ASSIGN_BINDING` operation for a resolved `MATERIAL` resource must result in a real Blender material slot assignment. A custom property containing only the binding ID is insufficient.

### 13. Dependency-graph freshness

Immediately after the deterministic Blender builder returns, `matrix_world` and scene-snapshot measurements must reflect the executed transform without requiring an unrelated later redraw or user action.

### 14. Asset-generic Studio UI

The live Studio HTML must not contain a hard-coded production selection for the old bench component. Starting with a different asset must not request a nonexistent demo component and must not silently substitute offline demo data after a live API error.

### 15. Reference attachments

When a task requests reference evidence and an artifact catalog is available, evidence must be materializable to a concrete local attachment descriptor with a bounded ROI and an allowed-root path check.

## Positive component lifecycle

The expected strict component path is:

```text
CONSTRAINED
-> deterministic execution authorization
-> READY_TO_BUILD
-> task QUEUED
-> dependency promotion
-> READY
-> RUNNING
-> Blender mutation
-> scene snapshot
-> trusted validators
-> REVIEW
-> trusted receipt set complete
-> APPROVED
-> component ACCEPTED
```

No transition may use worker confidence as a substitute for a required trusted validator.

## Real Blender 5.1 proof

The release runtime suite must prove at minimum:

1. a component task pack with an explicit transform is executed at that transform;
2. `CENTER_BOTTOM` semantics place the primitive above its declared bottom origin;
3. `matrix_world` is current immediately after execution;
4. dimensions remain numerically correct;
5. a resolved Astera-style MATERIAL binding creates/assigns a real Blender material;
6. test-created objects, meshes, collections and materials clean up completely.

## Token acceptance

The correctness fixes must preserve the component-scoped context policy:

```text
BUILD <= 8000 estimated input tokens
REPAIR <= 4000 estimated input tokens
```

Reference attachment descriptors may be added without replacing the text budget with repeated full-image descriptions.

## Release acceptance

Benchmark 91 passes only when:

1. Benchmarks 87–90 remain green;
2. all v0.21 unit and integration negative controls pass;
3. the geometry-stage bypass is blocked;
4. generic-box fallback for tactile/slotted/recessed representations is blocked;
5. canonical component placement survives task compilation;
6. the envelope/seam negative controls fail as expected and known-good controls pass;
7. worker self-certification cannot approve strict tasks;
8. exact trusted receipts can approve strict tasks;
9. trusted approval persists `component.state=ACCEPTED`;
10. the Studio UI is asset-generic;
11. the Blender 5.1 runtime proof passes;
12. generated library/runtime-index artifacts are deterministic and committed cleanly.

## Architectural invariant

```text
PERSISTENT STATE
+ EXECUTABLE CONSTRAINTS
+ CANONICAL PLACEMENT
+ REPRESENTATION CONTRACT
+ CURRENT BLENDER MEASUREMENTS
+ TRUSTED REVISION-BOUND VALIDATION
= APPROVABLE COMPONENT
```

A green task queue without those properties is not production success.

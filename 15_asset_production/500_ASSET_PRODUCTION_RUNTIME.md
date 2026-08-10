# Asset Production Runtime

Status: vNext implementation contract

## Purpose

BlenderSkill MUST persist production truth outside the conversational context and outside the `.blend` file. The LLM plans or diagnoses; deterministic executors own state mutation, parameter resolution, task packing and validation.

## Canonical hierarchy

```text
PROJECT
  -> DESIGN_SYSTEM
  -> ASSET
  -> COMPONENT
  -> GEOMETRY / DETAIL / MATERIAL BINDINGS
```

An asset is not one opaque modeling task. It is a component tree with explicit local frames, anchors, relationships, constraints and stage state.

## Asset record

Minimum record:

```yaml
asset_id: ASSET-005
name: Lafar Street Bench 3470
revision: 17
stage: STRUCTURAL_GEOMETRY
design_system_ids: [LAFAR, ASTERA_CIVIC]
global_dimensions_mm: {width: 2000, depth: 550, height: 820, seat_height: 460}
components: {}
corrections: []
history: []
bindings: {}
```

`.blend` is an implementation artifact. This record is authoring truth.

## Component contract

Each component owns a local coordinate system and may contain children.

```yaml
id: BACKREST
parent: BENCH
state: CONSTRAINED
origin: {type: CENTER_BOTTOM}
dimensions:
  width: {expr: "FRAME.inner_width", unit: mm, locked: true}
  height: {value: 390, unit: mm, locked: true}
  thickness: {value: 72, unit: mm}
  angle: {value: 13, unit: deg, locked: true}
anchors:
  LEFT_MOUNT: {x: -765, y: 0, z: 0}
  RIGHT_MOUNT: {x: 765, y: 0, z: 0}
allowed_mutation_scope: [BACKREST]
```

Global dimensions do not replace component dimensions. Derived dimensions SHOULD use relations instead of duplicated literals.

## Assembly contract

Component assembly is defined by anchor relations, not prose.

```yaml
relations:
  - id: BACKREST_LEFT
    type: COINCIDENT
    a: BACKREST.LEFT_MOUNT
    b: LEFT_SUPPORT.BACKREST_MOUNT
    tolerance_mm: 0.5
```

Supported initial relation types:

- `COINCIDENT`
- `OFFSET`
- `ALIGNED_AXIS`
- `CLEARANCE`

A component task may not mutate siblings simply to hide an assembly error.

## Persistent corrections

Human review is converted into machine state.

```yaml
id: COR-018
component_id: DRAINAGE_CHANNEL
stage: BLOCKOUT
kind: PARAMETER_OVERRIDE
parameter: z
value: -12
unit: mm
priority: HARD
status: OPEN
```

Resolved corrections remain in history with `resolved_in_revision`.

## Stage model

Asset stages:

```text
BRIEF
REFERENCE_ANALYSIS
RECONSTRUCTION_MANIFEST
BLOCKOUT
STRUCTURAL_GEOMETRY
DETAILS
MATERIALS
GAME_READY
FIDELITY_AUDIT
APPROVED
```

Components additionally use the canonical reconstruction states already defined by `NODE_STATE_STORE`.

## Mutation isolation

Every worker task MUST include:

```yaml
asset_id
asset_revision
component_id
stage
allowed_to_modify
read_only
resolved_parameters
anchors
open_corrections
resolved_design_bindings
validation_contract
```

The worker is not given the entire library or conversation by default.

## Blender boundary

External runtime owns:

- asset/component state;
- constraints;
- corrections;
- design-system bindings;
- revisions;
- routing and task queue;
- evidence references.

Blender owns:

- current scene implementation;
- deterministic geometry execution;
- renders;
- scene/mesh measurements;
- export artifacts.

No `.blend` datablock may silently override a locked external constraint.

## Required executors

- `ASSET_STATE_RUNTIME`
- `PARAMETER_GRAPH`
- `DESIGN_BINDING_RESOLVER`
- `COMPONENT_TASK_PACK`
- existing `ASSEMBLY_INTEGRITY_GATE`
- existing reconstruction and appearance gates

## Token policy

Normal component iteration MUST route through a compact task pack. Full source echo, whole-library loading and unchanged scene/source rereads are forbidden unless a concrete diagnostic requires them.

Targets for reference-driven hard-surface work:

- routine component repair: <= 4k input tokens;
- component build task: <= 8k input tokens;
- asset-level planning pass: <= 15k input tokens;
- full-library snapshot: never loaded for normal execution.

# Production Studio Runtime

Status: v0.19.0 implementation contract

## Purpose

This layer turns the v0.18/vNext component runtime into a persistent production system. The canonical workflow state, reusable design resources, task queue, scene deltas and human corrections live outside Blender and outside conversational context.

## Runtime chain

```text
REFERENCE EVIDENCE REGISTRY
        +
VERSIONED DESIGN SYSTEM REPOSITORY
        +
PERSISTENT ASSET STATE
        |
        v
PARAMETER GRAPH + DESIGN BINDINGS
        |
        v
COMPONENT TASK PACK
        |
        v
PERSISTENT TASK QUEUE / LIFECYCLE
        |
        v
LLM PLAN OR DIAGNOSIS
        |
        v
DETERMINISTIC BLENDER EXECUTION
        |
        v
COMPACT SCENE COMPONENT SNAPSHOT
        |
        v
MUTATION SCOPE + VALIDATION GATES
        |
        v
REVIEW -> APPROVAL -> NEW REVISION
```

## Design-system repository

`DESIGN_SYSTEM_REPOSITORY` owns reusable resources such as materials, texture sets, edge profiles, trim profiles, LED profiles, decals, fasteners, geometry modules and node groups.

Required behavior:

- immutable resource revision snapshots;
- semantic resource version stored independently from repository revision;
- optimistic concurrency when updating resources;
- explicit locked-resource state;
- binding resolution by design-system ID and resource ID;
- reverse-usage records from resource -> asset -> component -> binding;
- impact report before a shared resource change is promoted.

A shared Astera LED or profile is therefore one versioned resource referenced by many assets rather than duplicated geometry/prose.

## Task lifecycle

`PRODUCTION_TASK_LIFECYCLE` uses these states:

```text
QUEUED
READY
RUNNING
REVIEW
APPROVED
BLOCKED
FAILED
CANCELLED
```

Dependencies must be approved before a task becomes `READY`. A worker result cannot enter `REVIEW` without a result record. `APPROVED` requires a result with `validation_status=PASS`.

`PRODUCTION_TASK_REPOSITORY` persists the queue using immutable queue revisions and rejects stale writers.

## Scene boundary

Normal agent work MUST NOT depend on full Blender scene dumps.

`SCENE_COMPONENT_SNAPSHOT` retains only stable production-relevant data:

- object ID;
- component ID;
- object type and parent;
- transform and dimensions;
- mesh metrics;
- material IDs;
- modifier stack summary;
- design binding IDs;
- anchor IDs;
- visibility state.

Snapshots have deterministic hashes. Structural diffs report added, removed and changed objects. Volatile UI/session state is excluded.

## Mutation isolation

`PRODUCTION_ITERATION_GATE` checks the worker iteration before review:

1. task is still `RUNNING`;
2. task input asset revision is not stale;
3. scene before/after snapshots exist;
4. every changed object belongs to `allowed_to_modify`;
5. required validators return `PASS` or `NOT_REQUIRED`.

A BACKREST repair that modifies SEAT must fail even if the final render looks acceptable.

## Reference evidence routing

`REFERENCE_EVIDENCE_REGISTRY` is queried by component, feature and optional view. The orchestrator sends only matching evidence records to the task pack.

A routed record may include:

```yaml
evidence_id
reference_id
component_id
view
authority
feature_ids
roi
artifact_id
registration_id
```

Whole concept sheets are not normal task context when component-specific ROI evidence exists.

## Studio UI model

`ASSET_STUDIO_VIEW_MODEL` joins, without changing source-of-truth ownership:

- asset identity, revision and stage;
- component tree and component states;
- task summary and selected-component tasks;
- open corrections;
- scoped scene objects;
- design-system impact records;
- scene snapshot hash.

`studio/asset_production_studio.html` is a standalone inspection shell for this view model. It supports component selection, stage overview, task queue inspection, reference evidence, corrections, bindings and scoped scene records.

## Required v0.19 executors

- `ASSET_STATE_RUNTIME`
- `ASSET_REPOSITORY`
- `PARAMETER_GRAPH`
- `DESIGN_BINDING_RESOLVER`
- `REFERENCE_EVIDENCE_REGISTRY`
- `COMPONENT_TASK_PACK`
- `ASSET_PRODUCTION_ORCHESTRATOR`
- `HARD_SURFACE_RECIPE`
- `BLENDER_HARD_SURFACE_BUILDER`
- `ASSEMBLY_ANCHOR_GATE`
- `DESIGN_SYSTEM_REPOSITORY`
- `PRODUCTION_TASK_LIFECYCLE`
- `PRODUCTION_TASK_REPOSITORY`
- `SCENE_COMPONENT_SNAPSHOT`
- `PRODUCTION_ITERATION_GATE`
- `ASSET_STUDIO_VIEW_MODEL`

## Token and context invariant

Component execution remains token-bounded:

- repair task <= 4k estimated input tokens;
- build task <= 8k estimated input tokens;
- asset planning <= 15k input tokens;
- `_FULL_LIBRARY.md` forbidden for routine component execution;
- full scene dump forbidden when a component snapshot is sufficient.

## Source-of-truth invariant

Conversation history, prompt text and `.blend` state are never the canonical production database. They may provide evidence or implementation output, but persistent asset/design/task repositories own production truth.

# Benchmark 89 — Lafar Production Studio v0.19 Regression

Status: canonical v0.19 release benchmark

## Objective

Prove that the Lafar street-bench workflow is no longer a long conversational modeling session. The production system must preserve reusable Astera resources, component-scoped work, task dependencies, scene deltas and validation state as machine-readable persistent records.

## Fixture

Primary asset fixture:

`tests/fixtures/lafar_street_bench_vnext.json`

The asset contains `BENCH`, `LEFT_SUPPORT`, `RIGHT_SUPPORT`, `SEAT` and `BACKREST` with relational dimensions, assembly anchors and Astera design bindings.

## Required v0.19 behavior

### 1. Design resource reuse

A shared design-system resource has one canonical identity and revision history. Reverse usage can answer which assets/components consume the resource before a change is promoted.

### 2. Persistent task queue

Production tasks are revisioned independently from the asset. A stale queue writer is rejected. Dependencies prevent BACKREST work from becoming ready before its required structural predecessors are approved.

### 3. Compact scene snapshots

The worker receives and returns component-relevant scene state rather than a full Blender dump. Snapshot hashes are deterministic. A structural diff identifies changed objects and fields.

### 4. Mutation scope

For a BACKREST task:

```text
allowed_to_modify = [BACKREST]
read_only includes LEFT_SUPPORT, RIGHT_SUPPORT, SEAT
```

Changing the BACKREST is valid. Changing BACKREST and SEAT in the same worker result must fail `PRODUCTION_ITERATION_GATE`.

### 5. Reference evidence routing

When the worker requests `BACKREST_PROFILE`, the orchestrator routes the BACKREST evidence ROI and does not include an unrelated SEAT ROI.

### 6. Review barrier

A task cannot enter `REVIEW` without a result. It cannot become `APPROVED` unless the iteration result records `validation_status=PASS`.

### 7. Studio view model

The UI view model must expose:

- asset ID, revision and stage;
- stage progression;
- component tree;
- task summary;
- selected component inspector;
- corrections;
- scoped scene objects;
- design-system impact information.

The standalone Studio HTML must consume this compact model instead of requiring direct access to the Blender scene or full library.

## Regression acceptance

Benchmark 89 passes only when:

1. Benchmark 88 relational dimensions and component scope remain valid;
2. design-system resource revision history is immutable;
3. reverse usage identifies affected assets;
4. stale resource writes are rejected;
5. task queue revisions are immutable and stale writes are rejected;
6. task dependencies gate readiness;
7. scene snapshot hashes are deterministic;
8. scene diff detects only changed production fields;
9. mutation outside `allowed_to_modify` fails;
10. stale asset revision fails the production iteration;
11. failing validation blocks review acceptance;
12. reference evidence is filtered by component/feature;
13. component repair remains within the 4k task-pack token target;
14. the production Studio view model can be built from the canonical records;
15. the real Blender hard-surface runtime suite remains green.

## Architectural invariant

```text
SHARED RESOURCE != COPIED DETAIL
TASK != CHAT TURN
SCENE SNAPSHOT != FULL .BLEND DUMP
REVIEW != VISUAL GUESS
APPROVAL != UNVALIDATED WORKER OUTPUT
```

A production decision must survive model changes, Blender restarts and future asset revisions without requiring reconstruction from conversation history.

# Benchmark 90 — Lafar Operational Production Studio v0.20 Regression

Status: canonical v0.20 release benchmark

## Objective

Prove that the v0.19 Production Studio architecture is operational rather than only inspectable. A user must be able to manage one asset, its components, reference evidence, corrections, tasks, scene snapshots and shared design resources through a persistent service/API without treating Blender state or conversation history as the database.

## Primary fixture

`tests/fixtures/lafar_street_bench_vnext.json`

The benchmark retains the Lafar street bench dimensions and component graph from Benchmarks 88–89 and exercises the operational service layer added in v0.20.

## Required v0.20 behavior

### 1. Persistent workspace operations

`PRODUCTION_STUDIO_SERVICE` must create/load an asset and initialize its task queue and reference-evidence registry. Restarting the service over the same filesystem root must reconstruct the same canonical state.

### 2. Optimistic concurrency

Writes to asset state, task queue, reference evidence, scene snapshots and shared design resources must use explicit expected revisions. Stale writes must fail with machine-readable conflict reasons instead of silently overwriting newer state.

### 3. Component-scoped Studio view

A Studio request for `BACKREST` must return a compact inspector containing only relevant component parameters, corrections, bindings, evidence and scene records. The UI must not require a full `.blend` dump or `_FULL_LIBRARY.md`.

### 4. Operational task flow

The service must support:

```text
create task -> dependency promotion -> READY -> RUNNING -> result -> REVIEW -> APPROVED
```

Task preparation must still respect the v0.19 token budgets and mutation scope.

### 5. Reference evidence persistence

`REFERENCE_EVIDENCE_REPOSITORY` must persist component/feature ROI evidence with immutable revisions. Updating or deleting evidence creates a new revision. BACKREST task preparation must route BACKREST evidence and exclude unrelated SEAT evidence.

### 6. Scene snapshot persistence

`SCENE_SNAPSHOT_REPOSITORY` stores compact production snapshots independently from `.blend`. A new snapshot revision must preserve immutable history and reject stale publication.

### 7. Blender measurement adapter

`BLENDER_SCENE_SNAPSHOT_ADAPTER` must read Blender 5.1 scene data without mutating it and emit the compact `SCENE_COMPONENT_SNAPSHOT` schema: component IDs, transforms, dimensions, mesh metrics, material IDs, modifier summaries, binding IDs, anchors and visibility.

### 8. Shared design resources

`DESIGN_STUDIO_SERVICE` must list versioned resources, update them through `DESIGN_SYSTEM_REPOSITORY` and expose impact information before a shared Astera resource change affects consuming assets.

### 9. HTTP boundary

`studio/server.py` must expose the operational service through a loopback-first JSON API. HTTP is an adapter only; production truth remains in the repositories.

### 10. Live GUI

`studio/asset_production_studio.html` must operate against the server API and support at minimum:

- asset selection and refresh;
- component selection;
- stage advancement;
- add/resolve correction;
- add/delete reference evidence;
- prepare task pack;
- create/promote/transition tasks;
- inspect runtime revisions and scoped scene state.

The offline JSON inspection mode may remain as fallback but is not the canonical operational path.

## Regression acceptance

Benchmark 90 passes only when:

1. Benchmarks 88–89 remain green;
2. asset/task/evidence/scene/design repositories preserve immutable revisions;
3. stale writes are rejected across repository boundaries;
4. the Studio service reconstructs state after a fresh process/service instance;
5. BACKREST Studio view remains component-scoped;
6. BACKREST repair task remains within the 4k estimated input-token target;
7. reference evidence routing excludes unrelated component ROIs;
8. the production task lifecycle cannot bypass validation/review rules;
9. the HTTP integration tests pass;
10. the Blender scene snapshot adapter passes in real Blender 5.1;
11. generated library/runtime artifacts are deterministic and committed cleanly.

## Architectural invariant

```text
GUI != SOURCE OF TRUTH
HTTP != SOURCE OF TRUTH
BLENDER != SOURCE OF TRUTH
CHAT != SOURCE OF TRUTH

PERSISTENT REPOSITORIES + VERSIONED CONTRACTS = SOURCE OF TRUTH
```

The v0.20 release is successful when the user can operate the production workflow from the Studio interface while the same deterministic runtime remains usable from CLI, tests or future desktop adapters.

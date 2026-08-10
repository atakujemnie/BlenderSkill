# Operational Production Studio API

Status: v0.20.0 implementation contract

## Purpose

v0.20 turns the v0.19 Production Studio model into an operational local workflow engine. The user-facing Studio, HTTP API, CLI adapters and Blender adapters all compose the same persistent repositories; none of those adapters owns canonical production truth.

## Runtime boundary

```text
ASSET REPOSITORY
TASK REPOSITORY
REFERENCE EVIDENCE REPOSITORY
SCENE SNAPSHOT REPOSITORY
DESIGN SYSTEM REPOSITORY
        |
        v
PRODUCTION STUDIO SERVICE / DESIGN STUDIO SERVICE
        |
        +--------------------+
        |                    |
        v                    v
LOCAL HTTP API          CLI / FUTURE DESKTOP
        |
        v
LIVE STUDIO GUI

BLENDER -> READ-ONLY SCENE SNAPSHOT ADAPTER -> SCENE SNAPSHOT REPOSITORY
```

## Production Studio service

`PRODUCTION_STUDIO_SERVICE` composes existing v0.19 executors and repositories. It must provide deterministic operations for:

- listing and creating assets;
- loading a component-scoped Studio view;
- adding/resolving corrections;
- advancing asset stages;
- creating production tasks;
- promoting dependency-ready tasks;
- task transitions and review lifecycle;
- preparing token-bounded component task packs;
- adding/removing reference evidence;
- publishing compact scene snapshots.

Every mutating operation must preserve optimistic concurrency. The service may not hide repository revision conflicts.

## Reference Evidence Repository

`REFERENCE_EVIDENCE_REPOSITORY` persists the validated evidence registry per asset.

Required behavior:

- immutable revision files plus current state;
- atomic writes;
- explicit asset ID safety;
- stale-writer rejection;
- evidence upsert and delete as new revisions;
- compatibility with `REFERENCE_EVIDENCE_REGISTRY` query semantics.

Whole source images remain external artifacts referenced by IDs/ROIs. The repository stores evidence metadata, not repeated image payloads.

## Scene Snapshot Repository

`SCENE_SNAPSHOT_REPOSITORY` persists compact scene snapshots produced by `SCENE_COMPONENT_SNAPSHOT` or the Blender adapter.

Required behavior:

- one current snapshot and immutable revision history per asset;
- atomic publish;
- expected scene revision checks;
- deterministic snapshot validation/hash preservation;
- no full `.blend` serialization.

## Blender Scene Snapshot Adapter

`BLENDER_SCENE_SNAPSHOT_ADAPTER` is a read-only Blender 5.1 data-API adapter. It must emit only production-relevant records:

```yaml
object_id
component_id
object_type
parent_id
transform
  location_mm
  rotation_rad
  scale
dimensions_mm
mesh_metrics
material_ids
modifier_stack
binding_ids
anchor_ids
visibility
```

The adapter must not mutate scene data while measuring it. Objects without `blenderskill_component_id` are excluded from production snapshots by default.

## Design Studio service

`DESIGN_STUDIO_SERVICE` exposes operational listing and versioned mutation of shared design-system resources. It must preserve the semantics of `DESIGN_SYSTEM_REPOSITORY`:

- immutable revisions;
- lock state;
- semantic resource versions;
- optimistic concurrency;
- reverse usage;
- impact inspection before shared changes.

A GUI edit to an Astera LED/profile is therefore a repository revision, not an untracked Blender change.

## HTTP API

`studio/server.py` is a loopback-first JSON adapter over the service layer.

Rules:

1. HTTP handlers must delegate domain behavior to service/executor functions.
2. Repository roots must be explicit and local by default.
3. Errors must return machine-readable JSON and appropriate HTTP status classes.
4. Request bodies must be bounded and parsed as JSON.
5. The server must not become a second persistence implementation.
6. Asset/task/reference/scene/design-resource routes must expose runtime revision data required for optimistic writes.

## Live Studio GUI

`studio/asset_production_studio.html` is the operational UI for asset production. It should use the HTTP API for live mode and retain offline JSON loading only as a fallback inspection mode.

The UI is expected to surface:

- asset selector and asset/stage state;
- component tree;
- component inspector;
- resolved parameters and bindings;
- corrections;
- reference evidence;
- task queue and task state actions;
- scene snapshot records;
- runtime revision counters;
- task-pack preparation metrics.

`studio/design_system_studio.html` provides the corresponding shared-resource view and mutation surface.

## Required v0.20 executors

- `REFERENCE_EVIDENCE_REPOSITORY`
- `SCENE_SNAPSHOT_REPOSITORY`
- `BLENDER_SCENE_SNAPSHOT_ADAPTER`
- `PRODUCTION_STUDIO_SERVICE`
- `DESIGN_STUDIO_SERVICE`

They depend on the released v0.19 asset-production executors rather than replacing them.

## Token policy

The service layer must not expand context merely because a GUI/API exists. v0.19 limits remain mandatory:

- repair task <= 4k estimated input tokens;
- build task <= 8k;
- asset planning <= 15k;
- no full-library loading for routine component execution;
- no full scene dump where compact snapshot suffices;
- reference evidence routed by IDs/ROIs/features instead of whole-image repetition.

## Source-of-truth invariant

The canonical state hierarchy is:

```text
PERSISTENT REPOSITORIES
    > SERVICE/API REPRESENTATION
    > GUI STATE
    > BLENDER IMPLEMENTATION STATE
    > CONVERSATION HISTORY
```

Lower layers may display or execute higher-level decisions, but may not silently override them.

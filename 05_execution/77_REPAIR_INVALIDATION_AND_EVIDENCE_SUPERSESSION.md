# Repair Invalidation and Evidence Supersession

## Purpose

A repair to an accepted host invalidates more than that host's mesh.

The v0.11 lamp repair changed the `ARM` / `SENSOR_MODULE` junction after the asset had already accumulated green node, appearance and final fidelity evidence. Without dependency invalidation, old evidence can remain green for geometry that no longer exists.

## Fundamental rule

```text
accepted geometry changes
-> old node revision is no longer canonical
-> downstream geometry/evidence depending on it cannot stay ACCEPTED/PASS silently
```

## Canonical propagation

For a changed Shape Node:
1. increment the node revision;
2. mark the changed node `DIRTY`;
3. walk child + `depends_on` reverse edges;
4. mark already-built downstream nodes `DIRTY`;
5. mark not-yet-built downstream nodes `BLOCKED`;
6. invalidate Appearance Owners hosted by any affected node;
7. mark evidence records tied to affected node/owner revisions `SUPERSEDED`;
8. invalidate RDL/fidelity barriers that depended on superseded evidence;
9. preserve unrelated accepted branches.

## Example

```text
ARM repair
├── SENSOR_MODULE         -> DIRTY
│   └── SENSOR_LENS       -> BLOCKED/DIRTY
├── HEAD_ACCENT_CHANNEL   -> DIRTY
├── EDGE_LANGUAGE         -> DIRTY
└── SURFACE_FINISH        -> DIRTY

BASE                     -> remains ACCEPTED
```

## Evidence lifecycle

Never delete old evidence. Mark it:

```yaml
status: SUPERSEDED
superseded_by: repair:arm_sensor_seam
```

This preserves traceability and prevents stale green reports from being reused.

## Replay

A deterministic replay may rebuild affected nodes from frozen inputs, but it must generate new revision-bound evidence. Replaying a build does not reactivate superseded proof.

## Canonical executor

`executors/dependency_invalidator.py`

Skill ID: `DEPENDENCY_INVALIDATOR`.

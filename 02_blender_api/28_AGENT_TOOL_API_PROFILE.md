# Agent Tool API Profile

## Purpose

This file defines the capability contract an autonomous Blender agent must satisfy before it is allowed to mutate a production scene.

It separates:

```text
semantic skill
-> required capability
-> concrete connected tool
-> Blender API / BMesh execution
-> verification
```

The agent must never invent connector/tool names. It discovers and binds the tools available in the current runtime.

## Profile ID

```text
BLENDER_AGENT_TOOL_PROFILE_V1
```

## Required capabilities

### C1 — `scene_inspect`
Read-only access to the current Blender state.

Must support enough information to determine:
- Blender version;
- active scene;
- object inventory;
- object type/name/transform/dimensions;
- active object and mode;
- collections/hierarchy;
- mesh statistics where practical;
- materials/modifiers where practical.

Risk class: `READ_ONLY`.

### C2 — `python_execute`
Execute controlled Python in Blender with access to `bpy`; BMesh is required for skills that declare it.

Must support:
- deterministic script execution;
- exception reporting;
- access to `bpy.data` and scene data;
- explicit context inspection;
- return of compact structured diagnostics.

Risk class: `SCENE_WRITE`.

### C3 — `visual_capture`
Produce a render, viewport screenshot, or equivalent image used for QA.

Must permit stable camera/view selection or a scripted alternative.

Risk class: `READ_ONLY_OR_RENDER_SIDE_EFFECT`.

### C4 — `save_checkpoint`
Save a recoverable Blender source checkpoint or equivalent scene state.

Risk class: `FILE_WRITE`.

### C5 — `export_asset`
Export the requested runtime artifact when the current task reaches EXPORT.

Risk class: `FILE_WRITE`.

### C6 — `file_verify`
Verify that an exported file exists and, where the integration permits it, inspect enough metadata/content to confirm export success.

Risk class: `READ_ONLY`.

## Optional capabilities

### O1 — `ui_operator`
Mouse/keyboard/UI/operator automation.

This is never preferred over `python_execute` for deterministic mesh work. Use only when the required operation is unavailable or materially less reliable through data/BMesh APIs.

### O2 — `reference_image_access`
Direct access to reference images/files for reconstruction and QA.

### O3 — `external_diff`
Image-diff or mesh-diff capability outside Blender.

## Runtime binding record

At the beginning of a session, bind actual connected tools to semantic capabilities:

```yaml
agent_tool_profile:
  profile_id: BLENDER_AGENT_TOOL_PROFILE_V1
  blender_version: "5.1.x"
  bindings:
    scene_inspect:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    python_execute:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
      bpy: true
      bmesh: true
    visual_capture:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    save_checkpoint:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    export_asset:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
    file_verify:
      tool: ACTUAL_DISCOVERED_TOOL_NAME
      verified: true
```

Never fill `ACTUAL_DISCOVERED_TOOL_NAME` from memory or assumption.

## Capability states

Each capability is one of:

```text
UNKNOWN
DISCOVERED
TESTED
BOUND
FAILED
UNAVAILABLE
```

Mutation requires:

```text
scene_inspect = BOUND
python_execute = BOUND
```

Reference reconstruction that depends on image comparison additionally requires:

```text
visual_capture = BOUND
```

Export completion additionally requires:

```text
export_asset = BOUND
file_verify = BOUND
```

If a required capability is missing, the agent must return a capability blocker instead of improvising a different execution path silently.

## Preflight sequence

Before the first production mutation:

```text
1. discover tool schemas/capabilities
2. create Tool Registry
3. bind semantic capabilities
4. perform read-only scene inspection
5. verify Blender version and mode
6. run a minimal non-production capability test where needed
7. save profile state for the session
8. only then enter scene mutation
```

Do not rediscover unchanged capabilities before every operation.

## Minimal Python execution test

A safe initial test should be read-only where possible:

```python
import bpy
import bmesh

result = {
    "blender_version": bpy.app.version_string,
    "scene": bpy.context.scene.name if bpy.context.scene else None,
    "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
    "mode": bpy.context.mode,
    "bmesh_available": bmesh is not None,
}
```

This does not prove every modeling operation works, but verifies the critical Python/BMesh foundation.

## Tool-selection hierarchy

For equivalent outcomes prefer:

```text
1. read-only scene inspection
2. direct bpy.data / RNA
3. BMesh
4. non-destructive modifier configuration
5. controlled bpy.ops with explicit context
6. UI emulation
```

This ordering can be overridden only when a narrower method is demonstrably less reliable for the specific operation.

## Operation binding example

For `HS_PANEL_LINE`:

```yaml
operation_binding:
  skill_id: HS_PANEL_LINE
  requires:
    - scene_inspect
    - python_execute
  preferred_execution:
    - bpy_data
    - bmesh
    - modifiers
  verification:
    - evaluated_geometry
    - topology_report
    - optional_visual_capture
```

For `SUBD_TOPOLOGY_CONTROL`:

```yaml
operation_binding:
  skill_id: SUBD_TOPOLOGY_CONTROL
  requires:
    - scene_inspect
    - python_execute
  verification:
    - control_cage_metrics
    - evaluated_subdivision_metrics
    - optional_visual_capture
```

For `RECONSTRUCT_REFERENCE`:

```yaml
operation_binding:
  skill_id: RECONSTRUCT_REFERENCE
  requires:
    - scene_inspect
    - python_execute
    - visual_capture
  optional:
    - reference_image_access
    - external_diff
```

## Context-sensitive operators

If `bpy.ops` is required, the execution adapter must explicitly control:
- active object;
- selection;
- object/edit mode;
- scene/view layer;
- area/region context if applicable;
- operator poll result where applicable.

Prefer `bpy.context.temp_override(...)` when an override is required.

A failed operator must not be retried with the same unknown context repeatedly.

## Session persistence

The Tool Registry and this runtime binding should be cached for the current integration/version/session.

Invalidate the binding when:
- Blender version changes;
- connector schema changes;
- required capability starts failing;
- a tool returns output inconsistent with its recorded contract;
- a new session does not guarantee preserved connection state.

## Completion status

The agent reports one of:

```text
PROFILE_BOUND
PROFILE_PARTIAL
PROFILE_BLOCKED
```

`PROFILE_PARTIAL` may permit analysis/planning but not all mutations/export stages.

## Fundamental rule

Knowledge does not imply capability.

A skill may explain exactly how to build a feature, but the agent must still prove that the current connected runtime exposes the tools required to execute and verify that feature.

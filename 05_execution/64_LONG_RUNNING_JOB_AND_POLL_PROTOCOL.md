# Long-Running Blender Job and Poll Protocol

## Purpose

Expensive Blender operations such as AO bake, high-resolution bake, export and heavy Geometry Nodes evaluation may outlive a tool/MCP request timeout.

A transport timeout is not the same thing as a Blender failure.

Without this distinction an agent may launch the same expensive operation multiple times, corrupt state, overwrite outputs or waste large amounts of time/tokens.

---

# Core rule

```text
REQUEST TIMEOUT != PROVEN JOB FAILURE
```

After timeout:

```text
inspect state/artifacts
-> classify RUNNING / FINISHED / FAILED / UNKNOWN
-> only retry if FAILED or proven absent
```

Do not immediately execute the same expensive operation again.

---

# Job record

For a long-running stage maintain a compact record:

```yaml
job:
  id: BOLLARD_BAKE_ORM_001
  stage: BAKE
  operation: AO
  status: RUNNING
  started_at:
  expected_outputs:
    - aster_bollard_tmp_ao
  checkpoint_before:
  dirty_channels:
    - orm_ao
  last_error:
```

Status vocabulary:

```text
PENDING
RUNNING
FINISHED
FAILED
CANCELLED
UNKNOWN
```

---

# Evidence order after timeout

Check in this order:

1. explicit runtime/job status if the integration exposes one;
2. Blender scene/image state;
3. expected image/file existence and modification time;
4. compact output validation;
5. only then consider rerunning.

If output exists but its validity is uncertain, validate it. Do not recompute it merely to gain confidence.

---

# Blender threading caution

Do not move normal `bpy` scene mutation/bake logic into arbitrary Python background threads just to avoid an MCP timeout.

Blender API operations are generally expected to run in Blender's main execution context. Use mechanisms compatible with the active runtime, for example:
- supported timer/modal workflow;
- controlled external Blender process;
- integration-provided async job mechanism;
- synchronous execution followed by artifact/status inspection when transport timeout is possible.

Do not invent asynchronous capabilities that the connected tool does not expose.

---

# Channel checkpoints

Expensive multi-channel bake should checkpoint after each accepted channel:

```text
BaseColor PASS
Normal PASS
AO PASS
Roughness PASS
Metallic PASS
Emissive PASS
```

If Emissive later fails, do not destroy/recompute accepted BaseColor/Normal/AO unless a changed dependency invalidates them.

Use `05_execution/65_INCREMENTAL_DIRTY_STAGE_CACHE.md`.

---

# Retry policy

For an expensive job:
- at most one launch while state is `RUNNING` or `UNKNOWN`;
- timeout triggers inspection, not retry;
- proven `FAILED` may use one corrected retry of the same strategy;
- second proven failure requires strategy switch according to the global retry protocol.

---

# Compact polling

Poll only decision-grade state:

```yaml
job_status:
  id: BOLLARD_BAKE_AO_001
  status: FINISHED
  output_exists: true
  output_validation: PASS
  elapsed_s: 41.2
```

Do not return render logs, complete image arrays or full Blender console output during normal polling.

---

# Completion

A long-running job is complete only when:
- Blender/tool status is finished or artifact evidence proves completion;
- expected artifact exists;
- semantic validator accepts it;
- job state is persisted.

File existence without semantic validation is not enough.

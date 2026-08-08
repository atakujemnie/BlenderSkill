# Pipeline DAG Executor and Stage Reuse

## Purpose

`Incremental Dirty-Stage Cache` is not optional advice. The agent must execute the smallest dependency closure required by the current repair.

A manual sequence such as:

```text
build -> decals -> bake all -> export -> import -> test
```

is forbidden when some stages are already clean and independent.

## Canonical DAG

A typical hard-surface runtime asset may use:

```text
REFERENCE/CONTRACT
      |
   BUILD_GEOMETRY
      |\
      | UV_CONTRACT
      |    |
      | BAKE_CHANNELS
      |    |
DECAL_ASSET   RUNTIME_MATERIAL
      \       /
       PACKAGE_EXPORT
            |
     EXPORT_ROUNDTRIP
            |
      CATALOG_REGISTER
            |
       ENGINE_SMOKE_TEST
            |
      COMPLETION_GATE
```

Project profiles may override dependencies, but the dependency graph must be explicit.

## Stage record

```yaml
stage:
  id: BAKE_AO
  dependencies:
    - BUILD_GEOMETRY
    - UV_CONTRACT
    - AO_ISOLATION_PROFILE
  outputs:
    - TEXTURE_ORM_R
  signature: ...
  status: PASS
  dirty: false
```

## Execution planner

Before any non-trivial rebuild emit:

```yaml
execution_plan:
  changed_inputs:
    - UNDER_RIM_PROFILE
  dirty:
    - BUILD_GEOMETRY
    - BAKE_AO
    - BAKE_NORMAL
    - PACKAGE_EXPORT
    - EXPORT_ROUNDTRIP
    - ENGINE_SMOKE_TEST
  reuse:
    - DECAL_ASSET
    - BASECOLOR
    - ROUGHNESS
    - METALLIC
    - EMISSIVE
```

Then execute only the dirty topological order.

## Geometry change does not mean all textures are dirty

A geometry edit dirties channels only through declared dependencies.

Examples:
- tangent normal from geometry/procedural bump: likely dirty;
- AO: dirty;
- position-dependent dirt mask: dirty;
- constant/UV-authored metallic: normally clean;
- separate decal atlas: normally clean;
- emissive mask on unchanged diffuser UV/geometry: may remain clean.

When uncertain, mark the specific dependency `UNVERIFIED`; do not automatically execute every stage.

## Runtime binding/cache change

A stale Blender image datablock dirties:

```text
RUNTIME_IMAGE_BINDING
BAKED_RUNTIME_QA
```

It does **not** dirty the accepted texture file itself.

Expected repair:

```text
reload/synchronize image -> QA
```

not:

```text
rebake all maps
```

## Runtime-root change

Correcting export destination from one filesystem tree to another normally dirties:
- package copy/export destination;
- package readback;
- catalog path verification;
- engine smoke test.

It does not by itself dirty geometry or baked pixels if the accepted artifacts can be copied/re-exported without recomputation.

## Cache signatures

Use narrow signatures:
- geometry parameters/hash;
- UV contract ID;
- channel graph/parameter hash;
- decal source hash;
- runtime profile ID;
- export packaging profile ID;
- runtime asset root ID.

Do not hash the entire scene for every stage.

## No implicit top-level side effects

A stage runner may import stage modules only if they are import-safe.

Every production mutation must be behind an explicit callable entry point.

## Failure semantics

If stage `X` fails:
- dependents of `X` remain blocked/dirty;
- independent previously accepted stages remain clean;
- repair `X` or its failed dependency;
- rerun only the affected closure.

## Metrics

Track:

```text
stages_executed
stages_reused
expensive_stages_reused
full_pipeline_restarts
channels_rebaked
```

For an accepted hard-surface asset, `full_pipeline_restarts` after a local repair should normally be zero.

## Candidate executor

Use `executors/pipeline_dag.py` for deterministic dependency closure/planning when its contract fits the project.

The executor plans work; asset-specific stage callables remain owned by the project.
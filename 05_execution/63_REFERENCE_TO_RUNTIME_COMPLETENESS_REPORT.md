# Reference-to-Runtime Completeness Report

## Purpose

At the end of an asset task the agent must produce a compact, machine-readable report that distinguishes:
- reference fidelity;
- authoring-model completeness;
- game-ready completeness;
- project integration.

This report replaces vague endings such as "asset finished".

It also records execution efficiency so benchmark runs can compare library versions.

---

# Required report

```yaml
asset_report:
  asset_id: SM_EXAMPLE
  target_completion_level: GAME_READY_COMPLETE
  highest_passed_level: MODELING_COMPLETE

  completion:
    reconstruction: PASS
    modeling: PASS
    game_ready: FAIL
    pipeline_integrated: NOT_REQUIRED

  geometry:
    dimensions_mm: [210, 210, 1050]
    tris:
      LOD0: 2716
      LOD1: 1152
      LOD2: 480
      LOD3: 128
    collision_tris: 88
    mesh_validation: PASS

  surface:
    uv: PASS
    material_segmentation: PASS
    bake_gate: FAIL
    runtime_textures: MISSING
    emissive_authoring: PASS
    emissive_runtime: UNVERIFIED

  export:
    files_exist: true
    post_export_validation: PASS

  integration:
    asset_catalog: NOT_DONE

  blockers:
    - PBR_BAKE_NOT_DONE

  known_deviations: []
  deferred_features: []

  efficiency:
    approximate_tokens: 60000
    tool_calls: null
    failed_tool_calls: null
    retries: null
    broad_reference_rescans: null
```

Unknown metrics should be `null`, not invented.

---

# Fidelity section

For reconstruction-driven work include:
- locked dimensions and deviation;
- silhouette/multi-view status;
- known source conflicts;
- intentionally inferred geometry;
- human/reference-critical deviations.

Do not restate the full Evidence Ledger. Summarize only accepted facts and unresolved issues.

---

# Surface completeness

The report must distinguish:

```text
MATERIAL_LOOKDEV_PASS
TEXTURE_BAKE_PASS
RUNTIME_MATERIAL_BINDING_PASS
```

These are separate gates.

A procedural material that looks good in Blender may pass lookdev and still fail runtime completion.

---

# Emissive completeness

Report separately:

```yaml
emissive:
  geometry_mask_authoring: PASS
  blender_preview: PASS
  exported_data: PASS
  engine_bloom_tonemapping: UNVERIFIED
```

Do not claim final glow fidelity when only the Blender lookdev was tested.

---

# Pipeline integration

If the asset is exported but not registered in the project's asset catalog/database:

```text
pipeline_integrated = FAIL or NOT_REQUIRED
```

depending on the requested target.

Do not hide the distinction in prose.

---

# Efficiency metrics

For benchmark-capable runs record when available:
- total token usage;
- tokens before first blockout;
- tool calls;
- failed calls;
- repeated strategy attempts;
- raw outputs above Tool Output Budget;
- full-source echoes;
- full-reference rescans;
- number of localized repair cycles;
- time-to-first-valid-blockout;
- time-to-target-completion.

The purpose is to detect a system that becomes more verbose without becoming more capable.

---

# Completion wording

Allowed:

> Modeling complete; game-ready completion is blocked by texture bake and runtime material binding.

Not allowed:

> Asset complete.

when required downstream gates remain unfinished.

---

# Benchmark comparison

When comparing agent/library versions, prioritize in order:
1. no regression of MUST reference fidelity;
2. no regression of runtime correctness;
3. fewer unrecovered failures;
4. fewer repeated operations;
5. lower context/token cost;
6. lower wall-clock/tool cost.

Efficiency gains never justify losing protected features.

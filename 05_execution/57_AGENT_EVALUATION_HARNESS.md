# Agent Evaluation Harness

Biblioteka powinna być testowana na benchmarkach, a nie oceniana wyłącznie opisowo.

## Benchmark classes

### B1 — Primitive fidelity
Zbuduj asset z dokładnymi wymiarami i kilkoma cechami MUST.
Mierzy precision, naming, transforms, idempotency.

### B2 — Reference fidelity
Zbuduj hard-surface prop z front/side/top.
Mierzy silhouette, proportions, feature retention.

### B3 — Repair
Dostarcz celowo wadliwy asset.
Mierzy scene inspection, local patch, regression avoidance.

### B4 — API trap
Ustaw zły active object/Edit Mode/selection, unsaved `.blend` i version-sensitive API differences.
Mierzy context safety, runtime discovery i path stability.

### B5 — Optimization
Dostarcz zbyt ciężki asset.
Mierzy protected-feature retention, LOD generation, triangle reduction bez ślepego Decimate.

### B6 — Export
Dostarcz hierarchy + materials + texture/animation references as applicable.
Mierzy transform/export/readback i survival runtime bindings.

### B7 — End-to-end asset completion

```text
reference -> reconstruction -> modeling -> surface -> bake/runtime closure
-> LOD/collision -> export -> completion -> optional catalog integration
```

Canonical first B7:
- `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`.

### B8 — Bake/runtime closure regression

Start from accepted geometry/material authoring state and require Level C game-ready closure.

```text
UV contract -> dirty-channel plan -> bake -> bake validation
-> runtime material -> package export/readback -> baked-runtime QA
```

Measures:
- bake cancellation/target binding;
- BaseColor/Metallic/Emissive semantics;
- AO isolation;
- UV/LOD stability;
- foreign decal UV separation;
- clean channel reuse;
- long-job timeout handling;
- import-safe helper behavior;
- runtime package correctness.

Canonical B8:
- `07_examples/75_LAFAR_CIVIC_BOLLARD_BAKE_REGRESSION_BENCHMARK.md`.

### B9 — Pipeline integration proof and infrastructure reuse

Start from a Level C/game-ready exported asset and require truthful `PIPELINE_INTEGRATED`.

```text
canonical runtime root
-> package/round-trip invariants
-> catalog registration
-> target engine loader/test
-> trustworthy test oracle
-> completion gate with evidence kind
```

Measures:
- stale Blender image datablock detection without unnecessary rebake;
- canonical engine-visible asset-root reuse;
- absence of lookalike-root writes;
- final exported hard dimensions/contact datum;
- Blender round-trip kept separate from engine proof;
- engine loader/test actually resolves the final artifact;
- direct executable exit status rather than formatter/pipeline status;
- controlled bite-test validity for new assertions;
- Pipeline DAG stage reuse after local repairs;
- zero repeated build-system discovery when a matching project profile exists.

Canonical v0.7 B9:
- `07_examples/76_LAFAR_CIVIC_BOLLARD_PIPELINE_INTEGRATION_REGRESSION_BENCHMARK.md`.

## Metrics

Quality/runtime:
- MUST pass rate;
- hard dimension/contact error after export;
- silhouette/reference deviation;
- triangle count per LOD;
- collision cost;
- bake/runtime material status;
- BaseColor/Normal/ORM/Emissive semantic validation;
- image cache coherence status;
- UV contract status;
- package node/material/image readback;
- runtime asset root status;
- engine loader status/evidence kind;
- test oracle status;
- completion level;
- runtime contract violations;
- human visual score when available.

Efficiency:
- total/stage token usage;
- tool calls and Blender mutation calls;
- failed tool calls/retries/strategy switches;
- broad reference rescans;
- complete code echoes after artifact creation;
- full multichannel bake runs;
- channels rebaked;
- stages executed vs reused;
- full pipeline restarts;
- project profile rediscovery calls;
- build-system discovery calls;
- test runs and invalid/ambiguous test results;
- expensive jobs relaunched after timeout;
- time to requested completion.

Unknown metrics remain `null`; do not invent them.

## Najważniejsze metryki agenta

1. `MUST pass rate`
2. `reference/runtime correctness`
3. `regressions per repair`
4. `failed API/tool calls`
5. `completion truthfulness`
6. `token/context efficiency at equal quality`
7. `full-stage recomputes avoided`
8. `baked-runtime package correctness`
9. `runtime-root correctness`
10. `engine-proof/test-oracle integrity`

## Release gate biblioteki

Nowa wersja nie jest lepsza tylko dlatego, że ma więcej treści.

Release passes only if benchmark evidence shows at least one of:
- higher quality with comparable cost;
- lower cost with no quality regression;
- elimination of a previously observed failure class;
- stronger proven completion level without breaking protected features.

## Efficiency comparison rule

Token reduction is secondary to fidelity and runtime correctness.

Known Bollard evidence:
- first full baseline: ~60k tokens;
- captured v0.5 B8 continuation: ~36k tokens before full closure;
- final continuation after that: user-reported ~45k additional tokens;
- combined post-v0.5 continuation cost: roughly ~81k tokens.

Preferred v0.6 B8 target for an equivalent accepted hard-surface game-ready finish:

```yaml
stage_tokens: <= 15000
blender_python_mutation_calls: <= 10
full_multichannel_bake_runs: <= 2
accepted_silent_cancelled_bakes: 0
missing_uv_contracts: 0
baked_runtime_qa_required: true
```

Preferred v0.7 B9 target once Level C is already accepted and a matching project profile exists:

```yaml
pipeline_integration_tokens: <= 10000
project_profile_rediscovery_calls: 0
ambiguous_runtime_root_writes: 0
false_green_test_results: 0
blender_import_used_as_level_d_proof: 0
full_pipeline_restarts_after_local_repair: 0
engine_evidence_kind_required: true
```

These are benchmark goals, not universal limits.
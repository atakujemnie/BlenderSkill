# Agent Evaluation Harness

Biblioteka powinna być testowana na benchmarkach, a nie oceniana wyłącznie opisowo.

## Benchmark classes

### B1 — Primitive fidelity
Zbuduj asset z dokładnymi wymiarami i kilkoma cechami MUST.

Mierzy:
- precision,
- naming,
- transforms,
- idempotency.

### B2 — Reference fidelity
Zbuduj hard-surface prop z front/side/top.

Mierzy:
- silhouette,
- proportions,
- feature retention.

### B3 — Repair
Dostarcz celowo wadliwy asset.

Mierzy:
- scene inspection,
- local patch,
- regression avoidance.

### B4 — API trap
Ustaw:
- zły active object,
- Edit Mode,
- nietypową selection,
- unsaved `.blend`,
- render-engine/property differences covered by compatibility preflight.

Mierzy:
- odporność na context,
- version/runtime discovery,
- path stability.

### B5 — Optimization
Dostarcz zbyt ciężki asset.

Mierzy:
- czy agent redukuje koszt bez utraty MUST,
- czy nie używa bezmyślnie Decimate,
- czy potrafi generować LOD parametrycznie,
- czy protected features przeżywają redukcję.

### B6 — Export
Dostarcz hierarchy + materials + animation/texture references as applicable.

Mierzy:
- poprawność transform,
- export,
- post-export verification,
- survival of decals/material/texture bindings.

### B7 — End-to-end asset completion

Dostarcz technical concept sheet + brief i wymagaj assetu game-ready.

Mierzy cały pipeline:

```text
reference
-> reconstruction
-> modeling
-> surface
-> bake/runtime material closure
-> LOD/collision
-> export
-> completion report
-> optional catalog integration
```

Required checks:
- truthful completion level;
- material not left Blender-only without runtime disposition;
- emissive authoring separated from runtime glow;
- supplied branding source preserved;
- no hidden floating feature;
- no destructive build-script import side effects;
- reusable executors preferred over duplicate ad-hoc helpers.

Canonical v0.5 B7 benchmark:
- `07_examples/74_LAFAR_CIVIC_BOLLARD_BENCHMARK.md`.

## Metrics

Quality/runtime:
- feature pass rate,
- MUST regression count,
- dimension error,
- silhouette/reference deviation,
- triangle count per LOD,
- collision cost,
- material slot count,
- bake/runtime material status,
- exported texture/decal survival,
- completion level reached,
- runtime contract violations,
- human visual score when available.

Efficiency:
- total token usage,
- tokens before first valid blockout,
- number of tool calls,
- number of failed tool calls,
- retry count,
- strategy switches,
- broad reference rescans,
- raw outputs exceeding Tool Output Budget,
- complete source-code echoes after artifact creation,
- repair iterations,
- time-to-valid-blockout,
- time-to-target-completion.

Unknown metrics remain `null`; do not invent them after the run.

## Najważniejsze metryki agenta

1. `MUST pass rate`
2. `reference/runtime correctness`
3. `regressions per repair`
4. `failed API calls`
5. `tool calls per accepted feature`
6. `completion truthfulness`
7. `token/context efficiency at equal quality`

## Release gate biblioteki

Nowa wersja biblioteki nie powinna być uznana za lepszą tylko dlatego, że ma więcej treści.

Release passes only if benchmark evidence shows at least one of:
- higher quality with comparable cost;
- lower cost with no quality regression;
- elimination of a previously observed failure class;
- higher completion level without breaking protected reference features.

## Efficiency comparison rule

Token reduction is secondary to fidelity and runtime correctness.

For the Lafar Civic Bollard baseline (~60k tokens), v0.5 targets at least 35% reduction on an equivalent run, with preferred total <=35k and no visual/runtime regression.

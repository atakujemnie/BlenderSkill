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
- nietypową selection.

Mierzy:
- odporność na context.

### B5 — Optimization
Dostarcz zbyt ciężki asset.

Mierzy:
- czy agent redukuje koszt bez utraty MUST,
- czy nie używa bezmyślnie Decimate.

### B6 — Export
Dostarcz hierarchy + materials + animation.

Mierzy:
- poprawność transform,
- export,
- post-export verification.

## Metrics

- feature pass rate,
- MUST regression count,
- dimension error,
- triangle count,
- material slot count,
- number of tool calls,
- number of failed tool calls,
- repair iterations,
- bytes/tokens instrukcji załadowanych do zadania,
- time-to-valid-asset.

## Najważniejsze metryki agenta

1. `MUST pass rate`
2. `regressions per repair`
3. `failed API calls`
4. `tool calls per accepted feature`
5. `reference deviation`
6. `runtime contract violations`

## Release gate biblioteki

Nowa wersja biblioteki nie powinna być uznana za lepszą tylko dlatego, że ma więcej treści.
Musi poprawiać wynik benchmarków albo zmniejszać koszt przy tej samej jakości.

# Tool Call and Token Efficiency

## Cel

Minimalizuj:
- liczbę wywołań API,
- powtarzane inspekcje,
- duże logi,
- iteracyjne mikroruchy,
- generowanie kodu dla operacji, które można wykonać parametrycznie,
- przesyłanie do LLM danych, które mogą zostać zagregowane lokalnie.

Efektywność nie oznacza pomijania walidacji. Oznacza wykonywanie obliczeń tam, gdzie są najtańsze, i zwracanie modelowi tylko informacji potrzebnej do decyzji.

## Zasada batch

Jedno wywołanie powinno wykonywać logicznie spójny etap:
- stworzenie blockoutu,
- dodanie zestawu głównych modifierów,
- audit,
- generacja renderów kontrolnych.

Nie łącz w jednym batchu etapów o różnym ryzyku.

## Zasada inspect-before-act

Nie próbuj kolejnych losowych operatorów.
Najpierw odczytaj:
- mode,
- active object,
- modifier stack,
- mesh stats,
- dimensions.

## Zasada parameterize

Zamiast 20 poleceń:
`move vertex A, move vertex B...`

Utwórz parametry:
```python
WIDTH = 1.8
DEPTH = 0.55
HEIGHT = 0.82
FRAME = 0.04
BEVEL = 0.006
```

Buduj z nich geometrię.

## Zasada local patch

Przy błędzie napraw tylko:
- feature,
- obiekt,
- modifier,
- region.

Nie przebudowuj całego assetu, jeżeli problem jest lokalny.

# Tool Output Budget

## Core rule

```text
compute locally -> aggregate -> return decision-grade summary
```

Tool output is part of the context budget. A tool must not return a raw dataset merely because it can.

Default tool response should normally fit in a compact structured summary. Large diagnostic output requires a specific failing ROI/object/feature and explicit justification.

## Never return by default

Do not send to the language model:
- full pixel arrays or image buffers;
- one measurement per image row/column when aggregate statistics are sufficient;
- full vertex/edge/face coordinate dumps;
- complete RNA/property trees;
- complete scene inventories when a filtered subset answers the question;
- hundreds of unchanged samples;
- all threshold candidates from image analysis;
- repeated tool output that has not changed;
- entire source/build scripts when only a naming/path/material convention is needed.

## Preferred compact diagnostics

Return:
- operation/status;
- affected IDs/objects;
- key before/after metrics;
- aggregate error/deviation;
- confidence;
- failing ROI/feature if any;
- warnings/error code;
- next diagnostic target.

Example:

```yaml
status: PASS
view: FRONT
body_width_px: 70
body_width_variance_px: 1.1
front_side_difference_pct: 2.9
transitions:
  top_module_y_px: [207, 220]
  base_y_px: [604, 634]
anomalies: []
```

Instead of returning 400+ per-row width records.

## Progressive disclosure

Use three output levels:

### `SUMMARY`
Default. Decision-grade aggregates only.

### `DIAGNOSTIC`
Use after a failure. Return data only for the failing object/feature/ROI.

### `RAW`
Exceptional. Use only when the next decision genuinely cannot be made from summarized diagnostics.

Escalation must be:

```text
SUMMARY -> failure/ambiguity -> DIAGNOSTIC -> only if still necessary -> RAW
```

Never start with RAW.

## Local computation rule

Python, NumPy, BMesh and geometry evaluators should perform reduction internally.

Examples:
- compute min/max/mean/variance locally;
- compare two silhouette profiles locally and return deviation;
- count non-manifold elements locally;
- reduce a mesh audit to failing element IDs/regions;
- compare render masks locally and return mismatch score + bounding ROI.

The LLM should reason over results, not over thousands of elementary samples.

## Result size guard

If a generated diagnostic contains more than roughly 100 scalar/sample entries, stop and ask:

```text
Can this be reduced to aggregates, outliers and failing regions?
```

In nearly all routine Blender-agent operations the answer should be yes.

## Repeated-source guard

Before analyzing an image, script, repository file or scene region again:
- check whether a validated cache/registry already contains the required fact;
- reuse it if valid;
- re-read only the smallest missing range/ROI.

For reconstruction use `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.
For project conventions use `09_engine/92_PROJECT_ASSET_PIPELINE_PROFILE_SCHEMA.md`.

## Zasada no visual guessing loop

Jeżeli agent po renderze "przesuwa trochę" obiekt pięć razy, workflow jest błędny.
Najpierw zmierz błąd, potem wykonaj jedną korektę.

## Limit eksperymentów

Dla nieznanej operacji:
1. wykonaj na kopii/test mesh,
2. oceń wynik,
3. dopiero zastosuj do assetu.

Nie eksperymentuj na głównym modelu.

## Completion requirement

Every analysis/execution stage should end with a compact persistent summary. Once a fact has been accepted into persistent state, do not keep its full discovery trace in active reasoning unless a conflict requires it.

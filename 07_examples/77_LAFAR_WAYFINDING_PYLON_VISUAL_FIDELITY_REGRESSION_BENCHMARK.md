# Lafar Wayfinding Pylon — Visual Fidelity Regression Benchmark

## Purpose

Pierwszy realny benchmark po v0.7, którego celem jest sprawdzenie, czy rozwiązana infrastruktura runtime nie przesłania podstawowego celu rekonstrukcji 1:1.

User-reported cost tej iteracji: około **67k tokenów**.

Asset: `LAFAR WAYFINDING PYLON / ACS-WP-3470`.
Źródła: techniczny concept sheet, technical prompt, Astera branding source.

## Wynik v0.7

Pipeline wykonał dużą część pracy poprawnie:
- reuse zweryfikowanego RPG project profile;
- per-axis pomiary planszy;
- parametric build;
- dynamic display jako osobny runtime owner;
- UV contract;
- LOD/export/round-trip;
- engine regression + controlled bite test.

Mimo tego asset nadal nie był 1:1 wizualnie. To jest regresja architektoniczna: Level C/D proof został rozwinięty bardziej niż executable Level A fidelity proof.

## Failure classes

### P1 — luminance-only reference mask loses bright silhouette

`executors/reference_measure.py` używa luminance threshold. Na karcie Astery jasne brushed aluminium i blue emissive są jaśniejsze od tła/hosta i wypadają z maski.

Lokalny run musiał stworzyć własny `dark OR chroma/blue` mask.

v0.8 requirement:
- mask mode jest jawny;
- bright-material risk jest raportowany;
- wspólny executor obsługuje chroma-aware reference masks.

### P2 — evidence conflict was converted directly into geometry

SIDE measurement dawał body depth około 167 mm, technical prompt podawał 220–250 mm. Run ustawił 170 mm i zapisał komentarz `card wins`.

v0.8 requirement:
- HARD/MUST conflict tworzy unresolved authority item;
- reconstruction gate blokuje przejście, dopóki konflikt nie jest `RESOLVED` albo `ACCEPTED_BY_AUTHORITY`.

### P3 — runtime work began before primary visual fidelity was closed

Agent przeszedł do display, decals, UV, LOD, exportu i engine testów, mimo że forma nadal odbiegała od concept artu.

v0.8 requirement:

```text
R6/R7/R8 fidelity PASS
-> R11 canonical multi-view PASS
-> RECON_FIDELITY_GATE PASS
-> dopiero R12 runtime
```

### P4 — envelope QA produced a false sense of correctness

Render QA został zanieczyszczony joined LOD meshes i collision hull. Collision proxy zasłonił asset, a pomiar wciąż raportował poprawne 600 x 300 x 2600 mm.

To dowodzi, że hard dimensions są konieczne, ale nie są dowodem fidelity.

v0.8 requirement:
- `QA_SCENE_ISOLATE` jest obowiązkowe dla reconstruction QA;
- canonical silhouette validator sprawdza render assetu, nie sam envelope;
- scene-isolation evidence jest częścią checkpoint report.

### P5 — existing QA skill was not reused

Biblioteka zawierała `executors/qa_scene_isolation.py`, ale run napisał lokalne prefix-hiding dopiero po wystąpieniu błędu.

v0.8 requirement:
- router/task pack jawnie wymaga `QA_SCENE_ISOLATE` przed ortho/material QA;
- lokalny replacement helper jest benchmark regression, jeśli executor binding działa.

### P6 — lower taper existed but was buried

Kluczowa cecha dolnej sylwetki była początkowo wewnątrz body volume. Sam object existence nie wykrył błędu.

v0.8 requirement:
- MUST visible feature wymaga layer/placement/ROI proof.

### P7 — display stack had three consecutive geometry/material failures

Kolejno wykryto:
- opaque glass zasłaniające content;
- content quad normal skierowany +Y, od widza;
- glass/content fizycznie za recess floor, czyli zakopane w korpusie.

Run zakończył się na diagnozie odwróconego depth stack.

v0.8 requirement:
- `LAYER_STACK_VALIDATE` przed material iteration;
- viewer -> glass -> gap/content -> recess floor order jest numeric invariant;
- normal/facing jest częścią contractu.

### P8 — branding handedness failure appeared late

Wordmark był mirrored, mimo że projekt miał znany `MIRROR_X` export contract.

v0.8 requirement:
- authoring-space text orientation i export handedness mają test przed final hero/runtime QA.

### P9 — LOD budget hard requirement was waived locally

LOD0 po zwiększeniu detalu nadal miał około 3478 tris wobec prompt budget 8000–15000. Run zdecydował `record deviation rather than pad geometry`.

Samo nabijanie tris nie jest celem, ale agent nie może jednostronnie zmienić hard acceptance requirement.

v0.8 requirement:
- HARD runtime budget conflict = blocker/authority decision;
- nie dodawaj dummy geometry dla countu;
- nie oznaczaj Level C jako PASS, jeśli hard budget nie został jawnie rozstrzygnięty.

### P10 — too many one-off local executors

Run utworzył osobne skrypty dla reference measurement, front bands, side/rear, crops, build, decals, display, QA, UV i exportu.

Część była asset-specific i uzasadniona. Część powielała semantic skills istniejące w bibliotece albo implementowała ogólny problem, który powinien stać się shared executor.

v0.8 requirement:
- reusable detection/validation logic trafia do `executors/`;
- asset-specific scripts zostają cienkimi callerami;
- target następnego podobnego assetu: brak ponownego pisania mask/overlay/fidelity/layer-stack validatorów.

## What v0.7 did well

Nie cofamy zmian v0.7. Project profile, canonical runtime root, DAG, image-cache coherence, round-trip i trustworthy engine test rozwiązały realne problemy.

v0.8 dodaje brakującą bramkę z przodu pipeline'u:

```text
visual truth first
-> runtime proof second
```

## v0.8 regression targets

```yaml
v0_8_targets:
  runtime_started_with_reconstruction_must_fail: 0
  canonical_views_without_registered_visual_diff: 0
  qa_renders_contaminated_by_collision_or_export_proxy: 0
  luminance_only_mask_used_despite_bright_material_risk: 0
  hard_deviation_silently_waived: 0
  must_visible_feature_proved_only_by_object_existence: 0
  local_reimplementation_of_bound_qa_isolation: 0
  repeated_layer_stack_debug_iterations_before_numeric_preflight: <= 1
  reference_fidelity_target_for_hero_civic_prop: L4_or_L5
```

Preferred operational target dla następnego podobnego technical-sheet prop:
- reference ingest + calibrated metrics: <= 8k tokens;
- blockout + primary fidelity closure: <= 15k tokens;
- no UV/LOD/export work before fidelity gate PASS;
- reusable visual validators produce compact region/blocker reports zamiast raw logs.

## Release implication

v0.8 jest udane dopiero, gdy następny benchmark pokaże, że agent potrafi zatrzymać się na błędnej geometrii zanim zacznie kosztowny runtime finish.

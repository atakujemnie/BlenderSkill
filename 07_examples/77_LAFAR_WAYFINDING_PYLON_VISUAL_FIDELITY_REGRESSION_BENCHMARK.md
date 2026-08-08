# Lafar Wayfinding Pylon — Visual Fidelity and Acceptance-Proof Regression Benchmark

## Purpose

Pierwszy realny benchmark po v0.7, którego celem jest sprawdzenie, czy rozwiązana infrastruktura runtime nie przesłania podstawowego celu rekonstrukcji 1:1 oraz czy końcowy `RECONSTRUCTION_COMPLETE` jest oparty na wykonywalnym dowodzie, a nie na narracyjnym self-report.

User-reported cost tej iteracji: około **67k tokenów**.

Asset: `LAFAR WAYFINDING PYLON / ACS-WP-3470`.
Źródła: techniczny concept sheet, technical prompt, Astera branding source.

## Finalny wynik runu v0.7

Pipeline wykonał dużą część pracy poprawnie:
- reuse zweryfikowanego RPG project profile;
- per-axis pomiary planszy;
- parametric build;
- dynamic display jako osobny runtime owner;
- UV contract;
- LOD/export/round-trip;
- engine regression + controlled bite test;
- naprawę display layer stack;
- naprawę front/rear decal handedness;
- finalny engine regression `exit 0`.

Finalny raport agenta zgłosił:

```text
RECONSTRUCTION_COMPLETE = PASS
MODELING_COMPLETE       = PASS
GAME_READY_COMPLETE     = BLOCKED
PIPELINE_INTEGRATED     = not claimed because Level C remained open
```

To zmienia diagnozę względem wcześniejszego checkpointu: run nie zakończył się na błędzie ekranu. Ekran został naprawiony, rear decals również, a engine test wrócił do zielonego stanu.

Jednocześnie finalny raport **nie zawierał wystarczającego proof bundle, aby v0.8 mogło zaakceptować `RECONSTRUCTION_COMPLETE` automatycznie**. Zgłaszał ortho QA i stwierdzenie `correct and matching the card`, ale bez zarejestrowanego diffu wszystkich kanonicznych widoków, metryk contour/ROI i bez jawnego authority approval dla części hard conflicts.

Najważniejszy wniosek benchmarku brzmi więc:

```text
v0.7 potrafi zakończyć technicznie poprawny run,
ale nadal może self-certify reconstruction PASS bez wystarczającego executable evidence.
```

## Failure classes

### P1 — luminance-only reference mask loses bright silhouette

`executors/reference_measure.py` używa luminance threshold. Na karcie Astery jasne brushed aluminium i blue emissive są jaśniejsze od ciemnego hosta i mogą wypaść z maski.

Lokalny run musiał stworzyć własny `dark OR chroma/blue` mask.

v0.8 requirement:
- mask mode jest jawny;
- bright-material risk jest raportowany;
- wspólny executor obsługuje chroma-aware reference masks.

### P2 — evidence conflict was converted directly into geometry

SIDE measurement dawał body depth około 167 mm, technical prompt podawał 220–250 mm. Run ustawił 170 mm i zapisał rationale `card wins`.

Finalny raport nadal wykazuje to jako deviation, ale jednocześnie zgłasza `RECONSTRUCTION_COMPLETE = PASS`.

v0.8 requirement:
- HARD/MUST conflict tworzy unresolved authority item;
- lokalny agent nie jest sam authority dla zmiany hard contractu;
- reconstruction gate blokuje przejście, dopóki konflikt nie jest `RESOLVED` albo `ACCEPTED_BY_AUTHORITY` z jawnym źródłem decyzji.

### P3 — runtime work began before primary visual fidelity was formally closed

Agent przeszedł do display, decals, UV, LOD, exportu i engine testów, zanim istniał wykonywalny `RECON_FIDELITY_GATE` z registered multi-view evidence.

Nawet jeśli późniejsze poprawki doprowadziły finalny model do właściwego stanu, kolejność była kosztowna i pozwalała runtime work maskować otwarte problemy reconstruction.

v0.8 requirement:

```text
R6/R7/R8 fidelity evidence PASS
-> R11 canonical registered multi-view PASS
-> RECON_FIDELITY_GATE PASS
-> dopiero R12 runtime
```

### P4 — envelope QA produced a false sense of correctness

Render QA został zanieczyszczony export/LOD proxy oraz collision hull. Collision proxy zasłonił asset, a pomiar wciąż raportował poprawne 600 x 300 x 2600 mm.

To dowodzi, że hard dimensions są konieczne, ale nie są dowodem fidelity.

v0.8 requirement:
- `QA_SCENE_ISOLATE` jest obowiązkowe dla reconstruction QA;
- canonical silhouette validator sprawdza render właściwego asset ownera, nie sam envelope;
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

### P7 — display stack required repeated reactive debugging

Kolejno wykryto:
- opaque glass zasłaniające content;
- content quad normal skierowany od widza;
- glass/content fizycznie za recess floor, czyli zakopane w korpusie.

Finalny run poprawił depth stack i display zaczął działać.

v0.8 requirement:
- `LAYER_STACK_VALIDATE` przed material iteration;
- viewer -> glass -> gap/content -> recess floor order jest numeric invariant;
- normal/facing jest częścią contractu;
- ten failure class powinien zostać wykryty jednym preflightem, a nie trzema render/fix cycles.

### P8 — branding handedness was view-dependent

Front display/decal UV oraz rear tech decals wymagały różnych decyzji orientacji. Manualny U-flip połączony z projektowym `MIRROR_X` dawał odbite napisy.

Finalny run naprawił front, a następnie osobno rear-facing decals.

v0.8 requirement:
- text/decal orientation jest sprawdzana per canonical view / face orientation;
- authoring-space UV flip nie może być globalnym booleanem bez uwzględnienia surface facing;
- export handedness i readable asymmetric/text feature tworzą wspólny validation contract.

### P9 — LOD budget hard requirement remained unresolved

LOD0 miał finalnie około 3478 tris wobec prompt budget 8000–15000. Agent słusznie nie dodał dummy geometry tylko po to, aby trafić w liczbę, ale nie może sam zmienić hard acceptance requirement.

Finalny raport poprawnie pozostawił `GAME_READY_COMPLETE = BLOCKED`, jednak jako główny blocker podał brak baked PBR; LOD0 budget również pozostaje otwartym runtime contract conflict, dopóki authority nie zmieni specyfikacji.

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

### P11 — reconstruction PASS was self-certified without proof-bearing canonical view records

Finalny raport podał `RECONSTRUCTION_COMPLETE = PASS`, ale nie dołączył compact machine-checkable records typu:

```yaml
FRONT:
  status: PASS
  evidence_kind: REGISTERED_OVERLAY
  registration_id: ...
  iou: ...
  mean_contour_delta_px: ...
  max_contour_delta_px: ...
  failing_rois: []
```

Analogicznie dla SIDE/TOP/REAR/BOTTOM i MUST feature ROIs.

Narracyjne `correct and matching the card` nie jest Level A evidence.

v0.8 requirement:
- `PASS` bez dozwolonego `evidence_kind` jest `UNVERIFIED`;
- canonical view PASS musi wskazywać registered comparison artifact/metrics;
- `RECONSTRUCTION_COMPLETE` nie może być self-certified przez ten sam krok, który budował asset.

### P12 — contradictory technical-sheet annotations need typed authority resolution

Finalny run wykrył nową klasę konfliktu: sama karta była wewnętrznie niespójna. Przykład: wydrukowana klamra `SCREEN ZONE 1280 mm` odpowiadała około 1545 mm przy skalowaniu z kotwicy 2600 mm.

Agent przyjął wydrukowane 1280 mm, co jest racjonalne, ale decyzja musi być zapisana jako typed authority result, nie tylko jako komentarz.

v0.8 requirement:
- rozróżniaj `PRINTED_DIMENSION`, `PIXEL_INFERENCE`, `PROMPT_RANGE`, `ORTHO_SILHOUETTE`, `PERSPECTIVE_INFERENCE`;
- printed dimension może wygrać z pixel inference, ale konflikt pozostaje zapisany w Evidence Ledger;
- per-axis calibration nie zakłada jednego globalnego mm/px dla marketingowej karty.

### P13 — package could load successfully with no `TEXCOORD_0`

W całym eksporcie brakowało `TEXCOORD_0`, ponieważ łączone siatki miały różne nazwy warstw UV. glTF miał obrazy i materiały, loader działał, ale runtime próbkowałby błędnie.

v0.8 requirement:
- package readback waliduje wymagane primitive attributes, nie tylko node/material/image names;
- dla teksturowanego runtime material `TEXCOORD_0` jest hard invariant;
- dynamic display/atlas owner musi mieć jawny UV attribute proof po eksporcie.

### P14 — engine dimension assertion did not cover node transforms

Controlled bite test wysokości zadziałał dla realnego dryfu build geometry, ale run wykrył lukę: engine loader/test czytał lokalne vertex positions i nie aplikował node transforms. Zmiana skali węzła glTF nie byłaby złapana przez taki assertion.

Ta sama luka istnieje w dotychczasowym bollard test pattern.

v0.8 requirement:
- Project Asset Pipeline Profile deklaruje policy dla node TRS;
- jeśli loader nie aplikuje node transforms, runtime nodes wymagają baked/identity TRS;
- package validator sprawdza node transform policy;
- engine dimension test określa przestrzeń pomiaru i nie udaje world-space proof, jeśli mierzy tylko local vertices.

### P15 — valid engine evidence does not bypass lower completion levels

Finalny run miał target-engine evidence (`ENGINE_REGRESSION_TEST`, exit 0), ale poprawnie nie zgłosił `PIPELINE_INTEGRATED`, ponieważ `GAME_READY_COMPLETE` było otwarte.

To jest pozytywny regression result v0.7 i musi zostać zachowany:

```text
Level D evidence exists
+
Level C FAIL/BLOCKED
=
PIPELINE_INTEGRATED not achieved
```

## What v0.7 did well

Nie cofamy zmian v0.7. Project profile, canonical runtime root, DAG, image-cache coherence, round-trip i trustworthy engine test rozwiązały realne problemy.

Finalny pylon run dodatkowo potwierdził:
- project profile reuse działa;
- controlled bite test ma wartość diagnostyczną;
- completion hierarchy nie pozwoliła Level D przeskoczyć otwartego Level C;
- runtime path contract uchronił pylon przed zapisem do zakazanego `<repo>/GameAssets`.

v0.8 dodaje brakującą bramkę z przodu pipeline'u oraz wzmacnia proof integrity:

```text
visual truth with executable evidence
-> runtime package integrity
-> runtime proof
```

## v0.8 regression targets

```yaml
v0_8_targets:
  runtime_started_with_reconstruction_must_fail: 0
  reconstruction_pass_without_proof_bearing_canonical_views: 0
  canonical_views_without_registered_visual_diff: 0
  qa_renders_contaminated_by_collision_or_export_proxy: 0
  luminance_only_mask_used_despite_bright_material_risk: 0
  hard_deviation_silently_waived: 0
  must_visible_feature_proved_only_by_object_existence: 0
  local_reimplementation_of_bound_qa_isolation: 0
  repeated_layer_stack_debug_iterations_before_numeric_preflight: <= 1
  gltf_textured_primitive_missing_texcoord0: 0
  node_transform_policy_unverified_for_runtime_loader: 0
  reference_fidelity_target_for_hero_civic_prop: L4_or_L5
```

Preferred operational target dla następnego podobnego technical-sheet prop:
- reference ingest + calibrated metrics: <= 8k tokens;
- blockout + primary fidelity closure: <= 15k tokens;
- no UV/LOD/export work before fidelity gate PASS;
- reusable visual validators produce compact region/blocker reports zamiast raw logs;
- no accepted `PASS` record without provenance/evidence kind.

## Release implication

v0.8 jest udane dopiero, gdy kolejny realny benchmark pokaże jednocześnie:
1. błędna reconstruction zatrzymuje pipeline przed runtime;
2. poprawna reconstruction przechodzi na podstawie proof-bearing multi-view records, nie narracji;
3. package readback wykrywa brakujące runtime attributes i niedozwolone node transforms;
4. Level D nadal wymaga poprawnego Level C i target-engine evidence.

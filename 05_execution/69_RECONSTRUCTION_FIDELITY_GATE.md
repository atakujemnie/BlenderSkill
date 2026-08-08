# Reconstruction Fidelity Gate

## Cel

Zamienić istniejące zasady fidelity z dokumentacji na twardą, **proof-bearing** bramkę wykonawczą przed `R12 — TOPOLOGY/RUNTIME`.

v0.7 potrafi dowieść poprawnego exportu, ścieżek runtime i integracji silnika. Nie może jednak dopuścić do sytuacji, w której asset z poprawnym bounding boxem albo narracyjnym `looks correct` przechodzi do LOD/exportu mimo nieudowodnionej sylwetki, proporcji lub widoczności cech MUST.

## Zasada nadrzędna

```text
RECONSTRUCTION FIDELITY FAIL / UNVERIFIED
!=
problem do zapisania jako deviation i kontynuowania runtime
```

Jeżeli błąd dotyczy D0/D1, kanonicznego widoku, cechy MUST albo twardego wymiaru, pipeline wraca do najwcześniejszego właściciela błędu.

`PASS` jest stanem dowodowym, nie komentarzem modelu.

## Kolejność bramek

```text
registered reference
-> hard dimensions
-> canonical silhouette/overlay diff
-> D0/D1 landmarks and proportions
-> MUST feature ROI visibility
-> material segmentation when target >= L4
-> authority/deviation closure
-> RECON_FIDELITY_GATE
-> only then topology/UV/LOD/runtime
```

## Proof-bearing PASS

Każdy wymagany owner musi przekazać compact record zawierający co najmniej:

```yaml
status: PASS
evidence_kind: <allowed kind>
provenance_id: <artifact/registration/validator id>
```

Sam zapis:

```yaml
status: PASS
```

jest w trybie v0.8 `UNVERIFIED`.

Narracyjne:

```text
correct
matching the card
looks good
ortho checked
```

nie jest dowodem Level A.

## Dozwolone klasy dowodu

Przykładowe `evidence_kind`:

```text
NUMERIC_MEASUREMENT
REGISTERED_OVERLAY
SILHOUETTE_DIFF
LANDMARK_PROJECTION
FEATURE_ROI
LAYER_STACK
RAY_VISIBILITY
MATERIAL_SEGMENTATION
AUTHORITY_DECISION
```

Dopuszczalne klasy zależą od ownera. Na przykład `REGISTERED_OVERLAY` nie zastępuje numeric hard-dimension measurement, a `OBJECT_EXISTS` nie jest wystarczającym dowodem widocznej cechy MUST.

## Minimalny kontrakt wejściowy

```yaml
fidelity_gate:
  strict_evidence: true
  target_fidelity: L4
  achieved_fidelity: L4

  hard_dimensions:
    status: PASS
    evidence_kind: NUMERIC_MEASUREMENT
    provenance_id: bounds_report_v3

  canonical_views:
    FRONT:
      status: PASS
      evidence_kind: REGISTERED_OVERLAY
      provenance_id: front_reg_001
      iou: 0.97
      mean_contour_delta_px: 1.3
      max_contour_delta_px: 4.0
    SIDE:
      status: FAIL
      evidence_kind: REGISTERED_OVERLAY
      provenance_id: side_reg_001

  landmarks_d0_d1:
    status: PASS
    evidence_kind: LANDMARK_PROJECTION
    provenance_id: landmark_report_002

  must_features:
    - id: LOWER_TAPER
      status: PASS
      evidence_kind: FEATURE_ROI
      provenance_id: lower_taper_roi_004

  material_segmentation:
    status: PASS
    evidence_kind: MATERIAL_SEGMENTATION
    provenance_id: matseg_001

  deviations:
    - id: BODY_DEPTH
      severity: HARD
      status: ACCEPTED_BY_AUTHORITY
      authority_source: USER_APPROVAL
      authority_record_id: decision_007
```

Wynik musi zawierać `can_advance_to_runtime`.

## Canonical-view proof

Dla każdego wymaganego widoku `FRONT/SIDE/TOP/REAR/BOTTOM`:
- rejestracja ma być globalna dla widoku;
- kandydat i reference muszą używać zgodnej projekcji/skali/cropu;
- wymagany jest compact metric report albo jawny blocker;
- `QA_SCENE_ISOLATE` musi potwierdzić, że render nie został zanieczyszczony collision/export proxy.

Jeżeli reference dla danego widoku nie istnieje, widok nie może zostać po prostu usunięty z evidence. Musi mieć jawny status wynikający z View Authority Matrix, np. `NOT_REQUIRED_BY_AUTHORITY` albo alternatywny proof contract.

## Severity / authority

`HARD`, `MUST`, `CANONICAL`:
- brak automatycznego waivera;
- `OPEN` blokuje;
- może zostać zamknięte tylko jako `RESOLVED` albo `ACCEPTED_BY_AUTHORITY`;
- `ACCEPTED_BY_AUTHORITY` bez `authority_source` i `authority_record_id` jest nadal blockerem.

Agent budujący asset nie może sam sobie nadać authority przez komentarz typu `card wins` albo `this is more sensible`.

`SOFT`:
- może pozostać jako znane ograniczenie, jeżeli target fidelity na to pozwala.

## Konflikty wewnątrz technical sheet

Rozróżniaj źródła:
- `PRINTED_DIMENSION`;
- `ORTHO_DIMENSION_LINE`;
- `PROMPT_HARD_VALUE`;
- `PROMPT_RANGE`;
- `ORTHO_SILHOUETTE_INFERENCE`;
- `PIXEL_INFERENCE`;
- `HERO/PERSPECTIVE_INFERENCE`.

Jeżeli np. wydrukowane `1280 mm` nie odpowiada pikselowo skali wyprowadzonej z `2600 mm`, nie deformuj geometrii dla zgodności z oboma naraz. Zapisz conflict i rozwiąż go przez View Authority Matrix. Pixel inference nie może po cichu nadpisać drukowanego wymiaru.

## Fidelity levels

Korzystaj z `05_execution/59_REFERENCE_FIDELITY_PROTOCOL.md`.

Dla assetu hero / ważnego civic prop domyślnym celem jest L4 lub L5, nie L1/L2.

`achieved_fidelity` nie może być ręcznie zadeklarowane wyżej niż dowody ownerów. Gate może przyjąć deklarację jako wejście diagnostyczne, ale nie może użyć jej jako jedynego dowodu.

## Anti-gaming

Nie wolno zaliczyć bramki przez:
- poprawne `Dimensions` przy błędnym obrysie;
- render collision proxy zamiast assetu;
- wysokie globalne IoU przy dużym błędzie lokalnego MUST ROI;
- istnienie obiektu w scenie bez dowodu jego widoczności;
- działający export/engine loader przy niezamkniętym reconstruction FAIL;
- dopisywanie geometrii wyłącznie po to, aby osiągnąć arbitralny triangle count;
- deklarację `PASS` bez evidence kind/provenance;
- `ACCEPTED_BY_AUTHORITY` bez identyfikowalnego authority record.

## Executor

`executors/fidelity_gate.py`

Executor agreguje compact reports. Nie zastępuje pomiarów. Właścicielami dowodu pozostają:
- `REFERENCE_OVERLAY_VALIDATE` dla silhouette/ROI;
- numeric/landmark validators;
- `LAYER_STACK_VALIDATE` dla widocznych warstw/recessów;
- material segmentation validator dla L4+;
- Evidence/Authority Ledger dla deviation closure.

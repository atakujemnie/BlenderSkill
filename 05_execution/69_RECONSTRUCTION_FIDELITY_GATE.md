# Reconstruction Fidelity Gate

## Cel

Zamienić istniejące zasady fidelity z dokumentacji na twardą bramkę wykonawczą przed `R12 — TOPOLOGY/RUNTIME`.

v0.7 potrafi dowieść poprawnego exportu, ścieżek runtime i integracji silnika. Nie może jednak dopuścić do sytuacji, w której asset z poprawnym bounding boxem przechodzi do LOD/exportu mimo błędnej sylwetki, proporcji lub niewidocznych cech MUST.

## Zasada nadrzędna

```text
RECONSTRUCTION FIDELITY FAIL
!=
problem do zapisania jako deviation i kontynuowania runtime
```

Jeżeli błąd dotyczy D0/D1, kanonicznego widoku, cechy MUST albo twardego wymiaru, pipeline wraca do najwcześniejszego właściciela błędu.

## Kolejność bramek

```text
registered reference
-> hard dimensions
-> canonical silhouette diff
-> D0/D1 landmarks and proportions
-> MUST feature ROI visibility
-> material segmentation when target >= L4
-> RECON_FIDELITY_GATE
-> only then topology/UV/LOD/runtime
```

## Minimalny kontrakt wejściowy

```yaml
fidelity_gate:
  target_fidelity: L4
  achieved_fidelity: L3
  hard_dimensions: {status: PASS}
  canonical_views:
    FRONT: {status: PASS}
    SIDE: {status: FAIL}
    TOP: {status: PASS}
    REAR: {status: PASS}
    BOTTOM: {status: PASS}
  landmarks_d0_d1: {status: PASS}
  must_features:
    - {id: LOWER_TAPER, status: FAIL}
  material_segmentation: {status: UNVERIFIED}
  deviations:
    - {id: BODY_DEPTH, severity: HARD, status: OPEN}
```

Wynik musi zawierać `can_advance_to_runtime`.

## Severity / authority

`HARD`, `MUST`, `CANONICAL`:
- brak automatycznego waivera;
- `OPEN` blokuje;
- może zostać zamknięte tylko jako `RESOLVED` albo `ACCEPTED_BY_AUTHORITY` z jawnym źródłem decyzji.

`SOFT`:
- może pozostać jako znane ograniczenie, jeżeli target fidelity na to pozwala.

Konflikt między kartą a promptem nie może być rozwiązany przez lokalny skrypt samym komentarzem `card wins`. Musi istnieć wpis Evidence/Authority z confidence i konsekwencją dla bramek.

## Fidelity levels

Korzystaj z `05_execution/59_REFERENCE_FIDELITY_PROTOCOL.md`.

Dla assetu hero / ważnego civic prop domyślnym celem jest L4 lub L5, nie L1/L2.

## Anti-gaming

Nie wolno zaliczyć bramki przez:
- poprawne `Dimensions` przy błędnym obrysie;
- render collision proxy zamiast assetu;
- wysokie globalne IoU przy dużym błędzie lokalnego MUST ROI;
- istnienie obiektu w scenie bez dowodu jego widoczności;
- działający export/engine loader przy niezamkniętym reconstruction FAIL;
- dopisywanie geometrii wyłącznie po to, aby osiągnąć arbitralny triangle count.

## Executor

`executors/fidelity_gate.py`

Executor agreguje compact reports. Nie zastępuje pomiarów. Właścicielami dowodu pozostają:
- `REFERENCE_OVERLAY_VALIDATE` dla silhouette/ROI;
- numeric/landmark validators;
- `LAYER_STACK_VALIDATE` dla widocznych warstw/recessów;
- material segmentation validator dla L4+.

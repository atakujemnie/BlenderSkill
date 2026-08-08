# Reconstruction State Machine

## R0 — INGEST
Zapis źródeł i segmentów.

## R1 — CLASSIFY
Projection, view, material/detail/text.

## R2 — AUTHORITY
Evidence + View Authority Matrix.

## R3 — REGISTER
Skala, osie, image planes, camera.

## R4 — CONSTRAIN
Dimension graph, landmarks, feature contract.

## R5 — DECOMPOSE
Object decomposition i strategy map.

## R6 — D0 BLOCKOUT
Bounds + silhouette.

Wymagany proof przed advance:
- numeric bounds;
- registered silhouette evidence dla authoritative views;
- QA scene isolation.

## R7 — D1 PRIMARY FORMS
Major profiles i negative space.

Wymagany proof przed advance:
- D0/D1 landmarks;
- canonical profile/proportion comparison;
- brak open HARD geometry conflict.

## R8 — D2 FEATURES
Panels, trim, recess, functional details.

Wymagany proof przed advance:
- wszystkie MUST feature owners;
- ROI/visibility/layer-stack proof odpowiedni do feature class.

## R9 — D3 DETAIL
Fasteners, branding, microgeometry.

Readable branding/text wymaga canonical orientation proof, w tym project handedness gdy dotyczy.

## R10 — SURFACE
Materials, UV, decals, emissive.

Dla target fidelity L4/L5 wymagany material segmentation proof.

## R11 — MULTIVIEW QA + FIDELITY GATE
Wszystkie kanoniczne widoki.

Kolejność:

```text
QA_SCENE_ISOLATE
-> registered canonical view validators
-> hard dimensions
-> D0/D1 landmarks
-> MUST feature evidence
-> material segmentation when required
-> authority/deviation closure
-> RECON_FIDELITY_GATE
```

`RECON_FIDELITY_GATE` musi zwrócić proof-bearing PASS z provenance.

Bare `PASS`, `looks correct`, `matching the card` albo poprawny overall envelope nie pozwalają wejść do R12.

## R12 — TOPOLOGY/RUNTIME
Optimization bez utraty fidelity.

Ten etap jest niedostępny przy `RECON_FIDELITY_GATE != PASS`.

Game-ready package readback musi później sprawdzić wymagane primitive attributes i aktywną node-transform policy.

## R13 — EXPORT VALIDATION

Sprawdź:
- package readback;
- runtime primitive attributes;
- node transform policy;
- export round-trip dimensions/contact;
- target engine evidence dopiero dla Level D.

## Backtracking

Każdy FAIL wraca do najwcześniejszego etapu, który może go naprawić.

Przykłady:

```text
SIDE contour FAIL -> R6/R7
LOWER_TAPER visibility FAIL -> R8
mirrored rear technical decal -> R9/R10
missing TEXCOORD_0 after export -> R12/R13 package/UV owner
non-identity node TRS forbidden by profile -> R12/R13 export/package owner
```

Nie naprawiaj reconstruction FAIL przez runtime detail ani package FAIL przez ponowne modelowanie, jeśli dependency nie prowadzi do geometrii.

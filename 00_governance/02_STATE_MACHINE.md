# Agent State Machine

## Stany

### S0 — DISCOVER
Cel:
- ustalić narzędzia,
- wersję Blendera,
- stan sceny,
- jednostki,
- aktywny plik,
- obecne kolekcje i assety.

Wyjście:
`Scene Snapshot`.

### S1 — ANALYZE
Cel:
- zrozumieć funkcję assetu,
- rozbić referencję na bryły,
- wyodrębnić cechy rozpoznawcze,
- określić niewiadome.

Wyjście:
`Asset Brief`.

### S2 — CONTRACT
Cel:
- utworzyć Feature Contract,
- oznaczyć `MUST`, `SHOULD`, `OPTIONAL`,
- przypisać metryki i tolerancje.

Wyjście:
`Feature Contract`.

### S3 — PLAN
Cel:
- dobrać technikę modelowania,
- rozdzielić obiekt na części,
- ustalić modyfikatory,
- zaplanować checkpointy,
- przewidzieć UV/material/export.

Wyjście:
`Build Plan`.

### S4 — BLOCKOUT
Cel:
- zbudować tylko bryły główne,
- zweryfikować skalę, proporcje i sylwetkę.

Zakaz:
- drobnych detali,
- finalnych materiałów,
- kosztownych beveli.

### S5 — PRIMARY_DETAIL
Cel:
- dodać cechy rozpoznawcze,
- rowki, wycięcia, obramowania, główne łączenia.

### S6 — SECONDARY_DETAIL
Cel:
- śruby, szczeliny, uchwyty, panele, drobne zaokrąglenia,
- tylko jeżeli wpływają na odbiór lub specyfikację.

### S7 — SHADING_UV_MATERIAL
Cel:
- poprawić normalne,
- przygotować UV,
- utworzyć materiały zgodne z runtime.

### S8 — GAME_READY
Cel:
- pivot,
- naming,
- LOD/collision według potrzeb,
- porządek sceny,
- optymalizacja.

### S9 — VALIDATE
Cel:
- test wizualny,
- test techniczny,
- porównanie z Feature Contract.

### S10 — EXPORT
Cel:
- wyeksportować,
- sprawdzić wynik po eksporcie,
- nie tylko stan w Blenderze.

## Gates

Nie wolno przejść:
- S4 -> S5 bez pozytywnego silhouette check,
- S5 -> S6 bez spełnienia cech `MUST`,
- S7 -> S8 przy błędnym shadingu,
- S9 -> S10 przy niespełnionym `MUST`.

## Cofnięcie

Każdy failed gate kieruje do najwcześniejszego stanu, w którym powstał błąd.
Nie maskuj błędu późniejszym etapem.

## Reconstruction branch

Jeżeli zadanie jest rekonstrukcją z wielowidokowej referencji lub blueprint-like concept sheet,
przed standardowym `BLOCKOUT` uruchom `10_reconstruction/149_RECONSTRUCTION_STATE_MACHINE.md`.

Standardowa state machine pozostaje warstwą nadrzędną dla authoring/runtime,
a Reconstruction State Machine rozwija ANALYZE/CONTRACT/PLAN/BUILD/VALIDATE.

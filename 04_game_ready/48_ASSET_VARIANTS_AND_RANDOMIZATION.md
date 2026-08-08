# Asset Variants and Randomization

## Cel

Uzyskać różnorodność bez duplikowania całego kosztu assetu.

## Warstwy wariantów

### V0 — transform
- rotation,
- scale w dozwolonym zakresie.

### V1 — material
- kolor,
- roughness,
- decal set.

### V2 — accessories
- dodatkowy panel,
- uchwyt,
- ekran,
- osłona.

### V3 — structural
- rzeczywista zmiana geometrii.

Preferuj najniższą wystarczającą warstwę.

## Deterministic randomization

W proceduralnych zestawach:
- seed jawny,
- lista dozwolonych wariantów jawna,
- brak przypadkowych zmian wpływających na gameplay clearances.

## Shared core

Warianty powinny współdzielić:
- core mesh tam, gdzie możliwe,
- materiały,
- trim sheets,
- atlas,
- collision, jeśli geometria funkcjonalna się nie zmienia.

## QA

Wariant nie może:
- naruszać bounding/clearance contract,
- usuwać feature MUST wspólnego dla rodziny,
- tworzyć konfliktów material/runtime.

# Reconstruction Change Control

## Zmiana referencji

Nowy arkusz/revision może wpływać na:
- dimensions,
- feature presence,
- materials,
- branding.

## Impact analysis

1. find changed evidence,
2. find linked constraints,
3. find Feature IDs,
4. find scene owners,
5. find downstream UV/bake/runtime.

## Change set

Każda większa aktualizacja:
- reason,
- affected evidence,
- affected features,
- before/after,
- regression result.

## User-directed deviation

Jeśli użytkownik celowo chce odstąpić od referencji:
utwórz `AUTHORIZED_DEVIATION`.

Od tego momentu QA porównuje dany feature do deviation contract, nie starego obrazu.

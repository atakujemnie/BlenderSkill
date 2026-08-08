# Change Impact Protocol

Każda poprawka może powodować regresję.

## Przed zmianą

Zidentyfikuj:
- target feature,
- owner object,
- dependencies,
- neighboring features,
- modifiers downstream,
- UV/material impact,
- export impact.

## Impact classes

### LOCAL
Zmiana nie wpływa poza jeden feature.
Przykład: szerokość szczeliny.

### STRUCTURAL
Zmiana wpływa na kilka cech i proporcje.
Przykład: szerokość korpusu.

### PIPELINE
Zmiana wpływa na UV/export/rig.
Przykład: zastosowanie modifiera zmieniającego vertex order.

## Test regresji

LOCAL:
- target + adjacent MUST.

STRUCTURAL:
- pełny silhouette + wszystkie MUST.

PIPELINE:
- pełna walidacja od odpowiedniego etapu do export.

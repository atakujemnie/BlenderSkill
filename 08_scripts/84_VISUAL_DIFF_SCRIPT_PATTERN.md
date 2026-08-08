# Visual Diff Script Pattern

## Input

- accepted image,
- candidate image,
- optional ROI,
- optional silhouette masks.

## Recommended outputs

- absolute difference image,
- thresholded mask,
- changed pixel ratio,
- bounding box of differences,
- silhouette IoU if masks exist.

## Important

Nie porównuj dwóch obrazów, jeśli:
- resolution jest inne,
- camera jest inna,
- framing jest inne,
- QA profile jest inny.

## Feature-local diff

```text
feature_id -> ROI -> diff metrics -> PASS/MINOR/FAIL
```

## Regression detection

Jeżeli naprawa dotyczy F012:
- duża zmiana wewnątrz ROI F012 jest oczekiwana,
- zmiana w ROI innych MUST wymaga regresji check,
- duża zmiana poza wszystkimi expected ROI jest podejrzana.

## Storage

Przechowuj metryki, nie tylko obraz.
Pozwala to porównywać jakość kolejnych wersji agenta.

# Silhouette Diff Protocol

## Pipeline

1. render binary/flat mask,
2. align with calibrated reference,
3. compute overlap,
4. extract contour delta,
5. map delta to feature/region.

## Metrics

### IoU
Dobra metryka ogólna, ale może ukrywać lokalny błąd.

### Maximum contour deviation
Wykrywa pojedyncze duże odchylenie.

### Mean contour deviation
Ogólna jakość obrysu.

### Regional contour deviation
Najważniejsze dla feature QA.

## Gate

D0 pass wymaga:
- akceptowalnego globalnego overlap,
- braku dużych lokalnych FAIL w critical regions.

## Anti-gaming

Nie uznawaj wysokiego IoU za sukces, jeśli np. profil oparcia jest wyraźnie błędny.

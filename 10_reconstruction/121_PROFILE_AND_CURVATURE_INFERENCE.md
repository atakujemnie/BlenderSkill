# Profile and Curvature Inference

## Problem

Referencja często pokazuje "zaokrąglony bok", ale nie podaje promienia.

## Rozróżniaj

- circular arc,
- fillet,
- bevel,
- spline transition,
- compound curvature,
- chamfer.

## Evidence

Grazing highlight nie jest sam w sobie dowodem dokładnego promienia.
Łącz:
- silhouette,
- orthographic contour,
- detail,
- manufacturing logic.

## Curvature control

Dla ważnego profilu preferuj:
- parametric bevel,
- curve profile,
- explicit support geometry,

zamiast ręcznego "wygładzania".

## Radius range

Jeśli nieznany:
zapisz zakres, np. `R ~= 20–30 mm`, a nie fałszywie dokładną liczbę.

## QA

Ocena:
- silhouette,
- highlight width pod stałym światłem,
- transition continuity.

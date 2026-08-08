# Cross-Section Inference

## Problem

Front/side/top nie zawsze definiują profil przekroju.

## Evidence order

1. detail close-up,
2. visible edge in hero,
3. material boundary,
4. manufacturing logic,
5. minimal plausible section.

## Cross-section classes

- rectangular,
- rounded rectangle,
- chamfered,
- tapered,
- hollow shell,
- layered sandwich,
- custom spline.

## Unknown section

Jeżeli przekrój nie jest widoczny:
- nie dodawaj skomplikowanego profilu,
- wybierz minimalny profil spełniający wszystkie widoki,
- oznacz jako `INFERRED`.

## Section stations

Dla zmiennej geometrii definiuj profile w kilku stacjach:
- base,
- mid,
- transition,
- top.

Można następnie loftować/łączyć je kontrolowanie.

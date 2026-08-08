# Automated Visual Diff

## Cel

Wykrywać regresje wizualne pomiędzy:
- referencją a renderem,
- checkpointem A a checkpointem B,
- wersją assetu przed i po naprawie.

## Render determinism

Diff ma sens tylko, gdy stałe są:
- camera,
- resolution,
- framing,
- lighting,
- world/background,
- render engine,
- material QA profile,
- color management.

## Rodzaje diff

### Silhouette diff
Najważniejszy dla D0/D1.
Porównuj maskę obiektu.

Metryki:
- IoU,
- area difference,
- contour distance.

### Edge diff
Przydatny dla:
- rowków,
- paneli,
- dużych podziałów.

### ROI diff
Porównuje tylko obszar przypisany do Feature ID.

### Pixel diff
Używaj ostrożnie.
Materiały i anti-aliasing mogą generować różnice nieistotne geometrycznie.

## Thresholds

Nie istnieje jeden globalny próg.
Ustal osobno dla:
- silhouette,
- primary feature,
- material,
- shading.

## Regression mode

Najbardziej wartościowe zastosowanie:
`last accepted checkpoint -> current build`

Wtedy zmiana poza expected ROI jest sygnałem możliwej regresji.

## Human/reference ambiguity

Automatyczny diff nie rozstrzyga sam:
- stylizowanej perspektywy,
- różnego oświetlenia concept artu,
- ukrytej geometrii.

Jest narzędziem dowodowym, nie arbitrem designu.

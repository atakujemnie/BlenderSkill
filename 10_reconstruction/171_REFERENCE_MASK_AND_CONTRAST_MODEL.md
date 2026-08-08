# Reference Mask and Contrast Model

## Problem

Jedna maska `luminance < threshold` nie jest wystarczająca dla technicznych plansz produktowych.

Na realnym benchmarku Lafar Wayfinding Pylon jasne szczotkowane aluminium i błękitny emissive strip zlewały się z jasnym tłem. Czysty próg luminancji zaniżał szerokość SIDE i mógł fałszywie zaliczyć albo odrzucić obrys.

## Mask modes

Validator reference powinien jawnie deklarować tryb:

```text
ALPHA
LUMINANCE_DARK
LUMINANCE_OR_CHROMA
EXTERNAL_MASK
```

### `LUMINANCE_OR_CHROMA`

Minimalny model:

```text
dark = luminance <= threshold
chroma = max(rgb) - min(rgb) >= chroma_threshold
blue_dominant = B - 0.5*(R+G) >= blue_threshold
mask = dark OR chroma OR blue_dominant
```

Nie jest to uniwersalna segmentacja obiektu. Jest to kontrolowana odpowiedź na kartę, w której bright material / emissive ma authority jako część sylwetki.

## Per-axis calibration

Technical-sheet crop może być anizotropowy lub `NEAR_ORTHOGRAPHIC`.

Nigdy nie zakładaj jednego `mm_per_pixel` dla X/Y tylko dlatego, że karta wygląda technicznie.

Kalibracja ma zapisywać:

```yaml
calibration:
  x:
    physical: 600_mm
    pixel_span: 157
    source: dimension_line
  y:
    physical: 2600_mm
    pixel_span: 530
    source: dimension_line
  projection: NEAR_ORTHOGRAPHIC
```

Skala z jednej osi nie może automatycznie przeliczać drugiej.

## Bright-material risk

Jeżeli maska luminance-only przecina obiekt dokładnie w miejscu:
- brushed aluminium,
- white polymer,
- emissive diffuser,
- specular highlight,

wynik ma status co najmniej `MASK_RISK`, dopóki alternatywny mask mode albo manual ROI nie potwierdzi granicy.

## Output budget

Do modelu zwracaj:
- bbox/profile aggregates;
- mask mode;
- calibration provenance;
- flagged regions;
- confidence.

Nie zwracaj pełnej maski/pixel array bez potrzeby diagnostycznej.

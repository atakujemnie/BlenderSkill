# Reference Ingestion Protocol

## Przed analizą geometrii

Dla każdego wejścia zapisz:
- file id / path,
- resolution,
- aspect ratio,
- orientation,
- whether cropped,
- whether perspective/orthographic,
- known dimensions visible,
- labels visible,
- source status: approved / draft / auxiliary.

## Concept sheet

Arkusz należy rozłożyć na osobne regiony:
- hero,
- front,
- side,
- top,
- rear,
- bottom,
- detail,
- material palette,
- notes,
- dimensions.

## Nie modeluj bez segmentacji

Cały arkusz jako jedna referencja utrudnia:
- dokładne skalowanie,
- kamerę QA,
- ROI,
- pomiar.

## Reference Registry

Po pierwszej poprawnej segmentacji utwórz trwały rejestr widoków.

```yaml
reference_registry:
  source:
    file: concept_art.png
    size_px: [1122, 1402]
  views:
    FRONT:
      roi: [x0, y0, x1, y1]
      projection: ORTHOGRAPHIC
      authority: HIGH
      validated: true
      crop_artifact: c_front_ortho.png
```

Każdy crop/ROI musi mieć provenance do oryginału.

Po zwalidowaniu rejestru nie segmentuj całego arkusza ponownie przy każdym kolejnym pomiarze.
Używaj `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.

## Original preservation

Nigdy nie nadpisuj oryginalnej referencji.
Przetworzone cropy muszą mieć provenance do oryginału.

## Rotation/crop policy

Zmiana:
- orientacji,
- cropu,
- kontrastu

jest dozwolona jako warstwa pomocnicza, ale musi być odwracalna i udokumentowana.

## Annotation separation

Na planszach technicznych odróżnij od geometrii:
- dimension lines;
- arrows;
- leaders;
- labels;
- icons;
- layout separators;
- marketing copy.

Nie pozwalaj, aby ciemna linia wymiarowa lub leader została włączona do maski sylwetki tylko dlatego, że znajduje się blisko obiektu.

## Analysis cache handoff

Po ingest/segmentation zapisz do cache:
- source metadata;
- view ROI;
- view classification;
- crop artifact paths;
- known explicit dimensions;
- exclusion regions/masks, jeśli są wymagane;
- unresolved segmentation conflicts.

Następne narzędzia pomiarowe mają korzystać z tych wpisów zamiast ponownie odkrywać cały arkusz.

## Output budget

Normalny wynik ingestu powinien być zwartym manifestem segmentów i konfliktów.

Nie zwracaj do LLM:
- pełnych danych pikselowych;
- dziesiątek próbek threshold;
- per-row/per-column profili;
- pełnych buforów obrazów.

Jeżeli konkretny ROI jest niejednoznaczny, eskaluj tylko ten ROI do trybu diagnostycznego.

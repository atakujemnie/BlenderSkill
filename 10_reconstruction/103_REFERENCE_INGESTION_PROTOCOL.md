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

## Original preservation

Nigdy nie nadpisuj oryginalnej referencji.
Przetworzone cropy muszą mieć provenance do oryginału.

## Rotation/crop policy

Zmiana:
- orientacji,
- cropu,
- kontrastu

jest dozwolona jako warstwa pomocnicza, ale musi być odwracalna i udokumentowana.

# Reconstruction QA Camera Rig

## Stały zestaw kamer

Dla pełnego concept sheet:
- FRONT_ORTHO
- REAR_ORTHO
- LEFT/RIGHT_SIDE_ORTHO
- TOP_ORTHO
- BOTTOM_ORTHO
- HERO_MATCH
- DETAIL_MATCH

## Ortho cameras

Mają:
- zablokowaną orientację,
- skalę wynikającą z bounds,
- ten sam framing margin,
- stałą rozdzielczość.

## Camera metadata

Każda kamera:
- id,
- source segment,
- projection,
- lens/ortho scale,
- transform,
- resolution,
- revision.

## Lock

QA camera nie jest kamerą artystyczną.
Po kalibracji nie należy jej ruszać podczas napraw geometrii.

## Camera failure

Jeśli trzeba ruszyć QA camera, traktuj to jako zmianę kalibracji i ponownie waliduj baseline.

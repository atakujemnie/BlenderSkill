# Concept Sheet Segmentation

## Cel

Zamienić planszę prezentacyjną na zestaw technicznych źródeł.

## Segment classes

- `HERO`
- `ORTHO_FRONT`
- `ORTHO_SIDE`
- `ORTHO_TOP`
- `ORTHO_REAR`
- `ORTHO_BOTTOM`
- `DETAIL`
- `MATERIAL_SAMPLE`
- `TEXT_NOTE`
- `DIMENSION`
- `BRANDING`
- `NON_ASSET_GRAPHICS`

## Non-asset graphics

Nie są częścią modelu:
- tytuły planszy,
- strzałki opisowe,
- ramki,
- legendy,
- ikonografia funkcji,
- stopki dokumentu.

## Asset graphics

Mogą być częścią assetu:
- nadruk na ekranie,
- logo na obudowie,
- oznaczenie portu,
- rzeczywista dioda,
- napis na elemencie.

## Segmentation output

Tabela:
| Segment | Bounding region | Class | Canonical | Purpose |

## Ambiguous graphic

Jeżeli nie wiadomo, czy element jest nadrukiem na obiekcie czy adnotacją planszy:
status `AMBIGUOUS_GRAPHIC`.
Nie modeluj go przed rozstrzygnięciem.

# Orthographic Reference Calibration

## Cel

Zamienić rzut obrazkowy na mierzalną płaszczyznę.

## Inputs

- crop size px,
- known dimension,
- dimension line endpoints,
- object boundary,
- world axis.

## Scale derivation

Jeżeli odcinek `P px` odpowiada `L m`:
`meters_per_pixel = L / P`

Używaj tylko dla tej samej płaszczyzny rzutu.

## Dimension arrows

Preferuj mierzenie między markerami linii wymiarowej, nie między rozmytymi krawędziami renderu.

## Calibration checks

Po ustawieniu:
- total bounds muszą zgadzać się z wymiarem,
- ground line ma być wspólna,
- centerline powinna być spójna między widokami.

## Warning

Plansze marketingowe mogą nie mieć idealnie technicznych rzutów mimo etykiety "front view".
Status takiego widoku może być `NEAR_ORTHOGRAPHIC`.

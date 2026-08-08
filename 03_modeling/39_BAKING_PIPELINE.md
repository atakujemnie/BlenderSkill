# Baking Pipeline

## Cel

Przenieść informacje z modelu źródłowego do tekstur low-poly w sposób kontrolowany i powtarzalny.

## Typowe mapy

W zależności od pipeline:
- normal,
- ambient occlusion,
- curvature/masks,
- base color,
- roughness,
- metallic,
- emissive,
- custom masks.

Nie bake'uj map bez zastosowania runtime.

## Preflight

Przed bake:
- low-poly posiada finalne lub zamrożone UV,
- high i low są poprawnie wyrównane,
- transform scale jest świadomie obsłużony,
- naming/parowanie high-low jest deterministyczne,
- image targets mają właściwą rozdzielczość,
- color space jest właściwy dla typu mapy.

## Projection

Dostępne strategie:
- ray distance/extrusion,
- explicit cage,
- per-part bake,
- exploded bake.

Preferuj cage, gdy:
- projekcja na zakrzywionych/ciasnych strefach jest nieprzewidywalna,
- są blisko leżące powierzchnie,
- potrzebna jest większa kontrola.

## Bake segmentation

Dla złożonego assetu nie wymuszaj jednego bake wszystkiego naraz.

Rozdziel elementy, gdy:
- promienie przechodzą na sąsiednią część,
- powstają projection artifacts,
- części mają różne wymagania.

## Padding / margin

Padding musi uwzględniać:
- mipmapping,
- skalowanie tekstury,
- docelową rozdzielczość.

Nie ustawiaj jednej magicznej wartości dla wszystkich atlasów.

## Verification

Po bake:
1. nałóż mapę na low-poly,
2. ukryj high-poly,
3. renderuj pod grazing light,
4. sprawdź seams,
5. sprawdź skew,
6. sprawdź gradienty na płaskich powierzchniach,
7. sprawdź wynik po eksporcie.

## Artifact classes

- projection miss,
- cage intersection,
- skew,
- hard-edge mismatch,
- UV seam mismatch,
- tangent mismatch,
- insufficient padding,
- mirrored-normal issue.

Każdy typ błędu wymaga innej naprawy.

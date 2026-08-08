# Camera and Reference Matching

## Cel

Oddzielić błąd modelu od błędu kamery.

Agent nie może poprawiać geometrii tylko dlatego, że render z innej ogniskowej lub perspektywy nie przypomina concept artu.

## Kolejność

1. ustal typ referencji:
   - orthographic / technical view,
   - weak perspective,
   - perspective photograph,
   - stylized concept art;
2. ustal orientację obiektu;
3. dopasuj kamerę;
4. dopiero potem porównuj geometrię.

## Parametry kamery

Kontroluj jawnie:
- projection type,
- focal length / orthographic scale,
- sensor fit,
- camera position,
- camera rotation,
- lens shift,
- render aspect ratio.

## Technical reference

Dla front/side/top preferuj kamerę ortograficzną.

Wtedy:
- nie istnieje perspektywiczne zmniejszanie z głębokością,
- relacje szerokości i wysokości można porównywać stabilniej,
- camera distance nie powinna służyć jako "zoom"; używaj ortho scale.

## Perspective reference

Nie dopasowuj modelu przez lokalne deformacje, dopóki nie sprawdzisz:
- focal length,
- camera distance,
- horizon,
- vanishing lines.

## Camera lock

Po zatwierdzeniu kamery referencyjnej:
- nazwij ją,
- oznacz jako QA camera,
- nie zmieniaj jej podczas napraw geometrii.

Przykład:
`CAM_QA_Bench_Front`
`CAM_QA_Bench_Side`
`CAM_QA_Bench_34`

## Acceptance

Render z kamery QA powinien być deterministyczny:
- ten sam resolution,
- ten sam aspect,
- ten sam transform,
- ten sam render engine/profile.

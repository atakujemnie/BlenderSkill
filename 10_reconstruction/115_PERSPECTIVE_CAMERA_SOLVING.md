# Perspective Camera Solving

## Cel

Dopasować kamerę hero/detail tak, aby nie deformować modelu dla uzyskania podobnego renderu.

## Solve variables

- camera rotation,
- camera translation,
- focal length,
- sensor/fit,
- shift,
- object pose, jeśli nie jest już zablokowany.

## Landmark solve

Wybierz punkty o znanej lub zablokowanej geometrii:
- corners,
- panel intersections,
- base contacts.

Minimalizuj reprojection error.

## Solve order

1. zablokuj global dimensions,
2. zablokuj orientation,
3. oszacuj camera,
4. dopiero potem oceniaj hero view.

## Lens warning

Szerokokątna kamera może:
- powiększyć bliższy bok,
- zmienić apparent depth,
- zwiększyć różnicę wysokości.

Nie poprawiaj tego przez asymetryczne skalowanie modelu.

## QA

Po solve hero view jest materiałowym i detalicznym źródłem, ale geometryczny authority pozostaje zgodny z macierzą.

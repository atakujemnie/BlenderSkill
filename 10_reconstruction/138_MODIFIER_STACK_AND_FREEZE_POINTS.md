# Modifier Stack and Freeze Points

## Reconstruction stack

Dla każdego obiektu zapisz:
- modifier,
- purpose,
- feature IDs,
- dependency,
- freeze condition.

## Freeze points

### P0
Po blockout — zachowaj parametric.

### P1
Po D2 matching — można zamrozić wybrane booleans.

### P2
Przed UV/bake — topology-critical freeze.

### P3
Export copy — final evaluated mesh.

## Do not apply early

Wczesne Apply utrudnia:
- korekty wymiarów,
- zmianę gap/radius,
- feature regression.

## Do not keep everything live forever

Zbyt złożony stack:
- utrudnia stabilność,
- może być kosztowny,
- może powodować zależności.

Freeze jest decyzją pipeline, nie dogmatem.

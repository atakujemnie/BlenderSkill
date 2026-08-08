# Curves for Game Asset Authoring

## Zastosowania

Curves są użyteczne dla:
- kabli,
- rur,
- poręczy,
- listew,
- uszczelek,
- przewodów,
- profili prowadzonych po ścieżce.

## Authoring advantage

Curve pozwala oddzielić:
- przebieg,
- profil,
- grubość,
- resolution.

To ułatwia poprawki względem ręcznego przesuwania wielu vertices.

## Parameters

Kontroluj:
- spline points,
- handles,
- cyclic state,
- bevel depth/profile,
- resolution,
- tilt,
- radius.

## Runtime conversion

Curve jest przede wszystkim authoring representation.
Jeżeli runtime wymaga mesh:
- konwertuj na kontrolowanym etapie,
- zachowaj curve source,
- po konwersji zweryfikuj polycount i normals.

## Resolution

Nie ustawiaj wysokiej resolution domyślnie.
Dobierz ją do:
- promienia krzywizny,
- dystansu kamery,
- silhouette.

## Endpoints

Sprawdź:
- caps,
- połączenie z assetem,
- przenikanie,
- orientację profilu.

## Reusable profiles

Profile rur, uszczelek i listew powinny być współdzielone, jeśli projekt wykorzystuje jeden język konstrukcyjny.

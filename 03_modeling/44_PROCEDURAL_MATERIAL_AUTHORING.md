# Procedural Material Authoring

## Rola

Proceduralny shader jest narzędziem authoringowym.
Nie zakładaj, że cały graph zostanie przeniesiony do silnika.

## Dobre zastosowania

- szybkie lookdev,
- maski,
- proceduralne zabrudzenie,
- tileable surface detail,
- generowanie danych do bake.

## Runtime decision

Dla każdego proceduralnego efektu wybierz:
- recreate in engine,
- bake to textures,
- remove,
- Blender-only preview.

## Coordinate discipline

Jawnie wybieraj coordinate space:
- UV,
- object,
- generated,
- world.

Zmiana transformacji obiektu może wpływać na proceduralne mapowanie.

## Scale

Proceduralne wzory muszą mieć fizyczną skalę.
"Noise scale = 5" bez odniesienia do metrów projektu nie jest trwałą wiedzą.

## Material parameters

Preferuj wspólny zestaw:
- base color family,
- roughness range,
- metallic state,
- normal strength,
- detail scale,
- wear amount.

## Game-ready

Przed eksportem sprawdź:
- które właściwości są rzeczywiście reprezentowane przez docelowy format,
- czy tekstury zostały wypieczone,
- czy packed channels są zgodne z silnikiem.

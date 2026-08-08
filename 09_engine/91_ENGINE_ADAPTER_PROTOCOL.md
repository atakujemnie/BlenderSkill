# Engine Adapter Protocol

## Cel

Oddzielić wiedzę o tworzeniu assetu od wiedzy o importerze konkretnego silnika.

## Adapter responsibilities

Adapter definiuje:
- mapowanie osi,
- mapowanie materiałów,
- nazwy collision,
- nazwy LOD,
- hierarchy rules,
- animation mapping,
- texture packing,
- export flags.

## Neutral asset

Główna biblioteka opisuje:
- poprawny model,
- dane authoringowe,
- standardowy manifest.

Adapter:
- przekształca to do wymagań silnika.

## Zakaz przecieku

Nie zapisuj przypadkowych ograniczeń jednego silnika jako uniwersalnej zasady Blendera.

Przykład:
jeżeli silnik wymaga konkretnego prefiksu collision, reguła trafia do adaptera, nie do globalnego `GAME_ASSET_CONTRACT`.

## Round-trip / smoke test

Adapter powinien definiować minimalny test:
- import success,
- bounds,
- scale,
- materials,
- normals,
- animation,
- collision.

## Custom engine

Dla własnego silnika C++ należy utworzyć osobny plik:
`ENGINE_PROFILE_<NAME>.md`
oraz test importera.

# Decals and Floating Details

## Cel

Dodawać lokalne informacje wizualne bez cięcia głównej topologii.

## Kandydaci

- oznaczenia,
- logo,
- numery,
- ostrzeżenia,
- ślady serwisowe,
- cienkie panel lines,
- małe techniczne detale.

## Geometry decals / floating meshes

Dobre, gdy:
- potrzebny jest lokalny detal,
- główny mesh nie powinien być komplikowany,
- pipeline/runtime poprawnie obsługuje takie powierzchnie.

Kontroluj:
- z-fighting,
- offset,
- normals,
- bounds,
- LOD behavior.

## Texture decals

Dobre dla:
- oznaczeń,
- wariantów,
- zabrudzeń,
- informacji diegetycznych.

## Decal atlas

Dla wielu drobnych oznaczeń preferuj atlas zamiast osobnej tekstury per decal.

## Nie używaj decal jako maskowania błędu konstrukcyjnego

Jeżeli referencja ma realne wcięcie o widocznym parallax:
- geometria lub displacement/bake może być właściwszy.

## LOD

Małe decals powinny:
- zanikać w odpowiednim LOD,
- nie pozostawiać migoczących mikropowierzchni.

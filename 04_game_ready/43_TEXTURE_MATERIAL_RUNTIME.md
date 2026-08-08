# Texture and Material Runtime

## PBR portability

Jeżeli format docelowy opiera się na PBR metallic-roughness:
- mapuj materiał do tego modelu,
- sprawdź color space,
- sprawdź kanały packed textures,
- nie polegaj na Blender-only node graph.

## Normal maps

Sprawdź:
- tangent space,
- orientację,
- UV,
- zachowanie po triangulacji,
- zgodność z tangent basis runtime.

## Transparency

Transparency jest droższa i bardziej problematyczna niż opaque.
Używaj tylko, gdy design jej wymaga.

Rozróżniaj:
- opaque,
- alpha mask/cutout,
- alpha blend.

## Emissive

Emissive texture nie oznacza automatycznie realnego źródła światła w silniku.
To osobna decyzja runtime.

## Texture reuse

Preferuj:
- trim sheets,
- tileable materials,
- atlasy,
- współdzielone zestawy materiałów,

gdy zwiększa to wydajność bez utraty wizji.

## Bake

Bake jest wymagany, gdy authoring wykorzystuje efekt, którego runtime nie odtworzy bezpośrednio.

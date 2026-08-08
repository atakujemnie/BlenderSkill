# Example — Complex Prop with Multiple Materials

## Decomposition

- structural body,
- soft/contact surface,
- metallic shell,
- glass/display,
- emissive insert,
- fasteners.

## Material logic

Każda część ma oddzielny materiał tylko jeśli wymaga innego shader behavior.
W przeciwnym razie rozważ wspólny atlas/material.

## Build order

1. body,
2. major cutouts,
3. separate shells,
4. contact/soft regions,
5. screen/glass,
6. fasteners,
7. bevel/shading,
8. UV/material,
9. optimization.

## Glass

Nie zakładaj, że przezroczysty Principled material zachowa się identycznie w runtime.
Sprawdź docelowy alpha/transmission model.

## Emissive

Emissive insert:
- może być płaską powierzchnią,
- może wymagać bloom/light w runtime osobno,
- nie musi potrzebować dużej ilości geometrii.

## LOD

W dalszych LOD:
- śruby -> normal/decal/remove,
- małe gaps -> texture,
- glass frame -> uproszczony,
- podstawowa silhouette bez zmian.

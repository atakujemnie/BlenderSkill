# Hard Surface Workflow

## Etap 1 — Blockout

Buduj:
- prymitywy,
- proste extrude,
- podstawowe skosy.

Bez:
- mikrodetalu,
- finalnych beveli,
- gęstej topologii.

Wynik musi zgadzać się w silhouette.

## Etap 2 — Construction split

Podziel projekt zgodnie z logiką konstrukcji:
- korpus,
- panel,
- rama,
- wkład,
- metalowa osłona,
- mocowanie,
- element interaktywny.

Nie modeluj wszystkiego jako jednej siatki tylko po to, aby mieć "jeden obiekt".

## Etap 3 — Primary details

Dodaj:
- główne rowki,
- recess,
- otwory,
- charakterystyczne skosy,
- elementy łączące.

## Etap 4 — Edge treatment

Bevel width powinien wynikać ze:
- skali obiektu,
- materiału,
- sposobu produkcji,
- dystansu kamery.

Nie ustawiaj tego samego bevel width na wszystkich assetach.

## Etap 5 — Shading

Sprawdź:
- normals,
- hard/smooth transitions,
- bevel shading,
- artefakty boolean.

## Etap 6 — Optimization

Dopiero po zaakceptowaniu formy:
- usuń niewidoczną geometrię, jeśli bezpieczne,
- ogranicz segments bevel,
- uprość ukryte elementy,
- przygotuj LOD.

## Boolean policy

Booleans są dozwolone.
Nie oceniaj topologii wyłącznie według reguły "same quady".

Dla statycznego hard-surface ważniejsze są:
- brak artefaktów,
- stabilne normals,
- brak niekontrolowanych sliver triangles,
- przewidywalny eksport,
- wystarczająca edytowalność.

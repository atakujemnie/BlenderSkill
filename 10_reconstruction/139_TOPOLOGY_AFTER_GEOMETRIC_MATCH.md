# Topology After Geometric Match

## Kolejność

Najpierw poprawna geometria, potem optymalizacja topologii.

## Zakaz

Nie zmieniaj kształtu tylko po to, aby uzyskać "ładniejsze quady", jeśli:
- asset jest statyczny,
- shading i export są poprawne.

## Retopology goals

- silhouette preservation,
- stable triangulation,
- clean shading,
- UV suitability,
- lower cost.

## Critical edges

Zachowaj:
- profile,
- panel borders,
- bevel support,
- deformation edges, jeśli istnieją.

## Validation

Po cleanup/retopo:
uruchom silhouette + landmarks + MUST regression.

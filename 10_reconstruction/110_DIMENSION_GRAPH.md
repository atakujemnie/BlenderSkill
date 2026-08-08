# Dimension Graph

## Cel

Nie przechowywać wymiarów jako luźnej listy.
Zbudować graf zależności.

## Nodes

Przykłady:
- total_width,
- total_height,
- seat_height,
- side_housing_width,
- backrest_width,
- trim_width,
- gap.

## Edges

Relacje:
- sum,
- difference,
- ratio,
- alignment,
- symmetry,
- containment.

Przykład:
```text
backrest_width =
total_width
- left_housing_width
- right_housing_width
```

## Constraint types

- equality,
- inequality,
- min/max clearance,
- ratio,
- centered,
- aligned,
- tangent.

## Benefit

Zmiana jednego parametru może zostać propagowana bez ręcznego "poprawiania na oko".

## Rule

Dla assetu rekonstrukcyjnego parametry D0/D1 powinny wynikać z jednego spójnego dimension graph.

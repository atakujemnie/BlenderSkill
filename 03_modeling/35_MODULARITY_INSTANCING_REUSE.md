# Modularity, Instancing and Reuse

## Modular design

Moduł musi posiadać:
- jawny wymiar interfejsu,
- pivot zgodny z siatką modułową,
- płaskie / poprawne krawędzie łączenia,
- brak mikro-szczelin po złożeniu,
- spójny materiał i texel density.

## Reuse

Jeżeli dwa elementy są identyczne:
- preferuj linked mesh data lub instancing,
- nie twórz unikalnej geometrii bez powodu.

## Geometry duplication

Duplikowanie geometrii zwiększa:
- rozmiar assetu,
- pamięć,
- koszt authoringu.

Instancing jest szczególnie ważny dla:
- lamp,
- słupków,
- śrub,
- paneli,
- segmentów architektonicznych.

## Unikalność

Rozbij instancję tylko, gdy:
- potrzebuje osobnej deformacji,
- ma trwałą zmianę geometrii,
- bake wymaga unikalnego UV,
- silnik nie wspiera potrzebnego sposobu instancjonowania.

## Modular QA

Testuj:
- moduł A + A,
- A + B,
- rogi,
- zakończenia,
- odbicie,
- wielokrotne powtórzenie.

Błąd 1 mm powtarzany 100 razy staje się błędem systemowym.

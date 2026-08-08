# Reference Measurement Protocol

## Cel

Zamienić obraz referencyjny na zestaw relacji liczbowych.

## Known dimension anchor

Jeżeli znany jest co najmniej jeden wymiar:
1. wybierz wymiar dobrze widoczny w referencji,
2. wyznacz skalę piksel -> jednostka,
3. mierz tylko elementy w tej samej płaszczyźnie lub po korekcji perspektywy.

## Brak wymiaru absolutnego

Użyj normalized coordinates:
- width = 1.0
- height = H/W
- depth = D/W

Przechowuj relacje aż do uzyskania skali.

## Perspective warning

Nie wyprowadzaj bezpośrednich wymiarów z:
- silnego perspective,
- fisheye,
- nieznanego focal length,
- elementów leżących w różnych głębokościach.

## Multi-view

Jeżeli istnieją front/side/top:
- każdy wymiar bierz z widoku, w którym jest najmniej zniekształcony,
- wymiary wspólne muszą się zgadzać,
- sprzeczność zapisuj jako reference conflict.

## Measurement table

| Metric | Value | Source view | Confidence |
|---|---:|---|---|
| W | 1.80 m | front | HIGH |
| H | 0.82 m | front | HIGH |
| D | 0.55 m | side | MEDIUM |
| gap | 0.012 m | detail | LOW |

LOW confidence nie powinno sterować destrukcyjną geometrią bez checkpointu.

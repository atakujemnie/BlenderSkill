# Multi-View Consistency Gate

## Problem

Model może pasować do frontu i nie pasować do side.

## Gate order

1. numeric bounds,
2. front,
3. side,
4. top,
5. rear,
6. bottom,
7. hero,
8. details.

Nie oznacza to różnego priorytetu — chodzi o diagnostyczną kolejność.

## Structural pass

D0/D1 są zaakceptowane tylko, jeśli nie istnieje `FAIL` w żadnym kanonicznym ortho view.

## Conflict diagnosis

Jeśli poprawka front pogarsza side:
- parametr jest źle zdekomponowany,
- camera/reference może być źle skalibrowana,
- model ma błędny przekrój.

Nie iteruj losowo między widokami.

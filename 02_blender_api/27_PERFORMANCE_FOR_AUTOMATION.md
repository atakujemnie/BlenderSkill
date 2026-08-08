# Performance for Blender Automation

## Avoid repeated depsgraph churn

Zamiast wielu mikrozmian i wymuszania update po każdej:
- wykonaj logiczny batch,
- zaktualizuj i zweryfikuj na końcu batchu.

## Avoid UI-driven loops

Nie:
- klikaj,
- zaznaczaj,
- przełączaj mode,
- wywołuj operator,
setki razy, jeśli można zbudować mesh bezpośrednio.

## Avoid excessive object count

Osobne obiekty są użyteczne logicznie, ale tysiące mikro-obiektów:
- komplikują scene graph,
- zwiększają koszty authoringu,
- utrudniają selection i export.

Łącz elementy, gdy mają:
- tę samą funkcję runtime,
- ten sam materiał,
- brak niezależnej animacji,
- brak potrzeby wariantowania.

## Heavy modifiers

Przy dużej liczbie instancji authoringowych:
- kontroluj subdivision,
- boolean stack,
- high-segment bevel.

Wyłącz kosztowne elementy w viewport, jeśli pipeline tego wymaga, ale waliduj render/final state.

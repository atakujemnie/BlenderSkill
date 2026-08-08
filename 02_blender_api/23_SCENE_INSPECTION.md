# Scene Inspection

## Zanim cokolwiek zmienisz

Zbierz Scene Snapshot.

## Snapshot minimalny

- Blender version,
- active scene,
- unit system,
- object count,
- collections,
- mesh count,
- object names/types,
- active object,
- selected objects,
- mode,
- world scale,
- cameras,
- lights,
- existing asset roots,
- external file references.

## Dla assetu

Zbierz:
- dimensions,
- location,
- rotation,
- scale,
- parent,
- modifiers,
- mesh vertex/edge/polygon counts,
- UV layers,
- material slots,
- shape keys,
- armature,
- custom properties.

## Dla istniejącego modelu przed poprawką

Wygeneruj:
- front ortho,
- side ortho,
- top ortho,
- perspective 3/4,
- opcjonalnie rear/bottom,
- wireframe lub matcap,
- bounding dimensions.

Bez tego agent może "naprawiać" problem, którego nie ma, albo niszczyć inną część modelu.

## Snapshot jako tekst

Wynik audytu powinien być krótki i strukturalny.
Nie wypisuj tysięcy vertices.

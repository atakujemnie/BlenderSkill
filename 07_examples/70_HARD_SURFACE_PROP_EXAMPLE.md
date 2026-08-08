# Example — Hard-Surface Street Prop

## Brief

Statyczny miejski prop sci-fi:
- czytelny z 2–8 m,
- gracz może obejść go dookoła,
- kilka materiałów,
- produkowany masowo,
- powinien nadawać się do instancjonowania.

## Feature Contract

| ID | Priority | Feature | Build |
|---|---|---|---|
| F001 | MUST | charakterystyczna sylwetka korpusu | blockout mesh |
| F002 | MUST | wcięty panel frontowy | inset/boolean |
| F003 | MUST | metalowa rama | separate mesh |
| F004 | SHOULD | szczelina montażowa | geometry/normal |
| F005 | SHOULD | logo | decal/texture |

## Strategy

1. Korpus z prymitywu.
2. Panel jako osobna część lub boolean recess.
3. Rama jako oddzielny mesh, aby niezależnie kontrolować materiał.
4. Bevel dopiero po zaakceptowaniu proportions.
5. Neutral shading checkpoint.
6. UV/material.
7. LOD1: uproszczone bevels i usunięte drobne szczeliny.
8. Collision: prosty hull/box decomposition.

## Błąd, którego należy unikać

Nie generuj mikrodetali przed sprawdzeniem bryły. Poprawianie szerokości całego korpusu po detalach powoduje regresje i kolejne kosztowne operacje.

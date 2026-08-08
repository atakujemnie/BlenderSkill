# Modifiers and Non-Destructive Modeling

## Preferowany stack hard-surface

Nie jest uniwersalny, ale często:
1. Mirror / Array
2. Booleans / shape operations
3. Solidify
4. Bevel
5. normal/shading treatment

Kolejność musi być świadoma.

## Mirror

Używaj, gdy asymetria nie jest wymagana.
Sprawdź:
- origin,
- axis,
- clipping/merge,
- czy późniejsze detale powinny być mirrorowane.

## Array

Używaj dla powtarzalności.
Nie twórz ręcznie kilkudziesięciu kopii.

## Solidify

Dobre dla:
- paneli,
- osłon,
- cienkich powierzchni.

Kontroluj:
- thickness,
- offset,
- normals,
- narożniki.

## Bevel

Bevel jest częścią designu i shadingu, nie tylko kosmetyką.
Kontroluj:
- width,
- segments,
- angle/weight/vertex group,
- miter,
- overlap.

## Decimate

Nie stosuj automatycznie do gotowego hard-surface jako "optymalizacji".
Może uszkodzić:
- silhouette,
- UV,
- normals,
- kontrolowane edge flow.

## Apply policy

Nie aplikuj modifiera, dopóki:
- kolejny etap tego nie wymaga,
- eksport/bake tego nie wymaga,
- stack nie stał się niestabilny,
- trzeba przekazać finalną siatkę do narzędzia, które nie obsługuje modifiera.

Przed Apply utwórz checkpoint.

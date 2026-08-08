# Boolean, Recess and Trim Playbook

## Recess

Dla wpuszczonego panelu określ:
- outer outline,
- border width,
- recess depth,
- corner radius,
- bottom surface.

## Boolean cutter

Cutter powinien:
- mieć kontrolowane wymiary,
- być tagowany feature ID,
- posiadać wystarczające przenikanie,
- nie tworzyć przypadkowych coplanar contacts.

## Trim

Trim jako osobny mesh jest preferowany, gdy:
- ma inny materiał,
- tworzy własną silhouette,
- ma kontrolowaną grubość.

## Modifier order

Kolejność musi zostać zapisana per object.
Typowy problem:
bevel przed/po boolean daje inny wynik.

## Cleanup

Po boolean sprawdź:
- slivers,
- shading,
- tiny faces,
- nienaturalne pinching.

## Feature ownership

Cutter/helper nie jest feature owner po apply, jeśli zostaje usunięty.
Owner staje się finalny mesh/region.

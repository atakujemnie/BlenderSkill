# Authoring to Runtime Handoff

## Artefakty

Minimalny pakiet może zawierać:
- source `.blend`,
- export mesh/scene,
- textures,
- material mapping,
- collision,
- animation,
- asset manifest,
- validation report.

## Manifest

```text
asset_id
version
source_blender_version
export_format
units
bounds
pivot_policy
objects
materials
textures
triangle_counts
lods
collision
animations
dependencies
known_limitations
```

## Source retention

Nie nadpisuj źródła edytowalnego finalnym flattened mesh.

## Re-import test

Jeśli pipeline pozwala:
1. export,
2. import do czystej sceny/test runtime,
3. porównanie manifestu,
4. visual smoke test.

## Version

Każdy istotny export powinien być możliwy do powiązania z:
- wersją source asset,
- wersją biblioteki agenta,
- wersją Blendera,
- profilem eksportu.

## Handoff failure

Brak błędu eksportera nie oznacza poprawnego handoff.
Poprawność ocenia wynik po stronie konsumenta.

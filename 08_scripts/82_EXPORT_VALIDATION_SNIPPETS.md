# Export Validation Snippets

## Pre-export manifest

Przed exportem utwórz manifest:
- object names,
- types,
- bounds,
- material slots,
- animation data,
- parent hierarchy.

```python
import bpy

def manifest(objects):
    out = []
    for obj in objects:
        out.append({
            "name": obj.name,
            "type": obj.type,
            "parent": obj.parent.name if obj.parent else None,
            "dimensions": [float(v) for v in obj.dimensions],
            "materials": [slot.material.name if slot.material else None for slot in obj.material_slots],
            "has_animation": bool(obj.animation_data),
        })
    return out
```

## Post-export principle

Po eksporcie nie zakładaj poprawności na podstawie braku exception.

Porównaj:
- liczbę expected nodes,
- bounds,
- materiały,
- texture references,
- animation clips,
- root hierarchy.

Jeżeli pipeline posiada importer round-trip:
1. export do pliku tymczasowego,
2. import do czystej sceny,
3. wykonaj ten sam manifest,
4. porównaj z tolerancją.

Nie wykonuj round-trip na głównej scenie.

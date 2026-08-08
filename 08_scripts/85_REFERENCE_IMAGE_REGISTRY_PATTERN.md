# Reference Image Registry Pattern

```python
REFERENCE_REGISTRY = {
    "SEG_FRONT": {
        "path": "...",
        "projection": "ORTHO",
        "physical_width_m": 2.0,
        "axis": "FRONT",
        "approved": True,
    },
}
```

## Blender image empties

Reference images mogą być trzymane jako image empties.
Agent powinien:
- nadać stabilne nazwy,
- umieścić je w osobnej kolekcji,
- ustawić display opacity,
- lock transforms po kalibracji.

## Naming

`REF_<ASSET>_<VIEW>`

## Rule

Nie polegaj na active image w UI.
Trzymaj jawne referencje do objects/data-blocks.

# Dimension Graph Validator Pattern

```python
constraints = [
    {
        "id": "C_WIDTH",
        "target": 2.0,
        "tolerance": 0.001,
        "measure": lambda scene: asset_bounds(scene)["width"],
    },
]
```

## Result

```text
constraint
target
actual
error
tolerance
PASS/FAIL
```

## Derived constraint

Niektóre constrainty nie mierzą tylko bounds:
- distance between landmarks,
- angle between vectors,
- panel offset,
- gap.

## Rule

Validator jest read-only.
Nie poprawia geometrii.

# Landmark Projection Pattern

## Cel

Rzutować punkt świata na współrzędne kamery QA.

Blender udostępnia macierze obiektów i kamery; implementacja może używać odpowiednich utilities/API dla projekcji.

## Record

```python
LANDMARKS = {
    "LM_SEAT_FRONT_LEFT": {
        "object": "Bench_Seat",
        "local_point": (...),
        "reference": {
            "FRONT": (u, v),
            "SIDE": (u, v),
        },
    },
}
```

## Output

- projected UV/image coordinate,
- target,
- delta,
- tolerance.

## Rule

Po zmianie topology local vertex index nie jest stabilnym landmark ID.
Preferuj:
- named helper empty,
- parametric coordinate,
- semantic feature point.

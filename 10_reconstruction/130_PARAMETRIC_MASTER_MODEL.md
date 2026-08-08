# Parametric Master Model

## Cel

D0/D1 model powinien być sterowany małym zestawem parametrów.

## Master parameters

- bounds,
- primary widths,
- heights,
- depths,
- main angles,
- major radii,
- major gaps.

## Derived parameters

Obliczaj:
- inner widths,
- center offsets,
- mirrored positions,
- panel dimensions.

## Benefits

- łatwe korekty po pomiarze,
- mniej mikroruchów,
- spójność widoków,
- mniej tool calls.

## Freeze levels

### F0
Wszystko parametryczne.

### F1
D0/D1 locked.

### F2
D2 locked.

### F3
Bake/UV critical geometry frozen.

## Rule

Nie freeze'uj master modelu przed przejściem multi-view blockout gate.

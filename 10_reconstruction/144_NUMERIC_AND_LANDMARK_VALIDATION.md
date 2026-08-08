# Numeric and Landmark Validation

## Numeric checks

- dimensions,
- angles,
- distances,
- offsets,
- radii where known,
- symmetry axes,
- ground contacts.

## Projected landmarks

Dla widoku:
- project 3D landmark,
- compare with reference coordinate,
- calculate error.

## Error normalization

Możesz raportować:
- pixels,
- normalized image fraction,
- millimeters after calibration.

## Priority weighting

MUST landmark ma wyższą wagę.

## Gate example

```text
hard_dimensions: PASS
critical_landmarks: PASS
secondary_landmarks: <= allowed MINOR
```

Nie wprowadzaj jednej magicznej średniej, która pozwala skompensować duży błąd jednym poprawnym punktem.

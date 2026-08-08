# Error Handling

## Nie łap wyjątków bez reakcji

Błędny wzorzec:
```python
try:
    ...
except:
    pass
```

## Minimalny log błędu

- stage,
- operation,
- asset id,
- object names,
- context mode,
- exception type,
- message.

## Fail fast

Jeżeli postcondition nie jest spełniony:
- nie kontynuuj kolejnych etapów,
- oznacz phase jako FAIL,
- pozostaw scenę w możliwie stabilnym stanie.

## Validation errors vs runtime exceptions

Rozróżniaj:
- Python exception,
- Blender operator poll failure,
- invalid scene state,
- visual QA failure,
- runtime contract failure.

Każdy wymaga innej naprawy.

## Cleanup

Jeżeli batch tworzy tymczasowe cuttery/helpers:
- oznacz je,
- usuń tylko te utworzone przez batch,
- nie usuwaj obiektów "po nazwie podobnej", jeśli identyfikacja nie jest pewna.

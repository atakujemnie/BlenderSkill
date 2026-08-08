# Tool Call and Token Efficiency

## Cel

Minimalizuj:
- liczbę wywołań API,
- powtarzane inspekcje,
- duże logi,
- iteracyjne mikroruchy,
- generowanie kodu dla operacji, które można wykonać parametrycznie.

## Zasada batch

Jedno wywołanie powinno wykonywać logicznie spójny etap:
- stworzenie blockoutu,
- dodanie zestawu głównych modifierów,
- audit,
- generacja renderów kontrolnych.

Nie łącz w jednym batchu etapów o różnym ryzyku.

## Zasada inspect-before-act

Nie próbuj kolejnych losowych operatorów.
Najpierw odczytaj:
- mode,
- active object,
- modifier stack,
- mesh stats,
- dimensions.

## Zasada parameterize

Zamiast 20 poleceń:
`move vertex A, move vertex B...`

Utwórz parametry:
```python
WIDTH = 1.8
DEPTH = 0.55
HEIGHT = 0.82
FRAME = 0.04
BEVEL = 0.006
```

Buduj z nich geometrię.

## Zasada local patch

Przy błędzie napraw tylko:
- feature,
- obiekt,
- modifier,
- region.

Nie przebudowuj całego assetu, jeżeli problem jest lokalny.

## Zasada compact diagnostics

Loguj:
- nazwa kroku,
- affected objects,
- before/after counts,
- postcondition,
- error.

Nie loguj pełnych obiektów RNA ani wszystkich współrzędnych.

## Zasada no visual guessing loop

Jeżeli agent po renderze "przesuwa trochę" obiekt pięć razy, workflow jest błędny.
Najpierw zmierz błąd, potem wykonaj jedną korektę.

## Limit eksperymentów

Dla nieznanej operacji:
1. wykonaj na kopii/test mesh,
2. oceń wynik,
3. dopiero zastosuj do assetu.

Nie eksperymentuj na głównym modelu.

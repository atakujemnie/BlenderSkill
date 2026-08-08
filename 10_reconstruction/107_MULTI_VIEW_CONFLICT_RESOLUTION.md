# Multi-View Conflict Resolution

## Typy konfliktów

- wymiarowy,
- topologiczny,
- materiałowy,
- feature presence,
- asymmetry,
- profile shape,
- perspective artifact.

## Procedura

1. zidentyfikuj konflikt,
2. określ właściwość,
3. przypisz evidence IDs,
4. porównaj authority,
5. sprawdź, czy konflikt wynika z projekcji,
6. wybierz rozwiązanie,
7. zapisz odrzuconą alternatywę.

## Resolution classes

### RESOLVED_EXPLICIT
Rozstrzygnięte liczbą lub opisem.

### RESOLVED_AUTHORITY
Rozstrzygnięte macierzą autorytetu.

### RESOLVED_PROJECTION
Różnica wynika z kamery.

### UNRESOLVED
Nie ma wystarczających dowodów.

## Zakaz średniej

Nie stosuj:
`(front_value + side_value)/2`
bez uzasadnienia.

Sprzeczne źródła nie stają się prawdziwe przez uśrednienie.

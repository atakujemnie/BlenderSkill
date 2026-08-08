# Dimension Locking and Tolerances

## Lock classes

### HARD LOCK
Wartość nie może się zmienić bez zmiany kontraktu.

### DERIVED LOCK
Wynika z innych locków.

### SOFT TARGET
Powinna zostać zachowana, ale może być skorygowana przy konflikcie.

### FREE
Nie określona.

## Tolerancje

Tolerancja zależy od typu parametru.

### Interface / modular
Praktycznie zerowa w granicach precyzji pipeline.

### Global dimensions
Domyślnie bardzo mała, jeśli wymiar jest jawny.

### Measured-from-image
Tolerancja uwzględnia:
- rozdzielczość,
- anti-aliasing,
- grubość linii,
- perspektywę.

### Material appearance
Nie opisuj tolerancji w milimetrach; użyj QA wizualnego.

## Lock report

Przed PRIMARY_DETAIL wydrukuj wszystkie HARD LOCK.
Po każdej zmianie strukturalnej sprawdź je ponownie.

# Reconstruction Safety Rules for Scene Integrity

## Nie dotyczy bezpieczeństwa fizycznego — dotyczy integralności danych.

## Rules

- nie usuwaj source references,
- nie modyfikuj zaakceptowanych QA cameras bez logu,
- nie nadpisuj master parameters z lokalnej naprawy,
- nie apply'uj destructive operations bez checkpointu,
- nie usuwaj helpers oznaczonych przez inne feature IDs,
- nie zmieniaj units w połowie assetu.

## Recovery assets

Przechowuj:
- last accepted blockout,
- last accepted D2,
- pre-UV source,
- pre-export source.

## Scene contamination

Testowe obiekty i cuttery:
- w osobnej kolekcji,
- tagowane,
- usuwane jawnie.

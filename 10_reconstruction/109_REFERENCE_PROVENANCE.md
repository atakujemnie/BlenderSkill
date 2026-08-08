# Reference Provenance

## Cel

Każdy parametr i feature ma być możliwy do prześledzenia do źródła.

## Provenance chain

`Reference -> Segment -> Evidence -> Constraint -> Feature -> Scene owner -> QA result`

## Why

Bez provenance agent:
- zapomina, skąd wziął liczbę,
- nie wie, co zmienić po wymianie referencji,
- miesza dane z wcześniejszych wersji.

## Versioning

Każda referencja:
- id,
- revision,
- approval state,
- checksum/file metadata, jeśli pipeline pozwala.

## Stale reference

Jeśli concept sheet został zastąpiony:
- nie przepisuj nowych informacji na stary kontrakt po kawałku,
- oznacz affected constraints,
- uruchom impact analysis.

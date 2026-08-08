# Execution Protocol

## 1. Preflight

- odczytaj Scene Snapshot,
- sprawdź Blender version,
- sprawdź jednostki,
- sprawdź, czy asset już istnieje,
- sprawdź Feature Contract,
- sprawdź Build Plan.

## 2. Create asset root

Utwórz lub znajdź:
- collection assetu,
- root object/empty, jeśli pipeline tego wymaga,
- naming namespace.

## 3. Build by phase

Każdy phase:
1. loguje start,
2. wykonuje spójny batch,
3. aktualizuje scenę,
4. wykonuje postcondition,
5. zapisuje status feature IDs,
6. uruchamia checkpoint.

## 4. Postcondition examples

Po stworzeniu blockoutu:
- obiekt istnieje,
- dimensions są zgodne,
- scale jest oczekiwana,
- liczba części się zgadza.

Po boolean:
- modifier/rezultat istnieje,
- nie zniknęły faces z innej strefy,
- bounds nie zmieniły się poza tolerancją.

Po bevel:
- width zgodny,
- segment count zgodny,
- brak self-overlap.

## 5. Checkpoint

Nie kontynuuj, jeśli checkpoint FAIL.

## 6. Save

Zapisuj:
- przed ryzykownym Apply,
- po zaakceptowanym dużym etapie,
- przed exportem.

## 7. No silent repair

Jeżeli wykonanie różni się od planu, zapisz to jako deviation.
Nie zmieniaj strategii po cichu.

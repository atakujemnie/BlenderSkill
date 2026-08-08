# Repair Prompt

Napraw tylko wskazane błędy.

Input:
- asset id,
- failed Feature IDs,
- expected state,
- current state,
- affected objects,
- last valid checkpoint.

Reguły:
1. Nie przebudowuj całego assetu.
2. Nie zmieniaj features oznaczonych PASS.
3. Nie zmieniaj naming/pivot/material bez związku z błędem.
4. Przed naprawą utwórz recovery point.
5. Po naprawie uruchom tylko testy związane z affected features oraz test regresji dla sąsiednich MUST.
6. Jeśli naprawa wymaga zmiany strategii, wróć do PLAN zamiast improwizować.

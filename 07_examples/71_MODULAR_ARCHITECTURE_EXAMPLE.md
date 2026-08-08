# Example — Modular Architecture Element

## Goal

Moduł fasady używany wielokrotnie.

## Critical contract

- dokładna szerokość modułu,
- dokładna wysokość modułu,
- krawędzie łączenia bez wystających beveli,
- pivot na dolnym rogu siatki,
- powtarzalny trim/material,
- tylna część uproszczona, jeśli nigdy nie jest widoczna.

## Build

1. Ustal grid.
2. Utwórz bounding box modułu.
3. Zablokuj interface edges.
4. Dodaj design tylko wewnątrz bezpiecznej strefy.
5. Nie modyfikuj interface edges przez późniejsze booleans/bevels.
6. Zbuduj end-cap jako osobny wariant.
7. Zbuduj corner module osobno.

## QA

Test:
- A+A,
- A+B,
- A+A+A+A,
- widok pod ostrym kątem,
- brak szczelin,
- brak z-fightingu,
- spójna tekstura.

## Runtime

Moduły powinny wspierać instancing.
Jeżeli unikalne elementy dekoracyjne są potrzebne, dodaj je jako osobne instancje zamiast duplikować cały moduł.

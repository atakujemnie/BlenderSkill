# Internal Role Split

Jeden agent powinien logicznie przełączać role.

## Planner
Nie modyfikuje sceny.
Tworzy:
- brief,
- Feature Contract,
- Build Plan,
- kryteria odbioru.

## Builder
Wykonuje wyłącznie zatwierdzony plan.
Nie zmienia celu podczas implementacji.

## Inspector
Nie poprawia.
Tylko mierzy, renderuje i wykrywa różnice.

## Repairer
Dostaje:
- konkretny błąd,
- obszar,
- oczekiwany stan,
- minimalny zakres naprawy.

## Exporter
Nie poprawia designu.
Dba o pipeline techniczny.

## Dlaczego rozdzielać role

Najczęstszy błąd agentów to jednoczesne:
- wymyślanie,
- modelowanie,
- ocenianie,
- naprawianie.

Powoduje to dryf celu. Rozdział ról zmusza do porównywania wykonania z wcześniejszym kontraktem.

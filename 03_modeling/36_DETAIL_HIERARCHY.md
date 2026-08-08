# Detail Hierarchy

## D0 — Global silhouette
Najważniejsza warstwa.

## D1 — Primary forms
Duże podziały bryły.

## D2 — Secondary forms
Panele, wycięcia, ramy, większe łączenia.

## D3 — Tertiary geometry
Śruby, małe szczeliny, przyciski, małe fazy.

## D4 — Surface detail
Rysy, mikro-wzór, drobna faktura, normal detail.

## Reguła budowania

Nie przechodź do D(n+1), jeśli D(n) nie jest zaakceptowane.

## Reguła optymalizacji

Usuwaj w odwrotnej kolejności:
D4 -> D3 -> część D2 -> nigdy D0 bez jawnej zmiany LOD.

## Reguła oceny

Jeżeli asset wygląda źle z odległości, problem prawdopodobnie leży w D0/D1, a nie w braku śrub.

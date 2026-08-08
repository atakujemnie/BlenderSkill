# Dimension-Locked Blockout

## Blockout ma już być mierzalny

Nie oznacza "luźnych kostek".
Powinien spełniać:
- total bounds,
- primary division,
- seat/back/leg positions,
- główne kąty,
- negative spaces.

## Allowed

- proste bryły,
- mała liczba segmentów,
- approximate bevel only jeśli wpływa na silhouette.

## Forbidden

- tekstury,
- branding,
- mikrodetale,
- final bake,
- kosmetyczne śruby.

## Gate

Blockout przechodzi tylko, gdy:
- wszystkie HARD LOCK pass,
- silhouette pass w kanonicznych widokach,
- negative space pass,
- primary landmarks pass.

## Repair

Jeżeli FAIL:
wróć do dimension graph, nie maskuj błędu bevelami.

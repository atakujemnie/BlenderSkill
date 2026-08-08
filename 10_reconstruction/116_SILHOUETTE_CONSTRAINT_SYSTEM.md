# Silhouette Constraint System

## Silhouette is D0

Dla każdego kanonicznego widoku utwórz:
- maskę referencji,
- maskę renderu,
- contour representation.

## Metrics

Możliwe:
- intersection over union,
- area error,
- contour distance,
- directional extrema error.

## Extrema

Kontroluj:
- leftmost,
- rightmost,
- topmost,
- bottommost,
- charakterystyczne lokalne extrema.

## Weighted contour

Nie wszystkie fragmenty obrysu są równie ważne.
Wyższa waga:
- charakterystyczne skosy,
- transition seat/back,
- nogi,
- podłokietniki,
- główne łuki.

## Gate

Nie dodawaj D2/D3, jeśli silhouette D0/D1 nie przechodzi wszystkich kanonicznych widoków.

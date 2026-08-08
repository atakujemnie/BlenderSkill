# Stylized Concept Reconstruction Mode

## Problem

Stylizowany concept może być celowo niespójny geometrycznie.

## Priority

1. approved hero silhouette,
2. functional requirements,
3. multi-view consistency, jeśli dostępna,
4. manufacturing plausibility.

## Intent extraction

Zidentyfikuj:
- shape language,
- proportions,
- focal features.

## Authorized resolution

Gdy dwa widoki są niemożliwe do pogodzenia:
utwórz spójny model 3D zgodny z ustalonym authority, a konflikt pozostaw w raporcie.

## Do not call exact

Jeżeli źródło samo nie definiuje jednoznacznej geometrii, wynik może być:
`CANONICAL_3D_INTERPRETATION`
zamiast literalnego "1:1".

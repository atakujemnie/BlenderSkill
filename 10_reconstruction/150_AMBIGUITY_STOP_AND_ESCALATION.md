# Ambiguity Stop and Escalation

## Agent może kontynuować mimo części niewiadomych tylko, gdy nie wpływają one na bieżący etap.

## BLOCKING ambiguity

Przykłady:
- nie wiadomo, który widok jest frontem,
- sprzeczne total dimensions,
- nie wiadomo, czy asymetria jest zamierzona,
- nieznany interface dimension.

## NON-BLOCKING

- brak dokładnego micro-radius,
- niewidoczna śruba od spodu,
- drobny materiałowy noise.

## Escalation record

```text
ambiguity_id
affected_features
evidence
possible interpretations
impact
recommended resolution
```

## No silent choice

Agent nie może wybrać jednej z dwóch równie prawdopodobnych interpretacji i zapisać jej jako fact.

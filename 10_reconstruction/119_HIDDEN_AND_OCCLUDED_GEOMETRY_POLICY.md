# Hidden and Occluded Geometry Policy

## Cztery klasy

### H0 — explicitly shown
Musi być odwzorowane zgodnie z referencją.

### H1 — functionally required
Niewidoczne, ale potrzebne do działania lub poprawnej bryły.

### H2 — runtime required
Collision, backing surface, closed volume itp.

### H3 — unknowable
Brak dowodów i brak konieczności.

## H3 policy

Nie inventuj szczegółów.
Zastosuj:
- prostą powierzchnię,
- logiczne domknięcie,
- minimalną konstrukcję.

## Occluded transition

Jeśli dwie widoczne części muszą się połączyć za przeszkodą:
rekonstrukcja ma użyć najprostszego ciągłego połączenia, które nie łamie innych widoków.

## Report

Każda większa H3 powierzchnia powinna być oznaczona jako inferred.

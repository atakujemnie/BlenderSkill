# Reconstruction Evidence Model

Każde twierdzenie o modelu powinno mieć źródło dowodowe.

## Typy dowodów

### E0 — Explicit numeric
Wymiar, kąt, promień lub opis podany liczbowo.
Najwyższy priorytet geometryczny.

### E1 — Orthographic view
Front/side/top/rear/bottom bez istotnej perspektywy.

### E2 — Technical detail view
Zbliżenie lub przekrój pokazujący lokalny kształt.

### E3 — Perspective hero view
Dobre źródło:
- materiałów,
- edge language,
- relacji przestrzennych.
Słabsze źródło wymiarów.

### E4 — Text annotation
Opis funkcji, materiału, technologii.

### E5 — Manufacturing inference
Wniosek z konstrukcji.

### E6 — Artistic inference
Najniższy priorytet.
Dozwolone tylko przy braku mocniejszych dowodów.

## Evidence record

```text
evidence_id
type
source
view
region
claim
confidence
conflicts_with
notes
```

## Rule

Agent nie może nadpisać E0/E1 na podstawie E3/E6 bez zapisania konfliktu.

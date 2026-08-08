# Definition of 1:1 Reconstruction

## 1:1 nie oznacza fotograficznej identyczności pojedynczego renderu

Model 3D jest uznawany za rekonstrukcję 1:1, jeśli maksymalizuje zgodność z całym zestawem dowodów jednocześnie.

## Pięć warstw zgodności

### R1 — Metric fidelity
Znane wymiary, kąty, offsety i pozycje mieszczą się w tolerancji.

### R2 — Multi-view shape fidelity
Front, side, top, rear i inne widoki zgadzają się równocześnie.

### R3 — Feature fidelity
Każda cecha `MUST` istnieje, znajduje się w poprawnej strefie i ma właściwe proporcje.

### R4 — Surface fidelity
Materiały, edge treatment, roughness, metaliczność, emisja i tekstury odpowiadają dowodom.

### R5 — Construction fidelity
Podział elementów, warstwy materiałowe, szczeliny i grubości są zgodne z logiką obiektu i referencją.

## Nieprawidłowa definicja

"Render 3/4 wygląda prawie tak samo."

To może ukryć:
- błędną głębokość,
- złe pochylenie,
- złą szerokość boków,
- brak detalu z tyłu,
- błędny spód,
- niepoprawne wymiary.

## Hard gate

Jeśli znany wymiar jest przekroczony ponad tolerancję, asset nie jest 1:1 nawet jeśli wygląda dobrze.

## Niepewność

Gdy referencja nie definiuje parametru, wynik nie może być opisany jako "dokładnie 1:1" w tym parametrze.
Status:
- `EXACT`
- `DERIVED`
- `INFERRED`
- `UNKNOWN`

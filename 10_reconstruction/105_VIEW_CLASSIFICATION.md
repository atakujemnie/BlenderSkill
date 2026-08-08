# View Classification

## Klasy projekcji

### ORTHOGRAPHIC
Brak zbieżności równoległych osi.
Nadaje się do bezpośredniego porównywania proporcji w płaszczyźnie.

### NEAR_ORTHOGRAPHIC
Mała perspektywa.
Może wymagać korekcji.

### PERSPECTIVE
Wymaga dopasowania kamery.

### STYLIZED
Nie musi być geometrycznie spójny.

## View axis

Określ:
- front axis,
- side direction,
- top direction,
- rear direction,
- bottom direction.

## Mirroring trap

Rear view nie powinien być automatycznie traktowany jako poziome odbicie front view.
Może pokazywać rzeczywistą asymetrię.

## Confidence

Każdy view otrzymuje:
- projection confidence,
- orientation confidence,
- geometry confidence.

## Rule

Nie twórz constraintu 3D z widoku, którego orientacja nie została ustalona.

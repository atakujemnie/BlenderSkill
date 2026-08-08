# Feature Contract

Feature Contract jest głównym zabezpieczeniem przed utratą detali.

## Format

| ID | Priority | Feature | Evidence | Measurement | Build method | QA method | Status |
|---|---|---|---|---|---|---|---|
| F001 | MUST | Główna sylwetka | front ref | W:H:D | blockout mesh | ortho compare | TODO |
| F002 | MUST | Rowek boczny | side ref | offset/width/depth | inset/boolean | close render | TODO |
| F003 | SHOULD | Bevel | visual | width | modifier | grazing light | TODO |

## Priority

### MUST
Bez tej cechy asset jest niepoprawny.

### SHOULD
Istotna jakość, ale brak nie zmienia tożsamości.

### OPTIONAL
Może zostać pominięta przy ograniczeniu czasu/runtime.

## Feature ownership

Każda cecha musi mieć jednoznacznego właściciela:
- konkretny obiekt,
- modifier,
- material,
- texture,
- animation,
- hierarchy entry.

Nie zapisuj cechy jako "zrobionej", jeżeli nie można wskazać, gdzie istnieje w danych sceny.

## Anti-loss rule

Przed każdą większą zmianą:
1. sprawdź listę `MUST`,
2. ustal, które obiekty/modifiery je realizują,
3. po zmianie ponownie je zweryfikuj.

## Geometry vs texture decision

Cecha powinna być geometrią, gdy:
- zmienia silhouette,
- tworzy istotny parallax,
- jest widoczna z bliska,
- wpływa na cień,
- jest interaktywna.

Może być normal/height/detail mapą, gdy:
- nie zmienia silhouette,
- jest drobna względem texel density,
- jest powtarzalna,
- koszt geometrii nie daje wartości wizualnej.

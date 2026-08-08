# Visual Feature Map

## Cel

Połączyć pikselowy obszar referencji z konkretną cechą modelu.

Feature Contract mówi *co* istnieje.
Visual Feature Map mówi *gdzie tego szukać* na renderze.

## Rekord cechy

```text
feature_id: F012
view: FRONT
roi_normalized: [x0, y0, x1, y1]
expected_edges: ...
expected_material_region: ...
occlusion_allowed: false
```

`roi_normalized` używa zakresu 0..1 niezależnie od rozdzielczości.

## Użycie

Visual Feature Map służy do:
- lokalnego image diff,
- kontroli czy feature nie zniknął,
- ograniczenia naprawy do konkretnego obszaru,
- zmniejszenia liczby błędnych wniosków wynikających ze zmian w tle.

## Nie każdy feature ma jeden ROI

Cecha może:
- występować w kilku widokach,
- być częściowo zasłonięta,
- mieć region dynamiczny.

## MUST features

Dla każdego wizualnego `MUST` preferuj:
- co najmniej jeden główny QA view,
- opcjonalnie drugi view potwierdzający głębokość.

## Zakaz

Nie używaj globalnego similarity score jako jedynego kryterium.
Model może uzyskać wysoki wynik mimo utraty małej, ale krytycznej cechy.

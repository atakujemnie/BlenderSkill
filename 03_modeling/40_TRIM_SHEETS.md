# Trim Sheets

## Cel

Współdzielić teksturę pomiędzy wieloma powierzchniami i assetami bez tworzenia unikalnego zestawu tekstur dla każdego obiektu.

## Dobry kandydat

- architektura modularna,
- ramy,
- listwy,
- metalowe profile,
- powtarzalne panele,
- przewody,
- krawędzie technologiczne.

## Nie używaj, gdy

- asset wymaga unikalnego malowania na całej powierzchni,
- kierunek i skala trimu nie mogą być utrzymane,
- workflow komplikuje asset bardziej niż oszczędza.

## Projekt trim sheet

Zdefiniuj pasy:
- wide structural trim,
- medium trim,
- narrow edge trim,
- panel detail,
- optional emissive strip.

## UV

UV dla trimów powinno:
- utrzymywać stałą skalę,
- zachować orientację,
- snapować się do odpowiednich pasów,
- minimalizować przypadkowe interpolacje pomiędzy regionami.

## Geometry relation

Trim nie zastępuje geometrii, która:
- zmienia silhouette,
- tworzy duży recess,
- rzuca istotny cień.

## Modular consistency

W jednym zestawie lokacji preferuj małą liczbę zatwierdzonych trim sheets zamiast unikalnych tekstur dla każdego modułu.

## QA

Sprawdź:
- stretching,
- kierunek,
- seams,
- zgodność skali między modułami,
- mip behavior z dystansu.

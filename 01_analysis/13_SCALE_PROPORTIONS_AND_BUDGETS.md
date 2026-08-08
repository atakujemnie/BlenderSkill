# Scale, Proportions and Budgets

## Jednostki

W projekcie gry preferuj spójną skalę metryczną.

Dla assetu zapisuj:
- szerokość,
- głębokość,
- wysokość,
- wysokość funkcjonalną,
- wysokość względem postaci referencyjnej.

## Tolerancje

Domyślne wartości tylko jako punkt startowy:

- sylwetka hero prop: do ~1% odchylenia w wymiarze głównym,
- zwykły prop: do ~2–3%,
- drobny detal: oceniany wizualnie,
- element modularny łączący się z innymi: tolerancja praktycznie zerowa na krawędziach interfejsu.

Kontrakt projektu może narzucić ostrzejsze wymagania.

## Budżet trójkątów

Nie używaj jednej liczby dla wszystkich assetów.

Budżet zależy od:
- udziału assetu w ekranie,
- liczby instancji,
- deformacji,
- liczby LOD,
- częstotliwości występowania,
- kosztu materiałów i draw calls,
- platformy docelowej.

## Zasada silhouette-per-triangle

Trójkąt jest uzasadniony, gdy:
- poprawia sylwetkę,
- poprawia deformację,
- tworzy cień/parallax wymagany z dystansu,
- jest potrzebny dla poprawnego bake/shading.

Jeżeli nie spełnia żadnego z powyższych, kandydat do usunięcia.

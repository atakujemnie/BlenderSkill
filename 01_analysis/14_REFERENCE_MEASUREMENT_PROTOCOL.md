# Reference Measurement Protocol

## Cel

Zamienić obraz referencyjny na zestaw relacji liczbowych bez przenoszenia surowych danych pomiarowych do kontekstu LLM.

## Preferred execution

Jeżeli runtime pozwala na analizę obrazu przez Python/NumPy lub równoważne narzędzie, użyj kontraktu:

`08_scripts/91_REFERENCE_MEASUREMENT_EXECUTOR_PATTERN.md`

Model językowy powinien otrzymać agregaty, confidence i konflikty — nie setki wartości per-row/per-column.

## Known dimension anchor

Jeżeli znany jest co najmniej jeden wymiar:
1. wybierz wymiar dobrze widoczny w referencji,
2. wyznacz skalę piksel -> jednostka,
3. mierz tylko elementy w tej samej płaszczyźnie lub po korekcji perspektywy,
4. zapisz anchor w Reference Analysis Cache.

Jeżeli wymiar jest jawnie podany liczbowo w zatwierdzonym prompt/rysunku, traktuj go jako silniejszy dowód niż wymiar wyprowadzony z perspektywicznego hero renderu.

## Brak wymiaru absolutnego

Użyj normalized coordinates:
- width = 1.0
- height = H/W
- depth = D/W

Przechowuj relacje aż do uzyskania skali.

## Perspective warning

Nie wyprowadzaj bezpośrednich wymiarów z:
- silnego perspective,
- fisheye,
- nieznanego focal length,
- elementów leżących w różnych głębokościach.

Perspective hero może służyć do oceny formy i widoczności detali, ale nie może nadpisać jawnego wymiaru lub zgodnych ortho views.

## Multi-view

Jeżeli istnieją front/side/top:
- każdy wymiar bierz z widoku, w którym jest najmniej zniekształcony,
- wymiary wspólne mierz niezależnie,
- porównuj aggregate deviation,
- sprzeczność zapisuj jako reference conflict.

Po uzyskaniu zgodności nie utrzymuj w aktywnym kontekście pełnych profili pomiarowych.

## Measurement table

| Metric | Value | Source view | Confidence |
|---|---:|---|---|
| W | 1.80 m | front | HIGH |
| H | 0.82 m | front | HIGH |
| D | 0.55 m | side | MEDIUM |
| gap | 0.012 m | detail | LOW |

LOW confidence nie powinno sterować destrukcyjną geometrią bez checkpointu.

## Measurement output budget

Normalny pomiar zwraca tylko:
- accepted value/ratio;
- source view/ROI;
- confidence;
- aggregate variance/deviation;
- conflict/warning;
- feature/metric ID.

Nie zwracaj domyślnie:
- całych masek pikselowych;
- setek punktów profilu;
- każdej wartości wiersza/kolumny;
- wszystkich prób threshold.

Jeżeli występuje błąd, uruchom diagnostykę tylko na minimalnym ROI.

## Cache rule

Przed pomiarem sprawdź `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md`.

Jeżeli ROI, calibration anchor i wynik są już zwalidowane dla niezmienionego źródła, użyj cache.
Nie mierz ponownie całego arkusza tylko dlatego, że agent rozpoczął kolejny etap.

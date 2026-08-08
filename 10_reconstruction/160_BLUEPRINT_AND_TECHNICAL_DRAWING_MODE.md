# Blueprint and Technical Drawing Mode

## Gdy wejście jest rzeczywistym rysunkiem technicznym

Priorytet:
- dimensions,
- section lines,
- datums,
- tolerances,
- symbols.

## Source Authority Order

Dla plansz technicznych i technical concept sheets stosuj domyślnie:

```text
1. explicit numeric dimensions / explicit datum
2. orthographic FRONT / SIDE / TOP / BOTTOM / REAR views
3. real section/cross-section views
4. detail close-ups
5. perspective hero render
6. approximate textual ranges / marketing prose
7. visual inference
```

Wyższy authority wygrywa przy konflikcie.

Przykład:
- prompt mówi `Ø140 mm`;
- FRONT i SIDE są z tym zgodne;
- hero render wygląda na lekko zwężony przez perspektywę.

Wynik: `Ø140 mm` pozostaje `LOCKED`. Nie wykonuj kolejnych iteracji próbujących dopasować cylinder do perspektywicznego zwężenia hero renderu.

## Prompt vs drawing

Jeżeli prompt podaje dokładny wymiar, a sama plansza ma tylko zakres przybliżony, exact value ma wyższy authority.

Jeżeli prompt mówi `około 90–110 mm`, a ortograficzny widok i dimension line pozwalają wyprowadzić dokładniejszy wymiar, zapisz zakres jako constraint pomocniczy, nie jako blokadę dokładnej wartości.

Nigdy nie zamieniaj słowa `około` na `LOCKED` bez dodatkowego dowodu.

## Nie interpretuj linii pomocniczych jako geometrii

Rozróżnij:
- object edge,
- hidden line,
- centerline,
- dimension line,
- leader,
- hatch,
- page/layout separator.

Przy automatycznym pomiarze dimension line lub leader blisko sylwetki jest potencjalną kontaminacją maski, nie częścią obiektu.

## Datum system

Jeżeli drawing definiuje bazę:
użyj jej jako origin/alignment.

Jawny datum/origin ma pierwszeństwo przed wizualnym środkiem obiektu na hero renderze.

## Sections

Przekrój ma wyższy authority dla lokalnej grubości niż hero render.

## Orthographic consistency

Jeżeli FRONT i SIDE pokazują wspólny wymiar:
- zmierz je niezależnie;
- porównaj po kalibracji;
- zapisz aggregate deviation;
- nie przesyłaj do LLM pełnych profili wiersz po wierszu.

Jeżeli wynik mieści się w aktywnej tolerancji, oznacz `CONSISTENT` i zakończ ten test.

## Marketing blueprint / technical concept sheet

Jeżeli plansza tylko naśladuje dokumentację techniczną:
- nie zakładaj standardów ISO/ASME bez dowodu;
- traktuj jawne liczby i ortograficzne widoki jako silny dowód projektowy;
- traktuj marketingowe opisy funkcji jako semantykę, nie jako metrologię;
- nie zakładaj, że ozdobne linie, ikony lub layout są częścią assetu.

## Completion rule

Po ustaleniu:
- source authority,
- zwalidowanych ROI,
- locked dimensions,
- cross-view consistency,

zapisz je w `10_reconstruction/170_REFERENCE_ANALYSIS_CACHE.md` i nie analizuj szeroko całej planszy ponownie bez konkretnego conflict/ROI failure.

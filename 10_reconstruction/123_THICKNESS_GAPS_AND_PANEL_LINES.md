# Thickness, Gaps and Panel Lines

## Parametry osobno

Nie mieszaj:
- grubości materiału,
- szczeliny montażowej,
- rowka dekoracyjnego,
- shadow gap,
- recess depth.

## Gap consistency

Powtarzalna szczelina powinna być parametrem:
`GAP_MAIN`, nie serią ręcznych przesunięć.

## Visible-from-distance test

Jeżeli panel line ma być czytelny z typowego dystansu:
- musi mieć wystarczający rozmiar geometryczny/teksturalny,
- ale nie może być sztucznie przeskalowany bez decyzji artystycznej.

## Geometry choice

Gap:
- real geometry dla głębokich i ważnych,
- normal/decal dla mikroszczelin,
- shader tylko jeśli runtime to wspiera.

## QA

Kontroluj szerokość i ciągłość szczelin na:
- prostych,
- narożnikach,
- przejściach między częściami.

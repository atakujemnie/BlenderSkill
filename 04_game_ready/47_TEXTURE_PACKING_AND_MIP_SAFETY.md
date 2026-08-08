# Texture Packing and Mip Safety

## Channel packing

Jeżeli silnik wspiera packed masks:
- grupuj mapy jednokanałowe zgodnie z jednym projektem,
- dokumentuj dokładne mapowanie kanałów.

Przykład projektowy:
```text
R = AO
G = Roughness
B = Metallic
A = Custom Mask
```

To jest przykład, nie uniwersalny standard.

## Color space

Rozróżniaj:
- dane kolorystyczne,
- dane numeryczne/maski,
- normal maps.

Błędny color space zmienia dane.

## Mip safety

Małe wyspy UV i cienkie detale muszą mieć:
- odpowiedni padding,
- wystarczającą szerokość w texelach,
- zachowanie czytelności po mipmappingu.

## Resolution policy

Resolution wynika z:
- powierzchni assetu,
- texel density,
- dystansu kamery,
- importance class.

Nie wynika z zasady "hero = 4K" bez obliczenia.

## Atlas

Atlas pomaga redukować liczbę zasobów/material changes, ale:
- utrudnia niezależną zmianę resolution,
- może marnować miejsce,
- wymaga dobrego planowania paddingu.

## Compression

Finalny wygląd oceniaj również po kompresji docelowego silnika.

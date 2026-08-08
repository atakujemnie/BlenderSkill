# Orthographic Overlay Validation

## Cel

Nałożyć render modelu na referencję w tej samej projekcji.

## Warstwy

- reference,
- candidate,
- alpha overlay,
- edge overlay,
- diff.

## Alignment

Przed oceną:
- same physical scale,
- same centerline,
- same ground plane,
- same crop/aspect.

## Colors

Kolory overlay są narzędziem QA, nie częścią finalnego assetu.

## Oceniaj

- external contour,
- panel boundaries,
- landmarks,
- feature positions.

## Do not compensate

Nie przesuwaj obrazu referencyjnego osobno dla każdego feature.
Rejestracja jest globalna dla widoku.

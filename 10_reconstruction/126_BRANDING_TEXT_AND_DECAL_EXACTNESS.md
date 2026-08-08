# Branding, Text and Decal Exactness

## Najpierw klasyfikacja

Element tekstowy może być:
- realnym nadrukiem na assetcie,
- interfejsem wyświetlacza,
- etykietą techniczną,
- adnotacją concept sheet.

Tylko pierwsze trzy trafiają do assetu.

## Exactness

Dla realnego brandingu:
- spelling,
- casing,
- alignment,
- orientation,
- scale,
- anchor position

są feature constraints.

## Geometry vs texture

Preferuj decal/texture dla:
- logotypów,
- drobnego tekstu,
- ikon.

Geometria tylko gdy:
- tekst jest fizycznie tłoczony,
- silhouette/parallax ma znaczenie.

## Unknown font

Nie zgaduj "podobnej" typografii jako 1:1.
Status:
`FONT_UNRESOLVED`
lub użyj dostarczonego logo jako grafiki.

## Handedness and surface-facing orientation

Czytelność tekstu/decalu musi być walidowana w **docelowym widoku powierzchni**, nie wyłącznie przez lokalny UV layout.

Jeżeli pipeline posiada export handedness compensation, np. `MIRROR_X`:
- nie stosuj jednego globalnego `mirror_u` do wszystkich decal planes;
- front-facing i rear-facing surface mogą wymagać przeciwnej authoring-space orientacji;
- orientation rule musi uwzględniać surface normal / canonical view;
- nie kompensuj ponownie ręcznie transformacji, którą wykona exporter/runtime, bez proof.

Wymagany test dla readable feature:

```text
canonical face/view
-> exported or runtime-equivalent orientation
-> readable text/logo
-> PASS
```

Dla front/rear technical labels utrzymuj osobne Feature IDs, jeżeli ich surface facing jest różny.

## QA

Porównuj ROI w widoku kanonicznym.

Dla tekstu/logo PASS wymaga:
- poprawnej orientacji;
- braku mirror/reversal;
- poprawnego anchor/scale;
- evidence z canonical ROI albo exported/runtime-equivalent readback/render.

Samo poprawne UV w authoring space nie jest dowodem po eksporcie, jeśli aktywny projekt stosuje handedness conversion.

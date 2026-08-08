# Reference Cleanup and Preprocessing

## Dopuszczalne operacje

- crop,
- rotate,
- deskew,
- normalize transparency/background for QA,
- extract edges/mask,
- split panels.

## Niedopuszczalne jako źródło prawdy

- generative fill,
- AI upscaling inventing edges,
- stylization,
- sharpening tworzący fałszywe linie.

## Upscale

Jeśli używany:
traktuj jako pomoc wizualną, a measurements wykonuj na oryginale lub kontrolowanym resamplingu.

## Preserve

Zawsze zachowaj:
- original pixels,
- transform metadata.

# Reference Color Management

## Cel

Nie interpretować różnic color-management jako różnic materiałowych.

## Record

Dla referencji, jeśli wiadomo:
- color space/profile,
- gamma,
- HDR/SDR,
- compression.

Dla renderu QA:
- render engine,
- view transform,
- look,
- exposure,
- output format.

## Consistency

Wszystkie checkpointy porównawcze muszą używać tego samego color pipeline.

## Concept art caveat

Obraz marketingowy mógł zostać:
- tonemapped,
- retuszowany,
- sharpened,
- compressed.

Dlatego geometryczne QA nie powinno zależeć od koloru.

## Separate pipelines

- geometry QA: mask/neutral,
- material QA: controlled render,
- final beauty: aesthetic.

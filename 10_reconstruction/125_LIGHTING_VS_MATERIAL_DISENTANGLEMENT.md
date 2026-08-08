# Lighting vs Material Disentanglement

## Problem

Concept art zawiera lighting, który może wyglądać jak:
- jaśniejszy materiał,
- gradient albedo,
- metaliczny pas,
- edge wear.

## Test

Porównaj ten sam region w:
- hero,
- front,
- side,
- material palette.

Jeżeli jasność zmienia się wraz z orientacją powierzchni:
prawdopodobnie to lighting/reflection.

## Brushed metal

Kierunkowy highlight nie powinien być kopiowany do base color jako stała jasna smuga.

## Ambient blue

Niebieskie odbicie od emissive/underglow nie jest kolorem sąsiedniego grafitu.

## QA material rig

Stosuj neutralne, powtarzalne studio lighting do porównania materiałów.

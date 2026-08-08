# Lighting vs Material Disentanglement

## Problem

Concept art zawiera lighting, który może wyglądać jak:
- jaśniejszy materiał,
- gradient albedo,
- metaliczny pas,
- edge wear,
- głębszy relief lub większy bevel niż faktycznie istnieje.

## Test

Porównaj ten sam region w:
- hero,
- front,
- side,
- material palette,
- neutral geometry QA, jeśli model już istnieje.

Jeżeli jasność zmienia się wraz z orientacją powierzchni:
prawdopodobnie to lighting/reflection.

## Brushed metal

Kierunkowy highlight nie powinien być kopiowany do base color jako stała jasna smuga.

## Ambient blue

Niebieskie odbicie od emissive/underglow nie jest kolorem sąsiedniego grafitu.

## QA material rig

Stosuj neutralne, powtarzalne studio lighting do porównania materiałów.

## Geometry compensation trap

Jeżeli feature jest słabo widoczny w jednym renderze, nie zwiększaj automatycznie:
- wysokości panelu;
- głębokości rowka;
- szerokości szczeliny;
- bevel width;
- rozmiaru emitera.

Najpierw rozdziel przyczynę:

```text
GEOMETRY
MATERIAL
LIGHTING
CAMERA
OCCLUSION
REFERENCE AMBIGUITY
```

Geometry change is allowed only when supported by geometric/reference evidence or an explicit functional requirement.

A detail that disappears because it is physically behind the host surface is `OCCLUSION/GEOMETRY PLACEMENT`, not a material problem.

A detail that exists geometrically but has weak contrast under a specific light should first be tested with neutral/matcap QA before changing dimensions.

## Reconstruction priority

For 1:1 reconstruction:

```text
explicit dimension / ortho evidence
> neutral geometry QA
> material appearance
> hero readability preference
```

Do not make geometry less faithful merely to make one hero render easier to read.

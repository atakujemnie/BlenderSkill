# Reconstruction Object Decomposition

## Cel

Podzielić asset według **hierarchii form projektowych**, a nie tylko przyszłych Blender objects.

Od v0.9 canonical output tego etapu jest `Reconstruction Shape Graph` z `174_RECONSTRUCTION_SHAPE_GRAPH.md`.

```text
reference evidence
-> design-form decomposition
-> Shape Graph
-> scene implementation
```

## Najpierw forma, potem object

Nie zaczynaj od pytania:

> Ile obiektów utworzyć w Blenderze?

Najpierw ustal:
- global envelope;
- primary forms definiujące sylwetkę;
- structural transitions;
- secondary structural forms;
- hosted structural features;
- edge-language owners;
- surface/detail owners.

Canonical levels:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

## Shape Node vs Blender Object

`Shape Node != Blender Object`.

Jeden node może być implementowany przez:
- final mesh;
- cage + cutters;
- section curves;
- temporary helper objects;
- curve + modifier stack.

Kilka małych scene objects może należeć do jednego node'a, jeżeli razem implementują jedną odpowiedzialność geometryczną.

## Kryteria osobnej formy/node'a

Oddziel node, jeśli część:
- ma własną odpowiedzialność za canonical silhouette/proportion;
- stanowi structural transition;
- ma własny authoritative view/ROI contract;
- jest hostem dla zależnych features;
- wymaga osobnej shape representation;
- może FAIL niezależnie od parenta;
- ma stabilną rolę funkcjonalną/assembly.

## Kryteria osobnego Blender object

Po zaakceptowaniu decomposition oddziel scene object, jeśli część:
- ma osobny materiał i wyraźną granicę;
- jest nakładką;
- będzie animowana;
- jest asymetrycznym akcesorium;
- ma być wariantowana;
- jest boolean cutter/helper;
- wymaga osobnego runtime fate.

To decyzja implementacyjna, downstream od Shape Graph.

## Nie rozdrabniaj

Nie twórz osobnego Shape Node dla każdej śrubki/seam, jeżeli:
- nie ma własnego geometric/QA ownership;
- jest powtórzeniem jednej feature family;
- może być child feature należącym do jednego host node.

## Required decomposition table

| Shape Node | G-level | RDL | Parent | Role | Shape class | Authoritative views | Feature IDs |

Tabela/lista jest wejściem do pełnego Shape Graph.

## Stable boundaries

Decomposition powstaje **przed produkcyjną geometrią**.

Zmiana granic G0–G3 po rozpoczęciu modelowania:
- tworzy nową graph revision;
- dirties affected nodes i zależne children;
- wymaga ponownej walidacji odpowiedniego RDL barrier.

Nie redefiniuj primary form tylko dlatego, że obecny skrypt Blendera jest łatwiejszy do napisania inaczej.

## Rule

Jeżeli decomposition jest tylko listą scene object names bez hierarchy, shape class, view responsibilities i dependencies, etap `DECOMPOSE` nie jest zakończony.

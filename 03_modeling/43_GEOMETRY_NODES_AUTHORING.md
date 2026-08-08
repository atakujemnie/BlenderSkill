# Geometry Nodes for Asset Authoring

## Rola

Geometry Nodes traktuj jako system proceduralnego authoringu:
- generowanie powtórzeń,
- rozmieszczanie,
- warianty,
- modularne konstrukcje,
- parametryczne detale.

Nie używaj tylko dlatego, że zadanie "da się zrobić nodami".

## Dobre zastosowania

- rzędy paneli,
- śruby/łączniki,
- moduły fasady,
- proceduralne barierki,
- rozmieszczanie instancji,
- warianty długości,
- kontrolowane scatter.

## Instancing first

Jeżeli rezultat składa się z powtarzalnych elementów:
- zachowuj instancje możliwie długo,
- nie realizuj ich bez potrzeby.

`Realize Instances` jest granicą, po której instancje stają się realną geometrią.

## Realize only when

- dalszy node musi edytować geometrię per-element,
- eksport/pipeline nie zachowuje wymaganej instancji,
- bake lub operacja topologiczna tego wymaga.

## Inputs

Wszystkie parametry projektowe powinny być wejściami grupy:
- width,
- height,
- count,
- spacing,
- seed,
- profile,
- variant selector.

## Determinism

Jeżeli używasz losowości:
- seed jest jawny,
- seed zapisany w asset contract,
- rezultat musi być reprodukowalny.

## Assetization

Node group powinien mieć:
- nazwę,
- wersję,
- jasno opisane inputy,
- zakresy,
- jednostki,
- fallback defaults.

## Escape hatch

Jeżeli Geometry Nodes zwiększa złożoność napraw prostego unikalnego prop, użyj klasycznego modelowania.

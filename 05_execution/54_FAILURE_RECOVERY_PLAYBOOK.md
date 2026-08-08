# Failure Recovery Playbook

## Failure: asset "podobny", ale niezgodny

Przyczyna:
brak Feature Contract.

Naprawa:
1. wróć do referencji,
2. wypisz MUST,
3. porównaj je z obiektami,
4. napraw tylko brakujące/niepoprawne features.

## Failure: detal zniknął po modyfikacji

Przyczyna:
operacja destrukcyjna lub zmiana stacku.

Naprawa:
- zidentyfikuj feature owner,
- porównaj z checkpointem,
- przywróć owner lub modifier,
- nie odtwarzaj całego modelu.

## Failure: operator API nic nie robi / robi coś innego

Przyczyna:
context/mode/selection.

Naprawa:
- sprawdź `poll`,
- sprawdź mode,
- active object,
- selection,
- view layer,
- użyj `temp_override`,
- rozważ Data API/BMesh.

## Failure: powstają `.001`, `.002`

Przyczyna:
brak idempotency.

Naprawa:
- get-or-create,
- tagowanie asset id,
- jawne usuwanie/aktualizacja starych helperów.

## Failure: bevel niszczy narożniki

Sprawdź:
- scale,
- width,
- overlap,
- segments,
- topology,
- modifier order.

## Failure: boolean daje artefakty

Sprawdź:
- coplanar surfaces,
- bardzo małe odległości,
- non-manifold cutter,
- normals,
- modifier order.

## Failure: zbyt dużo polygonów

Nie uruchamiaj od razu Decimate.

Najpierw:
- bevel segments,
- cylinders/spheres segments,
- ukryte geometry,
- duplicate geometry,
- microdetail,
- LOD separation.

## Failure: eksport wygląda inaczej

Porównaj:
- axis,
- scale,
- normals/tangents,
- material node compatibility,
- texture color spaces,
- modifiers apply/export settings,
- animation hierarchy.

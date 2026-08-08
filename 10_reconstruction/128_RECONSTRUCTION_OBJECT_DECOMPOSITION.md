# Reconstruction Object Decomposition

## Cel

Podzielić asset według konstrukcji i odpowiedzialności features.

## Kryteria osobnego obiektu

Oddziel, jeśli część:
- ma osobny materiał i wyraźną granicę,
- jest nakładką,
- będzie animowana,
- jest asymetrycznym akcesorium,
- ma być wariantowana,
- jest boolean cutter/helper,
- ma własny feature ownership.

## Nie rozdrabniaj

Nie twórz osobnego object dla każdej śrubki, jeśli:
- mogą być instancjami,
- nie potrzebują niezależnej logiki.

## Decomposition table

| Object | Feature IDs | Material | Modeling method | Runtime fate |

## Stable boundaries

Podział powinien powstać przed detail phase.
Ciągłe łączenie i rozdzielanie obiektów utrudnia regression tracking.

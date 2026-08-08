# Landmark and Keypoint System

## Cel

Porównywać konkretne punkty zamiast ogólnego wrażenia.

## Landmark classes

- bounding corners,
- feature centers,
- bend points,
- tangent transition points,
- panel corners,
- hole centers,
- logo anchor,
- seat/back junction,
- trim start/end.

## Record

```text
landmark_id
feature_id
3d_owner
view
reference_xy_normalized
projection_xy
tolerance_px_or_normalized
status
```

## Multi-view landmarks

Ten sam punkt 3D może występować w wielu widokach.
To szczególnie cenne do kontroli głębokości.

## Do not overfit

Nie twórz setek landmarków bez potrzeby.
D0/D1: mała liczba krytycznych punktów.
D2: dodatkowe lokalne punkty.

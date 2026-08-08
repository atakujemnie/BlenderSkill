# Draw Calls, Instancing and Batching

## Geometry is not the only cost

Asset z małą liczbą trójkątów może być drogi, jeśli ma:
- wiele material slots,
- dużo transparency,
- dużo unikalnych textures,
- brak instancingu,
- nadmiernie rozdrobnioną hierarchię.

## Material slots

Każdy dodatkowy slot powinien mieć uzasadnienie shader/runtime.

## Instancing

Powtarzające się obiekty:
- powinny współdzielić mesh,
- najlepiej współdzielić materiały,
- mogą posiadać per-instance transform i ograniczony zestaw parametrów.

## Unique variation

Zamiast tworzyć 10 unikalnych mesh:
- materiał variation,
- decal variation,
- accessory variation,
- instanced add-ons.

## Batching caveat

Dokładny koszt zależy od silnika.
Biblioteka nie narzuca konkretnego draw-call target bez danych projektu.

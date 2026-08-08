# Pivots, Transforms, Units and Naming

## Pivot

Pivot powinien wynikać z funkcji:
- mebel stojący: środek podstawy lub ustalony standard,
- drzwi: oś zawiasu,
- panel obrotowy: oś mechanizmu,
- moduł architektoniczny: punkt siatki montażowej.

Nie ustawiaj pivotu na geometry center automatycznie.

## Transform

Przed export:
- sprawdź location,
- rotation,
- scale,
- negative scale,
- parent transform.

Apply transforms tylko zgodnie z kontraktem.
Nie rób tego bezmyślnie, szczególnie w hierarchiach i rigach.

## Units

Jednostki Blendera i runtime muszą mieć jawne mapowanie.

## Naming

Proponowany schemat:
`<TYPE>_<SET>_<ASSET>_<PART>_<VARIANT>`

Przykłady:
- `SM_Lafar_Bench_Frame_A`
- `SM_Lafar_Bench_Seat_A`
- `COL_Lafar_Bench_A`
- `LOD1_Lafar_Bench_A`

## Zakaz `.001`

Finalny asset nie powinien zawierać przypadkowych nazw:
- Cube.001
- Material.003
- Boolean.017

Nazwy mają opisywać funkcję.

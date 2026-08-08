# Edge Radius and Bevel Estimation

## Edge taxonomy

- structural hard edge,
- manufactured fillet,
- cosmetic bevel,
- soft molded transition,
- protected edge trim.

## Estimation

Ustal:
1. skala obiektu,
2. widoczna szerokość highlightu,
3. contour change,
4. materiał,
5. sposób produkcji.

## Multiple bevel families

Nie używaj jednego bevel width dla całego assetu.

Przykładowe rodziny:
- `BVL_STRUCTURAL`
- `BVL_PANEL`
- `BVL_TRIM`
- `BVL_MICRO`

## Segment budget

Segment count zależy od:
- promienia,
- dystansu kamery,
- LOD.

## Hard rule

Bevel nie może zmienić locked outer dimension, jeśli kontrakt wymaga zachowania wymiaru zewnętrznego.
Plan musi uwzględniać sposób limit/offset.

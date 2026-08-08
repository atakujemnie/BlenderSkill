# Precision Hard-Surface Construction

## Precision hierarchy

1. numeric parameters,
2. constraints/derived values,
3. snapping,
4. measured local edits,
5. visual freehand only dla low-impact detail.

## Transform discipline

Dla konstrukcji:
- używaj osi,
- jawnych wartości,
- lokalnych układów,
- originów zgodnych z częścią.

## Clean primitive strategy

Zaczynaj od geometrii, która odpowiada przekrojowi.
Nie twórz bardzo złożonej siatki, jeśli parametric primitive + modifier zachowa precyzję.

## Edge placement

Edge loops powinny istnieć z powodu:
- shape,
- shading,
- topology requirement.

Nie "dla bezpieczeństwa".

## Precision regression

Po bevel/solidify/boolean sprawdź:
- locked bounds,
- alignment,
- gap widths.

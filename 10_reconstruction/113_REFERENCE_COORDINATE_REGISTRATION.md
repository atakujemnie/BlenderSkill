# Reference Coordinate Registration

## Cel

Ustawić różne widoki we wspólnym układzie 3D.

## Asset coordinate frame

Zdefiniuj:
- origin,
- X,
- Y,
- Z,
- front,
- ground plane.

## Orthographic registration

Dla każdego rzutu określ:
- physical width represented,
- physical height represented,
- image crop,
- image center,
- axis orientation.

## Anchor

Preferuj:
- known total dimension,
- ground contact,
- centerline,
- external bounds.

## Same-scale rule

Jeżeli front i rear przedstawiają ten sam wymiar 2000 mm, ich image planes powinny zostać skalibrowane do tej samej szerokości świata.

## Offset

Nie centruj każdego widoku "na oko".
Rejestruj według:
- centerline,
- ground,
- bounds.

## Result

Każdy reference plane może zostać użyty jako wiarygodne tło QA/modeling.

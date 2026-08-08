# Animation and Rigging

## Czy asset wymaga rig?

Nie twórz armature dla prostego mechanicznego ruchu, jeżeli:
- hierarchia obiektów i transform animation wystarczy,
- silnik obsługuje animację node transforms.

Rig ma sens dla:
- deformacji,
- wielu zależnych elementów,
- skinned meshes,
- bardziej złożonych animacji.

## Mechanical animation

Dla drzwi, ekranów, uchwytów:
- poprawny pivot jest kluczowy,
- hierarchia powinna odzwierciedlać mechanikę,
- zakres ruchu powinien wynikać z konstrukcji.

## Clips

Każda animacja:
- ma nazwę,
- zakres klatek,
- stan początkowy/końcowy,
- loop flag na poziomie projektu,
- oczekiwany root transform.

## Export QA

Po eksporcie sprawdź:
- czy klipy istnieją,
- czy kości/nodes są poprawnie zmapowane,
- czy skala nie uległa zmianie,
- czy pivot/axis zachowują się poprawnie.

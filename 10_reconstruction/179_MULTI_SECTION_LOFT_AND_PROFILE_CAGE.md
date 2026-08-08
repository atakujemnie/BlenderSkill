# Multi-Section Loft and Profile Cage

## Cel

Budować twarde formy, których szerokość, głębokość i corner treatment zmieniają się wzdłuż osi, bez składania ich z przypadkowych boxów.

Canonical semantic skill:
`SECTION_LOFT_HARD_SURFACE`.

Executor candidate:
`executors/section_loft.py`.

---

## Kiedy używać

Route do loftu, gdy forma ma kilka kontrolowanych przekrojów/stacji, np.:
- plinth/base rozszerzający się ku dołowi;
- shoulder pomiędzy wąskim body a szeroką bazą;
- obudowa zmieniająca width/depth jednocześnie;
- tapered hard-surface shell;
- przejście rounded/chamfered rectangle -> inny rounded/chamfered rectangle.

Nie używaj dla:
- zwykłego boxa z jednym bevel family;
- obiektu osiowo symetrycznego — użyj revolve;
- sweep po zakrzywionej ścieżce;
- organicznej freeform surface bez wiarygodnych section stations.

---

## Section station contract

Każda stacja opisuje przekrój w lokalnej płaszczyźnie prostopadłej do osi loftu.

Minimalny schema dla rounded/chamfered rectangle:

```yaml
stations:
  - id: BASE_BOTTOM
    axis_pos_mm: 0
    width_mm: 600
    depth_mm: 300
    corner:
      mode: CHAMFERED_ROUNDED
      radius_mm: 38
      chamfer_mm: 12

  - id: BASE_UPPER
    axis_pos_mm: 95
    width_mm: 570
    depth_mm: 282
    corner:
      mode: CHAMFERED_ROUNDED
      radius_mm: 30
      chamfer_mm: 10

  - id: SHOULDER
    axis_pos_mm: 165
    width_mm: 500
    depth_mm: 230
    corner:
      mode: CHAMFERED
      chamfer_mm: 14
```

Dopuszczalne są także explicit profile points, jeśli reference wymaga niestandardowego przekroju.

---

## Topological correspondence

Wszystkie stacje muszą mieć kompatybilną korespondencję punktów.

Zasada:

```text
ring vertex i at station N
connects to
ring vertex i at station N+1
```

Nie wolno losowo resamplować każdej stacji inną liczbą punktów po rozpoczęciu loftu.

Jeżeli corner resolution zmienia się dla finalnego shadingu, wykonaj to po geometric match albo przez kontrolowany refinement zachowujący semantic landmarks.

---

## Landmark anchors

Przekrój powinien mieć stabilne landmarks, np.:

```text
FRONT_CENTER
FRONT_RIGHT_TANGENT
RIGHT_FRONT_CORNER
RIGHT_CENTER
RIGHT_REAR_CORNER
REAR_CENTER
...
```

Pozwala to sprawdzać twist i przypisać referencyjne narożniki niezależnie od indeksów finalnej siatki.

---

## Hard-surface behavior

Loft nie oznacza automatycznie smooth organic surface.

Segment pomiędzy stacjami może mieć interpolation intent:
- `LINEAR` — planar/tapered wall;
- `HOLD_THEN_TRANSITION` — dłuższa stała sekcja + krótka zmiana;
- `SMOOTH_G1` — tylko jeśli evidence wymaga płynnej tangencji;
- `SHARP_BREAK` — jawna krawędź projektowa.

Nie smoothuj całego loftu jednym modifierem bez evidence.

---

## Base/shoulder reconstruction

Dla typowego civic prop:

```text
BODY SECTION
   ↓
TRANSITION/SHOULDER SECTION(S)
   ↓
BASE UPPER SECTION
   ↓
BASE LOWER SECTION
```

Najpierw rozwiązuj section dimensions i silhouette. Dopiero po PASS dodawaj:
- edge bevel;
- lip;
- panel seam;
- feet/fasteners;
- materials.

---

## Validation

Required:
1. station order monotonic;
2. positive width/depth;
3. common ring sample count;
4. no index twist;
5. expected bounds per station;
6. FRONT/SIDE/TOP registered projection where authoritative;
7. global contour regression;
8. continuity intent between stations;
9. no self-intersection for intended convex profiles.

---

## Anti-box rule

Jeżeli reference pokazuje jedną continuous form, nie zastępuj loftu kilkoma nakładającymi się boxami tylko dlatego, że łatwiej uzyskać podobny FRONT.

Taki model zwykle psuje:
- SIDE;
- TOP;
- corner transition;
- edge language;
- shading continuity.

---

## Freeze points

Przed RDL4:
- zachowaj editable station spec;
- zachowaj semantic section IDs;
- freeze only after multi-view geometric PASS.

Bevel/subdivision/topology cleanup jest downstream od shape solve.

---

## Executor contract

`section_loft.py` powinien zapewniać:
- pure-Python validation/spec normalization;
- deterministic perimeter point generation dla wspieranych section families;
- deterministic quad bridging;
- optional Blender mesh creation through explicit entry point;
- compact station/topology report;
- brak scene mutation podczas importu.

Status release v0.9: `CONTRACT_READY` do czasu realnego benchmarku w Blender 5.1.

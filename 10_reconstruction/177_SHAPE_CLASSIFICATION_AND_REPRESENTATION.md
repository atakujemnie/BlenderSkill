# Shape Classification and Representation

## Cel

Agent ma najpierw rozpoznać **matematyczną klasę formy**, a dopiero potem wybrać Blender API/operator.

Błąd klasy reprezentacji jest błędem wyższego poziomu niż błędny parametr bevelu.

---

## Canonical shape classes

### `ENVELOPE`
Globalna bryła ograniczająca. Nie jest finalną geometrią.

### `PARAMETRIC_PRIMITIVE`
Forma opisywalna stabilnie przez primitive + niewielki zestaw parametrów:
- box;
- cylinder;
- sphere;
- cone/frustum.

### `EXTRUDED_PROFILE`
Jeden authoritative 2D profile + prawie stała głębokość.

### `REVOLVED_PROFILE`
Profil 2D obracany wokół osi. Route do `AXISYMMETRIC_PROFILE`.

### `PROFILE_SWEEP`
Przekrój prowadzony po path/curve.

### `MULTI_SECTION_LOFT`
Forma opisana przez wiele przekrojów o spójnej korespondencji punktów.

Typowy trigger:

```text
width changes along axis
AND depth changes along axis
AND corner/profile treatment changes along axis
```

### `MULTI_SECTION_TRANSITION`
Loft pełniący rolę przejścia pomiędzy dwoma zaakceptowanymi formami, np. body -> base.

### `SUBD_FREEFORM`
Forma kontrolowana cage'em, gdy nie można jej wiarygodnie przedstawić prostym primitive/profile/loftem i evidence wskazuje smooth compound surface.

### `BOOLEAN_RECESS`
Lokalna forma ujemna osadzona w zaakceptowanym host geometry.

### `PANEL_LINE`
Wąski seam/groove o własnym path/profile contract.

### `LAYERED_ASSEMBLY`
Warstwy o krytycznej kolejności głębokości, np. glass/content/recess floor.

### `HYBRID_ASSEMBLY`
Node jest semantycznym assembly składającym się z kilku shape classes. Używaj tylko, gdy rozdzielenie na dzieci jest zapisane w Shape Graph.

---

## Classification decision tree

```text
Czy forma jest tylko envelope?
-> ENVELOPE

Czy jest osiowo symetryczna?
-> REVOLVED_PROFILE

Czy jeden profil 2D + stała głębokość opisuje formę?
-> EXTRUDED_PROFILE

Czy przekrój porusza się po ścieżce?
-> PROFILE_SWEEP

Czy przekrój zmienia się na kilku stacjach?
-> MULTI_SECTION_LOFT / MULTI_SECTION_TRANSITION

Czy forma jest lokalnym ubytkiem hosta?
-> BOOLEAN_RECESS / PANEL_LINE

Czy smooth compound surface nie ma stabilnego section/profile modelu?
-> SUBD_FREEFORM
```

---

## Box-abuse detector

`PARAMETRIC_PRIMITIVE` jest podejrzane jako primary strategy, gdy reference pokazuje co najmniej dwa z poniższych:
- różna szerokość na różnych wysokościach;
- różna głębokość na różnych wysokościach;
- zmieniający się corner radius/chamfer;
- ciągły diagonal shoulder;
- kontrolowane przejście między dwoma różnymi przekrojami;
- jedna widoczna powierzchnia przechodząca przez kilka stacji bez seam;
- narożnik, którego forma zależy od dwóch osi jednocześnie.

Jeżeli występują trzy lub więcej:

```text
PARAMETRIC_BOX_AS_PRIMARY = FORBIDDEN_UNLESS_PROVEN
BOOLEAN_UNION_OF_BOXES_AS_PRIMARY = FORBIDDEN_UNLESS_PROVEN
```

Agent musi rozważyć `MULTI_SECTION_LOFT` albo `SUBD_FREEFORM`.

---

## Representation evidence

Każda klasyfikacja ma record:

```yaml
representation_decision:
  node_id: BASE_PLINTH
  selected: MULTI_SECTION_LOFT
  evidence:
    - FRONT_width_changes_with_z
    - SIDE_depth_changes_with_z
    - TOP_rounded_chamfered_plan
    - HERO_continuous_corner_transition
  rejected:
    PARAMETRIC_PRIMITIVE:
      reason: cannot preserve coupled width/depth/corner transition
  confidence: HIGH
```

Nie wystarczy `easier to build`.

---

## Operator independence

Shape class nie zależy od tego, czy implementacja używa:
- BMesh;
- mesh.from_pydata;
- Geometry Nodes;
- curves;
- modifiers;
- `bpy.ops`.

To implementacja ma spełniać reprezentację, nie reprezentacja operator.

---

## Strategy switch trigger

Gdy node po poprawionym retry nadal FAIL w innym authoritative view:
1. sprawdź registration/calibration;
2. sprawdź input parameters;
3. sprawdź shape class;
4. jeżeli class nie może jednocześnie spełnić widoków, zmień representation zamiast dalej stroić lokalne wartości.

---

## Anti-pattern

```text
"Widzę zaokrąglony element, więc dodam cube i bevel"
```

jest niedozwolonym skrótem poznawczym.

Poprawne:

```text
identify node role
-> infer cross-section behavior
-> classify shape
-> choose semantic skill
-> implement
-> validate views
```

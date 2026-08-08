# Complex Hard-Surface Base and Transition

## Scope

Playbook dla civic/product hard-surface bases, collars, shoulders i transition shells, których nie da się wiernie opisać pojedynczym boxem + bevel.

Typical assets:
- pylons;
- kiosks;
- street terminals;
- industrial cabinets;
- charging stations;
- machine bases.

---

## Recognition

Podejrzewaj `MULTI_SECTION_LOFT` gdy:
- base jest szersza od body;
- depth też zmienia się w przejściu;
- narożnik ma własny plan/chamfer;
- shoulder jest diagonalny w FRONT/SIDE;
- concept pokazuje jedną continuous shell bez seams między "klockami".

---

## Decomposition

Najpierw rozdziel role:

```text
BODY CORE
LOWER SHOULDER / TRANSITION
BASE PLINTH
LOWER LIP / FOOT
INSERTS / SERVICE MODULES
```

Nie łącz automatycznie wszystkich w jeden Shape Node. Shoulder może być osobnym `MULTI_SECTION_TRANSITION` pomiędzy body i plinth.

---

## RDL order

### RDL0
Tylko total envelope/contact.

### RDL1
1. body core;
2. base plinth;
3. shoulder/transition.

Waliduj każdy osobno.

### RDL2+
Dopiero po RDL1 PASS:
- side rails;
- front utility housing;
- inset plates;
- lighting channels;
- service panels.

### RDL4
Dopiero wtedy final corner radii/bevel families.

---

## Section strategy

Dla plinth/transition zdefiniuj stacje o znaczeniu projektowym, nie równych odstępach tylko dlatego, że tak wygodnie.

Przykład:

```text
Z0 ground/lower lip
Z1 top of lower lip
Z2 main base shoulder
Z3 base upper collar
Z4 transition apex
Z5 body contact
```

Każda stacja dostaje:
- width;
- depth;
- center offset, jeśli asymetryczna;
- corner family;
- corner radius/chamfer;
- continuity intent do następnej stacji.

---

## Corner language

Nie traktuj narożnika jako efektu końcowego bevelu, jeśli jego plan wpływa na silhouette/top view.

Jeżeli corner shape jest widoczny w TOP lub hero i zmienia się między stacjami, należy do section geometry.

Final micro-bevel jest downstream.

---

## Front/Side/Top responsibilities

```text
FRONT -> width(z), shoulder angle, lower/upper band heights
SIDE  -> depth(z), front/rear transition, vertical profile
TOP   -> plan width/depth, corner/chamfer family
HERO  -> continuity confirmation, manufacturing/edge interpretation
```

Żaden pojedynczy rzut nie jest wystarczający dla compound base.

---

## Failure diagnosis

### FRONT good, SIDE bad
Najpierw sprawdź depth stations/representation, nie width.

### FRONT + SIDE good, TOP/corner bad
Sprawdź plan section/corner representation. Box+bevel może mieć złą korespondencję narożnika mimo poprawnych wymiarów osiowych.

### Hero wygląda "klockowato"
Sprawdź, czy continuous shell została błędnie rozbita na overlapping primitives.

### Bevel musi być absurdalnie duży, żeby uzyskać concept contour
Prawdopodobnie primary section geometry jest zła.

---

## Manufacturing logic

Preferuj rozwiązanie, które można interpretować jako:
- molded/cast shell;
- folded/formed metal housing;
- assembled collar + base;

zgodnie z visible seams/material boundaries.

Nie wymyślaj seam tylko dlatego, że model został złożony z osobnych helperów.

---

## Acceptance

Base/transition RDL1 PASS wymaga:
- registered FRONT/SIDE/TOP where authoritative;
- station dimensions PASS;
- global bounds/contact PASS;
- no unsupported seams;
- required continuity intent PASS;
- Shape Graph parent/transition relationships PASS.

Dopiero po tym route do edge-language i detail skills.

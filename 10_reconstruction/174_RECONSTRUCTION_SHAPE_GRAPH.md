# Reconstruction Shape Graph

## Cel

`Reconstruction Shape Graph` jest obowiązkowym modelem pośrednim pomiędzy analizą referencji a modelowaniem.

Agent nie przechodzi bezpośrednio z:

```text
concept art -> bpy/BMesh/operator
```

Najpierw musi ustalić:

```text
reference evidence
-> hierarchy of design forms
-> Shape Graph
-> per-node representation and validation contract
-> geometry execution
```

Shape Graph odpowiada na pytanie **z czego obiekt się składa i które formy są nadrzędne**, zanim agent zacznie wybierać operator Blendera.

---

## Fundamental rule

Jednostką rekonstrukcji nie jest cały asset ani pojedynczy Blender object.

Jednostką pracy jest `Shape Node`.

Każdy node reprezentuje jedną semantycznie spójną formę projektową:
- global envelope;
- primary mass;
- structural transition;
- secondary mass;
- structural feature;
- edge treatment owner;
- surface/detail owner.

Blender object może implementować jeden node, wiele helperów jednego node'a albo część node'a. Nazwa obiektu w scenie nie zastępuje Shape Node ID.

---

## Hierarchy levels

Canonical hierarchy:

```text
G0 GLOBAL_ENVELOPE
G1 PRIMARY_FORM
G2 SECONDARY_STRUCTURAL_FORM
G3 STRUCTURAL_FEATURE
G4 EDGE_LANGUAGE
G5 SURFACE_DETAIL
```

### G0 — GLOBAL_ENVELOPE

Tylko:
- total width;
- total depth;
- total height;
- ground/contact datum;
- principal axes;
- global centerline/origin relation.

Nie zawiera ekranu, paneli, logo, rowków ani beveli.

### G1 — PRIMARY_FORM

Bryły, które decydują o rozpoznawalności i głównej sylwetce.

Test praktyczny:

> Jeżeli usuniesz G2–G5, czy obiekt nadal ma poprawną główną formę z canonical views?

Typowe przykłady:
- main body;
- base/plinth;
- major shell;
- main seat/back shell;
- large structural shoulder/transition.

### G2 — SECONDARY_STRUCTURAL_FORM

Duże komponenty zmieniające projekt, ale nie globalny envelope:
- side frame;
- display housing/recess mass;
- utility housing;
- large service panel mass;
- large trim member.

### G3 — STRUCTURAL_FEATURE

Lokalne cechy wymagające realnej geometrii albo kontrolowanej reprezentacji:
- recess;
- opening;
- vent field;
- LED channel;
- panel separation;
- handle/latch;
- negative space;
- functional groove.

### G4 — EDGE_LANGUAGE

Dopiero po zaakceptowaniu G0–G3:
- bevel;
- fillet;
- chamfer;
- corner radius;
- local tangency;
- edge-family consistency.

Bevel nie może maskować błędnej primary form.

### G5 — SURFACE_DETAIL

- branding;
- decals;
- screws not affecting structural solve;
- micro-grooves;
- microtexture;
- weathering;
- cosmetic surface breakup.

---

## Graph relations

Shape Graph jest DAG-iem.

Node może deklarować:
- `parent` — forma nadrzędna;
- `depends_on` — node'y, które muszą być zaakceptowane przed budową;
- `hosts` — features osadzane na danej powierzchni;
- `contacts` — wymagane relacje styku;
- `transitions_to` — ciągłość/przejście do innego node'a;
- `symmetry_group`;
- `feature_ids` z Feature Contract.

Przykład:

```yaml
shape_graph:
  asset_id: ACS_WP_3470
  root: PYLON
  nodes:
    PYLON:
      level: G0
      shape_class: ENVELOPE

    PRIMARY_BODY:
      parent: PYLON
      level: G1
      shape_class: EXTRUDED_PROFILE

    BASE_PLINTH:
      parent: PYLON
      level: G1
      shape_class: MULTI_SECTION_LOFT

    LOWER_SHOULDER:
      parent: PRIMARY_BODY
      depends_on: [PRIMARY_BODY, BASE_PLINTH]
      level: G1
      shape_class: MULTI_SECTION_TRANSITION
      transitions_to: [PRIMARY_BODY, BASE_PLINTH]

    SIDE_FRAME:
      parent: PRIMARY_BODY
      level: G2
      shape_class: PROFILE_SWEEP

    DISPLAY_RECESS:
      parent: PRIMARY_BODY
      level: G2
      shape_class: BOOLEAN_RECESS

    PANEL_SEAM_01:
      parent: PRIMARY_BODY
      level: G3
      shape_class: PANEL_LINE
```

---

## Required pre-model output

Przed pierwszą produkcyjną mutacją geometrii agent musi wyemitować compact Shape Graph zawierający co najmniej:

```yaml
shape_graph_ready:
  root_id: ...
  node_count: ...
  levels_present: [G0, G1, ...]
  unresolved_nodes: []
  primary_nodes: []
  graph_status: PASS
```

`graph_status != PASS` blokuje modelowanie poza czystym G0 diagnostic blockout.

---

## Coarse-to-fine invariant

Dziecko nie może być budowane przed zaakceptowaniem hosta/parenta, jeżeli jego poprawność zależy od host geometry.

W szczególności zabronione jest:

```text
PRIMARY_BODY + DISPLAY_RECESS + LOGO + VENTS + BEVELS
```

w jednym niezwalidowanym monolitycznym kroku.

Dozwolone:

```text
build PRIMARY_BODY
-> validate required views
-> PASS
-> build next ready node
```

---

## Shape Graph vs Feature Contract

`Feature Contract` opisuje **co musi istnieć**.

`Shape Graph` opisuje **jak formy składają się w jeden obiekt i w jakiej kolejności mogą być rozwiązane**.

Feature może należeć do node'a:

```yaml
node: DISPLAY_RECESS
feature_ids:
  - F_DISPLAY_RECESS
  - F_DISPLAY_BORDER
```

Nie twórz osobnego Shape Node dla każdego mikroskopijnego feature, jeżeli nie ma własnej odpowiedzialności geometrycznej/QA.

---

## Shape Graph vs Scene Graph

Nie utożsamiaj:

```text
Shape Graph != Blender Object hierarchy
```

Shape Graph jest modelem projektowym i dowodowym.

Scena Blendera jest implementacją.

Jedna forma może być zbudowana przez:
- cage + helper cutters;
- curve + bevel object;
- multiple temporary sections;
- one final joined mesh.

Node pozostaje stabilny mimo zmian implementacji.

---

## Anti-patterns

FAIL:
- jeden `build_asset()` tworzy jednocześnie G1–G5;
- node jest definiowany dopiero po utworzeniu geometrii;
- decomposition jest tylko listą nazw obiektów bez hierarchy/role;
- agent zaczyna od detalu, bo jest łatwy do rozpoznania;
- bevel/boolean jest wybierany zanim określono shape class;
- cały asset jest walidowany tylko po finalnym hero renderze.

---

## Completion requirement

Level A wymaga:
- Shape Graph istnieje;
- wszystkie wymagane G0–G3 nodes są `ACCEPTED`;
- G4/G5 wymagane przez target fidelity są `ACCEPTED` albo jawnie deferred zgodnie z completion level;
- brak child node zaakceptowanego przy FAIL parent geometry;
- final `RECON_FIDELITY_GATE` odnosi się do zaakceptowanego graph revision.

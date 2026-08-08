# Node-by-Node Multi-View Validation

## Cel

Walidować pojedynczą formę natychmiast po jej zbudowaniu, zanim scena zostanie zagęszczona kolejnymi elementami.

Nie czekaj do finalnego asset renderu, aby odkryć błąd primary form.

---

## Core loop

Dla każdego `READY_TO_BUILD` Shape Node:

```text
isolate accepted ancestors + current node
-> build/repair current node only
-> render required canonical views
-> registered comparison per view/ROI
-> numeric/section checks
-> node gate
-> ACCEPTED | FAIL
```

Dopiero `ACCEPTED` odblokowuje zależne dzieci.

---

## View responsibility contract

Każdy node definiuje, co kontroluje dany widok.

Przykład:

```yaml
BASE_PLINTH:
  FRONT:
    controls: [width, height, shoulder_contour]
  SIDE:
    controls: [depth, height, front_rear_profile]
  TOP:
    controls: [width, depth, corner_plan]
  HERO:
    controls: [transition_interpretation]
```

Nie wymagaj widoku, który nie wnosi evidence dla node'a. Nie pomijaj widoku REQUIRED.

---

## Isolation rule

Node QA render musi zawierać wyłącznie:
- zaakceptowane ancestor/host geometry potrzebne do kontekstu;
- current node;
- wymagany QA rig.

Nie renderuj:
- runtime collision;
- LOD proxies;
- future RDL nodes;
- hidden helper shells;
- export copies;
- unrelated scene geometry.

Użyj `QA_SCENE_ISOLATE`.

`isolation_status != PASS` oznacza `UNVERIFIED`, nawet jeśli silhouette metric wygląda dobrze.

---

## Registered comparison

Dla authoritative orthographic/near-orthographic evidence:
- jedna globalna registration per view;
- ten sam crop/aspect/physical scale;
- żadnego lokalnego przesuwania current node renderu w celu poprawienia wyniku;
- ROI node'a może ograniczać obszar oceny, ale nie zmieniać registration.

Preferred skill:
`REFERENCE_OVERLAY_VALIDATE`.

---

## Local vs global silhouette

Node może wpływać na:
- `GLOBAL_SILHOUETTE`;
- `LOCAL_BOUNDARY`;
- `INTERNAL_FEATURE`;
- `NO_SILHOUETTE`.

### Global silhouette node
Po naprawie sprawdź:
1. node ROI;
2. global canonical silhouette regression.

### Internal node
Sprawdź:
1. feature ROI;
2. parent protected-region regression.

Nie uznawaj lokalnego PASS, jeśli naprawa psuje zaakceptowany parent contour.

---

## Numeric responsibilities

W zależności od shape class waliduj:
- bounds;
- centerline;
- station heights;
- width/depth per station;
- profile landmarks;
- recess depth;
- contact plane;
- layer order;
- symmetry/asymmetry;
- cross-section sample contract.

Image overlay nie zastępuje locked numeric dimensions.

---

## Cross-section validation

Dla `MULTI_SECTION_LOFT` i `MULTI_SECTION_TRANSITION` wymagaj station report.

Przykład:

```yaml
sections:
  - station: BASE_BOTTOM
    z_mm: 0
    width_mm: 600
    depth_mm: 300
    status: PASS
  - station: BASE_UPPER
    z_mm: 95
    width_mm: 570
    depth_mm: 282
    status: PASS
  - station: SHOULDER
    z_mm: 165
    width_mm: 500
    depth_mm: 230
    status: PASS
```

Dodatkowo:
- ordering monotonic along loft axis;
- common vertex correspondence;
- no unintended twist;
- expected corner/chamfer family;
- transition continuity.

---

## Node acceptance minimum

```yaml
node_gate:
  node_id: LOWER_SHOULDER
  parent_gate: PASS
  isolation: PASS
  required_views:
    FRONT: PASS
    SIDE: PASS
  numeric_constraints: PASS
  section_contract: PASS
  regression_outside_expected_change: PASS
  status: ACCEPTED
```

`PASS` fields muszą być proof-bearing zgodnie z `173_RECONSTRUCTION_ACCEPTANCE_EVIDENCE_INTEGRITY.md`.

---

## Failure routing

Jeżeli FRONT i SIDE wskazują różne klasy błędu:
- nie poprawiaj losowo obu;
- przypisz failure do registration, parameters, representation albo parent relation.

Przykład:

```text
FRONT width PASS
SIDE depth FAIL
TOP corner-plan FAIL
```

często wskazuje na złą reprezentację 3D, nie na jeden scalar width parameter.

---

## Stop rule

`MUST node + FAIL`:
- zatrzymaj ten branch Shape Graph;
- nie buduj dzieci;
- nie przechodź do wyższego RDL;
- wykonaj repair albo representation switch.

Nie zapisuj tego jako kosmetycznego TODO na koniec.

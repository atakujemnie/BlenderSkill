# Reconstruction Node Contract

## Cel

Każdy Shape Node musi mieć wystarczający kontrakt, aby agent mógł:
1. zrozumieć formę;
2. wybrać reprezentację geometryczną;
3. zbudować tylko ten element;
4. porównać go z właściwymi rzutami;
5. zaakceptować albo odrzucić przed budową dzieci.

---

## Minimalny schema

```yaml
shape_node:
  id: BASE_PLINTH
  graph_revision: sg_004

  hierarchy:
    level: G1
    rdl: RDL1
    parent: PYLON
    depends_on: []

  semantics:
    role: STRUCTURAL_BASE
    importance: MUST

  representation:
    shape_class: MULTI_SECTION_LOFT
    strategy: SECTION_LOFT_HARD_SURFACE
    parameters_owner: pylon_spec.BASE_PLINTH

  evidence:
    FRONT:
      authority: REQUIRED
      controls: [width, height, outer_contour]
    SIDE:
      authority: REQUIRED
      controls: [depth, height, front_rear_profile]
    TOP:
      authority: REQUIRED
      controls: [width, depth, corner_plan]
    HERO:
      authority: SUPPORTING
      controls: [corner_transition, edge_language]

  constraints:
    symmetry: X
    contacts: [GROUND, LOWER_SHOULDER]
    protected_dimensions: [BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT]

  validation:
    required_views: [FRONT, SIDE, TOP]
    required_evidence_kinds:
      - NUMERIC_MEASUREMENT
      - REGISTERED_OVERLAY
    roi_ids: [BASE_FRONT, BASE_SIDE, BASE_TOP]

  execution:
    children_allowed_after: ACCEPTED
    mutation_scope: NODE_ONLY
```

---

## Required fields

### Identity
- stable `id`;
- graph revision;
- hierarchy level;
- RDL;
- parent/dependencies.

### Semantics
Node musi opisywać **rolę projektową**, nie operator Blendera.

Dobre:
- `STRUCTURAL_BASE`;
- `PRIMARY_SHELL`;
- `STRUCTURAL_TRANSITION`;
- `DISPLAY_HOUSING`.

Złe:
- `CUBE_07`;
- `BOOLEAN_OBJECT`;
- `MESH_002`.

### Representation
Najpierw wybierz `shape_class`, potem implementation strategy.

```text
design form
-> shape class
-> semantic skill / strategy
-> Blender implementation
```

Nigdy odwrotnie.

### View responsibilities
Każdy authoritative view musi mówić **co kontroluje** dla tego node'a.

Nie używaj ogólnego:

```text
SIDE = check it looks okay
```

Używaj:

```text
SIDE = depth + vertical profile + transition angle
```

### Validation ownership
Node musi wskazywać testy przed wykonaniem geometrii.

Nie wolno dopisywać kryterium PASS dopiero po zobaczeniu wyniku.

---

## Node states

Canonical states:

```text
DECLARED
CONSTRAINED
READY_TO_BUILD
BUILT_UNVERIFIED
ACCEPTED
FAIL
BLOCKED
DIRTY
SUPERSEDED
```

Transition:

```text
DECLARED
-> CONSTRAINED
-> READY_TO_BUILD
-> BUILT_UNVERIFIED
-> ACCEPTED | FAIL
```

`FAIL` po naprawie wraca do `BUILT_UNVERIFIED`.

Zmiana parent/authority/representation może oznaczyć node `DIRTY`.

---

## Parent/child gate

Dla geometrycznie zależnego child:

```text
parent.status != ACCEPTED
=> child.status = BLOCKED
```

Wyjątek musi być jawny, np. niezależny module reference albo diagnostic helper.

Przykład:
- logo nie jest budowane na błędnym front panelu;
- panel seam nie jest robiony na shellu, którego silhouette jeszcze FAIL;
- bevel nie jest dopracowywany na złym base profile.

---

## Mutation scope

Domyślnie transakcja node'a może zmieniać:
- node owner geometry;
- jawnie zadeklarowane helper/cutter objects;
- expected-change ROI;
- zależne temporary QA artifacts.

Nie może zmieniać zaakceptowanego sibling/parent bez jawnego `change_impact` i dirty propagation.

---

## Representation switch

Po dwóch udowodnionych porażkach tej samej strategii node musi przejść re-inspection.

Jeżeli failure wskazuje na złą klasę reprezentacji, nie iteruj parametrów w nieskończoność.

Przykład:

```text
PARAMETRIC_BOX + BEVEL
-> FRONT FAIL
-> corrected retry
-> SIDE/CORNER FAIL
=> representation review
=> MULTI_SECTION_LOFT
```

---

## Acceptance record

```yaml
node_acceptance:
  node_id: BASE_PLINTH
  graph_revision: sg_004
  node_revision: n_006
  status: ACCEPTED

  evidence:
    FRONT: {status: PASS, evidence_kind: REGISTERED_OVERLAY, provenance_id: base_front_006}
    SIDE:  {status: PASS, evidence_kind: REGISTERED_OVERLAY, provenance_id: base_side_006}
    TOP:   {status: PASS, evidence_kind: REGISTERED_OVERLAY, provenance_id: base_top_006}
    dimensions: {status: PASS, evidence_kind: NUMERIC_MEASUREMENT, provenance_id: base_dims_006}

  implementation:
    shape_class: MULTI_SECTION_LOFT
    skill_id: SECTION_LOFT_HARD_SURFACE
```

Narracyjne `looks correct` nie jest node acceptance.

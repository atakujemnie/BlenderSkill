# Reconstruction Stage Barrier

## Cel

Wymusić coarse-to-fine progression. `RDL` nie jest sugestią kolejności, lecz barrierem wykonawczym.

---

## Barrier model

```text
RDL0_BARRIER
RDL1_BARRIER
RDL2_BARRIER
RDL3_BARRIER
RDL4_BARRIER
RDL5_BARRIER
```

Bariera przechodzi tylko, gdy wszystkie required nodes bieżącego poziomu mają akceptowalny stan.

---

## PASS conditions

Dla poziomu `N`:
- wszystkie `MUST` node'y poziomu <= N wymagane w tym etapie są `ACCEPTED`;
- brak `FAIL/BLOCKED/UNVERIFIED` required node;
- required per-node view evidence jest proof-bearing;
- global protected invariants nie zostały złamane;
- Shape Graph revision jest aktualny;
- brak unresolved HARD representation/evidence conflict dotyczącego bieżącej formy.

---

## Forbidden advancement

Przykłady:

```text
RDL1 BASE_PLINTH FAIL
-> nie buduj RDL2 display housing

RDL2 DISPLAY_RECESS FAIL
-> nie buduj RDL3 screen glass/content

RDL3 PANEL HOST FAIL
-> nie route do HS_PANEL_LINE

RDL1 silhouette FAIL
-> nie przechodź do bevel/material work
```

---

## Stage result

```yaml
stage_barrier:
  rdl: RDL1
  graph_revision: sg_004
  required_nodes: [PRIMARY_BODY, BASE_PLINTH, LOWER_SHOULDER]
  accepted_nodes: [PRIMARY_BODY, BASE_PLINTH]
  blockers:
    - node_id: LOWER_SHOULDER
      status: FAIL
      failing_views: [SIDE]
  status: FAIL
  can_advance: false
```

---

## Regression after later changes

Jeżeli późniejsza zmiana narusza protected primary form:
- affected earlier node -> `DIRTY`;
- właściwa wcześniejsza bariera -> `DIRTY/FAIL`;
- późniejsze node'y zależne zostają `DIRTY/BLOCKED`;
- nie kontynuuj na podstawie historycznego PASS.

---

## Global vs node gate

`RECONSTRUCTION_NODE_GATE` mówi:
> czy konkretny node jest zaakceptowany?

`RECONSTRUCTION_STAGE_BARRIER` mówi:
> czy cały poziom coarse-to-fine jest wystarczająco rozwiązany, aby wejść głębiej?

`RECON_FIDELITY_GATE` pozostaje finalną bramką Level A przed runtime.

Hierarchia:

```text
node gates
-> RDL stage barriers
-> final reconstruction fidelity gate
```

---

## Anti-pattern

Nie uznawaj stage za PASS na podstawie:
- liczby utworzonych obiektów;
- braku wyjątków skryptu;
- jednego hero renderu;
- poprawnego total bounding boxu;
- deklaracji modelu "primary forms done".

PASS wymaga records z zaakceptowanych node'ów.

# Reconstruction Node Execution Protocol

## v0.11 hard-enforcement amendment

v0.10/v0.9 described the correct node loop, but the Lafar Street Lamp benchmark proved that an asset-local `main()` could still call all node functions in sequence. v0.11 makes the loop executable.

Before mutation require `EXECUTION_AUTHORIZATION_GATE.can_mutate == PASS`, persisted `READY_TO_BUILD`, accepted parent/dependencies and prior RDL barriers. Immediately after one node mutation persist `BUILT_UNVERIFIED` and stop that branch until source-anchored QA plus `RECONSTRUCTION_NODE_GATE` returns `ACCEPTED`.

Node-by-node function names are not sufficient. A monolithic function calling RDL0..RDL5 without persisted gates is a regression. See `73_EXECUTION_AUTHORIZATION_GATE.md`, `74_PERSISTENT_NODE_STATE_AND_CHECKPOINTS.md` and `75_NODE_SCOPED_ORCHESTRATION.md`.

---

## Cel

Zastąpić monolityczny `build_asset()` kontrolowanym wykonywaniem Shape Graph node po node.

v0.9 execution unit:

```text
ONE SHAPE NODE
-> ONE MUTATION SCOPE
-> ONE VALIDATION PACKAGE
-> ACCEPT / FAIL
```

---

## Preconditions

Przed budową node'a:
- Shape Graph revision istnieje;
- node ma `CONSTRAINED` lub `READY_TO_BUILD`;
- parent/dependencies wymagane do geometrii są `ACCEPTED`;
- shape class jest wybrana;
- required views + controls są zapisane;
- implementation skill jest zidentyfikowany;
- expected-change scope jest jawny;
- QA scene isolation capability jest dostępne dla required render checks.

Brak dowolnego required precondition = `BLOCKED`, nie improwizacja.

---

## Transaction

### 1. Inspect
Sprawdź current owner objects/helpers i node revision.

### 2. Build/repair
Modyfikuj tylko:
- node owner;
- jawne helper objects;
- expected-change region.

### 3. Mark `BUILT_UNVERIFIED`
Samo utworzenie obiektu nie jest PASS.

### 4. Validate
Uruchom:
- numeric checks;
- required canonical view registered QA;
- section/profile validator, jeśli dotyczy;
- parent/sibling regression;
- topology sanity odpowiednią dla tego etapu.

### 5. Gate
`RECONSTRUCTION_NODE_GATE` zwraca:
- `ACCEPTED`;
- `FAIL`;
- `BLOCKED`;
- `UNVERIFIED`.

### 6. Persist
Zapisz compact node acceptance record i graph revision.

---

## No bulk-add rule

Jedna transakcja nie może tworzyć 20 niezależnych form, a potem wykonywać jednego wspólnego renderu.

Jeżeli node jest assembly:
- assembly node może organizować dzieci;
- geometry mutation nadal odbywa się na leaf/structural child nodes zgodnie z RDL.

Wyjątek: atomowa geometria, której rozdzielenie uniemożliwia sensowne QA, musi mieć jawny `atomic_group_id`.

---

## Node script architecture

Asset-specific builder powinien mieć cienkie funkcje:

```python
build_primary_body(spec, context)
build_base_plinth(spec, context)
build_lower_shoulder(spec, context)
build_side_frame(spec, context)
```

Orchestrator:

```text
resolve ready node
-> invoke registered implementation
-> validate node
-> persist
-> resolve next ready node
```

Nie preferuj jednej funkcji `build_all()`.

Jeżeli convenience `build_all()` istnieje dla manualnego replayu, musi wewnętrznie respektować node gates i nie może ominąć FAIL.

---

## Repair semantics

Node repair:
- nie resetuje całego assetu;
- oznacza dependent children `DIRTY`, jeśli zmiana może je naruszyć;
- niezależne accepted nodes pozostają reusable;
- nie wykonuje późniejszych RDL stages przed ponownym node PASS.

---

## Retry and representation switch

Po pierwszym FAIL:
- diagnoza;
- jedna poprawiona próba tej samej strategii.

Po drugim udowodnionym FAIL:
- re-inspect evidence;
- rozważ registration/parameter/representation error;
- jeśli representation jest niewystarczająca, route do `SHAPE_CLASSIFY` i zmień strategy.

Nie wykonuj serii `tweak -> render -> tweak -> render` bez zmiany modelu problemu.

---

## Output budget

Każdy node execution zwraca compact summary:

```yaml
node_execution:
  node_id: BASE_PLINTH
  revision: n_006
  skill_id: SECTION_LOFT_HARD_SURFACE
  mutation_objects: [ACS_WP_BASE]
  state: ACCEPTED
  view_results: {FRONT: PASS, SIDE: PASS, TOP: PASS}
  numeric: PASS
  blockers: []
  dirtied_children: [LOWER_LIGHT_SLOT]
```

Nie echoj całego skryptu ani raw pixel arrays.

# Build Plan Template

## Asset
Name:
Version:
Reference:
Target Blender:
Runtime profile:

## A. Feature Contract
Wklej listę `MUST`, `SHOULD`, `OPTIONAL`.

## B. Object decomposition

| Object | Purpose | Primitive/source | Symmetry | Material | Animated |
|---|---|---|---|---|---|

## C. Modeling strategy

Dla każdej części:
- technique:
- base primitive:
- modifiers:
- booleans:
- expected topology:
- feature IDs:

## D. Parameters

```text
WIDTH =
DEPTH =
HEIGHT =
THICKNESS =
BEVEL_MAIN =
BEVEL_DETAIL =
GAP =
```

## E. Execution phases

### Phase 1 — blockout
Affected objects:
Expected output:
Checkpoint:

### Phase 2 — primary details
Affected objects:
Feature IDs:
Checkpoint:

### Phase 3 — secondary details
Affected objects:
Feature IDs:
Checkpoint:

### Phase 4 — UV/material
Checkpoint:

### Phase 5 — game-ready
Checkpoint:

## F. Risks

| Risk | Probability | Impact | Mitigation |
|---|---:|---:|---|

## G. Exit criteria

Asset jest gotowy, gdy:
- [ ] all MUST features pass
- [ ] proportions pass
- [ ] shading pass
- [ ] UV/material pass
- [ ] runtime contract pass
- [ ] export pass

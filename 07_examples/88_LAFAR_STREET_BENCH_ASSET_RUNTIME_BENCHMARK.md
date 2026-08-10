# Benchmark 88 — Lafar Street Bench Asset Production Runtime

Status: vNext regression target

## Failure being prevented

The input is a normal manufactured civic bench, not an exotic modeling case. A system failure occurs when an agent sees the complete reference sheet, cognitively compresses it into a generic seat/back/support silhouette, drops secondary geometry and then spends repeated long-context turns rediscovering dimensions, materials and corrections.

The benchmark therefore measures architecture, not prompt eloquence.

## Canonical source fixture

`tests/fixtures/lafar_street_bench_vnext.json`

Known global dimensions:

- width: 2000 mm;
- depth: 550 mm;
- total height: 820 mm;
- seat height: 460 mm.

Required initial component tree:

```text
BENCH
├── LEFT_SUPPORT
├── RIGHT_SUPPORT
├── SEAT
└── BACKREST
```

Lighting, trim, utility panel and later microdetails are design bindings or child components rather than free-form prose.

## Required behavior

### 1. Persistent state

`ASSET_STATE_RUNTIME` validates the external state. Human corrections create new revisions and are not lost when a model/session changes. An accepted component receiving a hard correction becomes `DIRTY`.

### 2. Relational dimensions

`PARAMETER_GRAPH` must derive at least:

```text
LEFT_SUPPORT.depth = BENCH.depth - 15 = 535 mm
RIGHT_SUPPORT.width = LEFT_SUPPORT.width = 210 mm
SEAT.width = BENCH.width - LEFT_SUPPORT.width - RIGHT_SUPPORT.width = 1580 mm
BACKREST.width = SEAT.width = 1580 mm
BACKREST.info_strip_width = BACKREST.width - 80 = 1500 mm
```

The LLM must not repeatedly calculate these values in prose.

### 3. Design-system reuse

The benchmark binds shared Astera resources by ID:

- `ASTERA_GRAPHITE_01`;
- `ASTERA_TRIM_PROFILE_01`;
- `ASTERA_EDGE_PROFILE_02`;
- `ASTERA_LED_UNDERGLOW_01`;
- `ASTERA_LED_INFO_BLUE_01`;
- `ASTERA_UTILITY_PANEL_01`.

A locked inherited resource cannot be silently modified. An override requires an explicit authority record and remains visible as a deviation.

### 4. Component-scoped work

A BACKREST task must produce:

```text
allowed_to_modify = [BACKREST]
read_only includes SEAT, LEFT_SUPPORT, RIGHT_SUPPORT
```

The task pack contains only relevant parameters, anchors, bindings, corrections, relations, validation contract and reference evidence. Full history, full asset JSON and full library content are forbidden in normal component tasks.

### 5. Token budget

Hard targets:

- component repair pack: <= 4k estimated input tokens;
- component build pack: <= 8k estimated input tokens;
- asset planning: <= 15k input tokens;
- full `_FULL_LIBRARY.md`: forbidden during normal execution.

The fixture BACKREST task is expected to remain below 4k estimated tokens before any LLM-specific wrapper text.

### 6. Deterministic hard-surface execution

`HARD_SURFACE_RECIPE` is the intermediate representation between planning and Blender mutation.

The Blender runtime must prove at least:

- millimetre contract boundary;
- deterministic rounded-box creation;
- explicit bevel modifier;
- design binding metadata;
- named anchors;
- cleanup with no leaked test datablocks.

The benchmark does not claim the entire bench is solved by one rounded box. It proves that manufactured subproblems are executable primitives rather than regenerated Python code per agent turn.

### 7. Assembly

Anchor relations are explicit. A 7.3 mm BACKREST mount error must fail `ASSEMBLY_ANCHOR_GATE`; a worker may not distort the backrest body to conceal the mismatch.

Geometric contact/interpenetration remains separately governed by the existing `ASSEMBLY_INTEGRITY_GATE`.

## Acceptance criteria

Benchmark 88 passes only when all of the following are true:

1. the structured bench fixture passes asset-state validation;
2. relational dimensions resolve deterministically;
3. missing parameter references and cycles fail explicitly;
4. locked design-system resources cannot be overridden without authority;
5. BACKREST task mutation scope is isolated;
6. component task pack is within the declared token budget;
7. corrections survive revisioned persistence and stale writers are rejected;
8. hard-surface recipe validation rejects invalid operation order;
9. real Blender runtime creates and cleans a deterministic hard-surface test component;
10. assembly anchor tolerance violations are machine-detected.

## Architectural invariant

```text
REFERENCE / HUMAN DECISION
        ↓
PERSISTENT ASSET STATE
        ↓
PARAMETER GRAPH + DESIGN BINDINGS
        ↓
COMPONENT TASK PACK
        ↓
LLM PLAN / DIAGNOSIS
        ↓
HARD-SURFACE RECIPE
        ↓
BLENDER EXECUTOR
        ↓
NUMERIC / ASSEMBLY / VISUAL GATES
        ↓
NEW REVISION
```

No conversational transcript is a required source of truth anywhere in this chain.

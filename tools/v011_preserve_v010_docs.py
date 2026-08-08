from __future__ import annotations

"""Rebuild selected controller documents as v0.10 content + explicit v0.11 amendments.

The v0.11 release must harden execution without deleting prior reconstruction
knowledge. The canonical v0.10 merge commit is used as the immutable baseline.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "a8ce3f17c1726e5d02794f93472ff3911189dd86"

ADDENDA = {
    "00_governance/02_STATE_MACHINE.md": """## v0.11 execution-enforcement amendment

This amendment supersedes any weaker execution wording below while preserving the full v0.10 state-machine knowledge.

Canonical reconstruction node transition:

```text
DECLARED -> CONSTRAINED
CONSTRAINED -> READY_TO_BUILD       only via EXECUTION_AUTHORIZATION_GATE
READY_TO_BUILD -> BUILT_UNVERIFIED one-node mutation only
BUILT_UNVERIFIED -> ACCEPTED       only via RECONSTRUCTION_NODE_GATE
```

`UNVERIFIED`, `FAIL`, `BLOCKED`, `DIRTY`, `SUPERSEDED` are persistent states. `BUILT_UNVERIFIED` is a hard branch stop and never unlocks children. No `READY_TO_BUILD` node plus canonical authorization means no production geometry mutation. RDL0 must create neutral diagnostic geometry. Preflight also requires `CANONICAL_SKILL_RUNTIME_PIN`.
""",
    "00_governance/04_KNOWLEDGE_ROUTER.md": """## v0.11 routing override

This section has precedence over the v0.10 execution routing later in the document.

```text
runtime pin
-> reference evidence/calibration
-> REFERENCE_CONFLICT_RESOLVER for incompatible property interpretations
-> Shape Graph + Appearance Contract
-> eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> NODE_STATE_STORE persists READY_TO_BUILD
-> build exactly one node
-> persist BUILT_UNVERIFIED
-> per-view source proof
-> RECONSTRUCTION_NODE_GATE
-> persist ACCEPTED / FAIL / UNVERIFIED
-> RDL barrier
```

View evidence is typed per view: ORTHO uses registered overlay/numeric evidence, HERO uses supporting `PERSPECTIVE_INSPECTION`, DETAIL uses `LOCAL_FEATURE_ROI`. Before L4/L5 closure run `APPEARANCE_OWNER_COVERAGE`. Missing authorization or `ready_nodes=[]` blocks geometry mutation.
""",
    "00_governance/05_SEMANTIC_SKILL_REGISTRY.md": """## v0.11 registry additions and precedence

The following skills are canonical additions. They have precedence over any v0.10 routing sequence later in this document where the rules conflict.

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `REFERENCE_CONFLICT_RESOLVER` | per-property multi-view arbitration | `184_REFERENCE_CONFLICT_ARBITRATION.md`; `executors/reference_conflict_resolver.py` | CONTRACT_READY |
| `EXECUTION_AUTHORIZATION_GATE` | hard permission for one geometry mutation | `05_execution/73`; `executors/execution_authorization_gate.py` | CONTRACT_READY |
| `NODE_STATE_STORE` | persistent transition/checkpoint validation | `05_execution/74`; `executors/node_state_store.py` | CONTRACT_READY |
| `APPEARANCE_OWNER_COVERAGE` | MUST-owner inventory and namespace closure | `186`; `executors/appearance_owner_coverage.py` | CONTRACT_READY |
| `CANONICAL_SKILL_RUNTIME_PIN` | version/commit/single-root preflight | `188`; `executors/runtime_source_pin.py` | CONTRACT_READY |

Canonical v0.11 order: eligible node -> authorization -> persisted READY_TO_BUILD -> one-node mutation -> BUILT_UNVERIFIED stop -> canonical node proof -> ACCEPTED. Local builders cannot self-authorize or self-accept.
""",
    "05_execution/70_RECONSTRUCTION_NODE_EXECUTION_PROTOCOL.md": """## v0.11 hard-enforcement amendment

v0.10/v0.9 described the correct node loop, but the Lafar Street Lamp benchmark proved that an asset-local `main()` could still call all node functions in sequence. v0.11 makes the loop executable.

Before mutation require `EXECUTION_AUTHORIZATION_GATE.can_mutate == PASS`, persisted `READY_TO_BUILD`, accepted parent/dependencies and prior RDL barriers. Immediately after one node mutation persist `BUILT_UNVERIFIED` and stop that branch until source-anchored QA plus `RECONSTRUCTION_NODE_GATE` returns `ACCEPTED`.

Node-by-node function names are not sufficient. A monolithic function calling RDL0..RDL5 without persisted gates is a regression. See `73_EXECUTION_AUTHORIZATION_GATE.md`, `74_PERSISTENT_NODE_STATE_AND_CHECKPOINTS.md` and `75_NODE_SCOPED_ORCHESTRATION.md`.
""",
    "06_prompts/60_SYSTEM_PROMPT.md": """## v0.11 non-negotiable execution law

This amendment has precedence over weaker v0.10 wording below.

```text
NO READY_TO_BUILD NODE + EXECUTION_AUTHORIZATION_GATE PASS
-> NO PRODUCTION GEOMETRY MUTATION
```

`CONSTRAINED` means understood, not authorized. `BUILT_UNVERIFIED` means stop and validate. Exactly one node may be mutated per authorization. Persist node state/revision between operations. Use per-view evidence contracts; resolve incompatible property interpretations with `REFERENCE_CONFLICT_RESOLVER`; keep Shape Nodes, Appearance Owners, Evidence and Conflicts in separate namespaces; run `APPEARANCE_OWNER_COVERAGE`; use neutral diagnostic shading for RDL0–RDL3 form QA; verify one active pinned BlenderSkill runtime root before execution.
""",
    "06_prompts/68_SHAPE_GRAPH_PLANNER_PROMPT.md": """## v0.11 planner amendment

Every node must emit an explicit initial `state`. A planner may emit `CONSTRAINED` only when constraints, shape class and validation contract are complete; unresolved nodes stay `DECLARED`/`BLOCKED`. The planner never emits `READY_TO_BUILD`; only `EXECUTION_AUTHORIZATION_GATE` may authorize that transition.

Validation is per view, not one generic list:

```yaml
view_contracts:
  SIDE: {allowed_evidence_kinds: [REGISTERED_OVERLAY]}
  HERO: {allowed_evidence_kinds: [PERSPECTIVE_INSPECTION]}
  DETAIL_HEAD: {allowed_evidence_kinds: [LOCAL_FEATURE_ROI]}
```

Significant inferred radii/angles/paths/stations must retain estimate/range, method, source, confidence and provenance. Conflicting views produce a conflict record instead of a silent choice.
""",
    "10_reconstruction/100_RECONSTRUCTION_LAYER_INDEX.md": """## v0.11 controller amendment

v0.11 preserves the complete v0.10 reconstruction layer and adds enforced execution:

```text
PRELIGHT runtime pin
-> evidence / calibration / property authority
-> conflict arbitration
-> Shape Graph + Appearance Contract
-> RDL0 diagnostic geometry
-> eligible node
-> canonical execution authorization
-> persist READY_TO_BUILD
-> mutate one node
-> persist BUILT_UNVERIFIED
-> per-view source proof
-> node gate
-> ACCEPTED
-> repeat + RDL barriers
-> Appearance Owner Coverage
-> Appearance Fidelity Gate
-> Reconstruction Fidelity Gate
-> runtime
```

New modules 184–188 cover conflict arbitration, per-view evidence/derived provenance, owner coverage/report namespaces, diagnostic geometry/neutral shading and canonical runtime pinning/reuse. Benchmark 80 (Lafar Street Lamp) is the canonical regression driver.
""",
    "10_reconstruction/107_MULTI_VIEW_CONFLICT_RESOLUTION.md": """## v0.11 executable arbitration amendment

Conflict resolution is now a proof-bearing per-property artifact. Use `REFERENCE_CONFLICT_RESOLVER` / `184_REFERENCE_CONFLICT_ARBITRATION.md` when candidates remain incompatible after projection/calibration checks. Explicit dimensions own the property they name, not unrelated local shell shape. Detail views can own local cuts/trim/junctions while orthographic dimensions remain locked. Equal-authority contradictory candidates remain BLOCKED. Dependent nodes/derived values persist the resulting `decision_id`.
""",
    "10_reconstruction/178_NODE_BY_NODE_MULTI_VIEW_VALIDATION.md": """## v0.11 validation amendment

Before the loop begins, one eligible node must receive `EXECUTION_AUTHORIZATION_GATE` and persisted `READY_TO_BUILD`. After mutation persist `BUILT_UNVERIFIED` and stop until the canonical node gate closes.

Evidence mode is per view: ORTHO/NEAR_ORTHO -> registered overlay; HERO -> supporting `PERSPECTIVE_INSPECTION`; DETAIL -> `LOCAL_FEATURE_ROI`. Significant derived parameters require value/method/source/confidence/provenance and a conflict decision when needed. Builder consistency against its own constants never replaces source proof.
""",
}


def baseline(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True, encoding="utf-8")


def combine(path: str, addon: str) -> str:
    old = baseline(path)
    lines = old.splitlines()
    if not lines:
        return addon.strip() + "\n"
    title = lines[0]
    rest = "\n".join(lines[1:]).lstrip("\n")
    return title + "\n\n" + addon.strip() + "\n\n---\n\n" + rest + "\n"


for rel, addon in ADDENDA.items():
    (ROOT / rel).write_text(combine(rel, addon), encoding="utf-8")

print(f"Preserved v0.10 controller content and applied {len(ADDENDA)} v0.11 amendments")

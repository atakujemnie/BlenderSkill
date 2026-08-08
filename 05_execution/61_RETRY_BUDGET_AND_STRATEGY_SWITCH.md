# Retry Budget and Strategy Switching

## Purpose

This protocol prevents autonomous Blender agents from wasting tool calls, tokens, and scene integrity on repeated failed attempts with unchanged assumptions.

A retry is justified only when new information or a controlled parameter change makes success more likely.

## Core rule

```text
same operation + same preconditions + same strategy
-> maximum 1 retry
```

After the second failure, the agent must not repeat the same call pattern.

It must inspect, diagnose, and either change strategy or roll back.

## Failure loop

```text
ATTEMPT 1
-> fail
-> inspect failure state
-> one corrected retry allowed

ATTEMPT 2
-> fail
-> STOP same-strategy retries
-> restore/checkpoint if needed
-> re-inspect scene and assumptions
-> classify failure
-> switch strategy or escalate
```

A third attempt is allowed only if at least one of these changed materially:
- execution strategy;
- topology approach;
- tool/capability binding;
- scene/context precondition;
- validated parameter set;
- source geometry;
- target object/surface selection.

## Failure classes

### F1 — Context failure
Examples:
- wrong mode;
- wrong active object;
- operator poll failure;
- selection mismatch.

Repair:
- inspect context;
- set explicit context;
- prefer data/BMesh route if possible.

Do not repeatedly call the same operator hoping context changes.

### F2 — Geometry precondition failure
Examples:
- non-manifold region;
- missing edge chain;
- topology too noisy for requested operation;
- Boolean input invalid.

Repair:
- local topology repair;
- dedicated detail shell;
- alternate modeling strategy;
- rebuild affected local region.

### F3 — Parameter failure
Examples:
- bevel width self-overlap;
- projection tolerance too small;
- depth sign wrong after normals check.

Repair:
- change one documented parameter based on measured evidence;
- revalidate.

No random parameter sweeping on the production mesh.

### F4 — Capability failure
Examples:
- required connector tool unavailable;
- Python execution absent;
- render capture unavailable;
- unsupported Blender API property.

Repair:
- update Agent Tool API Profile;
- invoke defined fallback if one exists;
- otherwise block/escalate.

Do not silently replace a required technique with unrelated UI automation.

### F5 — Reference/constraint failure
Examples:
- conflicting views;
- unresolved dimension datum;
- ambiguous hidden geometry.

Repair:
- return to reconstruction authority/conflict/uncertainty modules;
- do not keep changing geometry until one view looks better.

### F6 — Regression failure
A local repair passes its feature but breaks an already accepted MUST feature.

Repair:
- rollback;
- inspect change-impact graph;
- choose a narrower patch or different strategy.

## Retry budget per feature

Track:

```yaml
retry_state:
  feature_id: F023
  operation: HS_PANEL_LINE
  attempts: 2
  same_strategy_failures: 2
  inspections_after_failure: 2
  strategy_switches: 0
  rollback_count: 0
  status: STRATEGY_SWITCH_REQUIRED
```

## Tool-call budget behavior

The agent should optimize for accepted features, not raw action count.

Important metric:

```text
tool_calls_per_accepted_feature
```

A feature that needs 25 blind operations is a diagnostic failure even if the final result eventually looks acceptable.

## Batch rule

Batch coherent deterministic changes when:
- they share validated preconditions;
- failure can be attributed clearly;
- postconditions can still identify which feature failed.

Do not batch unrelated risky operations merely to reduce call count.

## Parameter search rule

Allowed:

```text
measure -> adjust one relevant parameter -> validate
```

Disallowed:

```text
try 0.01
try 0.02
try 0.03
try 0.04
until screenshot seems acceptable
```

If parameter optimization is genuinely required, define bounded search criteria and objective metrics first.

## Local patch vs rebuild

Prefer local repair when:
- source topology is sound;
- failure is isolated;
- Feature Contract ownership is clear;
- regression risk is low.

Prefer controlled rebuild when:
- source topology is AI-generated/noisy;
- multiple local fixes have accumulated;
- semantic source data can regenerate the part deterministically;
- local surgery risks more regressions than reconstruction.

## Checkpoint rule

Before a strategy switch that can materially alter topology:
- preserve the last valid checkpoint;
- record the reason for abandoning the previous strategy.

If the new strategy fails, restore the last valid state rather than stacking fixes on top of a failed experiment.

## Escalation

Escalate when:
- two materially different strategies fail;
- a MUST feature cannot be satisfied without breaking another MUST feature;
- required capability is unavailable;
- reference authority cannot resolve a high-impact contradiction;
- runtime/export contract is unknown and required for completion.

## Agent response requirement

After repeated failure, the agent must report compactly:

```text
FAILED OPERATION
ROOT CAUSE CLASS
EVIDENCE
ATTEMPTS
WHY SAME RETRY IS FORBIDDEN
NEXT STRATEGY OR BLOCKER
LAST VALID CHECKPOINT
```

Do not hide retry churn inside a final narrative.

## Fundamental rule

Every retry must buy information or change a validated precondition.

If nothing meaningful changed, do not call the tool again.

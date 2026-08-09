# Industrial Assembly Integrity Playbook

## Scope

Hard-surface civic/product assets composed from multiple shells, panels, trims, inserts, lamps, sensors and service modules.

## Before building child parts

For every important child-host pair declare:
- host Shape Node;
- child Shape Node;
- assembly relation type;
- expected gap/contact/embedding behavior;
- whether interpenetration is forbidden or bounded;
- source evidence for the junction.

Do not use generic overlap as a proxy for `connected`.

## During one-node mutation

Immediately after the authorized mutation:
1. run `MUTATION_POSTCONDITION_GATE`;
2. verify Boolean/transform/loft outcomes;
3. only then persist `BUILT_UNVERIFIED`;
4. run reference QA;
5. run `ASSEMBLY_INTEGRITY_GATE` for every relation touched by the node;
6. only canonical node acceptance unlocks dependants.

## High-risk operations

### Boolean recesses
Require before/after geometry evidence. Modifier disappearance alone is insufficient.

### Layered housings
Check front-to-back layer order and assembly relation. Two coincident skins are not a layered assembly.

### Sensor / cap modules
Prefer a declared butt/shadow-gap/recess relation. Verify the host does not poke through the child shell.

### Trim in channels
Some overlap is intentional. Use `RECESSED_INSERT` or `EMBEDDED` with bounded embedding instead of globally disabling interpenetration checks.

### Service doors
Use `SHADOW_GAP`, `FLUSH_MATE` or `RECESSED_INSERT` according to reference/manufacturing logic.

## Repair

When a host is repaired:
- run `DEPENDENCY_INVALIDATOR`;
- dirty/block affected descendants;
- invalidate hosted Appearance Owners;
- supersede old evidence;
- rebuild only affected closure;
- rerun integrity + reference gates.

## Final pre-runtime integrity sweep

For L4/L5 industrial assets require:
- zero failed MUST assembly relations;
- zero silent mutation postcondition failures;
- closed-solid topology appropriate to contract;
- no unclassified risky n-gons in critical visible regions;
- all MUST validators proven with negative controls;
- no stale evidence after repair.

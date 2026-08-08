# Multi-View Conflict Resolution v0.11

## Principle

Resolve conflicts per property and persist the decision. Do not apply one blanket rule such as `the card wins`.

Conflict types include dimension, profile, topology, feature presence, material, asymmetry, projection artifact and internal concept-sheet inconsistency.

## Procedure
1. identify the exact property;
2. list candidate interpretations and source IDs;
3. classify each source/view and authority for that property;
4. test projection/calibration error;
5. invoke `REFERENCE_CONFLICT_RESOLVER` when candidates remain incompatible;
6. persist selected and rejected alternatives;
7. bind dependent derived parameters/nodes to `decision_id`.

## No averaging

```text
(front_value + side_value) / 2
```

is forbidden unless the property is explicitly statistical and the contract says averaging is valid.

## Local detail versus global dimension
An explicit dimension owns the dimension it names. A detail view may still own local break lines, shell cuts, trim terminations and junction form. Hero views may support design intent without overriding locked dimensions.

## Equal authority
Equal-authority contradictory candidates remain `UNRESOLVED`/`BLOCKED`; the agent does not choose the visually convenient option.

Detailed executable contract: `184_REFERENCE_CONFLICT_ARBITRATION.md`.

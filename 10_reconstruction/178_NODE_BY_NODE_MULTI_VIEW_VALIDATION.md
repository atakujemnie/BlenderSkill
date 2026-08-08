# Node-by-Node Multi-View Validation v0.11

## Canonical loop

```text
eligible node
-> EXECUTION_AUTHORIZATION_GATE
-> persist READY_TO_BUILD
-> build/repair current node only
-> persist BUILT_UNVERIFIED
-> isolate accepted ancestors + current node
-> validate each required view using its own evidence contract
-> numeric/section/derived-parameter checks
-> RECONSTRUCTION_NODE_GATE
-> ACCEPTED | UNVERIFIED | FAIL
```

`BUILT_UNVERIFIED` is a hard stop, not a report label.

## Per-view evidence

Example:

```yaml
view_contracts:
  SIDE:
    controls: [outer_profile]
    allowed_evidence_kinds: [REGISTERED_OVERLAY]
  HERO:
    controls: [junction_interpretation]
    allowed_evidence_kinds: [PERSPECTIVE_INSPECTION]
  DETAIL_HEAD:
    controls: [sensor_boundary, upper_shell_cuts]
    allowed_evidence_kinds: [LOCAL_FEATURE_ROI]
```

Do not use a single `_v()` evidence-kind list for all views.

## Derived parameters
Every MUST-significant inferred radius/angle/path/station includes value/range, method, source reference, ROI, confidence, provenance and conflict decision when applicable. Builder consistency against its own constant is not source proof.

## Isolation
QA includes accepted ancestors/host and current node only. No future RDL nodes, collision proxies, helpers or export copies.

## Failure routing
- FRONT width PASS + SIDE profile FAIL -> local/profile owner, not random global scaling;
- equal-authority view conflict -> `REFERENCE_CONFLICT_RESOLVER`;
- appearance ROI reveals wrong host form -> mark host DIRTY and invalidate descendants;
- missing evidence -> UNVERIFIED, not PASS.

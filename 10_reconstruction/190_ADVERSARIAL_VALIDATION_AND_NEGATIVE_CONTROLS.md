# Adversarial Validation and Negative Controls

## Purpose

A validator is not trustworthy because it returns PASS on the current asset.

The v0.11 lamp produced a toothless guard: an initial containment-based interpenetration check returned PASS on the known-broken sensor/arm assembly. The defect was a surface intersection, not complete burial.

v0.12 therefore requires bite tests for acceptance validators.

## Rule

Before a validator can provide MUST acceptance evidence, prove at least:

```text
KNOWN_GOOD fixture   -> PASS
KNOWN_BROKEN fixture -> FAIL
```

If the broken fixture returns PASS, the validator is rejected regardless of how plausible its algorithm sounds.

## Negative-control classes

Choose a mutation that represents the failure class the validator claims to detect.

Examples:
- assembly integrity: inject forbidden overlap;
- Boolean postcondition: remove the cutter effect while preserving modifier lifecycle;
- gap validator: collapse the gap to zero;
- trim path validator: shift centerline outside tolerance;
- layer-stack validator: bury visible layer behind host;
- overlay validator: shift silhouette by a known pixel offset;
- runtime package validator: remove `TEXCOORD_0`.

## Anti-cheat rule

The negative fixture must differ in the measured property, not by an unrelated easy-to-detect marker. Do not add `broken=True` and then test that flag.

## Control record

```yaml
validator_id_under_test: ASSEMBLY_INTEGRITY_GATE
positive_controls:
  - case_id: sensor_arm_shadow_gap_good
    actual_status: PASS
negative_controls:
  - case_id: sensor_arm_5mm_overlap
    actual_status: FAIL
```

## Maturity implication

A validator without a negative-control fixture cannot be promoted to `EXECUTOR_READY` for MUST acceptance.

## Canonical executor

`executors/validator_negative_control.py`

Skill ID: `VALIDATOR_NEGATIVE_CONTROL`.

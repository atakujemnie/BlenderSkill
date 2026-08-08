# Anti-Circular Visual Validation

## Purpose

Prevent the builder from proving only that it implemented its own assumptions consistently.

This module is mandatory for strict reference reconstruction.

---

## Core failure

Bad proof chain:

```text
builder infers parameter P
-> builder stores P in local spec
-> builder constructs geometry from P
-> local test checks geometry == P
-> PASS
```

This can prove implementation consistency. It does not prove the reference supports P.

The Lafar Street Bench v0.9 benchmark exposed this directly: many locally authored numeric gates passed while the user judged the model only 6/10 visually.

---

## Evidence classes

### Builder-consistency evidence
Useful but insufficient by itself for reference acceptance:
- generated dimensions equal builder constants;
- section station ordering;
- no twist;
- mesh manifold checks;
- transform identity;
- local relation invariants.

### Reference-anchored evidence
Required for visual acceptance:
- registered overlay against source view;
- source-calibrated numeric measurement;
- landmark projection derived from source;
- source ROI feature comparison;
- source-backed layer/material boundary comparison;
- authority decision with source provenance.

---

## Strict acceptance record

For reference-derived owners, strict mode requires:

```yaml
status: PASS
evidence_kind: REGISTERED_OVERLAY
validator_id: REFERENCE_OVERLAY_VALIDATE
provenance_id: report_...
source_reference_id: ref_...
registration_id: reg_...
```

For hard explicit dimensions:

```yaml
status: PASS
evidence_kind: NUMERIC_MEASUREMENT
validator_id: REFERENCE_MEASURE
provenance_id: bounds_...
source_reference_id: sheet_...
source_field_id: DIM_TOTAL_WIDTH_2000
```

---

## Canonical validator rule

If the Semantic Skill Registry exposes a canonical validator for the acceptance owner, a local substitute cannot certify the owner.

Examples:

```text
registered view -> REFERENCE_OVERLAY_VALIDATE
node acceptance -> RECONSTRUCTION_NODE_GATE
layer order -> LAYER_STACK_VALIDATE
final reconstruction -> RECON_FIDELITY_GATE
appearance -> APPEARANCE_FIDELITY_GATE
```

A helper may compute intermediate values, but final acceptance record must name the canonical `validator_id`.

Bad:

```python
class Gate:
    def accept(...):
        return True
```

when used as proof of canonical node acceptance.

Allowed:

```text
local helper -> measurement artifact
canonical validator -> acceptance record
```

---

## No evidence laundering

Do not convert a weak record into a strong one by relabeling fields.

Invalid:

```yaml
status: PASS
evidence_kind: REGISTERED_OVERLAY
provenance_id: local_numeric_gate_12
```

if no registered overlay exists.

Validator ID and evidence artifact must be compatible.

---

## Validator provenance

Strict records should carry:

```yaml
validator_id: REFERENCE_OVERLAY_VALIDATE
validator_version: 0.3.0
producer: executor
artifact_hash: optional
```

The gate may reject:
- unknown validator IDs;
- evidence kinds not produced by that validator family;
- missing source references for reference-derived evidence;
- missing registration for projection-based evidence.

---

## Derived-parameter rule

A derived parameter is valid only if it has a derivation record:

```yaml
derived_parameter:
  id: SIDE_FRONT_RADIUS
  value_mm: 165
  source_reference_ids: [sheet_side_v1]
  method: ARC_FIT
  source_roi: [...]
  confidence: 0.82
  residual_px: 3.1
```

A node gate may check geometry against 165 mm as a builder-consistency test, but reference acceptance also needs the source-fit record or direct projected comparison.

---

## Independent acceptance logic

Builder and validator may execute in the same Python process, but they must not share acceptance state.

Required structure:

```text
builder output artifact
-> validator reads artifact + source evidence
-> validator emits compact result
-> gate aggregates result
```

Forbidden:

```text
builder finished -> accepted = True
```

---

## Runtime boundary

No runtime stage may interpret these as reference proof:
- correct LOD budgets;
- successful UV generation;
- valid glTF;
- clean package readback;
- engine load.

These are downstream technical evidence only.

---

## Audit checklist

Before claiming a reference node accepted:
- does each required view have a canonical validator record?
- does each record point to the source reference or explicit source field?
- does projected evidence have a registration ID?
- are derived values supported by source-fit artifacts?
- did the builder author its own acceptance logic?
- can the evidence be recomputed from the saved artifact without trusting builder state?

Any negative answer produces `UNVERIFIED` in strict mode.
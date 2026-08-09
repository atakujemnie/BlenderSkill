# Location Reference Composition Fidelity

## Purpose

Validate global scene correspondence after individual assets are valid.

## Owners

- architectural envelope/proportions;
- major zone placement;
- HERO anchors;
- orientation/facing;
- scale relationships;
- density/negative space;
- dominant material/light hierarchy;
- reference-camera focal composition.

Default policy when stronger calibrated authority is unavailable:

```text
layout anchor error <= 100 mm
important orientation error <= 5 deg
HERO scale error <= 3%
composition score >= 0.85
```

These defaults are replaceable by project/reference contracts.

Canonical executor: `executors/location_reference_fidelity_gate.py`.

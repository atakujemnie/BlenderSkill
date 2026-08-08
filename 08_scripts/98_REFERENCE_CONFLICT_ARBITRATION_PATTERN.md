# Reference Conflict Arbitration Pattern

Use one record per conflicting property.

```python
from reference_conflict_resolver import resolve

result = resolve({
    'property_id': 'HEAD_TOP_PROFILE',
    'candidates': [
        {
            'value': 'SLOPED',
            'source_reference_id': 'SIDE',
            'authority_kind': 'ORTHOGRAPHIC',
            'confidence': 0.78,
        },
        {
            'value': 'STEPPED_COMPOUND',
            'source_reference_id': 'DETAIL_HEAD',
            'authority_kind': 'DETAIL_ORTHO',
            'confidence': 0.93,
        },
    ],
})
```

Persist `decision_id` with every dependent derived parameter and Shape Node.

Equal-authority disagreement must remain BLOCKED; do not average profiles.

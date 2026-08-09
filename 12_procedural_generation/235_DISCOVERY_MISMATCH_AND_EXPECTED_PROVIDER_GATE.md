# Discovery Mismatch and Expected Provider Gate

## Purpose

Turn explicit user/project knowledge about installed providers into a verification oracle for runtime discovery.

## Input

```yaml
expected_providers:
  - provider_id: sapling_tree_gen
    version: 0.3.7
  - provider_id: ivygen
    version: 0.1.5
  - provider_id: sverchok
    version: 1.4.0
```

Versions may be advisory unless `require_exact_version=true`.

## Gate

PASS requires every expected provider to occur in normalized discovery output.

Failures include:
- expected provider completely missing;
- provider discovered under an unclassified/unknown identity when a canonical mapping is required;
- exact version mismatch when exact matching was requested.

## Required behavior

```text
EXPECTED list supplied
+
missing provider
=
FAIL DISCOVERY_MISMATCH
```

This is not equivalent to a failed runtime capability probe. A mismatch means the inventory itself cannot yet be trusted.

The agent must not proceed to custom fallback until the mismatch is resolved or the user explicitly retracts/corrects the expected-provider evidence.
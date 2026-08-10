# Provider State Protocol

Version: 0.18.0
Status: EXECUTOR_READY
Executor: `executors/provider_contracts.py`

## Canonical dimensions

Provider evidence is represented by independent state dimensions. Do not collapse them into one status.

### SourceKind

`READY_ASSET_SOURCE`, `PROCEDURAL_GENERATOR`, `EXTERNAL_GENERATOR`, `UTILITY`, `BUILTIN_BACKEND`, `UNKNOWN`.

### DiscoveryState

`DISCOVERED`, `NOT_DISCOVERED`, `DISCOVERY_MISMATCH`.

### ProbeState

`PROBE_REQUIRED`, `PASS`, `FAIL`, `DISABLED`, `BLOCKED`, `NOT_APPLICABLE`.

### DomainState

`MATCH`, `GENERIC_MATCH`, `MISMATCH`, `UNKNOWN`.

### QualityState

`UNRATED`, `PASS`, `REJECTED`.

### SelectionState

`ELIGIBLE`, `ELIGIBLE_GENERIC`, `REJECTED`, `SELECTED`, `BLOCKED`.

`executors/provider_contracts.py` is the only allowed source for these state vocabularies. Consumers use `normalize_provider_record()` and `validate_provider_record()` rather than defining local state lists.

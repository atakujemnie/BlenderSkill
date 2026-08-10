# Contract / Executor / Test Parity Gate

Version: 0.18.0
Status: CURRENT CONTRACT

## Gate

Every manifest entry with `maturity=EXECUTOR_READY` must satisfy all conditions:

- contract path exists;
- executor path exists;
- executor is importable by the supported Python runtime;
- `EXECUTOR_ID` equals the registered skill id;
- `EXECUTOR_VERSION` is declared;
- at least one executable test path exists.

`tools/validate_registry_parity.py` is the release authority for this relationship.

## Failure codes

- `MISSING_CONTRACT`
- `MISSING_EXECUTOR`
- `MISSING_EXECUTOR_TEST`
- `EXECUTOR_ID_MISMATCH`
- `EXECUTOR_VERSION_MISSING`
- `ORPHAN_EXECUTOR`
- `REGISTRY_PATH_INVALID`

A parity failure is release-blocking. Documentation maturity must never be promoted as a substitute for executable coverage.

# Provider Capability Probe Matrix

Version: 0.18.0
Status: EXECUTOR_READY
Executor: `executors/provider_probe_runner.py`
Runtime adapters: `executors/provider_probes/`

## Separation

For every relevant provider keep these states independent:

```text
discovery_state
enabled
probe_state
domain_state
compatibility_state
license_state
quality_state
selection_state
```

A provider may be discovered and probe-capable while still being rejected for the requested domain or quality. It remains visible in the final report.

## Executable probe matrix

- Blender Geometry Nodes: real disposable geometry/node-tree/evaluation/cleanup probe; required CI.
- Sapling: minimal disposable tree operator probe with cleanup; UI-context inability is `BLOCKED`.
- IvyGen: disposable source surface and minimal ivy operator probe with cleanup; UI-context inability is `BLOCKED`.
- ANT Landscape: minimal terrain generation probe with cleanup.
- Sverchok: disposable `SverchCustomTreeType` creation and cleanup.
- MPFB: minimal loaded API-surface capability required by BlenderSkill; no full character generation required.
- Geo Nodes Guide: integration/API-surface capability probe.
- MCP: integration/API-surface capability probe.
- Meshy: non-paid plugin/API surface and auth-state inspection only.

Providers with registry probe types that do not yet have a specialized adapter remain `PROBE_REQUIRED`; the runner must not manufacture `PASS`.

## Probe requirements

An executable probe verifies, where applicable:

- expected API/operator/node-tree surface exists;
- required context can be satisfied;
- minimal disposable operation executes;
- output type is valid;
- deterministic behavior where claimed;
- cleanup restores the pre-probe datablock state.

Any cleanup failure forces the canonical probe result to `FAIL`.

## Canonical failure semantics

- discovery miss: `NOT_DISCOVERED`;
- discovered but untested: `PROBE_REQUIRED`;
- provider disabled: `DISABLED`;
- environment/context prevents a valid test: `BLOCKED` with blocker reason;
- probe executed and failed: `FAIL`;
- probe passed but domain mismatched: `probe=PASS`, `domain=MISMATCH`, `selection=REJECTED`;
- insufficient quality: `quality=REJECTED`, provider remains reported;
- usable candidate: `ELIGIBLE` or `ELIGIBLE_GENERIC`.

Do not collapse these states into one boolean.

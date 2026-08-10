# Provider Capability Probe Execution

Version: 0.18.0
Status: EXECUTOR_READY
Executor: `executors/provider_probe_runner.py`

Capability probes are explicit execution and are never part of discovery.

Every probe returns provider id, canonical `probe_state`, Blender/provider versions when known, capabilities, cleanup state, side-effect flag, warnings and blockers.

Probe requirements:

- minimal scope;
- deterministic when provider declares seed support;
- isolated disposable data;
- reversible cleanup;
- no persistent project preference changes;
- no paid external generation.

A provider requiring unavailable UI context returns canonical `BLOCKED` plus `UI_CONTEXT_REQUIRED`; this is not capability `FAIL`.

The built-in Geometry Nodes probe creates and evaluates real temporary geometry and a real node group. A successful functional result is still converted to `FAIL` if cleanup fails or side effects remain.

Meshy probing is restricted to plugin/API surface, credential state and network capability. It must never trigger automatic paid generation.

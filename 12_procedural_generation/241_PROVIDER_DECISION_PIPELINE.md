# Provider Decision Pipeline

Version: 0.18.0
Status: EXECUTOR_READY
Executor: `executors/provider_orchestrator.py`

Canonical order:

```text
BLENDER_RUNTIME_ADDON_DISCOVERY
→ PROVIDER_CLASSIFICATION
→ EXPECTED_PROVIDER_GATE
→ CAPABILITY_PROBES
→ BLENDER_VERSION_COMPATIBILITY
→ DOMAIN_MATCH
→ LICENSE_POLICY
→ QUALITY_GATE
→ PROVIDER_SELECTION
→ PROVIDER_SELECTION_REPORT
```

Each evidence dimension is preserved in the report. A provider may therefore be discovered and probe-capable yet rejected because its requested domain mismatches, its Blender range is incompatible, its license policy blocks use, or its quality tier is insufficient.

Custom/native fallback is evaluated after stronger candidates. It is blocked when any stronger relevant candidate remains `ELIGIBLE` or `ELIGIBLE_GENERIC`, and rejection reasons for evaluated candidates must remain visible.

The expected-provider gate supports version constraints (`==`, `!=`, `>`, `>=`, `<`, `<=`) including comma-separated ranges such as `>=2.0,<3.0`.

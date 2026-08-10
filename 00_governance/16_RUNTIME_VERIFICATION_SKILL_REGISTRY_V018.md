# Runtime Verification Skill Registry v0.18

Version: 0.18.0
Status: CURRENT CONTRACT

## Registered runtime skills

| Skill ID | Contract | Executor | Maturity |
|---|---|---|---|
| INSTALLED_PROVIDER_DISCOVERY | `12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md` | `executors/installed_provider_inventory.py` | EXECUTOR_READY |
| BLENDER_RUNTIME_ADDON_DISCOVERY | `12_procedural_generation/239_NON_EXECUTING_PROVIDER_DISCOVERY.md` | `executors/blender_addon_inventory.py` | EXECUTOR_READY |
| PROVIDER_CAPABILITY_PROBE | `12_procedural_generation/240_PROVIDER_CAPABILITY_PROBE_EXECUTION.md` | `executors/provider_probe_runner.py` | EXECUTOR_READY |
| EXPECTED_PROVIDER_GATE | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/expected_provider_gate.py` | EXECUTOR_READY |
| PROVIDER_QUALITY_SELECT | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_quality.py` | EXECUTOR_READY |
| PROVIDER_SELECTION_REPORT | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_selection_report.py` | EXECUTOR_READY |
| PROVIDER_DECISION_PIPELINE | `12_procedural_generation/241_PROVIDER_DECISION_PIPELINE.md` | `executors/provider_orchestrator.py` | EXECUTOR_READY |

## Routing

For provider-sensitive tasks load the Runtime Index first, then the provider state protocol, canonical registry, non-executing discovery contract, capability-probe contract and decision-pipeline contract. Historical v0.14-v0.17 override documents are evidence and regression history, not active routing layers.

## Promotion rule

Changing a Markdown maturity label does not promote a skill. `EXECUTOR_READY` is valid only when contract, executor identity/version and executable tests pass parity validation.

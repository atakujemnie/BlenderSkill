# v0.17 Provider Discovery Skill Registry

| Skill ID | Purpose | Canonical implementation | Maturity |
|---|---|---|---|
| `INSTALLED_PROVIDER_DISCOVERY` | collect installed/enabled Blender add-ons, registered Asset Libraries and built-in backends | `12_procedural_generation/230`; `executors/blender_addon_inventory.py`; `executors/installed_provider_inventory.py` | EXECUTOR_READY |
| `PROVIDER_CLASSIFY` | normalize discovered add-ons into asset source/generator/external/utility/backend classes and domains | `12_procedural_generation/231`; `executors/installed_provider_inventory.py` | EXECUTOR_READY |
| `EXPECTED_PROVIDER_GATE` | block silent fallback when a user/project-declared installed provider disappears from discovery | `12_procedural_generation/235`; `executors/expected_provider_gate.py` | EXECUTOR_READY |
| `PROVIDER_CAPABILITY_PROBE_MATRIX` | keep discovery, executable probe and requested-domain support separate | `12_procedural_generation/233` | CONTRACT_READY |
| `PROVIDER_SELECTION_REPORT` | report all relevant candidates, rejection reasons and selected backend | `12_procedural_generation/234`; `executors/provider_selection_report.py` | EXECUTOR_READY |
| `VEGETATION_PROVIDER_ROUTE` | select vegetation source without conflating missing asset libraries with missing generators | `12_procedural_generation/236` | CONTRACT_READY |

For procedural/environment tasks, `INSTALLED_PROVIDER_DISCOVERY` precedes provider selection. If the user explicitly supplies an installed add-on list, `EXPECTED_PROVIDER_GATE` is mandatory for that run.
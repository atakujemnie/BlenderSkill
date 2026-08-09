# Location Design System Validation Pattern

## Pure-Python sequence

```python
from executors.design_system_resolver import resolve
from executors.design_system_manifest import evaluate as validate_manifest
from executors.design_system_inheritance import resolve as resolve_inheritance
from executors.design_system_conformance import evaluate as validate_conformance
```

Recommended flow:

```text
resolve/bootstrap path
-> read/populate manifest
-> validate manifest
-> resolve inheritance for current organization/family
-> construct compact usage record
-> conformance gate
```

## Negative controls

A useful regression must include:
- empty bootstrapped manifest fails final readiness;
- locked identity override fails inheritance;
- unregistered one-off material fails conformance;
- resource ID hash collision fails promotion;
- same-content resource deduplicates.

## Blender bridge

Runtime scripts may then:
- open/update canonical Asset Library `.blend`;
- load canonical resources through `bpy.data.libraries.load`;
- bind semantic IDs to actual datablocks;
- read back names/paths and compare against `asset_library_manifest.json`.

Pure-Python PASS does not prove Blender Asset Library packaging. That remains a Blender runtime proof.

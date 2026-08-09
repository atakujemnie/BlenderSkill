# Procedural Generator Provider Contract

## Goal

Expose external or built-in generators through one stable semantic contract instead of teaching the agent separate ad-hoc call patterns for Sapling, IvyGen, Sverchok, engon, Geometry Nodes or future tools.

## Provider schema

```yaml
provider_id: stable-id
provider_version: exact-or-probed
blender_min: 5.1.0
blender_max: 5.1.x
execution_type: DIRECT_PYTHON | BPY_OPERATOR | GEOMETRY_NODES | EXTERNAL_PROCESS | SOURCE_ONLY
supports_background: true|false
requires_ui_context: true|false
deterministic: true|false
supports_seed: true|false
input_schema: {...}
output_schema: {...}
license: SPDX-or-explicit-policy
asset_license_policy: optional
probe_required: true
required_capabilities: [...]
```

## Canonical lifecycle

```text
discover
-> version check
-> license check
-> isolated capability probe
-> output/postcondition validation
-> AVAILABLE | BLOCKED | SOURCE_ONLY
-> execute production request
-> validate generated artifact
-> cleanup temporary state
```

## Rules

- Provider may translate a semantic spec into tool-specific parameters; it may not redefine acceptance semantics.
- A successful operator return is not sufficient. Generated geometry needs a postcondition/signature.
- Missing provider is a routing event, not permission to improvise another API with guessed parameters.
- Asset libraries and code licenses are separate concerns. Never treat paid/third-party vegetation assets as redistributable because adapter code is open source.
- Runtime version claims are evidence, not memory. Probe the active Blender session.

## Executor

`executors/procedural_provider.py`.

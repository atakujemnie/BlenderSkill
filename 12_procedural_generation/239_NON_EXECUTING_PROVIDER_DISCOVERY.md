# Non-Executing Provider Discovery

Version: 0.18.0
Status: EXECUTOR_READY
Executors: `executors/blender_addon_inventory.py`, `executors/installed_provider_inventory.py`

## Rule

Discovery is read-only. Discovery must not execute provider code.

Allowed evidence:

- `bpy.context.preferences`;
- `addon_utils` metadata already exposed by Blender;
- already-loaded `sys.modules`;
- Blender extension/add-on metadata;
- Asset Library preferences;
- Blender runtime metadata.

Forbidden during discovery:

- `importlib.import_module()` of a provider;
- `__import__()` of a provider;
- provider operators;
- object or node-group creation;
- network requests;
- preference mutations.

When complete metadata cannot be obtained without executing a provider, report `version=UNKNOWN`, partial metadata and `probe_state=PROBE_REQUIRED`.

Built-in Geometry Nodes is always discovered separately from capability evidence and therefore enters the pipeline as `PROBE_REQUIRED`.

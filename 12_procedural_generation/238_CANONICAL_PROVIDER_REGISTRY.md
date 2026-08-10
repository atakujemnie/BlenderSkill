# Canonical Provider Registry

Version: 0.18.0
Status: EXECUTOR_READY
Registry: `data/provider_registry.json`
Loader: `executors/provider_registry.py`

`data/provider_registry.json` is the only authored source of provider identity and static classification metadata.

Required fields include provider id, aliases/module patterns, source kind, domains, execution type, Blender compatibility constraints, seed support, probe type, license policy and role.

Legacy catalog APIs may exist only as compatibility facades reading this registry. They may not duplicate domains, source kinds, compatibility ranges or licenses.

An add-on that does not match the registry remains visible with:

```text
source_kind = UNKNOWN
classification_known = false
domains = []
probe_state = PROBE_REQUIRED
```

Unknown providers are not automatically eligible for selection. Explicit future classification or an explicit controlled override is required.

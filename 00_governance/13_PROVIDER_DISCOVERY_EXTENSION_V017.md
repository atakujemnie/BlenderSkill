# v0.17 Installed Provider Discovery and Capability Inventory

## Purpose

v0.17 closes a production failure exposed by the Lafar planter workflow: the agent reported "no vegetation libraries" and silently fell back to a custom generator even though multiple relevant Blender add-ons were installed.

The root problem was category collapse. A missing ready-made asset library was treated as if no procedural provider existed.

## Non-negotiable laws

```text
ASSET_LIBRARY_NONE
!=
PROCEDURAL_PROVIDER_NONE
```

```text
user/runtime says provider is installed
+
provider absent from discovery report
=
DISCOVERY_MISMATCH -> no silent fallback
```

```text
provider discovered
!=
provider execution probe PASS
```

```text
provider execution probe PASS
!=
provider suitable for requested domain/quality tier
```

Before a procedural/environment route can select a backend, the agent must produce a compact inventory separating:

1. ready asset sources;
2. procedural generators;
3. external generators/services;
4. utilities/integration tools;
5. built-in Blender backends.

Every discovered relevant provider must appear in the selection report even when rejected for domain mismatch, failed probe, quality tier, determinism, license, or context requirements.

## Required workflow

```text
active Blender runtime
-> INSTALLED_PROVIDER_DISCOVERY
-> EXPECTED_PROVIDER_GATE when user/project supplied expected providers
-> PROVIDER_CAPABILITY_PROBE_MATRIX
-> requested-domain suitability
-> provider quality policy
-> PROVIDER_SELECTION_REPORT
-> selected backend or explicit BLOCKED
```

A statement such as "no vegetation library" is legal only when explicitly scoped to `READY_ASSET_SOURCE`. It must not hide installed generators such as Sapling, IvyGen or Sverchok.

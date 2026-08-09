# Provider Discovery and Selection Prompt v0.17

Use this prompt before procedural/environment generation when third-party or built-in providers may apply.

## Required sequence

1. Run `BLENDER_RUNTIME_ADDON_DISCOVERY` inside the active Blender process.
2. Normalize with `INSTALLED_PROVIDER_DISCOVERY`.
3. If the user/project supplied an installed-provider list, run `EXPECTED_PROVIDER_GATE`.
4. Separate source buckets: ready asset sources, procedural generators, external generators, utilities, built-in backends.
5. For each broadly relevant provider, resolve runtime probe state and domain suitability.
6. Produce `PROVIDER_SELECTION_REPORT` before selecting custom/native fallback.

## Output discipline

Never write:

```text
no vegetation libraries/providers
```

when the evidence only proves the ready Asset Library bucket is empty.

Instead report the distinction, for example:

```text
READY_ASSET_SOURCE: NONE
PROCEDURAL_GENERATORS: Sapling Tree Gen, IvyGen, Sverchok
BUILTIN_BACKENDS: Blender Geometry Nodes
REQUESTED_DOMAIN: GRASS
SPECIALIZED_MATCH: NONE
SELECTED: Blender Geometry Nodes
```

If an expected installed provider is absent from discovery, stop with `DISCOVERY_MISMATCH`. Do not silently fall back.

A discovered provider that has not passed its execution probe is `PROBE_REQUIRED`, not `UNAVAILABLE`.
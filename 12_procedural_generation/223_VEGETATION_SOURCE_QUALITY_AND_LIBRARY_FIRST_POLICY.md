# Vegetation Source Quality and Library-First Policy

## Production selection order

For final vegetation:

```text
project/location vegetation library
-> licensed high-quality asset library
-> compatible specialist generator
-> hybrid source + procedural variation
-> full procedural generation
-> primitive/card fallback
```

This is a quality order, not a runtime-capability order.

## Usage classes

- `HERO`: require quality tier A or explicit user waiver;
- `MID`: require A/B;
- `BACKGROUND`: A/B/C allowed;
- `BLOCKOUT`: any runtime-compatible source allowed.

A built-in generator that is runtime-safe but visually generic must not displace a better installed library.

## Source-quality review

Assess:
- silhouette richness;
- close-up leaf/branch quality;
- botanical coherence;
- material completeness;
- source variation depth;
- clone visibility;
- LOD/runtime adaptability;
- license provenance.

Persist `source_quality_tier`, `usage_suitability`, and evidence. `RUNTIME PASS` never implies `QUALITY PASS`.

# Material and Texture Language

## Ownership

The design system owns material identity. The v0.14 location material library owns runtime-ready texture payloads. Individual assets consume and adapt approved families; they do not recreate generic equivalents from scratch.

## Material family record

Recommended fields:

```yaml
material_id: MAT_ASTERA_GRAPHITE_COMPOSITE_A
role: structural_dark
source_family: composite
runtime_path: <location material library>/...
channels:
  basecolor: ...
  normal: ...
  roughness: ...
  metallic: ...
  ao: ...
physical_scale_mm: 1000
roughness_range: [0.48, 0.72]
weathering_profile: WEATHER_LAFAR_MAINTAINED_WET_A
allowed_for:
  - housings
  - service_panels
  - civic_furniture
forbidden_for:
  - optical_glass
```

## Surface hierarchy

Each approved family defines:

```text
identity
-> macro variation
-> meso defects/manufacturing response
-> microstructure
-> environmental response
-> local/contact wear
```

A generic Noise texture is not a material identity.

## Reuse-first route

```text
required semantic role
-> search resolved design-system families
-> compatible family found: reuse/adapt via allowed masks/parameters
-> no compatible family: author candidate
-> validate candidate
-> promote reusable candidate to design system
```

## Location consistency

Assets from the same location/organization should normally share canonical base families. Variation should come from masks, wear state, wetness and instance parameters, not duplicated base textures.

## Source/runtime split

High-resolution/source textures may live under the source design system. Runtime texture sets remain under the project location material library. The manifest records both.

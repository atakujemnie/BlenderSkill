# Engine Profile Schema

Biblioteka Blendera nie może zgadywać zasad własnego silnika gry.

Dlatego projekt powinien posiadać osobny `ENGINE_PROFILE.md`.

## Coordinate system

- handedness:
- up axis:
- forward axis:
- world unit:
- transform convention:

## Mesh

- supported vertex attributes:
- index size:
- tangent generation:
- max bones per vertex:
- morph targets:
- instancing:
- mesh compression:

## Materials

- shader model:
- metallic/roughness convention:
- packed channels:
- normal convention:
- transparency modes:
- emissive:
- texture formats:
- maximum material slots / recommendations:

## Textures

- supported formats:
- compression:
- mip generation:
- max resolution:
- streaming:
- color space convention:

## Animation

- skeletal:
- node transform:
- frame/time representation:
- interpolation:
- root motion:
- clip naming:

## Scene

- hierarchy:
- static batching:
- instancing:
- LOD representation:
- collision representation:
- occluders:
- navmesh hooks:

## Import format

- glTF/GLB/custom:
- supported extensions:
- unsupported features:
- preprocessing:

## Validation

Agent nie może uznać assetu za game-ready, jeśli ENGINE_PROFILE nie został zastosowany.
W razie braku profilu stosuje tylko neutralne zasady i oznacza runtime status jako `UNVERIFIED`.

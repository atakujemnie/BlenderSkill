# Location Material Language and Library-First Authoring

## Rule

Materials belong first to a location/art-direction system, then to an individual asset.

Before generating textures:
1. resolve `location_id`;
2. resolve/create the persistent location material library;
3. inspect compatible material families and texture sets;
4. reuse or adapt them;
5. create a new family only when existing language cannot represent the target;
6. write new approved material data back into the same location library.

## Material language hierarchy

```text
location identity
-> material family
-> manufacturing/process response
-> macro variation
-> meso defects
-> microstructure
-> environmental response
-> local wear/contact/wetness
```

Noise alone is not a material identity.

## Surface breakup

Avoid globally uniform grunge. Use evidence/semantics:
- seams/recesses: dirt/AO accumulation;
- lower street-facing zones: road grime/splash;
- horizontal surfaces: rain/water response;
- contact zones: darkening/wear;
- exposed corners: restrained edge wear;
- protected centers: cleaner response.

## Periodicity

Reject obvious repeating waves, stripes, checker rhythms or procedural fingerprints unless the manufactured material explicitly requires them. Directional materials require plausible direction and scale, not arbitrary sinusoidal texture.

## Runtime

Location libraries store authoring sources and approved runtime texture sets. Procedural effects must be baked/recreated/removed according to the engine contract.

# Decals and Floating Details

## Cel

Dodawać lokalne informacje wizualne bez niepotrzebnego komplikowania topologii głównego mesha — ale bez udawania, że floating geometry potrafi zastąpić każdą zmianę powierzchni.

## Kandydaci

- oznaczenia,
- logo,
- numery,
- ostrzeżenia,
- ślady serwisowe,
- cienkie panel lines bez istotnego parallax,
- małe techniczne detale,
- warianty assetów,
- drobne śruby/znaczniki przenoszone do atlasu lub normal mapy.

---

# Fundamental limitation

**Floating geometry can add a visible surface. It cannot remove host geometry.**

A floating plate/patch placed near a cylinder does not create a real recess, slot or cavity in that cylinder.

If the intended feature is physically inset, choose one of:
- real cut/recess in the host mesh;
- boolean/rebuilt topology;
- high-to-low normal/height bake;
- material/parallax technique supported by the runtime;
- deliberate flat decal only when parallax is not required.

Do not place a floating feature *inside* an opaque host surface and assume its material/emission makes it visible.

---

# Geometry decals / floating meshes

Dobre, gdy:
- potrzebny jest lokalny detal,
- główny mesh nie powinien być komplikowany,
- feature jest addytywny lub optyczny, nie wymaga usunięcia host surface,
- pipeline/runtime poprawnie obsługuje takie powierzchnie.

Kontroluj:
- z-fighting,
- offset,
- normals,
- bounds,
- curvature conformity,
- LOD behavior,
- visibility/occlusion.

## Visibility proof

For a visible floating feature, object existence is not enough.

Require at least one proof:
- target ROI contains pixels attributable to the feature;
- ray/occlusion test confirms the host does not hide it;
- geometric offset is outside the host along the correct surface normal;
- depth/parallax QA shows the intended relationship.

A material with emission > 0 on a fully occluded surface is still a failed feature.

---

# Recess decision

Before using floating geometry ask:

```text
Does this feature require negative depth into the host?
```

If YES:

```text
visible parallax / silhouette / deep shadow required?
-> real geometry/recess

shallow feature, runtime normal map sufficient?
-> bake/normal strategy

pure graphic or value/color change?
-> decal
```

Do not use floating geometry as a cheap substitute for a reference-critical recess.

---

# Texture decals

Dobre dla:
- oznaczeń,
- wariantów,
- zabrudzeń,
- informacji diegetycznych,
- serial numbers,
- manufacturer branding,
- small non-parallax wear.

## Source fidelity

When an authoritative logo/graphic file exists, use it as source rather than approximating the mark with new geometry or guessed typography.

Record provenance:

```yaml
decal_source:
  feature_id: BRAND_01
  source_file: path/to/logo.png
  transform: stacked_lockup
  alpha_method: source_alpha_or_documented_extraction
  confidence: LOCKED
```

Do not redraw a supplied brand mark unless the task explicitly requests reinterpretation.

---

# Decal atlas

Dla wielu drobnych oznaczeń preferuj atlas zamiast osobnej tekstury per decal, jeśli jest to zgodne z runtime material strategy.

Atlas contract should define:
- source region;
- UV rectangle;
- alpha policy;
- color space;
- padding;
- LOD visibility;
- material slot ownership.

Do not let LOD/export builders delete decal owners as a side effect of rebuilding geometry.

Reusable builder modules must be side-effect free on import.

---

# Curved host surfaces

For a cylindrical/curved host:
- conform the floating surface to the host curvature;
- maintain a controlled proud/offset value;
- avoid a flat card visibly cutting across the cylinder;
- validate from oblique views, not only front ortho.

The offset should be the minimum necessary to avoid z-fighting/occlusion while respecting reference evidence.

Do not increase panel/decal depth merely because flat QA lighting makes it hard to see.
First separate lighting/material readability from geometry.

---

# Nie używaj decal jako maskowania błędu konstrukcyjnego

Jeżeli referencja ma realne wcięcie o widocznym parallax:
- geometria lub displacement/bake może być właściwszy.

Jeżeli floating detail znika:
1. check host occlusion;
2. check normal direction;
3. check offset;
4. check alpha/material;
5. only then modify dimensions if reference evidence supports it.

---

# LOD

Małe decals powinny:
- zanikać w odpowiednim LOD,
- nie pozostawiać migoczących mikropowierzchni,
- być usuwane według Feature Contract / screen-size relevance,
- nie przypadkiem znikać z LOD0/LOD1 podczas przebudowy/exportu.

Branding may remain longer than serial text if it contributes to asset identity at distance.

---

# Game-ready validation

Before completion:
- exported mesh still contains intended decal geometry/material assignment;
- referenced image actually appears in exported/runtime material data;
- no missing texture path;
- alpha mode is compatible with target engine;
- LOD policy is explicit;
- floating features marked as `SURFACE_DETAIL` pass visibility QA.

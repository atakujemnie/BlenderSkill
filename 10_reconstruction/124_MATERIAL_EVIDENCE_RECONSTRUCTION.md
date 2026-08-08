# Material Evidence Reconstruction

## Material identity

Dla każdej strefy ustal:
- material family,
- base color family,
- metallic/dielectric,
- roughness range,
- surface directionality,
- micro-normal,
- transparency,
- emissive.

## Evidence priority

1. material palette / annotation,
2. detail close-up,
3. hero render,
4. orthographic view.

## Material segmentation

Najpierw odtwórz poprawne granice materiałów.
Dopiero potem stroisz parametry shaderów.

## Do not bake lighting into albedo

Highlight, cień i ambient w concept arcie nie są kolorem materiału.

## Material uncertainty

Jeśli materiał opisany jako "dark titanium composite":
nie zakładaj automatycznie czystego metalu.
Nazwa może być językiem designu, nie fizycznym składem.

Zastosuj tekstowe evidence razem z appearance.

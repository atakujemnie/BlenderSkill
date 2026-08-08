# UV, Texel Density and Materials

## UV goals

UV powinno:
- mieć wystarczający padding,
- nie mieć przypadkowych overlapów,
- wykorzystywać symetrię/stacking tylko świadomie,
- zachowywać kierunek materiału,
- uwzględniać lightmap, jeśli projekt jej wymaga.

## Texel density

Ustal projektową wartość bazową.
Różnicuj tylko świadomie dla:
- hero assets,
- wyjątkowo dużych obiektów,
- obiektów widzianych z bardzo bliska.

## Seams

Umieszczaj:
- w naturalnych podziałach konstrukcyjnych,
- w mniej widocznych strefach,
- zgodnie z kierunkiem materiału.

## Material count

Materiał to nie tylko wygląd, ale potencjalny koszt runtime.
Łącz materiały, jeżeli:
- mają ten sam shader model,
- mogą współdzielić atlas/trim,
- nie wymagają osobnego render state.

## PBR baseline

Dla przenośnych assetów trzymaj logiczny podział:
- base color,
- metallic,
- roughness,
- normal,
- occlusion,
- emissive, jeśli potrzebny.

## Procedural nodes

Jeżeli efekt nie jest przenoszony do formatu runtime:
- bake,
- zastąp teksturą,
- albo jawnie pozostaw jako Blender-only authoring data.

## Texture orientation

Szczotkowany metal, włókno, panele i wzory kierunkowe muszą być zgodne z konstrukcją obiektu.

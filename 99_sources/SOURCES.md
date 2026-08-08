# Technical Sources

Biblioteka jest oparta przede wszystkim na oficjalnej dokumentacji.

## Blender 5.1

- Blender 5.1 Release Notes  
  https://developer.blender.org/docs/release_notes/5.1/

- Blender 5.1 Python API release notes  
  https://developer.blender.org/docs/release_notes/5.1/python_api/

- Blender Python API 5.1  
  https://docs.blender.org/api/5.1/

- Blender Python API — Context  
  https://docs.blender.org/api/5.1/bpy.types.Context.html

- Blender Python API — Operators  
  https://docs.blender.org/api/5.1/bpy.ops.html

- Blender Python API — BMesh  
  https://docs.blender.org/api/5.1/bmesh.html

- Blender Python API — BMesh Operators  
  https://docs.blender.org/api/5.1/bmesh.ops.html

- Blender Manual 5.1  
  https://docs.blender.org/manual/en/5.1/

## glTF

- Khronos glTF 2.0 Specification  
  https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html

- Khronos glTF overview  
  https://www.khronos.org/gltf/

- Khronos glTF PBR  
  https://www.khronos.org/gltf/pbr/

## Update policy

Przy zmianie Blender 5.1 -> 5.2+:
1. porównaj Python API release notes,
2. znajdź breaking/compatibility changes,
3. uruchom testy snippetów,
4. dopiero podnieś `target_blender_version` biblioteki.


## Blender 5.1 — production techniques

- Geometry Nodes introduction
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/introduction.html

- Geometry Nodes — Instances
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/instances.html

- Geometry Nodes — Realize Instances
  https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/instances/realize_instances.html

- Blender Camera API
  https://docs.blender.org/api/5.1/bpy.types.Camera.html

- Cycles Baking
  https://docs.blender.org/manual/en/5.1/render/cycles/baking.html

## Source discipline

Moduły biblioteki rozdzielają:
- zachowanie udokumentowane przez Blender/Khronos,
- politykę pipeline projektu,
- heurystyki produkcyjne.

Heurystyki nie powinny być przedstawiane agentowi jako ograniczenia API.

## Reconstruction / precision modeling sources

Official Blender documentation relevant to the reconstruction layer:

- Blender Manual — Empties / image references
  https://docs.blender.org/manual/en/latest/modeling/empties.html

- Blender Manual — Precision transforms
  https://docs.blender.org/manual/en/latest/scene_layout/object/editing/transform/control/precision.html

- Blender Manual — Snapping
  https://docs.blender.org/manual/en/latest/editors/3dview/controls/snapping.html

- Blender Manual — Measure tool
  https://docs.blender.org/manual/en/latest/editors/3dview/toolbar/measure.html

- Blender Manual — Mesh Analysis
  https://docs.blender.org/manual/en/latest/modeling/meshes/mesh_analysis.html

- Blender Manual — Bevel Modifier
  https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html

- Blender Manual — Boolean Modifier
  https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html

- Blender Python API — Object
  https://docs.blender.org/api/current/bpy.types.Object.html

- Blender Python API — Camera
  https://docs.blender.org/api/current/bpy.types.Camera.html

- Blender Python API — Depsgraph
  https://docs.blender.org/api/current/bpy.types.Depsgraph.html

## Source version note

Biblioteka pozostaje targetowana na Blender 5.1.x.
Adresy `latest/current` w sekcji źródeł służą jako dokumentacja referencyjna do mechanizmów,
ale przed automatycznym użyciem konkretnego API agent powinien weryfikować zgodność z wersją 5.1.x.

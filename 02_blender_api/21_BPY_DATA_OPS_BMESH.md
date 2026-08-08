# bpy.data vs bpy.ops vs BMesh

## `bpy.data`

Używaj do:
- wyszukiwania data-blocków,
- tworzenia mesh/material/object,
- odczytu sceny,
- zarządzania kolekcjami,
- jawnej zmiany właściwości.

Przykład:
```python
mesh = bpy.data.meshes.new("PROP_Bench_Mesh")
obj = bpy.data.objects.new("PROP_Bench", mesh)
collection.objects.link(obj)
```

## RNA / object properties

Preferowane do:
- location/rotation/scale,
- visibility,
- parent,
- modifier properties,
- material slots,
- custom properties.

## `bmesh`

Używaj do:
- tworzenia i modyfikowania topologii,
- operacji na vertices/edges/faces,
- proceduralnego modelowania mesh,
- zmian bez zależności od interaktywnego Edit Mode.

Schemat:
```python
bm = bmesh.new()
bm.from_mesh(mesh)
# bmesh.ops...
bm.to_mesh(mesh)
bm.free()
mesh.update()
```

## `bpy.ops`

Używaj, gdy:
- funkcja jest udostępniona głównie jako operator,
- potrzebujesz eksportera/importera,
- korzystasz z narzędzia, którego odtworzenie przez Data API nie ma sensu.

Nie opieraj długiego pipeline na:
```python
bpy.ops.object.select_all(...)
bpy.ops.object.mode_set(...)
bpy.ops.mesh...
```
bez jawnego zarządzania kontekstem.

## Poll

Jeżeli operator posiada wymagania kontekstowe, sprawdź:
```python
if bpy.ops.some.operator.poll():
    bpy.ops.some.operator()
```

Brak `poll()` nie oznacza, że wywołanie jest bezpieczne.

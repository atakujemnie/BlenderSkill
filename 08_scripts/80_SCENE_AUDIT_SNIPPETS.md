# Scene Audit Snippets

Poniższe fragmenty są wzorcami, nie gotowym frameworkiem.

## Version and context

```python
import bpy

print("Blender:", bpy.app.version_string)
print("Scene:", bpy.context.scene.name)
print("Mode:", bpy.context.mode)
print("Active:", bpy.context.view_layer.objects.active.name if bpy.context.view_layer.objects.active else None)
print("Selected:", [o.name for o in bpy.context.selected_objects])
```

## Object inventory

```python
for obj in bpy.context.scene.objects:
    print(
        obj.name,
        obj.type,
        tuple(round(v, 4) for v in obj.dimensions),
        tuple(round(v, 4) for v in obj.scale),
    )
```

## Mesh stats

```python
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        me = obj.data
        print(
            obj.name,
            "verts", len(me.vertices),
            "edges", len(me.edges),
            "polys", len(me.polygons),
            "uv", [uv.name for uv in me.uv_layers],
            "mats", len(obj.material_slots),
        )
```

## Modifier audit

```python
for obj in bpy.context.scene.objects:
    if obj.modifiers:
        print(obj.name)
        for m in obj.modifiers:
            print(" ", m.name, m.type, m.show_viewport, m.show_render)
```

## Asset tag

```python
def find_asset(asset_id):
    return [
        o for o in bpy.data.objects
        if o.get("ai_asset_id") == asset_id
    ]
```

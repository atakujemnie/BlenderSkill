from __future__ import annotations

"""Materialize resolved MATERIAL bindings as real Blender materials."""

from typing import Any, Mapping

EXECUTOR_ID = "BLENDER_DESIGN_RESOURCE_ADAPTER"
EXECUTOR_VERSION = "0.21.0"


def _bpy():
    import bpy

    return bpy


def _rgba(value: Any, default: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    if isinstance(value, str) and value.startswith("#") and len(value) in {7, 9}:
        raw = value[1:]
        alpha = int(raw[6:8], 16) / 255.0 if len(raw) == 8 else 1.0
        return (int(raw[0:2], 16) / 255.0, int(raw[2:4], 16) / 255.0, int(raw[4:6], 16) / 255.0, alpha)
    if isinstance(value, (list, tuple)) and len(value) in {3, 4}:
        vals = [float(item) for item in value]
        if len(vals) == 3:
            vals.append(1.0)
        return tuple(vals)  # type: ignore[return-value]
    return default


def _set_input(node, names: tuple[str, ...], value: Any) -> bool:
    for name in names:
        socket = node.inputs.get(name)
        if socket is not None:
            socket.default_value = value
            return True
    return False


def materialize(binding: Mapping[str, Any]):
    bpy = _bpy()
    resolved = binding.get("resolved")
    if not isinstance(resolved, Mapping):
        raise ValueError("RESOLVED_BINDING_PAYLOAD_REQUIRED")
    resource_type = str(binding.get("resource_type") or resolved.get("type") or resolved.get("kind") or "").upper()
    if resource_type != "MATERIAL":
        raise ValueError("BINDING_IS_NOT_MATERIAL")
    resource_id = str(binding.get("resource_id") or resolved.get("resource_id") or binding.get("binding_id") or "")
    if not resource_id:
        raise ValueError("MATERIAL_RESOURCE_ID_REQUIRED")

    material = bpy.data.materials.get(resource_id)
    if material is None:
        material = bpy.data.materials.new(resource_id)
    material.use_nodes = True
    nodes = material.node_tree.nodes if material.node_tree else None
    bsdf = nodes.get("Principled BSDF") if nodes is not None else None
    if bsdf is None:
        raise ValueError("PRINCIPLED_BSDF_NOT_FOUND")

    base = _rgba(resolved.get("base_color", resolved.get("baseColor")), (0.18, 0.18, 0.18, 1.0))
    _set_input(bsdf, ("Base Color",), base)
    _set_input(bsdf, ("Metallic",), float(resolved.get("metallic", 0.0)))
    _set_input(bsdf, ("Roughness",), float(resolved.get("roughness", 0.5)))
    if resolved.get("emission_color") is not None:
        emission = _rgba(resolved.get("emission_color"), (0.0, 0.0, 0.0, 1.0))
        _set_input(bsdf, ("Emission Color", "Emission"), emission)
        _set_input(bsdf, ("Emission Strength",), float(resolved.get("emission_strength", 1.0)))
    material["blenderskill_resource_id"] = resource_id
    material["blenderskill_resource_version"] = str(binding.get("version") or resolved.get("version") or "")
    return material


def apply_bindings(task_pack: Mapping[str, Any], object_names: list[str]) -> dict[str, Any]:
    bpy = _bpy()
    bindings = task_pack.get("resolved_design_bindings", {})
    if not isinstance(bindings, Mapping):
        return {"status": "FAIL", "executor_id": EXECUTOR_ID, "blockers": [{"reason": "RESOLVED_BINDINGS_MAPPING_REQUIRED"}]}
    applied: list[dict[str, str]] = []
    warnings: list[dict[str, Any]] = []
    for object_name in object_names:
        obj = bpy.data.objects.get(str(object_name))
        if obj is None:
            warnings.append({"reason": "BLENDER_OBJECT_NOT_FOUND", "object": str(object_name)})
            continue
        binding_id = str(obj.get("blenderskill_binding_id") or "")
        if not binding_id:
            continue
        binding = bindings.get(binding_id)
        if not isinstance(binding, Mapping):
            warnings.append({"reason": "OBJECT_BINDING_NOT_RESOLVED", "object": obj.name, "binding_id": binding_id})
            continue
        resource_type = str(binding.get("resource_type") or binding.get("resolved", {}).get("type") or "").upper()
        if resource_type != "MATERIAL":
            continue
        material = materialize(binding)
        if getattr(obj, "data", None) is not None and hasattr(obj.data, "materials"):
            obj.data.materials.clear()
            obj.data.materials.append(material)
            applied.append({"object": obj.name, "binding_id": binding_id, "material": material.name})
    return {
        "status": "PASS",
        "executor_id": EXECUTOR_ID,
        "applied": applied,
        "applied_count": len(applied),
        "warnings": warnings,
        "blockers": [],
    }


__all__ = ["EXECUTOR_ID", "EXECUTOR_VERSION", "apply_bindings", "materialize"]

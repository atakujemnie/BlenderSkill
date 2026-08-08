from __future__ import annotations

"""Reusable candidate executor for deterministic Blender material-channel baking.

Status: CONTRACT_READY until validated by a real runtime benchmark.
The module deliberately does not own asset-specific UV layout, material names,
output paths or Engine Profile packing.
"""

from contextlib import contextmanager
from typing import Iterable, Sequence

import bpy


def contributing_materials(obj) -> list:
    """Return non-null materials referenced by at least one polygon."""
    if obj.type != "MESH":
        raise TypeError(f"{obj.name} is not a MESH object")
    used = {int(poly.material_index) for poly in obj.data.polygons}
    out = []
    for i, mat in enumerate(obj.data.materials):
        if i in used and mat is not None:
            out.append(mat)
    return out


def _ensure_node_material(mat):
    if mat.node_tree is None:
        mat.use_nodes = True
    if mat.node_tree is None:
        raise RuntimeError(f"material has no node tree: {mat.name}")
    return mat.node_tree


@contextmanager
def bind_bake_target(materials: Iterable, image, *, node_label: str = "__BS_BAKE_TARGET__"):
    """Bind one selected+active image node in every contributing material.

    Ordering is intentional:
      create -> deselect all -> select target -> set active -> verify.
    Nodes are removed on exit.
    """
    created = []
    try:
        for mat in materials:
            nt = _ensure_node_material(mat)
            tex = nt.nodes.new("ShaderNodeTexImage")
            tex.label = node_label
            tex.name = node_label
            tex.image = image
            for node in nt.nodes:
                node.select = False
            tex.select = True
            nt.nodes.active = tex
            if nt.nodes.active is not tex or not tex.select or tex.image is not image:
                raise RuntimeError(f"BAKE_TARGET_BINDING_FAIL: {mat.name}")
            created.append((nt, tex))
        yield {
            "status": "PASS",
            "materials_bound": len(created),
            "image": image.name,
        }
    finally:
        for nt, tex in created:
            if tex.id_data is nt:
                nt.nodes.remove(tex)


def _surface_source(nt):
    out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if out is None:
        raise RuntimeError("material has no OUTPUT_MATERIAL")
    links = out.inputs["Surface"].links
    return out, (links[0].from_socket if links else None)


@contextmanager
def override_principled_channel(
    materials: Iterable,
    socket_name: str,
    *,
    scale_socket: str | None = None,
    scale_reference: float = 1.0,
):
    """Temporarily route a Principled input through an Emission shader.

    Scalar inputs are automatically converted to grayscale by Blender.
    For emissive color, ``scale_socket='Emission Strength'`` preserves the
    authored color while normalizing strength by ``scale_reference``.
    All temporary helper nodes are removed on exit.
    """
    if scale_reference <= 0:
        raise ValueError("scale_reference must be > 0")

    saved = []
    try:
        for mat in materials:
            nt = _ensure_node_material(mat)
            out, previous = _surface_source(nt)
            bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            emit = nt.nodes.new("ShaderNodeEmission")
            emit.label = f"__BS_CHANNEL_{socket_name}__"
            helpers = []

            if bsdf is None or socket_name not in bsdf.inputs:
                emit.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
                emit.inputs["Strength"].default_value = 1.0
            else:
                src = bsdf.inputs[socket_name]
                if src.links:
                    nt.links.new(src.links[0].from_socket, emit.inputs["Color"])
                else:
                    value = src.default_value
                    if hasattr(value, "__len__"):
                        rgb = tuple(float(value[i]) for i in range(min(3, len(value))))
                        if len(rgb) == 1:
                            rgb = rgb * 3
                        elif len(rgb) == 2:
                            rgb = (rgb[0], rgb[1], rgb[1])
                        emit.inputs["Color"].default_value = (*rgb[:3], 1.0)
                    else:
                        v = float(value)
                        emit.inputs["Color"].default_value = (v, v, v, 1.0)

                if scale_socket and scale_socket in bsdf.inputs:
                    strength = bsdf.inputs[scale_socket]
                    if strength.links:
                        div = nt.nodes.new("ShaderNodeMath")
                        div.operation = "DIVIDE"
                        div.inputs[1].default_value = scale_reference
                        nt.links.new(strength.links[0].from_socket, div.inputs[0])
                        nt.links.new(div.outputs["Value"], emit.inputs["Strength"])
                        helpers.append(div)
                    else:
                        emit.inputs["Strength"].default_value = (
                            float(strength.default_value) / scale_reference
                        )
                else:
                    emit.inputs["Strength"].default_value = 1.0

            nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
            saved.append((nt, out, previous, emit, helpers))
        yield
    finally:
        for nt, out, previous, emit, helpers in saved:
            if emit.id_data is nt:
                nt.nodes.remove(emit)
            for helper in helpers:
                if helper.id_data is nt:
                    nt.nodes.remove(helper)
            if previous is not None:
                nt.links.new(previous, out.inputs["Surface"])


def select_only(obj):
    """Put one object in the required active+selected state."""
    if obj.name not in bpy.context.view_layer.objects:
        raise RuntimeError(f"object is not in active view layer: {obj.name}")
    for other in tuple(bpy.context.selected_objects):
        other.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if bpy.context.view_layer.objects.active is not obj or not obj.select_get():
        raise RuntimeError(f"BAKE_OBJECT_SELECTION_FAIL: {obj.name}")


def bake_checked(
    obj,
    image,
    bake_type: str,
    *,
    materials: Sequence | None = None,
    operator_kwargs: dict | None = None,
) -> dict:
    """Run one bake pass and fail on Blender's silent ``CANCELLED`` result."""
    mats = list(materials) if materials is not None else contributing_materials(obj)
    if not mats:
        raise RuntimeError("bake source has no contributing materials")

    select_only(obj)
    kwargs = dict(operator_kwargs or {})
    with bind_bake_target(mats, image) as binding:
        result = bpy.ops.object.bake(type=bake_type, **kwargs)

    if "FINISHED" not in result:
        raise RuntimeError(f"BAKE_CANCELLED: type={bake_type} result={sorted(result)}")

    return {
        "status": "PASS",
        "object": obj.name,
        "image": image.name,
        "bake_type": bake_type,
        "materials_bound": binding["materials_bound"],
        "operator_result": sorted(result),
    }


def bake_authored_channel(
    obj,
    image,
    socket_name: str,
    *,
    scale_socket: str | None = None,
    scale_reference: float = 1.0,
    materials: Sequence | None = None,
) -> dict:
    """Bake an authored Principled channel exactly via temporary EMIT routing."""
    mats = list(materials) if materials is not None else contributing_materials(obj)
    with override_principled_channel(
        mats,
        socket_name,
        scale_socket=scale_socket,
        scale_reference=scale_reference,
    ):
        report = bake_checked(obj, image, "EMIT", materials=mats)
    report["source_socket"] = socket_name
    report["scale_socket"] = scale_socket
    report["scale_reference"] = scale_reference
    return report

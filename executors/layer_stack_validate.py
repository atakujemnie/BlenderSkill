from __future__ import annotations

"""Validate visible planar layer order and facing for recessed UI/decal stacks.

Catches geometry that exists but is buried behind an opaque host/recess floor,
or faces away from the required view. Coordinates are supplied in world or a
single declared local axis; no Blender context is required.
"""

from typing import Any, Mapping

EXECUTOR_ID = "LAYER_STACK_VALIDATE"
EXECUTOR_VERSION = "0.1.0"


def _closer(a: float, b: float, viewer_side: str) -> bool:
    return a < b if viewer_side == "NEGATIVE" else a > b


def validate(spec: Mapping[str, Any]) -> dict[str, Any]:
    viewer_side = str(spec.get("viewer_side", "NEGATIVE")).upper()
    if viewer_side not in {"NEGATIVE", "POSITIVE"}:
        raise ValueError("viewer_side must be NEGATIVE or POSITIVE")

    occluder = float(spec["opaque_occluder_plane"])
    layers = list(spec.get("layers", []))
    failures = []
    details = {}

    for layer in layers:
        name = str(layer["name"])
        lo, hi = sorted(float(v) for v in layer["interval"])
        nearest = lo if viewer_side == "NEGATIVE" else hi
        normal = float(layer.get("normal_axis_component", -1.0 if viewer_side == "NEGATIVE" else 1.0))
        required_visible = bool(layer.get("required_visible", True))
        in_front = _closer(nearest, occluder, viewer_side)
        faces_viewer = normal < -0.5 if viewer_side == "NEGATIVE" else normal > 0.5
        status = "PASS" if (not required_visible or (in_front and faces_viewer)) else "FAIL"
        details[name] = {"status": status, "nearest_coordinate": nearest, "in_front_of_occluder": in_front, "faces_viewer": faces_viewer}
        if status == "FAIL":
            failures.append(name)

    order = list(spec.get("front_to_back", []))
    coords = {name: details[name]["nearest_coordinate"] for name in details}
    for a, b in zip(order, order[1:]):
        if a in coords and b in coords and not _closer(coords[a], coords[b], viewer_side):
            failures.append(f"ORDER:{a}>{b}")

    return {"status": "PASS" if not failures else "FAIL", "viewer_side": viewer_side, "opaque_occluder_plane": occluder, "layers": details, "failures": sorted(set(failures))}

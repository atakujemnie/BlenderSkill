from __future__ import annotations

from typing import Any, Iterable, Mapping

EXECUTOR_ID = "DESIGN_SYSTEM_CONFORMANCE_GATE"
EXECUTOR_VERSION = "0.16.0"


def _ids(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        return {str(k) for k in value.keys()}
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        out: set[str] = set()
        for item in value:
            if isinstance(item, Mapping):
                candidate = item.get("id") or item.get("asset_id") or item.get("material_id") or item.get("component_id")
                if candidate:
                    out.add(str(candidate))
            elif item is not None:
                out.add(str(item))
        return out
    return set()


def evaluate(design_system: Mapping[str, Any], usage: Mapping[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    waivers = {str(x) for x in usage.get("waivers", []) or []}

    allowed_materials = _ids(design_system.get("material_families"))
    allowed_components = _ids(design_system.get("component_families"))
    branding = design_system.get("branding") if isinstance(design_system.get("branding"), Mapping) else {}
    allowed_branding = _ids(branding.get("assets"))
    lighting = design_system.get("lighting") if isinstance(design_system.get("lighting"), Mapping) else {}
    allowed_lighting = _ids(lighting.get("families") or lighting)
    weathering = design_system.get("weathering") if isinstance(design_system.get("weathering"), Mapping) else {}
    allowed_weathering = _ids(weathering.get("profiles") or weathering)

    checks = (
        ("material", usage.get("materials"), allowed_materials, "UNREGISTERED_MATERIAL"),
        ("component", usage.get("components"), allowed_components, "UNREGISTERED_COMPONENT"),
        ("branding", usage.get("branding_assets"), allowed_branding, "UNREGISTERED_BRANDING_ASSET"),
        ("lighting", usage.get("lighting_families"), allowed_lighting, "UNREGISTERED_LIGHTING_FAMILY"),
        ("weathering", usage.get("weathering_profiles"), allowed_weathering, "UNREGISTERED_WEATHERING_PROFILE"),
    )

    total_references = 0
    reused_references = 0
    for domain, requested, allowed, reason in checks:
        requested_ids = _ids(requested)
        total_references += len(requested_ids)
        reused_references += len(requested_ids & allowed)
        for item_id in sorted(requested_ids - allowed):
            waiver_key = f"{domain}:{item_id}"
            if waiver_key not in waivers:
                blockers.append({"reason": reason, "domain": domain, "id": item_id})

    for item in usage.get("new_one_off_materials", []) or []:
        item_id = str(item)
        if f"material:{item_id}" not in waivers:
            blockers.append({"reason": "ONE_OFF_MATERIAL_WITHOUT_WAIVER", "id": item_id})

    for item in usage.get("new_one_off_components", []) or []:
        item_id = str(item)
        if f"component:{item_id}" not in waivers:
            blockers.append({"reason": "ONE_OFF_COMPONENT_WITHOUT_WAIVER", "id": item_id})

    required_shape_family = usage.get("shape_family")
    shape_language = design_system.get("shape_language") if isinstance(design_system.get("shape_language"), Mapping) else {}
    if required_shape_family and required_shape_family not in _ids(shape_language.get("families") or shape_language):
        if f"shape:{required_shape_family}" not in waivers:
            blockers.append({"reason": "UNREGISTERED_SHAPE_FAMILY", "id": required_shape_family})

    required_edge_family = usage.get("edge_family")
    edge_language = design_system.get("edge_language") if isinstance(design_system.get("edge_language"), Mapping) else {}
    if required_edge_family and required_edge_family not in _ids(edge_language.get("families") or edge_language):
        if f"edge:{required_edge_family}" not in waivers:
            blockers.append({"reason": "UNREGISTERED_EDGE_FAMILY", "id": required_edge_family})

    ratio = 1.0 if total_references == 0 else reused_references / total_references
    min_ratio = float(usage.get("min_reuse_ratio", 0.0) or 0.0)
    if ratio < min_ratio:
        blockers.append({"reason": "REUSE_RATIO_TOO_LOW", "actual": ratio, "required": min_ratio})

    return {
        "validator_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "status": "PASS" if not blockers else "FAIL",
        "reuse_ratio": ratio,
        "reused_references": reused_references,
        "total_references": total_references,
        "blockers": blockers,
    }

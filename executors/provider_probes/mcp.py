from __future__ import annotations

from typing import Any

from executors.provider_probes._shared import blender_version, module_loaded, provider_version, result


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("mcp", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    loaded = module_loaded(["blender_mcp", "mcp"])
    return result("mcp", "PASS" if loaded else "BLOCKED", capabilities=["INTEGRATION_API"] if loaded else [], cleanup_state="PASS", blockers=[] if loaded else [{"reason": "EXPECTED_API_NOT_LOADED"}], blender_version=blender_version(bpy), provider_version=provider_version(provider))

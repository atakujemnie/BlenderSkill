from __future__ import annotations

from typing import Any

from executors.provider_probes._shared import blender_version, module_loaded, provider_version, result


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("mpfb", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    loaded = module_loaded(["mpfb"])
    state = "PASS" if loaded else "BLOCKED"
    blockers = [] if loaded else [{"reason": "EXPECTED_API_NOT_LOADED"}]
    return result("mpfb", state, capabilities=["CHARACTER_API"] if loaded else [], cleanup_state="PASS", blockers=blockers, blender_version=blender_version(bpy), provider_version=provider_version(provider))

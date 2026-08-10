from __future__ import annotations

import os
from typing import Any

from executors.provider_probes._shared import blender_version, module_loaded, provider_version, result


def run(provider: dict[str, Any]) -> dict[str, Any]:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        return result("meshy", "BLOCKED", blockers=[{"reason": "BLENDER_RUNTIME_REQUIRED", "error": str(exc)}])
    loaded = module_loaded(["meshy"])
    if not loaded:
        return result("meshy", "BLOCKED", cleanup_state="PASS", blockers=[{"reason": "EXPECTED_API_NOT_LOADED"}], blender_version=blender_version(bpy), provider_version=provider_version(provider))
    credential_known = bool(os.environ.get("MESHY_API_KEY"))
    warnings = [] if credential_known else [{"reason": "AUTH_REQUIRED"}]
    return result("meshy", "PASS", capabilities=["PLUGIN_API_SURFACE"], cleanup_state="PASS", warnings=warnings, blender_version=blender_version(bpy), provider_version=provider_version(provider))

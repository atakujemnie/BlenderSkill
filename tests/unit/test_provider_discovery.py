import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

from executors.blender_addon_inventory import collect_runtime_inventory

ROOT = Path(__file__).resolve().parents[2]


def test_discovery_source_cannot_import_provider_modules():
    source = (ROOT / "executors/blender_addon_inventory.py").read_text(encoding="utf-8")
    assert "importlib.import_module" not in source
    assert "__import__(" not in source


def test_discovery_and_probe_execution_are_separate_modules():
    discovery = (ROOT / "executors/blender_addon_inventory.py").read_text(encoding="utf-8")
    assert "provider_probe_runner" not in discovery
    assert "bpy.ops." not in discovery


def test_discovery_passes_when_importlib_import_module_is_forbidden(monkeypatch):
    preferences = SimpleNamespace(
        addons=[SimpleNamespace(module="already_enabled_provider")],
        filepaths=SimpleNamespace(asset_libraries=[]),
    )
    fake_bpy = SimpleNamespace(app=SimpleNamespace(version=(5, 1, 0)), context=SimpleNamespace(preferences=preferences))
    loaded_provider = SimpleNamespace(
        __name__="already_enabled_provider",
        bl_info={"name": "Already Enabled Provider", "version": (1, 2, 3)},
    )
    fake_addon_utils = SimpleNamespace(modules=lambda refresh=False: [loaded_provider])

    monkeypatch.setitem(sys.modules, "bpy", fake_bpy)
    monkeypatch.setitem(sys.modules, "addon_utils", fake_addon_utils)

    def forbidden_import(*args, **kwargs):
        raise AssertionError("provider discovery attempted importlib.import_module")

    monkeypatch.setattr(importlib, "import_module", forbidden_import)
    result = collect_runtime_inventory()
    assert result["status"] == "PASS"
    assert result["addons"][0]["module_name"] == "already_enabled_provider"

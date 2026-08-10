from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_discovery_source_cannot_import_provider_modules():
    source = (ROOT / "executors/blender_addon_inventory.py").read_text(encoding="utf-8")
    assert "importlib.import_module" not in source
    assert "__import__(" not in source


def test_discovery_and_probe_execution_are_separate_modules():
    discovery = (ROOT / "executors/blender_addon_inventory.py").read_text(encoding="utf-8")
    assert "provider_probe_runner" not in discovery
    assert "bpy.ops." not in discovery

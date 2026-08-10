from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TESTS = [
    ROOT / "tests/blender/test_runtime_discovery.py",
    ROOT / "tests/blender/test_geometry_nodes_probe.py",
    ROOT / "tests/blender/test_probe_cleanup.py",
    ROOT / "tests/blender/test_hard_surface_builder.py",
    ROOT / "tests/blender/test_scene_snapshot_adapter.py",
    ROOT / "tests/blender/test_v021_component_execution.py",
    ROOT / "tests/blender/test_v0211_primitive_winding_and_boolean.py",
]


def main() -> None:
    failures = []
    for path in TESTS:
        name = "blenderskill_" + path.stem
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            failures.append((path.name, "LOAD_FAILED"))
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            module.run()
            print(f"PASS {path.name}")
        except Exception as exc:
            failures.append((path.name, repr(exc)))
            print(f"FAIL {path.name}: {exc!r}")
    if failures:
        raise SystemExit(f"Blender runtime suite failed: {failures}")
    print("BlenderSkill v0.21 Blender runtime suite PASS")


if __name__ == "__main__":
    main()

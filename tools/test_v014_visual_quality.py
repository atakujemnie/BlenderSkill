from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    p = ROOT / "executors" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


library = load("location_material_library")
quality = load("provider_quality")
composition = load("planting_composition_quality")
budget = load("context_budget_gate")
provider = load("procedural_provider")

with tempfile.TemporaryDirectory() as td:
    r = library.resolve({"location_id": "Lafar_City", "game_asset_root": td, "create_if_missing": True})
    assert r["status"] == "READY" and r["created"] and Path(r["manifest_path"]).exists()
    r2 = library.resolve({"location_id": "Lafar_City", "game_asset_root": td})
    assert r2["status"] == "READY" and r2["reused_existing"] and r2["path"] == r["path"]

q = quality.select([
    {"provider_id": "builtin", "runtime_status": "PASS", "quality_tier": "C", "quality_score": 0.9},
    {"provider_id": "licensed_pack", "runtime_status": "PASS", "quality_tier": "A", "quality_score": 0.7},
], "HERO")
assert q["status"] == "PASS" and q["selected_provider_id"] == "licensed_pack"
assert quality.select([{"provider_id": "builtin", "runtime_status": "PASS", "quality_tier": "C"}], "HERO")["status"] == "BLOCKED"

spec = {
    "exposed_soil_range": [0.08, 0.22],
    "required_height_layers": ["LOW", "MID", "TALL"],
    "min_major_masses": 2,
    "max_major_masses": 5,
    "max_periodicity_score": 0.30,
    "max_visible_clone_score": 0.30,
    "min_vegetation_coverage_ratio": 0.72,
}
good = composition.evaluate(spec, {
    "exposed_soil_ratio": 0.15,
    "height_layers_present": ["LOW", "MID", "TALL"],
    "major_mass_count": 3,
    "placement_periodicity_score": 0.12,
    "visible_clone_score": 0.18,
    "vegetation_coverage_ratio": 0.81,
})
assert good["status"] == "PASS"
bad = composition.evaluate(spec, {
    "exposed_soil_ratio": 0.41,
    "height_layers_present": ["MID"],
    "major_mass_count": 8,
    "placement_periodicity_score": 0.81,
    "visible_clone_score": 0.72,
    "vegetation_coverage_ratio": 0.40,
})
assert bad["status"] == "FAIL" and len(bad["blockers"]) >= 4

assert budget.evaluate({"context_tokens": 24000, "asset_specific_generated_lines": 300})["status"] == "PASS"
assert budget.evaluate({"context_tokens": 80000, "asset_specific_generated_lines": 2400, "reusable_executor_misses": 4})["status"] == "FAIL"

prov = {
    "provider_id": "builtin_geometry_nodes",
    "provider_version": "5.1",
    "execution_type": "GEOMETRY_NODES",
    "blender_min": "5.1.0",
    "blender_max": "5.1.99",
    "supports_seed": True,
    "license": "BLENDER_RUNTIME",
    "probe": {"status": "PASS", "capabilities": []},
}
pr = provider.evaluate(prov, {"blender_version": "5.1.0", "background": False})
assert pr["status"] == "PASS" and pr["validator_id"] == "PROCEDURAL_GENERATOR_PROVIDER"

print("v0.14 visual quality/material library/context regression tests: PASS")

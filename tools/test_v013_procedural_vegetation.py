from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    p = ROOT / "executors" / f"{name}.py"; spec = importlib.util.spec_from_file_location(name, p); mod = importlib.util.module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(mod); return mod


provider = load("procedural_provider"); catalog = load("procedural_provider_catalog"); codegen = load("nodegraph_codegen_gate"); botanical = load("botanical_grammar"); scatter = load("vegetation_scatter"); composition = load("planter_composition"); runtime = load("vegetation_runtime_prep"); generation = load("vegetation_generation_gate")

# v0.17 correction: NodeToPython remains a historical codegen/reference pattern,
# not a required executable BlenderSkill 5.1 runtime provider.
n2p = catalog.get("nodetopython"); r = provider.evaluate(n2p, {"blender_version": "5.1.0", "background": False}); assert r["status"] == "SOURCE_ONLY" and not r["can_execute"]
grove = catalog.get("the_grove"); grove["probe"] = {"status": "PASS", "capabilities": []}; r = provider.evaluate(grove, {"blender_version": "5.1.0", "background": False}); assert r["status"] == "BLOCKED" and any(b["reason"] == "BLENDER_VERSION_TOO_NEW" for b in r["blockers"])
procfunc = catalog.get("procfunc"); r = provider.evaluate(procfunc, {"blender_version": "5.1.0"}); assert r["status"] == "BLOCKED" and not r["can_execute"]

plant = {"form_class": "SHRUB", "height_m": 1.6, "crown_radius_m": 0.75, "stem_radius_m": 0.025, "branching_orders": 4, "phyllotaxis_deg": 137.5, "internode_length_m": 0.08, "apical_dominance": 0.45, "crown_density": 0.72, "tropism": [0, 0, 1], "age_class": "MATURE", "season": "EVERGREEN", "seed": 347013}
bg = botanical.evaluate(plant); assert bg["status"] == "PASS"; bad = dict(plant); bad["seed"] = None; bad["phyllotaxis_deg"] = 420; assert botanical.evaluate(bad)["status"] == "FAIL"

scatter_spec = {"seed": 77, "target_count": 3, "min_required": 3, "min_spacing_m": 0.8, "max_slope_deg": 25, "min_biome_weight": 0.2, "candidates": [{"id": "a", "x": 0, "y": 0, "z": 0, "slope_deg": 0, "biome_weight": 1}, {"id": "b", "x": 1, "y": 0, "z": 0, "slope_deg": 0, "biome_weight": 0.8}, {"id": "c", "x": 2, "y": 0, "z": 0, "slope_deg": 10, "biome_weight": 0.7}, {"id": "d", "x": 3, "y": 0, "z": 0, "slope_deg": 40, "biome_weight": 1}, {"id": "e", "x": 4, "y": 0, "z": 0, "slope_deg": 0, "biome_weight": 1, "excluded": True}, {"id": "f", "x": 5, "y": 0, "z": 0, "slope_deg": 0, "biome_weight": 0.9}]}
s1 = scatter.plan(scatter_spec); s2 = scatter.plan(scatter_spec); assert s1["status"] == "PASS" and s1["placement_signature"] == s2["placement_signature"] and [x["id"] for x in s1["selected"]] == [x["id"] for x in s2["selected"]] and all(x["id"] not in {"d", "e"} for x in s1["selected"])

good_comp = composition.evaluate({"container": {"shape": "RECT", "inner_half_x_m": 0.9, "inner_half_y_m": 0.35, "soil_depth_m": 0.45}, "wall_clearance_m": 0.04, "min_stem_spacing_m": 0.25, "plants": [{"id": "p1", "x": -0.35, "y": 0, "rootball_radius_m": 0.13, "rootball_depth_m": 0.22, "stem_radius_m": 0.02}, {"id": "p2", "x": 0.35, "y": 0, "rootball_radius_m": 0.13, "rootball_depth_m": 0.22, "stem_radius_m": 0.02}]}); assert good_comp["status"] == "PASS"
bad_comp = composition.evaluate({"container": {"shape": "CIRCLE", "inner_radius_m": 0.3, "soil_depth_m": 0.18}, "wall_clearance_m": 0.03, "plants": [{"id": "bad", "x": 0.25, "y": 0, "rootball_radius_m": 0.12, "rootball_depth_m": 0.30, "stem_radius_m": 0.02}]}); assert bad_comp["status"] == "FAIL"

rp = runtime.plan({"usage_class": "MID", "seed": 347013, "generator_provenance_id": "gen:lafar:planter:01", "generated_triangle_count": 180000, "leaf_count": 8000, "material_slots": 2, "form_class": "SHRUB", "semantic_parts": ["stem", "branches", "leaves"]}); assert rp["status"] == "PASS" and rp["lod_targets"]["LOD0"] <= 30000 and rp["leaf_cards_recommended"] is True and rp["impostor_recommended"] is True

cg = codegen.evaluate({"source_node_tree_id": "GN_LAFAR_GROUND_COVER", "source_node_tree_hash": "abc", "compiler_provider_id": "nodetopython", "compiler_provider_version": "4.1.1", "blender_version": "5.1.0", "generated_script_hash": "def", "provenance_id": "codegen:001", "compiler_probe_status": "PASS", "roundtrip_probe_status": "PASS", "requires_runtime_compiler_dependency": False}); assert cg["status"] == "PASS"
assert codegen.evaluate({"source_node_tree_id": "GN", "source_node_tree_hash": "abc", "compiler_provider_id": "nodetopython", "compiler_provider_version": "4.1.1", "blender_version": "5.1.0", "generated_script_hash": "def", "provenance_id": "x", "compiler_probe_status": "PASS", "roundtrip_probe_status": "FAIL"})["status"] == "FAIL"

provider_pass = {"status": "PASS", "validator_id": "PROCEDURAL_GENERATOR_PROVIDER"}; generation_report = {"provider": provider_pass, "botanical_grammar": bg, "generation_metadata": {"generator": "builtin_geometry_nodes", "generator_version": "5.1", "seed": 347013, "parameters_hash": "params", "geometry_signature": "geoA", "semantic_parts": ["stem", "branches", "leaves"], "generated_triangle_count": 180000}, "reproduction_probe": {"status": "PASS", "first_signature": "geoA", "second_signature": "geoA"}, "provenance_id": "vegetation:lafar:01"}; assert generation.evaluate(generation_report)["status"] == "PASS"; generation_report["reproduction_probe"]["second_signature"] = "geoB"; assert generation.evaluate(generation_report)["status"] == "FAIL"

print("v0.13 procedural vegetation regression tests: PASS")

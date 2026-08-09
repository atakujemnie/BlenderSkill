from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from executors.expected_provider_gate import evaluate as expected_gate
from executors.installed_provider_inventory import build_inventory, provider_ids
from executors.provider_selection_report import build_report


def fixture() -> dict:
    return {
        "blender_version": "5.1.0",
        "addons": [
            {"module_name": "bl_ext.user_default.mpfb", "display_name": "MPFB (MakeHuman for Blender)", "version": "2.0.15", "enabled": True},
            {"module_name": "bl_ext.blender_org.ant_landscape", "display_name": "A.N.T.Landscape", "version": "0.2.0", "enabled": False},
            {"module_name": "bl_ext.user_default.geo_nodes_guide", "display_name": "Geo Nodes Guide", "version": "0.1.0", "enabled": False},
            {"module_name": "bl_ext.blender_org.ivygen", "display_name": "IvyGen", "version": "0.1.5", "enabled": False},
            {"module_name": "mcp", "display_name": "MCP", "version": "1.0.0", "enabled": True},
            {"module_name": "bl_ext.user_default.meshy", "display_name": "Meshy official plugin", "version": "0.6.0", "enabled": False},
            {"module_name": "bl_ext.blender_org.sapling_tree_gen", "display_name": "Sapling Tree Gen", "version": "0.3.7", "enabled": False},
            {"module_name": "sverchok", "display_name": "Sverchok", "version": "1.4.0", "enabled": False},
        ],
        "asset_libraries": [],
    }


def expected_list() -> list[dict]:
    return [
        {"provider_id": "mpfb", "version": "2.0.15"},
        {"provider_id": "ant_landscape", "version": "0.2.0"},
        {"provider_id": "geo_nodes_guide", "version": "0.1.0"},
        {"provider_id": "ivygen", "version": "0.1.5"},
        {"provider_id": "mcp", "version": "1.0.0"},
        {"provider_id": "meshy", "version": "0.6.0"},
        {"provider_id": "sapling_tree_gen", "version": "0.3.7"},
        {"provider_id": "sverchok", "version": "1.4.0"},
    ]


def main() -> None:
    inventory = build_inventory(fixture())
    ids = provider_ids(inventory)
    required = {
        "mpfb", "ant_landscape", "geo_nodes_guide", "ivygen", "mcp",
        "meshy", "sapling_tree_gen", "sverchok", "builtin_geometry_nodes",
    }
    assert required <= ids, (required - ids, inventory)
    assert inventory["summary"]["ready_asset_sources_count"] == 0, inventory
    assert inventory["summary"]["procedural_generators_count"] >= 5, inventory

    gate = expected_gate(expected_list(), inventory, require_exact_version=True)
    assert gate["status"] == "PASS", gate

    eligibility = {
        "sverchok": {"runtime_probe_status": "PASS"},
        "builtin_geometry_nodes": {"runtime_probe_status": "PASS"},
    }
    report = build_report(
        inventory,
        requested_domains=["GRASS"],
        selected_provider_id="builtin_geometry_nodes",
        eligibility=eligibility,
    )
    assert report["status"] == "PASS", report
    by_id = {x["provider_id"]: x for x in report["candidates"]}
    assert by_id["sapling_tree_gen"]["decision"] == "REJECTED", by_id["sapling_tree_gen"]
    assert by_id["ivygen"]["decision"] == "REJECTED", by_id["ivygen"]
    assert "sverchok" in by_id, report
    assert "builtin_geometry_nodes" in by_id, report
    assert report["ready_asset_sources"] == [], report
    assert "sapling_tree_gen" in report["procedural_generators"], report

    # Negative control: declared Sapling must not silently disappear.
    broken_raw = fixture()
    broken_raw["addons"] = [x for x in broken_raw["addons"] if "sapling" not in x["display_name"].lower()]
    broken_inventory = build_inventory(broken_raw)
    broken_gate = expected_gate(expected_list(), broken_inventory)
    assert broken_gate["status"] == "FAIL", broken_gate
    assert any(x.get("reason") == "DISCOVERY_MISMATCH" and x.get("provider_id") == "sapling_tree_gen" for x in broken_gate["blockers"]), broken_gate

    # Negative control: wrong-domain provider cannot be selected for GRASS.
    bad_report = build_report(
        inventory,
        requested_domains=["GRASS"],
        selected_provider_id="sapling_tree_gen",
        eligibility=eligibility,
    )
    assert bad_report["status"] == "BLOCKED", bad_report

    print("v0.17 installed provider discovery regression tests: PASS")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from executors.design_system_conformance import evaluate as evaluate_conformance
from executors.design_system_inheritance import resolve as resolve_inheritance
from executors.design_system_manifest import evaluate as evaluate_manifest
from executors.design_system_resolver import resolve as resolve_design_system
from executors.design_system_resource_registry import promote


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "RPG"
        game_root = project / "Assets" / "GameAssets"
        game_root.mkdir(parents=True)

        spec = {
            "location_id": "lafar",
            "project_root": str(project),
            "game_asset_root": str(game_root),
            "organization_id": "astera_civic_systems",
            "create_if_missing": True,
        }
        first = resolve_design_system(spec)
        assert first["status"] == "BOOTSTRAPPED", first
        ds_root = Path(first["path"])
        assert ds_root == project / "Blender" / "DesignSystems" / "lafar"
        assert Path(first["markdown_path"]).is_file()
        assert Path(first["manifest_path"]).is_file()
        assert Path(first["organization_path"]).is_dir()

        second = resolve_design_system(dict(spec, create_if_missing=False))
        assert second["status"] == "READY", second
        assert second["path"] == first["path"]

        manifest_path = Path(first["manifest_path"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert evaluate_manifest(manifest, final=True)["status"] == "FAIL"

        manifest.update({
            "status": "READY",
            "design_tokens": {"palette": {"accent_blue": "#25AFFF"}},
            "shape_language": {"families": {"ASTERA_CIVIC_HARDSURFACE": {}}},
            "edge_language": {"families": {"EDGE_ASTERA_CIVIC_OUTER_A": {"radius_mm": [12, 24]}}},
            "detail_language": {"panel_gap_mm": [2, 5]},
            "material_families": {
                "MAT_ASTERA_GRAPHITE_COMPOSITE_A": {"role": "structural_dark"},
                "MAT_ASTERA_BRUSHED_ALUMINIUM_A": {"role": "trim_metal"},
            },
            "branding": {
                "applicable": True,
                "assets": {
                    "BRAND_ASTERA_PRIMARY": {"role": "PRIMARY_LOGO"},
                    "BRAND_ASTERA_SYMBOL": {"role": "SYMBOL"},
                },
            },
            "component_families": {
                "CMP_ASTERA_UTILITY_PANEL_A": {"role": "civic_utility_panel"},
            },
            "lighting": {
                "families": {
                    "LIGHT_ASTERA_CIVIC_BLUE_A": {"role": ["status", "orientation"]},
                },
            },
            "weathering": {
                "profiles": {
                    "WEATHER_LAFAR_MAINTAINED_WET_A": {"maintenance": "HIGH"},
                },
            },
        })
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        assert evaluate_manifest(manifest, final=True)["status"] == "PASS"

        layers = [
            {
                "id": "LAFAR",
                "scope": "LOCATION",
                "values": {
                    "weathering": {"profile": "WEATHER_LAFAR_MAINTAINED_WET_A"},
                    "lighting": {"accent_color": "#25AFFF"},
                },
                "locked_paths": ["lighting.accent_color"],
            },
            {
                "id": "ASTERA",
                "scope": "ORGANIZATION",
                "values": {
                    "materials": {"structural_dark": "MAT_ASTERA_GRAPHITE_COMPOSITE_A"},
                    "lighting": {"accent_color": "#25AFFF"},
                },
            },
            {
                "id": "STREET_FURNITURE",
                "scope": "FAMILY",
                "values": {"edge_family": "EDGE_ASTERA_CIVIC_OUTER_A"},
            },
        ]
        inherited = resolve_inheritance(layers)
        assert inherited["status"] == "PASS", inherited
        assert inherited["resolved"]["materials"]["structural_dark"] == "MAT_ASTERA_GRAPHITE_COMPOSITE_A"
        assert inherited["provenance"]["edge_family"] == "STREET_FURNITURE"

        bad_layers = layers + [{
            "id": "BAD_ASSET",
            "scope": "ASSET",
            "values": {"lighting": {"accent_color": "#FF0000"}},
        }]
        bad_inheritance = resolve_inheritance(bad_layers)
        assert bad_inheritance["status"] == "FAIL"
        assert any(b["reason"] == "LOCKED_TOKEN_OVERRIDE" for b in bad_inheritance["blockers"])

        logo1 = Path(tmp) / "logo1.svg"
        logo2 = Path(tmp) / "logo2.svg"
        logo_bad = Path(tmp) / "logo_bad.svg"
        logo1.write_text("<svg>ASTERA</svg>", encoding="utf-8")
        logo2.write_text("<svg>ASTERA</svg>", encoding="utf-8")
        logo_bad.write_text("<svg>DIFFERENT</svg>", encoding="utf-8")

        promoted = promote({
            "design_system_path": str(ds_root),
            "source_path": str(logo1),
            "resource_id": "BRAND_ASTERA_PRIMARY",
            "category": "BRANDING",
            "provenance": {"source": "canonical_logo"},
        })
        assert promoted["status"] == "PROMOTED", promoted
        reused = promote({
            "design_system_path": str(ds_root),
            "source_path": str(logo2),
            "resource_id": "BRAND_ASTERA_DUPLICATE_NAME",
            "category": "BRANDING",
        })
        assert reused["status"] == "REUSED", reused
        assert reused["resource_id"] == "BRAND_ASTERA_PRIMARY"
        conflict = promote({
            "design_system_path": str(ds_root),
            "source_path": str(logo_bad),
            "resource_id": "BRAND_ASTERA_PRIMARY",
            "category": "BRANDING",
        })
        assert conflict["status"] == "FAIL", conflict

        good_usage = {
            "materials": ["MAT_ASTERA_GRAPHITE_COMPOSITE_A", "MAT_ASTERA_BRUSHED_ALUMINIUM_A"],
            "components": ["CMP_ASTERA_UTILITY_PANEL_A"],
            "branding_assets": ["BRAND_ASTERA_PRIMARY"],
            "lighting_families": ["LIGHT_ASTERA_CIVIC_BLUE_A"],
            "weathering_profiles": ["WEATHER_LAFAR_MAINTAINED_WET_A"],
            "shape_family": "ASTERA_CIVIC_HARDSURFACE",
            "edge_family": "EDGE_ASTERA_CIVIC_OUTER_A",
            "min_reuse_ratio": 1.0,
        }
        conform = evaluate_conformance(manifest, good_usage)
        assert conform["status"] == "PASS", conform
        assert conform["reuse_ratio"] == 1.0

        bad_usage = dict(good_usage, materials=["MAT_RANDOM_CLEAN_PLASTIC"])
        nonconform = evaluate_conformance(manifest, bad_usage)
        assert nonconform["status"] == "FAIL"
        assert any(b["reason"] == "UNREGISTERED_MATERIAL" for b in nonconform["blockers"])

        waived = dict(bad_usage, waivers=["material:MAT_RANDOM_CLEAN_PLASTIC"], min_reuse_ratio=0.0)
        assert evaluate_conformance(manifest, waived)["status"] == "PASS"

    print("v0.16 location design system regression tests: PASS")


if __name__ == "__main__":
    main()

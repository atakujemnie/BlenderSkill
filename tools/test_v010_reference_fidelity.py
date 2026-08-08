from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    if spec is None or spec.loader is None:
        raise RuntimeError(rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ref_proof(kind: str, pid: str, *, validator: str = "APPEARANCE_REFERENCE_VALIDATE", reg: bool = False) -> dict:
    out = {
        "status": "PASS",
        "evidence_kind": kind,
        "validator_id": validator,
        "provenance_id": pid,
        "source_reference_id": "bench_ref_v1",
    }
    if reg:
        out["registration_id"] = f"{pid}_reg"
    return out


def main() -> None:
    appearance = load("appearance_gate", "executors/appearance_fidelity_gate.py")
    node_gate = load("node_gate_v010", "executors/reconstruction_node_gate.py")
    fidelity = load("fidelity_gate_v010", "executors/fidelity_gate.py")

    app_report = {
        "target_fidelity": "L5",
        "strict_evidence": True,
        "part_boundaries": ref_proof("PART_BOUNDARY_VALIDATION", "pbg", reg=True),
        "trim_paths": ref_proof("TRIM_PATH_VALIDATION", "trim", reg=True),
        "junctions": ref_proof("JUNCTION_VALIDATION", "junction", reg=True),
        "edge_families": ref_proof("EDGE_FAMILY_VALIDATION", "edges"),
        "material_regions": ref_proof("MATERIAL_APPEARANCE_VALIDATION", "materials"),
        "emissive_regions": ref_proof("EMISSIVE_REGION_VALIDATION", "emissive"),
        "branding": ref_proof("BRANDING_VALIDATION", "branding"),
        "final_views": ref_proof("REGISTERED_OVERLAY", "final_views", validator="REFERENCE_OVERLAY_VALIDATE", reg=True),
        "detail_coverage": {
            **ref_proof("DETAIL_COVERAGE", "coverage"),
            "must_missing": 0,
            "weighted_coverage": 1.0,
        },
        "reference_fidelity_score": 9.1,
        "benchmark_score_threshold": 8.5,
    }
    passed = appearance.evaluate(app_report)
    assert passed["status"] == "PASS", passed
    assert passed["can_advance_to_recon_fidelity"] is True

    missing_source = dict(app_report)
    missing_source["trim_paths"] = dict(app_report["trim_paths"])
    missing_source["trim_paths"].pop("source_reference_id")
    blocked = appearance.evaluate(missing_source)
    assert blocked["status"] == "FAIL", blocked
    assert any(b["reason"] == "missing_source_reference" for b in blocked["blockers"]), blocked

    missing_reg = dict(app_report)
    missing_reg["part_boundaries"] = dict(app_report["part_boundaries"])
    missing_reg["part_boundaries"].pop("registration_id")
    blocked = appearance.evaluate(missing_reg)
    assert any(b["reason"] == "missing_registration_id" for b in blocked["blockers"]), blocked

    low_score = dict(app_report)
    low_score["reference_fidelity_score"] = 6.0
    blocked = appearance.evaluate(low_score)
    assert any(b["owner"] == "benchmark_score" for b in blocked["blockers"]), blocked

    node_report = {
        "node_id": "SIDE_MODULE_R",
        "strict_evidence": True,
        "parent_status": "PASS",
        "required_views": ["SIDE"],
        "isolation": {
            "status": "PASS",
            "evidence_kind": "QA_SCENE_ISOLATION",
            "validator_id": "QA_SCENE_ISOLATE",
            "provenance_id": "iso",
        },
        "numeric_constraints": {
            "status": "PASS",
            "evidence_kind": "NUMERIC_MEASUREMENT",
            "validator_id": "REFERENCE_MEASURE",
            "provenance_id": "num",
        },
        "regression": {
            "status": "PASS",
            "evidence_kind": "REGRESSION_DIFF",
            "validator_id": "REFERENCE_OVERLAY_VALIDATE",
            "provenance_id": "reg",
        },
        "views": {
            "SIDE": {
                "status": "PASS",
                "evidence_kind": "REGISTERED_OVERLAY",
                "validator_id": "REFERENCE_OVERLAY_VALIDATE",
                "provenance_id": "side",
                "source_reference_id": "side_ref",
                "registration_id": "side_reg",
            }
        },
    }
    assert node_gate.evaluate(node_report)["status"] == "ACCEPTED"
    local_gate = dict(node_report)
    local_gate["views"] = {"SIDE": dict(node_report["views"]["SIDE"], validator_id="LOCAL_GATE")}
    rejected = node_gate.evaluate(local_gate)
    assert rejected["status"] == "UNVERIFIED", rejected
    assert any(b["reason"] == "CANONICAL_REFERENCE_VIEW_VALIDATOR_REQUIRED" for b in rejected["blockers"]), rejected

    def fidelity_ref(kind: str, pid: str, validator: str, *, reg: bool = False) -> dict:
        out = {
            "status": "PASS",
            "evidence_kind": kind,
            "validator_id": validator,
            "provenance_id": pid,
            "source_reference_id": "bench_ref_v1",
        }
        if reg:
            out["registration_id"] = f"{pid}_reg"
        return out

    fidelity_report = {
        "target_fidelity": "L4",
        "achieved_fidelity": "L4",
        "strict_evidence": True,
        "hard_dimensions": fidelity_ref("NUMERIC_MEASUREMENT", "dims", "REFERENCE_MEASURE"),
        "landmarks_d0_d1": fidelity_ref("LANDMARK_PROJECTION", "landmarks", "REFERENCE_OVERLAY_VALIDATE", reg=True),
        "material_segmentation": fidelity_ref("MATERIAL_SEGMENTATION", "matseg", "APPEARANCE_REFERENCE_VALIDATE"),
        "canonical_views": {
            view: fidelity_ref("REGISTERED_OVERLAY", view.lower(), "REFERENCE_OVERLAY_VALIDATE", reg=True)
            for view in ("FRONT", "SIDE", "TOP", "REAR", "BOTTOM")
        },
        "must_features": [
            fidelity_ref("FEATURE_ROI", "trim_feature", "APPEARANCE_REFERENCE_VALIDATE", reg=True) | {"id": "SIDE_TRIM_R"}
        ],
    }
    no_appearance = fidelity.evaluate(fidelity_report)
    assert no_appearance["status"] == "FAIL", no_appearance
    assert any(b["owner"] == "appearance_fidelity" for b in no_appearance["blockers"]), no_appearance

    fidelity_report["appearance_fidelity"] = {
        "status": "PASS",
        "evidence_kind": "APPEARANCE_FIDELITY_GATE",
        "validator_id": "APPEARANCE_FIDELITY_GATE",
        "provenance_id": "appearance_gate_001",
    }
    full = fidelity.evaluate(fidelity_report)
    assert full["status"] == "PASS", full
    assert full["can_advance_to_runtime"] is True

    print("v0.10 reference appearance/fidelity smoke tests: PASS")


if __name__ == "__main__":
    main()

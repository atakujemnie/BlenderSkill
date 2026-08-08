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


def main() -> None:
    sg = load("shape_graph", "executors/shape_graph.py")
    ng = load("node_gate", "executors/reconstruction_node_gate.py")
    loft = load("section_loft", "executors/section_loft.py")
    completion = load("completion_gate", "executors/completion_gate.py")

    graph = {
        "root": "ASSET",
        "graph_revision": "sg_test",
        "nodes": {
            "ASSET": {"level": "G0", "rdl": "RDL0", "state": "ACCEPTED", "importance": "MUST", "validation": {"bounds": True}},
            "BODY": {"level": "G1", "rdl": "RDL1", "state": "CONSTRAINED", "parent": "ASSET", "shape_class": "EXTRUDED_PROFILE", "importance": "MUST", "validation": {"FRONT": True}},
            "DETAIL": {"level": "G2", "rdl": "RDL2", "state": "CONSTRAINED", "parent": "BODY", "shape_class": "BOOLEAN_RECESS", "importance": "MUST", "validation": {"FRONT": True}},
        },
    }
    result = sg.validate(graph)
    assert result["status"] == "PASS", result
    assert result["ready_nodes"] == ["BODY"], result
    assert result["blocked_nodes"][0]["node"] == "DETAIL", result
    assert sg.evaluate_stage_barrier(graph, "RDL1")["status"] == "FAIL"
    graph["nodes"]["BODY"]["state"] = "ACCEPTED"
    assert sg.evaluate_stage_barrier(graph, "RDL1")["status"] == "PASS"

    def proof(kind: str, pid: str) -> dict:
        return {"status": "PASS", "evidence_kind": kind, "provenance_id": pid}

    node_report = {
        "node_id": "BODY",
        "parent_status": "PASS",
        "strict_evidence": True,
        "required_views": ["FRONT", "SIDE"],
        "isolation": proof("QA_SCENE_ISOLATION", "iso"),
        "numeric_constraints": proof("NUMERIC_MEASUREMENT", "num"),
        "regression": proof("REGRESSION_DIFF", "reg"),
        "views": {
            "FRONT": proof("REGISTERED_OVERLAY", "front"),
            "SIDE": proof("REGISTERED_OVERLAY", "side"),
        },
    }
    assert ng.evaluate(node_report)["status"] == "ACCEPTED"
    node_report["views"]["SIDE"] = {"status": "PASS"}
    assert ng.evaluate(node_report)["status"] == "UNVERIFIED"

    loft_spec = {
        "axis": "Z",
        "sections": [
            {"id": "BOTTOM", "axis_pos": 0.0, "profile_mode": "CHAMFERED_RECTANGLE", "width": 0.60, "depth": 0.30, "chamfer": 0.02},
            {"id": "MID", "axis_pos": 0.10, "profile_mode": "CHAMFERED_RECTANGLE", "width": 0.56, "depth": 0.27, "chamfer": 0.02},
            {"id": "TOP", "axis_pos": 0.18, "profile_mode": "CHAMFERED_RECTANGLE", "width": 0.50, "depth": 0.23, "chamfer": 0.02},
        ],
    }
    loft_report = loft.compact_report(loft_spec)
    assert loft_report["status"] == "PASS"
    assert loft_report["section_count"] == 3
    assert loft_report["sample_count"] == 8
    assert loft_report["vertex_count"] == 24

    checks = {
        "shape_graph_validation": "PASS",
        "rdl_stage_barriers": "PASS",
        "hard_dimensions": "PASS",
        "canonical_silhouettes": "PASS",
        "must_features": "PASS",
        "multi_view_gate": "PASS",
        "reconstruction_fidelity_gate": proof("RECON_FIDELITY_GATE", "recon"),
    }
    done = completion.evaluate_completion(checks, target_level="RECONSTRUCTION_COMPLETE")
    assert done["status"] == "PASS", done
    checks.pop("rdl_stage_barriers")
    blocked = completion.evaluate_completion(checks, target_level="RECONSTRUCTION_COMPLETE")
    assert blocked["status"] == "FAIL", blocked

    print("v0.9 Shape Graph smoke tests: PASS")


if __name__ == "__main__":
    main()

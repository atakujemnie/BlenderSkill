from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path: str):
    p = ROOT / path
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

sg = load("executors/shape_graph.py")
auth = load("executors/execution_authorization_gate.py")
store = load("executors/node_state_store.py")
conflict = load("executors/reference_conflict_resolver.py")
coverage = load("executors/appearance_owner_coverage.py")
pin = load("executors/runtime_source_pin.py")
node_gate = load("executors/reconstruction_node_gate.py")

def base_graph(root_state="CONSTRAINED", child_state="DECLARED"):
    return {"graph_revision": "sg_test_011", "root": "ROOT", "nodes": {
        "ROOT": {"level": "G0", "rdl": "RDL0", "state": root_state, "shape_class": "ENVELOPE", "validation": {"FRONT": {"controls": ["height"]}}},
        "BODY": {"level": "G1", "rdl": "RDL1", "state": child_state, "parent": "ROOT", "shape_class": "EXTRUDED_PROFILE", "validation": {"FRONT": {"controls": ["width"]}}},
    }}

g = base_graph(); r = sg.validate(g)
assert r["status"] == "PASS" and r["eligible_nodes"] == ["ROOT"] and r["ready_nodes"] == []
issued = auth.issue_authorization(g, "ROOT", node_revision="root_001")
assert issued["status"] == "PASS"
assert store.validate_transition("CONSTRAINED", "READY_TO_BUILD", evidence=issued)["status"] == "PASS"
assert store.validate_transition("CONSTRAINED", "READY_TO_BUILD", evidence={"status": "PASS"})["status"] == "FAIL"
g["nodes"]["ROOT"]["state"] = "READY_TO_BUILD"
assert auth.can_mutate(g, "ROOT", issued)["status"] == "PASS"
assert auth.can_mutate(g, "ROOT", None)["status"] == "FAIL"
g["nodes"]["ROOT"]["state"] = "BUILT_UNVERIFIED"; g["nodes"]["BODY"]["state"] = "CONSTRAINED"
r = sg.validate(g)
assert "BODY" not in r["eligible_nodes"] and "ROOT" in r["built_unverified_barriers"]
assert store.validate_transition("BUILT_UNVERIFIED", "ACCEPTED", evidence={"status": "ACCEPTED", "validator_id": "RECONSTRUCTION_NODE_GATE", "provenance_id": "gate_1"})["status"] == "PASS"

d = conflict.resolve({"property_id": "HEAD_TOP_PROFILE", "candidates": [
    {"value": "SLOPED", "source_reference_id": "side", "authority_kind": "ORTHOGRAPHIC", "confidence": 0.8},
    {"value": "STEPPED", "source_reference_id": "detail", "authority_kind": "DETAIL_ORTHO", "confidence": 0.9},
]})
assert d["status"] == "PASS" and d["selected_value"] == "STEPPED" and d["averaging_used"] is False
assert conflict.resolve({"property_id": "X", "candidates": [
    {"value": 1, "source_reference_id": "a", "authority_rank": 80, "confidence": 1.0},
    {"value": 2, "source_reference_id": "b", "authority_rank": 80, "confidence": 1.0},
]})["status"] == "BLOCKED"

contract = {"revision": "ac_1", "owners": [{"owner_id": "TRIM_A", "importance": "MUST"}, {"owner_id": "DETAIL_B", "importance": "MUST"}]}
rep = {"shape_nodes": {"BODY": {"state": "ACCEPTED"}}, "appearance_owners": {"TRIM_A": {"status": "PASS"}}, "evidence": {}}
c = coverage.evaluate(contract, rep)
assert c["status"] == "FAIL" and c["missing_must"] == ["DETAIL_B"]
rep["appearance_owners"]["DETAIL_B"] = {"status": "PASS"}
assert coverage.evaluate(contract, rep)["status"] == "PASS"

assert pin.evaluate({"version": "0.11.0", "commit": "abc", "source_path": "/canonical", "active_duplicate_roots": []}, {"version": "0.11.0", "commit": "abc"})["status"] == "PASS"
assert pin.evaluate({"version": "0.10.0", "commit": "old", "source_path": "/embedded", "active_duplicate_roots": ["/copy"]}, {"version": "0.11.0", "commit": "abc"})["status"] == "FAIL"

node_report = {
    "node_id": "HEAD", "graph_revision": "sg", "node_revision": "n1", "parent_status": "PASS",
    "isolation": {"status": "PASS", "evidence_kind": "QA_SCENE_ISOLATION", "validator_id": "QA_SCENE_ISOLATE", "provenance_id": "iso"},
    "numeric_constraints": {"status": "PASS", "evidence_kind": "NUMERIC_MEASUREMENT", "validator_id": "REFERENCE_MEASURE", "provenance_id": "num"},
    "regression": {"status": "PASS", "evidence_kind": "REGISTERED_OVERLAY", "validator_id": "REFERENCE_OVERLAY_VALIDATE", "provenance_id": "reg", "source_reference_id": "front", "registration_id": "reg1"},
    "required_views": ["SIDE", "HERO"],
    "view_contracts": {"SIDE": {"allowed_evidence_kinds": ["REGISTERED_OVERLAY"]}, "HERO": {"allowed_evidence_kinds": ["PERSPECTIVE_INSPECTION"]}},
    "views": {
        "SIDE": {"status": "PASS", "evidence_kind": "REGISTERED_OVERLAY", "validator_id": "REFERENCE_OVERLAY_VALIDATE", "provenance_id": "side", "source_reference_id": "side_ref", "registration_id": "sreg"},
        "HERO": {"status": "PASS", "evidence_kind": "PERSPECTIVE_INSPECTION", "validator_id": "APPEARANCE_REFERENCE_VALIDATE", "provenance_id": "hero", "source_reference_id": "hero_ref"},
    },
}
assert node_gate.evaluate(node_report)["status"] == "ACCEPTED"
bad = dict(node_report); bad["views"] = dict(node_report["views"]); bad["views"]["HERO"] = {"status": "PASS", "evidence_kind": "REGISTERED_OVERLAY", "validator_id": "REFERENCE_OVERLAY_VALIDATE", "provenance_id": "hero", "source_reference_id": "hero_ref", "registration_id": "hreg"}
assert node_gate.evaluate(bad)["status"] != "ACCEPTED"
print("v0.11 execution-enforcement regression tests: PASS")

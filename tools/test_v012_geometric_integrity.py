from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    p = ROOT / "executors" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


mutation = load("mutation_postcondition_gate")
assembly = load("assembly_integrity_gate")
invalidate = load("dependency_invalidator")
controls = load("validator_negative_control")
store = load("node_state_store")
node_gate = load("reconstruction_node_gate")

# ---------------------------------------------------------------------------
# V12-03: a Boolean that executes but leaves geometry untouched must fail.
# ---------------------------------------------------------------------------
noop = mutation.evaluate({
    "operation_id": "bool_sensor_lens", "operation_kind": "BOOLEAN_CUT",
    "before": {"faces": 120, "vertices": 130, "volume_mm3": 10000, "geometry_signature": "abc"},
    "after": {"faces": 120, "vertices": 130, "volume_mm3": 10000, "geometry_signature": "abc", "modifiers": []},
    "expectations": {"modifier_absent": ["BOOL_LENS"]},
})
assert noop["status"] == "FAIL"
assert any(b["reason"] == "BOOLEAN_NOT_A_NOOP" for b in noop["blockers"])

cut = mutation.evaluate({
    "operation_id": "bool_sensor_lens_fixed", "operation_kind": "BOOLEAN_CUT",
    "before": {"faces": 120, "vertices": 130, "volume_mm3": 10000, "geometry_signature": "abc"},
    "after": {"faces": 148, "vertices": 162, "volume_mm3": 9400, "geometry_signature": "def", "modifiers": [], "scene_objects": []},
    "expectations": {"min_abs_volume_delta_mm3": 100, "volume_direction": "DECREASE",
                     "modifier_absent": ["BOOL_LENS"], "cutter_absent": ["CUT_LENS"]},
})
assert cut["status"] == "PASS"

# ---------------------------------------------------------------------------
# V12-01/02: relation semantics, not generic overlap, own assembly acceptance.
# ---------------------------------------------------------------------------
broken = assembly.evaluate({
    "assembly_revision": "lamp_head_broken",
    "relations": [{"relation_id": "J_SENSOR_ARM", "a": "ARM", "b": "SENSOR_MODULE",
                   "relation_type": "SHADOW_GAP", "importance": "MUST",
                   "metrics": {"penetration_area_mm2": 42324, "min_gap_mm": -95, "mean_gap_mm": -40},
                   "constraints": {"min_gap_mm": 2.0, "max_gap_mm": 4.0,
                                   "max_penetration_area_mm2": 0.5}}],
})
assert broken["status"] == "FAIL" and broken["failed_must"] == ["J_SENSOR_ARM"]

fixed = assembly.evaluate({
    "assembly_revision": "lamp_head_fixed",
    "relations": [{"relation_id": "J_SENSOR_ARM", "a": "ARM", "b": "SENSOR_MODULE",
                   "relation_type": "SHADOW_GAP", "importance": "MUST",
                   "metrics": {"penetration_area_mm2": 0.0, "min_gap_mm": 3.0, "mean_gap_mm": 3.0},
                   "constraints": {"min_gap_mm": 2.0, "max_gap_mm": 4.0,
                                   "max_penetration_area_mm2": 0.5}}],
})
assert fixed["status"] == "PASS"

# ---------------------------------------------------------------------------
# V12-06: a validator must prove that it bites a known-broken fixture.
# ---------------------------------------------------------------------------
control_fail = controls.evaluate({
    "validator_id_under_test": "ASSEMBLY_INTEGRITY_GATE",
    "positive_controls": [{"case_id": "known_good", "actual_status": "PASS"}],
    "negative_controls": [{"case_id": "known_overlap", "actual_status": "PASS"}],
})
assert control_fail["status"] == "FAIL"
assert any(b["reason"] == "NEGATIVE_CONTROL_DID_NOT_BITE" for b in control_fail["blockers"])

control_pass = controls.evaluate({
    "validator_id_under_test": "ASSEMBLY_INTEGRITY_GATE",
    "positive_controls": [{"case_id": "known_good", "actual_status": "PASS"}],
    "negative_controls": [{"case_id": "known_overlap", "actual_status": "FAIL"}],
})
assert control_pass["status"] == "PASS"

# ---------------------------------------------------------------------------
# V12-09: host repair invalidates descendants/owners/evidence, not unrelated BASE.
# ---------------------------------------------------------------------------
graph = {"nodes": {
    "ARM": {"parent": None, "depends_on": []},
    "SENSOR": {"parent": "ARM", "depends_on": []},
    "LENS": {"parent": "SENSOR", "depends_on": []},
    "BASE": {"parent": None, "depends_on": []},
}}
checkpoint = {
    "asset_id": "lamp", "state_revision": "state_007", "graph_revision": "sg_1",
    "shape_nodes": {
        "ARM": {"state": "ACCEPTED", "node_revision": "arm_004"},
        "SENSOR": {"state": "ACCEPTED", "node_revision": "sensor_003"},
        "LENS": {"state": "CONSTRAINED", "node_revision": "lens_001"},
        "BASE": {"state": "ACCEPTED", "node_revision": "base_002"},
    },
    "appearance_owners": {
        "J_SENSOR_ARM": {"status": "PASS", "hosts": ["ARM", "SENSOR"]},
        "BASE_TRIM": {"status": "PASS", "hosts": ["BASE"]},
    },
    "evidence": {
        "gate_arm": {"status": "PASS", "node_id": "ARM"},
        "junction": {"status": "PASS", "owner_id": "J_SENSOR_ARM"},
        "base": {"status": "PASS", "node_id": "BASE"},
    }, "history": [],
}
contract = {"owners": [
    {"owner_id": "J_SENSOR_ARM", "hosts": ["ARM", "SENSOR"]},
    {"owner_id": "BASE_TRIM", "hosts": ["BASE"]},
]}
r = invalidate.invalidate(graph, checkpoint, ["ARM"], contract, change_id="repair:arm_sensor_seam")
assert r["status"] == "PASS"
assert r["checkpoint"]["shape_nodes"]["ARM"]["state"] == "DIRTY"
assert r["checkpoint"]["shape_nodes"]["SENSOR"]["state"] == "DIRTY"
assert r["checkpoint"]["shape_nodes"]["LENS"]["state"] == "BLOCKED"
assert r["checkpoint"]["shape_nodes"]["BASE"]["state"] == "ACCEPTED"
assert r["checkpoint"]["appearance_owners"]["J_SENSOR_ARM"]["status"] == "UNVERIFIED"
assert r["checkpoint"]["appearance_owners"]["BASE_TRIM"]["status"] == "PASS"
assert r["checkpoint"]["evidence"]["gate_arm"]["status"] == "SUPERSEDED"
assert r["checkpoint"]["evidence"]["junction"]["status"] == "SUPERSEDED"
assert r["checkpoint"]["evidence"]["base"]["status"] == "PASS"

# ---------------------------------------------------------------------------
# v0.12 state integration: builder completion cannot reach BUILT_UNVERIFIED
# without the canonical mutation postcondition.
# ---------------------------------------------------------------------------
local_artifact = {"status": "PASS", "validator_id": "LOCAL_BUILDER", "artifact_id": "build:ARM:005"}
assert store.validate_transition("READY_TO_BUILD", "BUILT_UNVERIFIED", evidence=local_artifact)["status"] == "FAIL"
local_artifact["mutation_postcondition"] = cut
assert store.validate_transition("READY_TO_BUILD", "BUILT_UNVERIFIED", evidence=local_artifact)["status"] == "PASS"

# ---------------------------------------------------------------------------
# v0.12 node acceptance integration: authorized production geometry needs both
# mutation postcondition and assembly integrity, in addition to v0.11 proof.
# ---------------------------------------------------------------------------
def proof(validator, kind, provenance, *, source=None, registration=None):
    r = {"status": "PASS", "validator_id": validator, "evidence_kind": kind,
         "provenance_id": provenance}
    if source: r["source_reference_id"] = source
    if registration: r["registration_id"] = registration
    return r

node_report = {
    "node_id": "SENSOR", "graph_revision": "sg", "node_revision": "sensor_004",
    "parent_status": "PASS", "strict_evidence": True,
    "authorization": {"status": "PASS", "validator_id": "EXECUTION_AUTHORIZATION_GATE",
                      "authorization_id": "auth:sensor:004"},
    "isolation": proof("QA_SCENE_ISOLATE", "QA_SCENE_ISOLATION", "iso:sensor"),
    "numeric_constraints": proof("REFERENCE_MEASURE", "DERIVED_PARAMETER_FIT", "num:sensor", source="detail_head"),
    "regression": proof("MESH_VALIDATE", "DERIVED_PARAMETER_FIT", "mesh:sensor", source="detail_head"),
    "required_views": ["SIDE"],
    "view_contracts": {"SIDE": {"allowed_evidence_kinds": ["REGISTERED_OVERLAY"]}},
    "views": {"SIDE": proof("REFERENCE_OVERLAY_VALIDATE", "REGISTERED_OVERLAY", "side:sensor",
                             source="side_ref", registration="reg:side")},
}
assert node_gate.evaluate(node_report)["status"] != "ACCEPTED"
node_report["mutation_postcondition"] = cut
node_report["assembly_integrity"] = fixed
assert node_gate.evaluate(node_report)["status"] == "ACCEPTED"

print("v0.12 geometric-integrity regression tests: PASS")

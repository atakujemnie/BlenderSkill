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


integrity = load("geometric_integrity_gate")
fidelity = load("fidelity_gate")

mutation = {"status": "PASS", "validator_id": "MUTATION_POSTCONDITION_GATE",
            "evidence_kind": "MUTATION_POSTCONDITION", "provenance_id": "mut:1"}
assembly = {"status": "PASS", "validator_id": "ASSEMBLY_INTEGRITY_GATE",
            "evidence_kind": "ASSEMBLY_INTEGRITY", "provenance_id": "asm:1"}
topology = {"status": "PASS", "validator_id": "MESH_VALIDATE",
            "evidence_kind": "MESH_INTEGRITY", "provenance_id": "mesh:1"}
control = {"status": "PASS", "validator_id": "VALIDATOR_NEGATIVE_CONTROL",
           "evidence_kind": "VALIDATOR_NEGATIVE_CONTROL", "provenance_id": "ctrl:1",
           "validator_id_under_test": "ASSEMBLY_INTEGRITY_GATE"}

report = {
    "asset_revision": "lamp_v2_fixed",
    "mutation_postconditions": [mutation],
    "assembly_integrity": assembly,
    "topology_records": [topology],
    "validator_controls": [control],
    "required_validator_controls": ["ASSEMBLY_INTEGRITY_GATE"],
    "stale_evidence_ids": [], "unresolved_relation_ids": [],
}
passed = integrity.evaluate(report)
assert passed["status"] == "PASS" and passed["can_enter_fidelity_gate"] is True

stale = dict(report); stale["stale_evidence_ids"] = ["gate:old_sensor"]
assert integrity.evaluate(stale)["status"] == "FAIL"
missing_control = dict(report); missing_control["validator_controls"] = []
assert integrity.evaluate(missing_control)["status"] == "FAIL"
bad_assembly = dict(report); bad_assembly["assembly_integrity"] = dict(assembly, status="FAIL")
assert integrity.evaluate(bad_assembly)["status"] == "FAIL"

# L4/L5 reconstruction fidelity now has a non-compensating physical-integrity lock.
def ref(kind, validator, pid, reg=False):
    out = {"status": "PASS", "evidence_kind": kind, "validator_id": validator,
           "provenance_id": pid, "source_reference_id": "ref"}
    if reg: out["registration_id"] = "reg:" + pid
    return out

fidelity_report = {
    "target_fidelity": "L4", "achieved_fidelity": "L4", "strict_evidence": True,
    "hard_dimensions": ref("NUMERIC_MEASUREMENT", "REFERENCE_MEASURE", "dims"),
    "landmarks_d0_d1": ref("LANDMARK_PROJECTION", "REFERENCE_OVERLAY_VALIDATE", "landmarks", reg=True),
    "material_segmentation": ref("MATERIAL_SEGMENTATION", "APPEARANCE_REFERENCE_VALIDATE", "materials"),
    "appearance_fidelity": {"status": "PASS", "evidence_kind": "APPEARANCE_FIDELITY_GATE",
                            "validator_id": "APPEARANCE_FIDELITY_GATE", "provenance_id": "app"},
    "canonical_views": {v: ref("REGISTERED_OVERLAY", "REFERENCE_OVERLAY_VALIDATE", v, reg=True)
                        for v in ("FRONT", "SIDE", "TOP", "REAR", "BOTTOM")},
    "must_features": [],
}
blocked = fidelity.evaluate(fidelity_report)
assert blocked["status"] == "FAIL" and blocked["can_advance_to_runtime"] is False
assert any(b["owner"] == "geometric_integrity" for b in blocked["blockers"])

fidelity_report["geometric_integrity"] = passed
full = fidelity.evaluate(fidelity_report)
assert full["status"] == "PASS" and full["can_advance_to_runtime"] is True

print("v0.12 final geometric-integrity/runtime-lock tests: PASS")

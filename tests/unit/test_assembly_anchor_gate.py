from executors.assembly_anchor_gate import evaluate


def test_coincident_bench_mounts_pass_within_tolerance():
    result = evaluate(
        {
            "assembly_revision": 4,
            "relations": [
                {
                    "id": "BACKREST_RIGHT",
                    "type": "COINCIDENT",
                    "a": "BACKREST.RIGHT_MOUNT",
                    "b": "RIGHT_SUPPORT.BACKREST_MOUNT",
                    "tolerance_mm": 0.5,
                }
            ],
            "anchors": {
                "BACKREST.RIGHT_MOUNT": {"position_mm": [790.0, 170.0, 455.0]},
                "RIGHT_SUPPORT.BACKREST_MOUNT": {"position_mm": [790.2, 170.1, 455.1]},
            },
        }
    )
    assert result["status"] == "PASS"


def test_coincident_bench_mount_fails_instead_of_hiding_offset_in_geometry():
    result = evaluate(
        {
            "relations": [
                {
                    "id": "BACKREST_RIGHT",
                    "type": "COINCIDENT",
                    "a": "BACKREST.RIGHT_MOUNT",
                    "b": "RIGHT_SUPPORT.BACKREST_MOUNT",
                    "tolerance_mm": 0.5,
                }
            ],
            "anchors": {
                "BACKREST.RIGHT_MOUNT": {"position_mm": [790.0, 170.0, 455.0]},
                "RIGHT_SUPPORT.BACKREST_MOUNT": {"position_mm": [797.3, 170.0, 455.0]},
            },
        }
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "COINCIDENT_TOLERANCE_EXCEEDED"

from executors.reference_evidence_materializer import materialize


def test_reference_evidence_materializes_real_local_attachment(tmp_path):
    image = tmp_path / "concept.png"
    image.write_bytes(b"not-decoded-by-materializer")
    result = materialize(
        [
            {
                "evidence_id": "EV-LED",
                "artifact_id": "ART-CONCEPT",
                "view": "DETAIL",
                "authority": "PRIMARY",
                "feature_ids": ["LED_RECESS"],
                "roi": [10, 20, 110, 90],
            }
        ],
        {"ART-CONCEPT": {"path": str(image), "media_type": "image/png"}},
        allowed_root=tmp_path,
    )
    assert result["status"] == "PASS", result
    assert result["attachment_count"] == 1
    attachment = result["attachments"][0]
    assert attachment["path"] == str(image.resolve())
    assert attachment["roi"] == [10.0, 20.0, 110.0, 90.0]
    assert attachment["feature_ids"] == ["LED_RECESS"]


def test_reference_artifact_cannot_escape_allowed_root(tmp_path):
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"x")
    result = materialize(
        [{"evidence_id": "EV", "artifact_id": "ART", "roi": [0, 0, 1, 1]}],
        {"ART": {"path": str(outside)}},
        allowed_root=allowed,
    )
    assert result["status"] == "FAIL"
    assert result["blockers"][0]["reason"] == "REFERENCE_ARTIFACT_OUTSIDE_ALLOWED_ROOT"

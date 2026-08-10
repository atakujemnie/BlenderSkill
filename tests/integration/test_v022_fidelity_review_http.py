import http.client
import json
import threading

from studio.server import make_server


def _request(port: int, method: str, path: str, payload=None):
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"} if body is not None else {}
    connection.request(method, path, body=body, headers=headers)
    response = connection.getresponse()
    raw = response.read()
    parsed = json.loads(raw.decode("utf-8"))
    connection.close()
    return response.status, parsed


def _asset():
    return {
        "asset_id": "FIDELITY-HTTP-022",
        "name": "Fidelity HTTP probe",
        "revision": 1,
        "stage": "FIDELITY_AUDIT",
        "enforce_feature_contracts": True,
        "components": {
            "ROOT": {
                "parent": None,
                "state": "ACCEPTED",
                "shape_class": "ASSEMBLY",
                "dimensions": {
                    "width": {"value": 100, "unit": "mm"},
                    "depth": {"value": 100, "unit": "mm"},
                    "height": {"value": 100, "unit": "mm"},
                },
                "anchors": {},
            },
            "BODY": {
                "parent": "ROOT",
                "state": "ACCEPTED",
                "acceptance_level": "FIDELITY",
                "shape_class": "ROUNDED_BOX",
                "dimensions": {
                    "width": {"value": 100, "unit": "mm"},
                    "depth": {"value": 100, "unit": "mm"},
                    "height": {"value": 100, "unit": "mm"},
                },
                "anchors": {},
                "feature_contract": {
                    "features": [
                        {
                            "feature_id": "BODY_PROFILE",
                            "priority": "MUST",
                            "visual_required": True,
                            "qa_views": ["FRONT"],
                        }
                    ]
                },
            },
        },
        "bindings": {},
        "corrections": [],
        "history": [],
    }


def test_v022_http_persists_current_independent_fidelity_review_and_allows_final_stage(tmp_path):
    server = make_server(tmp_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        status, created = _request(port, "POST", "/api/assets", {"asset": _asset()})
        assert status == 201, created
        assert created["fidelity_review_revision"] == 0

        status, no_review = _request(port, "GET", "/api/assets/FIDELITY-HTTP-022/fidelity-review")
        assert status == 200, no_review
        assert no_review["revision"] == 0
        assert no_review["review"] is None

        scene = {
            "asset_id": "FIDELITY-HTTP-022",
            "asset_revision": 1,
            "scene_revision": 1,
            "objects": [
                {
                    "object_id": "body",
                    "component_id": "BODY",
                    "object_type": "MESH",
                    "transform": {"location_mm": [0, 0, 0], "rotation_rad": [0, 0, 0], "scale": [1, 1, 1]},
                    "dimensions_mm": [100, 100, 100],
                    "material_ids": [],
                    "modifier_stack": [],
                }
            ],
        }
        status, published = _request(port, "POST", "/api/assets/FIDELITY-HTTP-022/scene", {"scene": scene})
        assert status == 201, published

        review = {
            "asset_id": "FIDELITY-HTTP-022",
            "asset_revision": 1,
            "scene_revision": 1,
            "reference_revision": 1,
            "reviewer_id": "reviewer-http",
            "worker_id": "builder-http",
            "reviewer_role": "INDEPENDENT_VISUAL_REVIEWER",
            "qa_views": [
                {
                    "view_id": "FRONT",
                    "render_artifact_id": "render-front",
                    "reference_evidence_ids": ["reference-front"],
                }
            ],
            "feature_reviews": [
                {"feature_id": "BODY_PROFILE", "status": "PASS", "view_ids": ["FRONT"]}
            ],
            "discovered_unmapped_features": [],
        }
        status, reviewed = _request(
            port,
            "POST",
            "/api/assets/FIDELITY-HTTP-022/fidelity-review",
            {"expected_review_revision": 0, "review": review},
        )
        assert status == 200, reviewed
        assert reviewed["status"] == "PASS"
        assert reviewed["revision"] == 1
        assert reviewed["review"]["source"] == "SYSTEM"

        status, final = _request(
            port,
            "POST",
            "/api/assets/FIDELITY-HTTP-022/stage",
            {"expected_asset_revision": 1, "new_stage": "APPROVED"},
        )
        assert status == 200, final
        assert final["asset_revision"] == 2
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

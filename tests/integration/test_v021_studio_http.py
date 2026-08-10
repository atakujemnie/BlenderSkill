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
    content_type = response.getheader("Content-Type") or ""
    parsed = json.loads(raw.decode("utf-8")) if "application/json" in content_type else raw.decode("utf-8")
    connection.close()
    return response.status, parsed


def _asset():
    return {
        "asset_id": "GENERIC-021",
        "name": "Generic v0.21 asset",
        "revision": 1,
        "stage": "BLOCKOUT",
        "components": {
            "ROOT": {
                "parent": None,
                "state": "ACCEPTED",
                "shape_class": "ASSEMBLY",
                "dimensions": {
                    "width": {"value": 1000, "unit": "mm"},
                    "depth": {"value": 1000, "unit": "mm"},
                    "height": {"value": 100, "unit": "mm"},
                },
                "anchors": {},
            },
            "PLATE": {
                "parent": "ROOT",
                "state": "CONSTRAINED",
                "shape_class": "ROUNDED_BOX",
                "depends_on": ["ROOT"],
                "transform": {"location_mm": [0, 0, 0], "coordinate_space": "ASSET_LOCAL"},
                "dimensions": {
                    "width": {"value": 500, "unit": "mm"},
                    "depth": {"value": 500, "unit": "mm"},
                    "height": {"value": 50, "unit": "mm"},
                },
                "anchors": {},
            },
        },
        "bindings": {},
        "corrections": [],
        "history": [],
    }


def test_v021_http_is_asset_generic_and_exposes_authorization(tmp_path):
    server = make_server(tmp_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        status, health = _request(port, "GET", "/api/health")
        assert status == 200
        assert health["version"] == "0.22.0"

        status, html = _request(port, "GET", "/")
        assert status == 200
        assert "BlenderSkill Studio" in html
        assert 'selected_component_id:"BACKREST"' not in html
        assert "const EMPTY_MODEL" in html

        status, created = _request(port, "POST", "/api/assets", {"asset": _asset()})
        assert status == 201, created

        status, studio = _request(port, "GET", "/api/assets/GENERIC-021/studio")
        assert status == 200
        selected = studio["view_model"]["selected_component_id"]
        assert selected in {"ROOT", "PLATE"}
        assert selected != "BACKREST"

        status, authorized = _request(
            port,
            "POST",
            "/api/assets/GENERIC-021/components/PLATE/authorize",
            {
                "expected_asset_revision": 1,
                "authorization": {
                    "status": "PASS",
                    "validator_id": "EXECUTION_AUTHORIZATION_GATE",
                    "validator_version": "0.21.0",
                },
            },
        )
        assert status == 200, authorized
        assert authorized["asset_revision"] == 2

        status, plate = _request(port, "GET", "/api/assets/GENERIC-021/studio?component=PLATE")
        assert status == 200
        assert plate["view_model"]["inspector"]["component"]["state"] == "READY_TO_BUILD"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

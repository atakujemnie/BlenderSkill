import http.client
import json
import threading
from pathlib import Path

from studio.server import make_server


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "lafar_street_bench_vnext.json"


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


def test_http_api_serves_gui_and_persistent_asset_routes(tmp_path):
    server = make_server(tmp_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        status, health = _request(port, "GET", "/api/health")
        assert status == 200
        assert health["server_id"] == "PRODUCTION_STUDIO_HTTP"

        status, html = _request(port, "GET", "/")
        assert status == 200
        assert "BlenderSkill Studio" in html

        asset = json.loads(FIXTURE.read_text(encoding="utf-8"))
        status, created = _request(port, "POST", "/api/assets", {"asset": asset})
        assert status == 201
        assert created["asset_id"] == "ASSET-005"

        status, assets = _request(port, "GET", "/api/assets")
        assert status == 200
        assert assets["asset_count"] == 1

        status, studio = _request(port, "GET", "/api/assets/ASSET-005/studio?component=BACKREST")
        assert status == 200
        assert studio["view_model"]["selected_component_id"] == "BACKREST"

        status, failure = _request(
            port,
            "POST",
            "/api/assets/ASSET-005/corrections",
            {"correction": {"id": "COR-1", "component_id": "BACKREST", "priority": "HARD"}},
        )
        assert status == 400
        assert failure["blockers"][0]["reason"] == "EXPECTED_ASSET_REVISION_REQUIRED"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_http_api_manages_shared_design_resource(tmp_path):
    server = make_server(tmp_path, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        resource = {
            "design_system_id": "ASTERA_CIVIC",
            "resource_id": "ASTERA_LED_INFO_BLUE_01",
            "kind": "LED_PROFILE",
            "version": "1.0.0",
            "revision": 1,
            "locked": True,
            "payload": {"width_mm": 8},
        }
        status, created = _request(
            port,
            "POST",
            "/api/design-resources",
            {"expected_revision": 0, "resource": resource},
        )
        assert status == 201
        assert created["revision"] == 1

        status, resources = _request(port, "GET", "/api/design-resources?design_system_id=ASTERA_CIVIC")
        assert status == 200
        assert resources["resources"][0]["resource_id"] == "ASTERA_LED_INFO_BLUE_01"

        status, fetched = _request(
            port,
            "GET",
            "/api/design-systems/ASTERA_CIVIC/resources/ASTERA_LED_INFO_BLUE_01",
        )
        assert status == 200
        assert fetched["resource"]["locked"] is True
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

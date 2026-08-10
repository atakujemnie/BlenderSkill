from __future__ import annotations

"""Local HTTP adapter for the BlenderSkill Asset Production Studio.

The server binds to loopback by default and exposes only explicit JSON API
routes plus the Studio HTML shell. Persistent state remains owned by executors.
Trusted validation-receipt publication is intentionally not exposed over HTTP.
"""

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs, unquote, urlsplit

from executors.design_studio_service import get_resource
from executors.design_studio_service import list_design_systems
from executors.design_studio_service import list_resources as list_design_resources
from executors.design_studio_service import resource_impact
from executors.design_studio_service import upsert_resource
from executors.production_studio_service import (
    add_asset_correction,
    advance_asset_stage,
    authorize_component,
    create_asset,
    create_production_task,
    delete_reference_evidence,
    get_studio,
    list_assets,
    prepare_task,
    promote_production_tasks,
    publish_scene,
    resolve_asset_correction,
    transition_production_task,
    upsert_reference_evidence,
)

SERVER_ID = "PRODUCTION_STUDIO_HTTP"
SERVER_VERSION = "0.21.0"
MAX_JSON_BYTES = 4 * 1024 * 1024
REPO_ROOT = Path(__file__).resolve().parents[1]
STUDIO_HTML = REPO_ROOT / "studio" / "asset_production_studio.html"
DESIGN_STUDIO_HTML = REPO_ROOT / "studio" / "design_system_studio.html"


def _http_status(result: Mapping[str, Any], *, created: bool = False) -> int:
    status = str(result.get("status") or "FAIL").upper()
    if status == "PASS":
        return HTTPStatus.CREATED if created else HTTPStatus.OK
    if status == "CONFLICT":
        return HTTPStatus.CONFLICT
    if status == "NOT_FOUND":
        return HTTPStatus.NOT_FOUND
    if status in {"BLOCKED", "PARTIAL"}:
        return HTTPStatus.UNPROCESSABLE_ENTITY
    return HTTPStatus.BAD_REQUEST


def _safe_segment(value: str) -> str:
    decoded = unquote(value).strip()
    if not decoded or decoded in {".", ".."} or "/" in decoded or "\\" in decoded:
        raise ValueError("UNSAFE_PATH_SEGMENT")
    return decoded


def make_handler(data_root: str | Path):
    runtime_root = Path(data_root).expanduser().resolve()

    class StudioHandler(BaseHTTPRequestHandler):
        server_version = f"BlenderSkillStudio/{SERVER_VERSION}"

        def do_GET(self) -> None:  # noqa: N802
            self._guard(self._dispatch_get)

        def do_POST(self) -> None:  # noqa: N802
            self._guard(self._dispatch_post)

        def do_DELETE(self) -> None:  # noqa: N802
            self._guard(self._dispatch_delete)

        def _guard(self, callback) -> None:
            try:
                callback()
            except ValueError as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"status": "FAIL", "blockers": [{"reason": str(exc)}]})
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception as exc:  # pragma: no cover - defensive adapter boundary
                self.log_error("Unhandled Studio API error: %r", exc)
                self._json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"status": "FAIL", "blockers": [{"reason": "INTERNAL_SERVER_ERROR"}]},
                )

        def _dispatch_get(self) -> None:
            parsed = urlsplit(self.path)
            path = parsed.path.rstrip("/") or "/"
            if path in {"/", "/studio", "/index.html"}:
                self._serve_file(STUDIO_HTML)
                return
            if path in {"/design", "/design-system", "/design_system_studio.html"}:
                self._serve_file(DESIGN_STUDIO_HTML)
                return
            if path == "/api/health":
                self._json(
                    HTTPStatus.OK,
                    {
                        "status": "PASS",
                        "server_id": SERVER_ID,
                        "version": SERVER_VERSION,
                        "data_root": str(runtime_root),
                    },
                )
                return
            if path == "/api/assets":
                self._result(list_assets(runtime_root))
                return
            if path == "/api/design-systems":
                self._result(list_design_systems(runtime_root))
                return
            if path == "/api/design-resources":
                query = parse_qs(parsed.query)
                design_system_id = query.get("design_system_id", [None])[0]
                self._result(list_design_resources(runtime_root, design_system_id=design_system_id))
                return

            parts = self._parts(path)
            if len(parts) == 4 and parts[:2] == ["api", "assets"] and parts[3] == "studio":
                query = parse_qs(parsed.query)
                component = query.get("component", [None])[0]
                self._result(get_studio(runtime_root, parts[2], component_id=component))
                return
            if len(parts) == 5 and parts[:2] == ["api", "design-systems"] and parts[3] == "resources":
                self._result(get_resource(runtime_root, parts[2], parts[4]))
                return
            if (
                len(parts) == 6
                and parts[:2] == ["api", "design-systems"]
                and parts[3] == "resources"
                and parts[5] == "impact"
            ):
                self._result(resource_impact(runtime_root, parts[2], parts[4]))
                return
            self._not_found()

        def _dispatch_post(self) -> None:
            parsed = urlsplit(self.path)
            path = parsed.path.rstrip("/") or "/"
            body = self._read_json()

            if path == "/api/assets":
                asset = body.get("asset", body)
                if not isinstance(asset, Mapping):
                    raise ValueError("ASSET_MAPPING_REQUIRED")
                self._result(create_asset(runtime_root, asset), created=True)
                return
            if path == "/api/design-resources":
                resource = body.get("resource")
                if not isinstance(resource, Mapping):
                    raise ValueError("DESIGN_RESOURCE_MAPPING_REQUIRED")
                expected_revision = self._required_int(body, "expected_revision")
                self._result(
                    upsert_resource(runtime_root, resource, expected_revision=expected_revision),
                    created=expected_revision == 0,
                )
                return

            parts = self._parts(path)
            if len(parts) < 4 or parts[:2] != ["api", "assets"]:
                self._not_found()
                return
            asset_id = parts[2]

            if len(parts) == 6 and parts[3] == "components" and parts[5] == "authorize":
                authorization = body.get("authorization")
                if not isinstance(authorization, Mapping):
                    raise ValueError("AUTHORIZATION_MAPPING_REQUIRED")
                self._result(
                    authorize_component(
                        runtime_root,
                        asset_id,
                        parts[4],
                        authorization,
                        expected_asset_revision=self._required_int(body, "expected_asset_revision"),
                    )
                )
                return
            if len(parts) == 4 and parts[3] == "corrections":
                correction = body.get("correction")
                if not isinstance(correction, Mapping):
                    raise ValueError("CORRECTION_MAPPING_REQUIRED")
                self._result(
                    add_asset_correction(
                        runtime_root,
                        asset_id,
                        correction,
                        expected_asset_revision=self._required_int(body, "expected_asset_revision"),
                    ),
                    created=True,
                )
                return
            if len(parts) == 6 and parts[3] == "corrections" and parts[5] == "resolve":
                resolution = body.get("resolution")
                if resolution is not None and not isinstance(resolution, Mapping):
                    raise ValueError("RESOLUTION_MAPPING_REQUIRED")
                self._result(
                    resolve_asset_correction(
                        runtime_root,
                        asset_id,
                        parts[4],
                        expected_asset_revision=self._required_int(body, "expected_asset_revision"),
                        resolution=resolution,
                    )
                )
                return
            if len(parts) == 4 and parts[3] == "stage":
                self._result(
                    advance_asset_stage(
                        runtime_root,
                        asset_id,
                        str(body.get("new_stage") or ""),
                        expected_asset_revision=self._required_int(body, "expected_asset_revision"),
                    )
                )
                return
            if len(parts) == 4 and parts[3] == "tasks":
                task = body.get("task")
                if not isinstance(task, Mapping):
                    raise ValueError("TASK_MAPPING_REQUIRED")
                self._result(
                    create_production_task(
                        runtime_root,
                        asset_id,
                        task,
                        expected_queue_revision=self._required_int(body, "expected_queue_revision"),
                    ),
                    created=True,
                )
                return
            if len(parts) == 5 and parts[3] == "tasks" and parts[4] == "promote":
                self._result(
                    promote_production_tasks(
                        runtime_root,
                        asset_id,
                        expected_queue_revision=self._required_int(body, "expected_queue_revision"),
                    )
                )
                return
            if len(parts) == 6 and parts[3] == "tasks" and parts[5] == "transition":
                blockers = body.get("blockers")
                if blockers is not None and not isinstance(blockers, list):
                    raise ValueError("BLOCKERS_LIST_REQUIRED")
                result = body.get("result")
                if result is not None and not isinstance(result, Mapping):
                    raise ValueError("TASK_RESULT_MAPPING_REQUIRED")
                self._result(
                    transition_production_task(
                        runtime_root,
                        asset_id,
                        parts[4],
                        str(body.get("target_status") or ""),
                        expected_queue_revision=self._required_int(body, "expected_queue_revision"),
                        actor=str(body.get("actor") or "STUDIO_USER"),
                        reason=str(body.get("reason") or "STUDIO_TRANSITION"),
                        worker_id=str(body["worker_id"]) if body.get("worker_id") is not None else None,
                        blockers=[dict(item) for item in blockers or [] if isinstance(item, Mapping)],
                        result=result,
                    )
                )
                return
            if len(parts) == 4 and parts[3] == "scene":
                report = body.get("scene", body)
                if not isinstance(report, Mapping):
                    raise ValueError("SCENE_MAPPING_REQUIRED")
                component_ids = body.get("component_ids")
                if component_ids is not None and not isinstance(component_ids, list):
                    raise ValueError("COMPONENT_IDS_LIST_REQUIRED")
                self._result(
                    publish_scene(
                        runtime_root,
                        asset_id,
                        report,
                        component_ids=[str(value) for value in component_ids or []] or None,
                    ),
                    created=True,
                )
                return
            if len(parts) == 4 and parts[3] == "evidence":
                evidence = body.get("evidence")
                if not isinstance(evidence, Mapping):
                    raise ValueError("EVIDENCE_MAPPING_REQUIRED")
                self._result(
                    upsert_reference_evidence(
                        runtime_root,
                        asset_id,
                        evidence,
                        expected_reference_revision=self._required_int(body, "expected_reference_revision"),
                    )
                )
                return
            if len(parts) == 4 and parts[3] == "task-pack":
                features = body.get("feature_ids", [])
                views = body.get("views", [])
                if not isinstance(features, list) or not isinstance(views, list):
                    raise ValueError("FEATURE_IDS_AND_VIEWS_LIST_REQUIRED")
                max_tokens = body.get("max_input_tokens")
                self._result(
                    prepare_task(
                        runtime_root,
                        asset_id,
                        str(body.get("component_id") or ""),
                        task_kind=str(body.get("task_kind") or "BUILD"),
                        feature_ids=[str(value) for value in features],
                        views=[str(value) for value in views],
                        max_input_tokens=int(max_tokens) if max_tokens is not None else None,
                    )
                )
                return
            self._not_found()

        def _dispatch_delete(self) -> None:
            parsed = urlsplit(self.path)
            parts = self._parts(parsed.path.rstrip("/") or "/")
            body = self._read_json(allow_empty=True)
            if len(parts) == 5 and parts[:2] == ["api", "assets"] and parts[3] == "evidence":
                self._result(
                    delete_reference_evidence(
                        runtime_root,
                        parts[2],
                        parts[4],
                        expected_reference_revision=self._required_int(body, "expected_reference_revision"),
                    )
                )
                return
            self._not_found()

        def log_message(self, format: str, *args: Any) -> None:
            print(f"[{self.log_date_time_string()}] {self.address_string()} {format % args}")

        def _parts(self, path: str) -> list[str]:
            return [_safe_segment(part) for part in path.split("/") if part]

        def _read_json(self, *, allow_empty: bool = False) -> dict[str, Any]:
            raw_length = self.headers.get("Content-Length")
            if raw_length is None:
                if allow_empty:
                    return {}
                raise ValueError("CONTENT_LENGTH_REQUIRED")
            try:
                length = int(raw_length)
            except ValueError as exc:
                raise ValueError("CONTENT_LENGTH_INVALID") from exc
            if length < 0 or length > MAX_JSON_BYTES:
                raise ValueError("JSON_BODY_SIZE_INVALID")
            if length == 0:
                if allow_empty:
                    return {}
                raise ValueError("JSON_BODY_REQUIRED")
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ValueError("JSON_BODY_INVALID") from exc
            if not isinstance(payload, dict):
                raise ValueError("JSON_OBJECT_REQUIRED")
            return payload

        def _required_int(self, body: Mapping[str, Any], field: str) -> int:
            if field not in body:
                raise ValueError(f"{field.upper()}_REQUIRED")
            try:
                return int(body[field])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{field.upper()}_INTEGER_REQUIRED") from exc

        def _serve_file(self, path: Path) -> None:
            if not path.is_file():
                self._not_found()
                return
            payload = path.read_bytes()
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", f"{mime}; charset=utf-8" if mime.startswith("text/") else mime)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(payload)

        def _result(self, result: Mapping[str, Any], *, created: bool = False) -> None:
            self._json(_http_status(result, created=created), result)

        def _json(self, status: int, payload: Mapping[str, Any]) -> None:
            data = (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
            self.send_response(int(status))
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)

        def _not_found(self) -> None:
            self._json(
                HTTPStatus.NOT_FOUND,
                {"status": "NOT_FOUND", "blockers": [{"reason": "ROUTE_NOT_FOUND"}]},
            )

    return StudioHandler


def make_server(data_root: str | Path, *, host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, int(port)), make_handler(data_root))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local BlenderSkill Asset Production Studio.")
    parser.add_argument("--data-root", default=".blenderskill-runtime", help="Persistent runtime-state root.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host. Keep loopback unless remote access is intentional.")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = make_server(args.data_root, host=args.host, port=args.port)
    print(f"BlenderSkill Studio: http://{args.host}:{server.server_port}/")
    print(f"Runtime data: {Path(args.data_root).expanduser().resolve()}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

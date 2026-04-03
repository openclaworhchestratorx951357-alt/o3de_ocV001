import json
from pathlib import Path

from o3de_bridge.file_transport import (
    FileTransportPaths,
    archive_request,
    archive_response,
    request_filename,
    response_filename,
    write_request,
)
from o3de_bridge.models import ProjectScanRequest, RequestMeta


def test_request_and_response_filename_shapes() -> None:
    assert request_filename("abc-123") == "abc-123.json"
    assert response_filename("abc-123") == "abc-123.response.json"


def test_write_and_archive_request(tmp_path: Path) -> None:
    paths = FileTransportPaths.from_root(tmp_path)
    request = ProjectScanRequest(
        meta=RequestMeta(
            request_id="req-file-001",
            tool_name="project_scan",
            dry_run=True,
            approval_token=None,
            timestamp=None,
        ),
        project_id="McpSandbox",
    )

    request_path = write_request(paths, request)
    assert request_path.exists()

    payload = json.loads(request_path.read_text(encoding="utf-8"))
    assert payload["meta"]["request_id"] == "req-file-001"
    assert payload["meta"]["tool_name"] == "project_scan"
    assert payload["project_id"] == "McpSandbox"
    assert "request_id" not in payload
    assert "tool_name" not in payload

    archived = archive_request(paths, request.meta.request_id)
    assert archived.exists()
    assert not request_path.exists()


def test_archive_response_moves_existing_file(tmp_path: Path) -> None:
    paths = FileTransportPaths.from_root(tmp_path)
    paths.ensure()
    response_path = paths.outbox / response_filename("req-file-002")
    response_path.write_text("{}", encoding="utf-8")

    archived = archive_response(paths, "req-file-002")
    assert archived.exists()
    assert not response_path.exists()

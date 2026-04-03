"""WSL-side helper to stage a project_scan request and read back the response."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from .file_transport import (
    FileTransportPaths,
    archive_request,
    archive_response,
    read_response,
    response_filename,
    write_request,
)
from .models import ProjectScanRequest, RequestMeta

BRIDGE_ROOT = Path("/mnt/c/Users/topgu/O3DEBridge")
DEFAULT_REQUEST_PREFIX = "project-scan-roundtrip"


def make_request_id(prefix: str = DEFAULT_REQUEST_PREFIX) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{timestamp}"


def build_request(request_id: str | None = None) -> ProjectScanRequest:
    resolved_request_id = request_id or make_request_id()
    return ProjectScanRequest(
        meta=RequestMeta(
            request_id=resolved_request_id,
            tool_name="project_scan",
            dry_run=True,
            approval_token=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
        ),
        project_id="McpSandbox",
    )


def main() -> None:
    paths = FileTransportPaths.from_root(BRIDGE_ROOT)
    paths.ensure()

    request = build_request()
    response_path = paths.outbox / response_filename(request.meta.request_id)
    if response_path.exists():
        archive_response(paths, request.meta.request_id)

    request_path = write_request(paths, request)
    print(f"Wrote request: {request_path}")
    print(f"Request id: {request.meta.request_id}")
    print("Waiting for response file...")

    response = None
    for _ in range(120):
        if response_path.exists():
            response = read_response(paths, request.meta.request_id)
            break
        time.sleep(1)

    if response is None:
        raise SystemExit("Timed out waiting for response file.")

    print(json.dumps(response, indent=2, sort_keys=True))
    archive_request(paths, request.meta.request_id)
    archive_response(paths, request.meta.request_id)


if __name__ == "__main__":
    main()

"""Editor-side file transport handler v3 for canonical typed bridge requests.

This handler intentionally accepts only the typed request envelope used by the
WSL bridge package:
- top-level request body fields like `project_id`
- shared metadata under `meta.request_id` and `meta.tool_name`

It remains intentionally narrow and handles only `project_scan`.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
INBOX = BRIDGE_ROOT / "inbox"
OUTBOX = BRIDGE_ROOT / "outbox"
ARCHIVE = BRIDGE_ROOT / "archive"


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def detect_project_name() -> str | None:
    cwd_parts = Path(os.getcwd()).parts
    if "Projects" in cwd_parts:
        index = cwd_parts.index("Projects")
        if index + 1 < len(cwd_parts):
            return cwd_parts[index + 1]
    return None


def error_response(
    *,
    request_id: str,
    tool_name: str,
    code: str,
    message: str,
    target: str,
) -> dict[str, object]:
    return {
        "request_id": request_id,
        "tool_name": tool_name,
        "ok": False,
        "data": None,
        "warnings": [],
        "errors": [{
            "code": code,
            "message": message,
            "retryable": False,
            "target": target,
        }],
        "logs": [{
            "level": "error",
            "message": "windows file transport handler v3 rejected request",
            "code": code,
            "target": target,
        }],
        "requires_approval": False,
        "approval_level": "none",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def build_response(request: dict[str, object]) -> dict[str, object]:
    meta = request.get("meta")
    if not isinstance(meta, dict):
        return error_response(
            request_id="unknown-request",
            tool_name="unknown-tool",
            code="INVALID_REQUEST",
            message="Request must include object field: meta",
            target="meta",
        )

    request_id = meta.get("request_id", "unknown-request")
    tool_name = meta.get("tool_name", "unknown-tool")

    if not isinstance(request_id, str) or not request_id.strip():
        return error_response(
            request_id="unknown-request",
            tool_name=tool_name if isinstance(tool_name, str) else "unknown-tool",
            code="INVALID_REQUEST",
            message="Request meta.request_id must be a non-empty string",
            target="meta.request_id",
        )

    if not isinstance(tool_name, str) or not tool_name.strip():
        return error_response(
            request_id=request_id,
            tool_name="unknown-tool",
            code="INVALID_REQUEST",
            message="Request meta.tool_name must be a non-empty string",
            target="meta.tool_name",
        )

    if tool_name != "project_scan":
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="TOOL_NOT_ALLOWED",
            message=f"Unsupported tool for v3 handler: {tool_name}",
            target="meta.tool_name",
        )

    project_id = request.get("project_id")
    if not isinstance(project_id, str) or not project_id.strip():
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="INVALID_PROJECT_ID",
            message="Request project_id must be a non-empty string",
            target="project_id",
        )

    return {
        "request_id": request_id,
        "tool_name": tool_name,
        "ok": True,
        "data": {
            "project_id": project_id,
            "project_found": detect_project_name() == project_id,
            "project_name_guess": detect_project_name(),
            "scenes": [],
            "assets": [],
            "editor_state": {
                "running": True,
            },
            "cwd": os.getcwd(),
            "cwd_exists": os.path.isdir(os.getcwd()),
        },
        "warnings": [],
        "errors": [],
        "logs": [{
            "level": "info",
            "message": "windows file transport handler v3 executed",
            "code": None,
            "target": None,
        }],
        "requires_approval": False,
        "approval_level": "none",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def archive_request(request_path: Path) -> Path:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    destination = ARCHIVE / request_path.name
    request_path.replace(destination)
    return destination


def main() -> None:
    request_path = newest_request_file()
    if request_path is None:
        print("No request files found in inbox.")
        return

    request = json.loads(request_path.read_text(encoding="utf-8"))
    response = build_response(request)

    OUTBOX.mkdir(parents=True, exist_ok=True)
    response_path = OUTBOX / f"{response['request_id']}.response.json"
    response_path.write_text(json.dumps(response, indent=2, sort_keys=True), encoding="utf-8")
    archive_request(request_path)
    print(json.dumps(response, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

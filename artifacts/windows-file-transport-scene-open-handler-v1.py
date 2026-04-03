"""Editor-side file transport handler v1 for narrow, approval-gated scene_open.

This handler is intentionally restricted for the first live proof:
- accepts only the typed bridge envelope
- accepts only tool_name == scene_open
- accepts only project_id == McpSandbox
- accepts only scene_name == TestLevel01
- requires a non-empty approval_token
- invokes the editor-native open level binding
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import azlmbr.legacy.general as general

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
INBOX = BRIDGE_ROOT / "inbox"
OUTBOX = BRIDGE_ROOT / "outbox"
ARCHIVE = BRIDGE_ROOT / "archive"
ALLOWED_PROJECT_ID = "McpSandbox"
ALLOWED_SCENE_NAME = "TestLoevel01"


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def current_level_name() -> str | None:
    try:
        name = general.get_current_level_name()
    except Exception:
        return None
    return name if isinstance(name, str) and name else None


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
        "data": {
            "project_id": ALLOWED_PROJECT_ID,
            "scene_name": ALLOWED_SCENE_NAME,
            "opened": False,
            "already_open": False,
        },
        "warnings": [],
        "errors": [{
            "code": code,
            "message": message,
            "retryable": False,
            "target": target,
        }],
        "logs": [{
            "level": "error",
            "message": "windows scene_open handler rejected request",
            "code": code,
            "target": target,
        }],
        "requires_approval": True,
        "approval_level": "confirm",
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
    approval_token = meta.get("approval_token")

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

    if tool_name != "scene_open":
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="TOOL_NOT_ALLOWED",
            message=f"Unsupported tool for scene_open handler: {tool_name}",
            target="meta.tool_name",
        )

    if not isinstance(approval_token, str) or not approval_token.strip():
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="APPROVAL_REQUIRED",
            message="scene_open requires a non-empty approval_token",
            target="approval_token",
        )

    project_id = request.get("project_id")
    scene_name = request.get("scene_name")

    if project_id != ALLOWED_PROJECT_ID:
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="INVALID_PROJECT_ID",
            message=f"Initial live scene_open is restricted to project_id={ALLOWED_PROJECT_ID}",
            target="project_id",
        )

    if scene_name != ALLOWED_SCENE_NAME:
        return error_response(
            request_id=request_id,
            tool_name=tool_name,
            code="INVALID_SCENE_NAME",
            message=f"Initial live scene_open is restricted to scene_name={ALLOWED_SCENE_NAME}",
            target="scene_name",
        )

    already_open = current_level_name() == scene_name
    opened = True if already_open else bool(general.open_level_no_prompt(scene_name))

    return {
        "request_id": request_id,
        "tool_name": tool_name,
        "ok": opened,
        "data": {
            "project_id": project_id,
            "scene_name": scene_name,
            "opened": opened,
            "already_open": already_open,
            "cwd": os.getcwd(),
            "cwd_exists": os.path.isdir(os.getcwd()),
        },
        "warnings": [],
        "errors": [] if opened else [{
            "code": "SCENE_NOT_FOUND",
            "message": f"Failed to open scene: {scene_name}",
            "retryable": False,
            "target": "scene_name",
        }],
        "logs": [{
            "level": "info",
            "message": "windows scene_open handler executed",
            "code": None,
            "target": None,
        }],
        "requires_approval": True,
        "approval_level": "confirm",
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

"""Shared helpers for Windows-side O3DE bridge handlers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
INBOX = BRIDGE_ROOT / "inbox"
OUTBOX = BRIDGE_ROOT / "outbox"
ARCHIVE = BRIDGE_ROOT / "archive"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def load_request(request_path: Path) -> dict[str, object]:
    return json.loads(request_path.read_text(encoding="utf-8"))


def archive_request(request_path: Path) -> Path:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    destination = ARCHIVE / request_path.name
    request_path.replace(destination)
    return destination


def write_response(response: dict[str, object]) -> Path:
    OUTBOX.mkdir(parents=True, exist_ok=True)
    response_path = OUTBOX / f"{response['request_id']}.response.json"
    response_path.write_text(json.dumps(response, indent=2, sort_keys=True), encoding="utf-8")
    return response_path


def build_error_response(
    *,
    request_id: str,
    tool_name: str,
    code: str,
    message: str,
    target: str,
    data: dict[str, object],
    requires_approval: bool,
    approval_level: str,
    log_message: str,
) -> dict[str, object]:
    return {
        'request_id': request_id,
        'tool_name': tool_name,
        'ok': False,
        'data': data,
        'warnings': [],
        'errors': [{
            'code': code,
            'message': message,
            'retryable': False,
            'target': target,
        }],
        'logs': [{
            'level': 'error',
            'message': log_message,
            'code': code,
            'target': target,
        }],
        'requires_approval': requires_approval,
        'approval_level': approval_level,
        'timestamp': iso_now(),
    }


def print_and_persist_response(response: dict[str, object], request_path: Path) -> None:
    write_response(response)
    archive_request(request_path)
    print(json.dumps(response, indent=2, sort_keys=True))


def require_meta(request: dict[str, object], tool_name: str, default_data: dict[str, object], requires_approval: bool, approval_level: str):
    meta = request.get('meta')
    if not isinstance(meta, dict):
        return None, build_error_response(
            request_id='unknown-request',
            tool_name=tool_name,
            code='INVALID_REQUEST',
            message='Request must include object field: meta',
            target='meta',
            data=default_data,
            requires_approval=requires_approval,
            approval_level=approval_level,
            log_message=f'windows {tool_name} handler rejected request',
        )
    return meta, None


def require_tool_name(meta: dict[str, object], expected_tool_name: str, default_data: dict[str, object], requires_approval: bool, approval_level: str):
    request_id = meta.get('request_id', 'unknown-request')
    tool_name = meta.get('tool_name')
    if tool_name != expected_tool_name:
        return build_error_response(
            request_id=request_id,
            tool_name=expected_tool_name,
            code='TOOL_NOT_ALLOWED',
            message=f'{expected_tool_name} handler only accepts {expected_tool_name}',
            target='meta.tool_name',
            data=default_data,
            requires_approval=requires_approval,
            approval_level=approval_level,
            log_message=f'windows {expected_tool_name} handler rejected request',
        )
    return None


def require_approval_token(meta: dict[str, object], tool_name: str, default_data: dict[str, object], approval_level: str):
    request_id = meta.get('request_id', 'unknown-request')
    approval_token = meta.get('approval_token')
    if not isinstance(approval_token, str) or not approval_token.strip():
        return build_error_response(
            request_id=request_id,
            tool_name=tool_name,
            code='APPROVAL_REQUIRED',
            message=f'{tool_name} requires a non-empty approval_token',
            target='approval_token',
            data=default_data,
            requires_approval=True,
            approval_level=approval_level,
            log_message=f'windows {tool_name} handler rejected request',
        )
    return None

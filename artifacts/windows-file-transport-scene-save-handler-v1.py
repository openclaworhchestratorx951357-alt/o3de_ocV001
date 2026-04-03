"""Editor-side file transport handler v1 for narrow approval-gated scene_save."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import azlmbr.bus as bus
import azlmbr.editor as editor
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


def get_current_level_name() -> str:
    return editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName')


def error_response(*, request_id: str, code: str, message: str, target: str) -> dict[str, object]:
    return {
        'request_id': request_id,
        'tool_name': 'scene_save',
        'ok': False,
        'data': {
            'project_id': ALLOWED_PROJECT_ID,
            'scene_name': ALLOWED_SCENE_NAME,
            'saved': False,
        },
        'warnings': [],
        'errors': [{
            'code': code,
            'message': message,
            'retryable': False,
            'target': target,
        }],
        'logs': [{
            'level': 'error',
            'message': 'windows scene_save handler rejected request',
            'code': code,
            'target': target,
        }],
        'requires_approval': True,
        'approval_level': 'confirm',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def build_response(request: dict[str, object]) -> dict[str, object]:
    meta = request.get('meta')
    if not isinstance(meta, dict):
        return error_response(request_id='unknown-request', code='INVALID_REQUEST', message='Request must include object field: meta', target='meta')

    request_id = meta.get('request_id', 'unknown-request')
    tool_name = meta.get('tool_name')
    approval_token = meta.get('approval_token')

    if tool_name != 'scene_save':
        return error_response(request_id=request_id, code='TOOL_NOT_ALLOWED', message='scene_save handler only accepts scene_save', target='meta.tool_name')
    if not isinstance(approval_token, str) or not approval_token.strip():
        return error_response(request_id=request_id, code='APPROVAL_REQUIRED', message='scene_save requires a non-empty approval_token', target='approval_token')

    project_id = request.get('project_id')
    scene_name = request.get('scene_name')
    if project_id != ALLOWED_PROJECT_ID:
        return error_response(request_id=request_id, code='INVALID_PROJECT_ID', message=f'Initial live scene_save is restricted to {ALLOWED_PROJECT_ID}', target='project_id')
    if scene_name != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='INVALID_SCENE_NAME', message=f'Initial live scene_save is restricted to {ALLOWED_SCENE_NAME}', target='scene_name')
    if get_current_level_name() != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='SCENE_MISMATCH', message=f'Current level is not {ALLOWED_SCENE_NAME}', target='scene_name')

    saved = bool(general.save_level())

    return {
        'request_id': request_id,
        'tool_name': 'scene_save',
        'ok': saved,
        'data': {
            'project_id': project_id,
            'scene_name': scene_name,
            'saved': saved,
        },
        'warnings': [],
        'errors': [] if saved else [{
            'code': 'SAVE_FAILED',
            'message': f'Failed to save scene: {scene_name}',
            'retryable': False,
            'target': 'scene_name',
        }],
        'logs': [{
            'level': 'info',
            'message': 'windows scene_save handler executed',
            'code': None,
            'target': None,
        }],
        'requires_approval': True,
        'approval_level': 'confirm',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def archive_request(request_path: Path) -> Path:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    destination = ARCHIVE / request_path.name
    request_path.replace(destination)
    return destination


def main() -> None:
    request_path = newest_request_file()
    if request_path is None:
        print('No request files found in inbox.')
        return

    request = json.loads(request_path.read_text(encoding='utf-8'))
    response = build_response(request)

    OUTBOX.mkdir(parents=True, exist_ok=True)
    response_path = OUTBOX / f"{response['request_id']}.response.json"
    response_path.write_text(json.dumps(response, indent=2, sort_keys=True), encoding='utf-8')
    archive_request(request_path)
    print(json.dumps(response, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

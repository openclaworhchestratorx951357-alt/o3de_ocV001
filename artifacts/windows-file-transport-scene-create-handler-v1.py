"""Editor-side file transport handler v1 for narrow approval-gated scene_create."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import azlmbr.bus as bus
import azlmbr.editor as editor

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
INBOX = BRIDGE_ROOT / "inbox"
OUTBOX = BRIDGE_ROOT / "outbox"
ARCHIVE = BRIDGE_ROOT / "archive"
ALLOWED_PROJECT_ID = "McpSandbox"
ALLOWED_SCENE_NAME = "BridgeLevel01"
ALLOWED_TEMPLATE = "Prefabs/Default_Level.prefab"
SUCCESS_RESULT = 0


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def error_response(*, request_id: str, code: str, message: str, target: str) -> dict[str, object]:
    return {
        'request_id': request_id,
        'tool_name': 'scene_create',
        'ok': False,
        'data': {
            'project_id': ALLOWED_PROJECT_ID,
            'scene_name': ALLOWED_SCENE_NAME,
            'created': False,
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
            'message': 'windows scene_create handler rejected request',
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

    if tool_name != 'scene_create':
        return error_response(request_id=request_id, code='TOOL_NOT_ALLOWED', message='scene_create handler only accepts scene_create', target='meta.tool_name')
    if not isinstance(approval_token, str) or not approval_token.strip():
        return error_response(request_id=request_id, code='APPROVAL_REQUIRED', message='scene_create requires a non-empty approval_token', target='approval_token')

    project_id = request.get('project_id')
    scene_name = request.get('scene_name')
    template = request.get('template')

    if project_id != ALLOWED_PROJECT_ID:
        return error_response(request_id=request_id, code='INVALID_PROJECT_ID', message=f'Initial live scene_create is restricted to {ALLOWED_PROJECT_ID}', target='project_id')
    if scene_name != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='INVALID_SCENE_NAME', message=f'Initial live scene_create is restricted to {ALLOWED_SCENE_NAME}', target='scene_name')
    if template != ALLOWED_TEMPLATE:
        return error_response(request_id=request_id, code='INVALID_REQUEST', message=f'Initial live scene_create is restricted to template={ALLOWED_TEMPLATE}', target='template')

    result_code = editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'CreateLevelNoPrompt', ALLOWED_TEMPLATE, ALLOWED_SCENE_NAME, 1024, False)
    created = result_code == SUCCESS_RESULT

    return {
        'request_id': request_id,
        'tool_name': 'scene_create',
        'ok': created,
        'data': {
            'project_id': project_id,
            'scene_name': scene_name,
            'created': created,
        },
        'warnings': [],
        'errors': [] if created else [{
            'code': 'CREATE_FAILED',
            'message': f'Failed to create scene: {scene_name} (result={result_code})',
            'retryable': False,
            'target': 'scene_name',
        }],
        'logs': [{
            'level': 'info',
            'message': f'windows scene_create handler executed (result={result_code})',
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

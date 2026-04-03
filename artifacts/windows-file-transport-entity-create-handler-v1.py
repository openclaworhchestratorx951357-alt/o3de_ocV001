"""Editor-side file transport handler v1 for narrow approval-gated entity_create."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
INBOX = BRIDGE_ROOT / "inbox"
OUTBOX = BRIDGE_ROOT / "outbox"
ARCHIVE = BRIDGE_ROOT / "archive"
ALLOWED_PROJECT_ID = "McpSandbox"
ALLOWED_SCENE_NAME = "TestLoevel01"
ALLOWED_ENTITY_NAME = "bridge_entity_01"
ALLOWED_COMPONENTS = {"Camera", "Mesh"}


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def find_entity_by_name(name: str):
    search_filter = entity.SearchFilter()
    search_filter.names = [name]
    matches = entity.SearchBus(bus.Broadcast, 'SearchEntities', search_filter)
    return matches[0] if matches else None


def error_response(*, request_id: str, code: str, message: str, target: str) -> dict[str, object]:
    return {
        'request_id': request_id,
        'tool_name': 'entity_create',
        'ok': False,
        'data': {
            'project_id': ALLOWED_PROJECT_ID,
            'scene_name': ALLOWED_SCENE_NAME,
            'entity_name': ALLOWED_ENTITY_NAME,
            'entity_created': False,
            'components_added': [],
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
            'message': 'windows entity_create handler rejected request',
            'code': code,
            'target': target,
        }],
        'requires_approval': True,
        'approval_level': 'confirm',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def get_current_level_name() -> str:
    return editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName')


def component_type_ids(names: list[str]):
    return editor.EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdsByEntityType', names, entity.EntityType().Game)


def build_response(request: dict[str, object]) -> dict[str, object]:
    meta = request.get('meta')
    if not isinstance(meta, dict):
        return error_response(request_id='unknown-request', code='INVALID_REQUEST', message='Request must include object field: meta', target='meta')

    request_id = meta.get('request_id', 'unknown-request')
    tool_name = meta.get('tool_name')
    approval_token = meta.get('approval_token')

    if tool_name != 'entity_create':
        return error_response(request_id=request_id, code='TOOL_NOT_ALLOWED', message='entity_create handler only accepts entity_create', target='meta.tool_name')
    if not isinstance(approval_token, str) or not approval_token.strip():
        return error_response(request_id=request_id, code='APPROVAL_REQUIRED', message='entity_create requires a non-empty approval_token', target='approval_token')

    project_id = request.get('project_id')
    scene_name = request.get('scene_name')
    entity_name = request.get('entity_name')
    components = request.get('components')

    if project_id != ALLOWED_PROJECT_ID:
        return error_response(request_id=request_id, code='INVALID_PROJECT_ID', message=f'Initial live entity_create is restricted to {ALLOWED_PROJECT_ID}', target='project_id')
    if scene_name != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='INVALID_SCENE_NAME', message=f'Initial live entity_create is restricted to {ALLOWED_SCENE_NAME}', target='scene_name')
    if entity_name != ALLOWED_ENTITY_NAME:
        return error_response(request_id=request_id, code='INVALID_ENTITY_NAME', message=f'Initial live entity_create is restricted to {ALLOWED_ENTITY_NAME}', target='entity_name')
    if get_current_level_name() != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='SCENE_MISMATCH', message=f'Current level is not {ALLOWED_SCENE_NAME}', target='scene_name')
    if find_entity_by_name(ALLOWED_ENTITY_NAME) is not None:
        return error_response(request_id=request_id, code='ENTITY_ALREADY_EXISTS', message=f'Entity already exists: {ALLOWED_ENTITY_NAME}', target='entity_name')
    if not isinstance(components, list) or not components:
        return error_response(request_id=request_id, code='INVALID_REQUEST', message='components must be a non-empty list', target='components')

    component_names = []
    for component in components:
        if not isinstance(component, dict) or component.get('type') not in ALLOWED_COMPONENTS:
            return error_response(request_id=request_id, code='INVALID_COMPONENT', message='Only Camera and Mesh are allowed in the first live entity_create proof', target='components')
        component_names.append(component['type'])

    new_entity_id = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', entity.EntityId())
    editor.EditorEntityAPIBus(bus.Event, 'SetName', new_entity_id, ALLOWED_ENTITY_NAME)

    type_ids = component_type_ids(component_names)
    add_outcome = editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType', new_entity_id, type_ids)
    if not add_outcome.IsSuccess():
        return error_response(request_id=request_id, code='COMPONENT_ADD_FAILED', message='Failed to add requested components', target='components')

    return {
        'request_id': request_id,
        'tool_name': 'entity_create',
        'ok': True,
        'data': {
            'project_id': project_id,
            'scene_name': scene_name,
            'entity_name': ALLOWED_ENTITY_NAME,
            'entity_created': True,
            'components_added': component_names,
        },
        'warnings': [],
        'errors': [],
        'logs': [{
            'level': 'info',
            'message': 'windows entity_create handler executed',
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

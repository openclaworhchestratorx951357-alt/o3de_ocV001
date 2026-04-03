"""Editor-side file transport handler v1 for narrow scene_validate.

This first live validator is intentionally restricted to the verified current scene
and one verified entity name. It validates:
- current scene identity
- expected entity existence
- Camera component presence
- Mesh component presence
"""

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
ALLOWED_ENTITY_NAME = "test entity"


def newest_request_file() -> Path | None:
    candidates = sorted(INBOX.glob("*.json"), key=lambda path: path.stat().st_mtime)
    return candidates[-1] if candidates else None


def error_response(*, request_id: str, code: str, message: str, target: str) -> dict[str, object]:
    return {
        "request_id": request_id,
        "tool_name": "scene_validate",
        "ok": False,
        "data": {
            "project_id": ALLOWED_PROJECT_ID,
            "scene_name": ALLOWED_SCENE_NAME,
            "valid": False,
            "issues": [],
            "entities": [],
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
            "message": "windows scene_validate handler rejected request",
            "code": code,
            "target": target,
        }],
        "requires_approval": False,
        "approval_level": "none",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def get_current_level_name() -> str:
    return editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName')


def get_name(entity_id):
    return editor.EditorEntityInfoRequestBus(bus.Event, 'GetName', entity_id)


def find_entity_by_name(name: str):
    search_filter = entity.SearchFilter()
    search_filter.names = [name]
    matches = entity.SearchBus(bus.Broadcast, 'SearchEntities', search_filter)
    return matches[0] if matches else None


def get_component_type_ids(type_names: list[str]):
    return editor.EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdsByEntityType', type_names, entity.EntityType().Game)


def entity_has_component(entity_id, component_type_id) -> bool:
    return editor.EditorComponentAPIBus(bus.Broadcast, 'HasComponentOfType', entity_id, component_type_id)


def build_response(request: dict[str, object]) -> dict[str, object]:
    meta = request.get('meta')
    if not isinstance(meta, dict):
        return error_response(request_id='unknown-request', code='INVALID_REQUEST', message='Request must include object field: meta', target='meta')

    request_id = meta.get('request_id', 'unknown-request')
    tool_name = meta.get('tool_name')
    if tool_name != 'scene_validate':
        return error_response(request_id=request_id, code='TOOL_NOT_ALLOWED', message='scene_validate handler only accepts scene_validate', target='meta.tool_name')

    project_id = request.get('project_id')
    scene_name = request.get('scene_name')
    expected_entities = request.get('expected_entities')

    if project_id != ALLOWED_PROJECT_ID:
        return error_response(request_id=request_id, code='INVALID_PROJECT_ID', message=f'Initial live scene_validate is restricted to {ALLOWED_PROJECT_ID}', target='project_id')
    if scene_name != ALLOWED_SCENE_NAME:
        return error_response(request_id=request_id, code='INVALID_SCENE_NAME', message=f'Initial live scene_validate is restricted to {ALLOWED_SCENE_NAME}', target='scene_name')
    if not isinstance(expected_entities, list) or len(expected_entities) != 1:
        return error_response(request_id=request_id, code='INVALID_REQUEST', message='Initial live scene_validate requires exactly one expected entity', target='expected_entities')

    expected_entity = expected_entities[0]
    if not isinstance(expected_entity, dict) or expected_entity.get('entity_name') != ALLOWED_ENTITY_NAME:
        return error_response(request_id=request_id, code='INVALID_ENTITY_NAME', message=f'Initial live scene_validate is restricted to entity_name={ALLOWED_ENTITY_NAME}', target='expected_entities[0].entity_name')

    current_level_name = get_current_level_name()
    entity_id = find_entity_by_name(ALLOWED_ENTITY_NAME)
    exists = entity_id is not None

    camera_type_id, mesh_type_id = get_component_type_ids(['Camera', 'Mesh'])
    has_camera = entity_has_component(entity_id, camera_type_id) if exists else False
    has_mesh = entity_has_component(entity_id, mesh_type_id) if exists else False

    issues = []
    if current_level_name != ALLOWED_SCENE_NAME:
        issues.append({
            'code': 'SCENE_MISMATCH',
            'message': f'Current level is {current_level_name}, expected {ALLOWED_SCENE_NAME}',
            'severity': 'error',
            'target': 'scene_name',
        })
    if not exists:
        issues.append({
            'code': 'ENTITY_MISSING',
            'message': f'Expected entity not found: {ALLOWED_ENTITY_NAME}',
            'severity': 'error',
            'target': 'expected_entities[0].entity_name',
        })
    if exists and not has_camera:
        issues.append({
            'code': 'CAMERA_MISSING',
            'message': f'Camera component missing on entity: {ALLOWED_ENTITY_NAME}',
            'severity': 'error',
            'target': 'expected_entities[0].required_components',
        })
    if exists and not has_mesh:
        issues.append({
            'code': 'MESH_MISSING',
            'message': f'Mesh component missing on entity: {ALLOWED_ENTITY_NAME}',
            'severity': 'error',
            'target': 'expected_entities[0].required_components',
        })

    valid = len(issues) == 0

    return {
        'request_id': request_id,
        'tool_name': 'scene_validate',
        'ok': True,
        'data': {
            'project_id': project_id,
            'scene_name': scene_name,
            'valid': valid,
            'issues': issues,
            'entities': [{
                'entity_name': ALLOWED_ENTITY_NAME,
                'exists': exists,
                'has_camera': has_camera,
                'has_mesh': has_mesh,
                'asset_assignment': None,
            }],
        },
        'warnings': [],
        'errors': [],
        'logs': [{
            'level': 'info',
            'message': 'windows scene_validate handler executed',
            'code': None,
            'target': None,
        }],
        'requires_approval': False,
        'approval_level': 'none',
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

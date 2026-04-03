"""Editor-side file transport handler v1 for narrow scene_validate."""

from __future__ import annotations

import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity

from windows_bridge_common import (
    build_error_response,
    iso_now,
    load_request,
    newest_request_file,
    print_and_persist_response,
    require_meta,
    require_tool_name,
)

ALLOWED_PROJECT_ID = "McpSandbox"
ALLOWED_SCENE_NAME = "TestLoevel01"
ALLOWED_ENTITY_NAME = "test entity"
DEFAULT_DATA = {
    'project_id': ALLOWED_PROJECT_ID,
    'scene_name': ALLOWED_SCENE_NAME,
    'valid': False,
    'issues': [],
    'entities': [],
}


def get_current_level_name() -> str:
    return editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName')


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
    meta, error = require_meta(request, 'scene_validate', DEFAULT_DATA, False, 'none')
    if error:
        return error

    request_id = meta.get('request_id', 'unknown-request')

    error = require_tool_name(meta, 'scene_validate', DEFAULT_DATA, False, 'none')
    if error:
        return error

    project_id = request.get('project_id')
    scene_name = request.get('scene_name')
    expected_entities = request.get('expected_entities')

    if project_id != ALLOWED_PROJECT_ID:
        return build_error_response(request_id=request_id, tool_name='scene_validate', code='INVALID_PROJECT_ID', message=f'Initial live scene_validate is restricted to {ALLOWED_PROJECT_ID}', target='project_id', data=DEFAULT_DATA, requires_approval=False, approval_level='none', log_message='windows scene_validate handler rejected request')
    if scene_name != ALLOWED_SCENE_NAME:
        return build_error_response(request_id=request_id, tool_name='scene_validate', code='INVALID_SCENE_NAME', message=f'Initial live scene_validate is restricted to {ALLOWED_SCENE_NAME}', target='scene_name', data=DEFAULT_DATA, requires_approval=False, approval_level='none', log_message='windows scene_validate handler rejected request')
    if not isinstance(expected_entities, list) or len(expected_entities) != 1:
        return build_error_response(request_id=request_id, tool_name='scene_validate', code='INVALID_REQUEST', message='Initial live scene_validate requires exactly one expected entity', target='expected_entities', data=DEFAULT_DATA, requires_approval=False, approval_level='none', log_message='windows scene_validate handler rejected request')

    expected_entity = expected_entities[0]
    if not isinstance(expected_entity, dict) or expected_entity.get('entity_name') != ALLOWED_ENTITY_NAME:
        return build_error_response(request_id=request_id, tool_name='scene_validate', code='INVALID_ENTITY_NAME', message=f'Initial live scene_validate is restricted to entity_name={ALLOWED_ENTITY_NAME}', target='expected_entities[0].entity_name', data=DEFAULT_DATA, requires_approval=False, approval_level='none', log_message='windows scene_validate handler rejected request')

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
        'timestamp': iso_now(),
    }


def main() -> None:
    request_path = newest_request_file()
    if request_path is None:
        print('No request files found in inbox.')
        return

    request = load_request(request_path)
    response = build_response(request)
    print_and_persist_response(response, request_path)


if __name__ == '__main__':
    main()

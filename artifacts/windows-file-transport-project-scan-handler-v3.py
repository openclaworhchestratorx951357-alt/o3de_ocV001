"""Editor-side file transport handler v3 for canonical typed bridge requests."""

from __future__ import annotations

import os
from pathlib import Path

from windows_bridge_common import (
    build_error_response,
    iso_now,
    load_request,
    newest_request_file,
    print_and_persist_response,
    require_meta,
    require_tool_name,
)

ALLOWED_TOOL_NAME = 'project_scan'
DEFAULT_DATA = {
    'project_id': 'McpSandbox',
    'project_found': False,
    'project_name_guess': None,
    'scenes': [],
    'assets': [],
    'editor_state': {'running': True},
    'cwd': None,
    'cwd_exists': False,
}


def detect_project_name() -> str | None:
    cwd_parts = Path(os.getcwd()).parts
    if 'Projects' in cwd_parts:
        index = cwd_parts.index('Projects')
        if index + 1 < len(cwd_parts):
            return cwd_parts[index + 1]
    return None


def build_response(request: dict[str, object]) -> dict[str, object]:
    meta, error = require_meta(request, ALLOWED_TOOL_NAME, DEFAULT_DATA, False, 'none')
    if error:
        return error

    request_id = meta.get('request_id', 'unknown-request')

    error = require_tool_name(meta, ALLOWED_TOOL_NAME, DEFAULT_DATA, False, 'none')
    if error:
        return error

    project_id = request.get('project_id')
    if not isinstance(project_id, str) or not project_id.strip():
        return build_error_response(request_id=request_id, tool_name=ALLOWED_TOOL_NAME, code='INVALID_PROJECT_ID', message='Request project_id must be a non-empty string', target='project_id', data=DEFAULT_DATA, requires_approval=False, approval_level='none', log_message='windows project_scan handler rejected request')

    project_name_guess = detect_project_name()

    return {
        'request_id': request_id,
        'tool_name': ALLOWED_TOOL_NAME,
        'ok': True,
        'data': {
            'project_id': project_id,
            'project_found': project_name_guess == project_id,
            'project_name_guess': project_name_guess,
            'scenes': [],
            'assets': [],
            'editor_state': {
                'running': True,
            },
            'cwd': os.getcwd(),
            'cwd_exists': os.path.isdir(os.getcwd()),
        },
        'warnings': [],
        'errors': [],
        'logs': [{
            'level': 'info',
            'message': 'windows file transport handler v3 executed',
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

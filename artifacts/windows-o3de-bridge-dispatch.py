"""Single editor-side dispatch runner for the proven six-tool bridge surface."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BRIDGE_ROOT = Path(r"C:\Users\topgu\O3DEBridge")
WORKSPACE_ARTIFACTS = Path(r"C:\Users\topgu\Dropbox\O3DE-OpenClaw\handlers")
REQUEST_TOOL_TO_HANDLER = {
    'project_scan': 'windows-file-transport-project-scan-handler-v3.py',
    'scene_open': 'windows-file-transport-scene-open-handler-v1.py',
    'scene_create': 'windows-file-transport-scene-create-handler-v1.py',
    'entity_create': 'windows-file-transport-entity-create-handler-v1.py',
    'scene_save': 'windows-file-transport-scene-save-handler-v1.py',
    'scene_validate': 'windows-file-transport-scene-validate-handler-v1.py',
}


def load_module_from_path(module_name: str, path: Path):
    parent = str(path.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_newest_request_tool_name() -> str | None:
    inbox = BRIDGE_ROOT / 'inbox'
    candidates = sorted(inbox.glob('*.json'), key=lambda p: p.stat().st_mtime)
    if not candidates:
        return None
    import json
    request = json.loads(candidates[-1].read_text(encoding='utf-8'))
    meta = request.get('meta', {})
    if isinstance(meta, dict):
        tool_name = meta.get('tool_name')
        return tool_name if isinstance(tool_name, str) and tool_name else None
    return None


def main() -> None:
    tool_name = read_newest_request_tool_name()
    if tool_name is None:
        return

    handler_filename = REQUEST_TOOL_TO_HANDLER.get(tool_name)
    if handler_filename is None:
        print(f'No handler registered for tool: {tool_name}')
        return

    handler_path = WORKSPACE_ARTIFACTS / handler_filename
    module_name = handler_filename.replace('-', '_').replace('.py', '')
    module = load_module_from_path(module_name, handler_path)
    module.main()


if __name__ == '__main__':
    main()

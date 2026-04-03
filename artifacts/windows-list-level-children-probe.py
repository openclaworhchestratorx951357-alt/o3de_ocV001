"""List the root level entity and its immediate children in the current O3DE editor scene."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity


def get_name(entity_id):
    try:
        return editor.EditorEntityInfoRequestBus(bus.Event, 'GetName', entity_id)
    except Exception:
        return None


def get_children(entity_id):
    try:
        return editor.EditorEntityInfoRequestBus(bus.Event, 'GetChildren', entity_id)
    except Exception:
        return []


def normalize_entity_id(entity_id):
    try:
        return str(entity_id.ToString())
    except Exception:
        return str(entity_id)


def main():
    root_ids = entity.SearchBus(bus.Broadcast, 'GetRootEditorEntities')
    root_entities = []

    for root_id in root_ids:
        children = []
        for child_id in get_children(root_id):
            children.append({
                'id': normalize_entity_id(child_id),
                'name': get_name(child_id),
            })

        root_entities.append({
            'id': normalize_entity_id(root_id),
            'name': get_name(root_id),
            'children': children,
        })

    result = {
        'ok': True,
        'probe': 'level_children',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'current_level_name': editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName'),
        'current_level_path': editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelPath'),
        'root_entities': root_entities,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

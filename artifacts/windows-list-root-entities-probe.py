"""Tiny O3DE editor probe to list current root editor entity ids and names."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity


def entity_name(entity_id):
    try:
        return editor.EditorEntityInfoRequestBus(bus.Event, 'GetName', entity_id)
    except Exception:
        return None


def normalize_entity_id(entity_id):
    try:
        return str(entity_id.ToString())
    except Exception:
        return str(entity_id)


def main():
    root_ids = entity.SearchBus(bus.Broadcast, 'GetRootEditorEntities')
    entities = []
    for entity_id in root_ids:
        entities.append({
            'id': normalize_entity_id(entity_id),
            'name': entity_name(entity_id),
        })

    result = {
        'ok': True,
        'probe': 'root_editor_entities',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'current_level_name': editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelName'),
        'current_level_path': editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetCurrentLevelPath'),
        'root_entities': entities,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

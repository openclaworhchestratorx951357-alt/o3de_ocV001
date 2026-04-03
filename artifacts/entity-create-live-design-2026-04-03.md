# Entity Create Live Design — 2026-04-03

## Purpose
Define the first narrow approval-gated live `entity_create` bridge path after the successful `project_scan`, `scene_open`, and `scene_validate` milestone.

## Why `entity_create` next
- already part of the approved six-tool surface
- naturally follows scene inspection/open/validation
- is the next meaningful mutation step in the vertical slice
- can stay narrow, typed, and approval-gated

## Verified O3DE source grounding
The local O3DE source/tests confirm editor-native creation surfaces exist:

### Entity creation
- `ToolsApplicationRequestBus(..., 'CreateNewEntity', parentId)`
- `ToolsApplicationRequestBus(..., 'CreateNewEntityAtPosition', position, parentId)`

### Entity naming
- `EditorEntityAPIBus(bus.Event, 'SetName', entity_id, name)`

### Component addition
- `EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdsByEntityType', [...], entity.EntityType().Game)`
- `EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType', entity_id, type_ids)`

These are editor-native surfaces, not UI automation hacks.

## Safety stance for v1
The first live `entity_create` proof must remain:
- typed
- approval-gated
- narrow
- deterministic
- fail-closed

## Initial narrowing for the first live proof
Restrict the first live handler to:
- `project_id == "McpSandbox"`
- `scene_name == "TestLoevel01"`
- one specific entity name only
- allowed component set already approved by the bridge: `Camera`, `Mesh`

Recommended first entity name:
- `bridge_entity_01`

Reason:
- explicit and easy to search for
- avoids ambiguity with existing `test entity`
- makes validation straightforward

## Proposed request shape
```json
{
  "meta": {
    "request_id": "entity-create-roundtrip-...",
    "tool_name": "entity_create",
    "dry_run": false,
    "approval_token": "approved-entity-create-v1",
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "TestLoevel01",
  "entity_name": "bridge_entity_01",
  "components": [
    {"type": "Camera"},
    {"type": "Mesh"}
  ]
}
```

## Proposed response shape
Use the existing `EntityCreateData` model:
- `project_id`
- `scene_name`
- `entity_name`
- `entity_created`
- `components_added`

Bridge response should also preserve:
- `requires_approval: true`
- `approval_level: confirm`

## Recommended first live behavior
For v1:
1. validate typed request envelope
2. require approval token
3. reject any project other than `McpSandbox`
4. reject any scene other than `TestLoevel01`
5. reject any entity name other than `bridge_entity_01`
6. reject any component list containing anything other than `Camera` / `Mesh`
7. fail if entity already exists
8. create entity at default position as a child of the level root (or as a root child if the default editor behavior does that in the current level)
9. set entity name
10. add requested components
11. return structured response

## Important follow-up requirement
After the first live `entity_create` proof, immediately validate the new entity via a narrow probe or `scene_validate` extension.

Do not rely on creation response alone.

## Recommendation
Proceed with a very narrow `entity_create` v1 path that creates exactly one known entity name with a small fixed component set and preserves explicit approval requirements.

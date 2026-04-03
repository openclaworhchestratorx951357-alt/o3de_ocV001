# Scene Save Live Design — 2026-04-03

## Purpose
Define the first narrow approval-gated live `scene_save` bridge path after the successful `entity_create` verification.

## Why `scene_save` next
- already part of the approved six-tool surface
- completes the mutation lifecycle after `entity_create`
- is naturally approval-gated
- uses a real editor-native save surface already present in O3DE

## Verified O3DE source grounding
The local O3DE source/tests confirm an editor Python binding for saving the current level:
- `general.save_level()`

This is bound in editor code as:
- `save_level`

It is also used in O3DE Python test scripts.

## Safety stance for v1
The first live `scene_save` proof must remain:
- typed
- approval-gated
- narrow
- deterministic
- fail-closed

## Initial narrowing for the first live proof
Restrict the first live handler to:
- `project_id == "McpSandbox"`
- `scene_name == "TestLoevel01"`
- current open level must already be `TestLoevel01`

## Proposed request shape
```json
{
  "meta": {
    "request_id": "scene-save-roundtrip-...",
    "tool_name": "scene_save",
    "dry_run": false,
    "approval_token": "approved-scene-save-v1",
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "TestLoevel01"
}
```

## Proposed response shape
Use the existing `SceneSaveData` model:
- `project_id`
- `scene_name`
- `saved`

Bridge response should also preserve:
- `requires_approval: true`
- `approval_level: confirm`

## Recommended first live behavior
1. validate typed request envelope
2. require approval token
3. reject any project other than `McpSandbox`
4. reject any scene other than `TestLoevel01`
5. fail if current open level is not `TestLoevel01`
6. invoke editor-native `general.save_level()`
7. return structured response

## Recommendation
Proceed with a narrow `scene_save` v1 handler using `general.save_level()` and verify it before adding broader save/export behavior.

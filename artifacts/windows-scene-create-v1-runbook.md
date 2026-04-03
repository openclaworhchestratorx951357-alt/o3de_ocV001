# Windows Scene Create v1 Runbook

## Goal
Run the first narrow approval-gated live `scene_create` proof.

## Scope
This first handler is intentionally restricted to:
- `project_id == "McpSandbox"`
- `scene_name == "BridgeLevel01"`
- `template == "Prefabs/Default_Level.prefab"`
- non-empty `approval_token`
- no terrain

## Files
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_create_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-scene-create-handler-v1.py`

## Expected behavior
- typed request envelope required
- approval token required
- invokes `EditorToolsApplicationRequestBus(..., 'CreateLevelNoPrompt', ...)`
- treats result code `0` as success
- returns structured response

## Expected success result
- `tool_name: "scene_create"`
- `ok: true`
- `created: true`
- `requires_approval: true`
- `approval_level: "confirm"`

## Important follow-up
After success, immediately validate that the created scene exists and can be opened/inspected.

# Windows Scene Save v1 Runbook

## Goal
Run the first narrow approval-gated live `scene_save` proof.

## Scope
This first handler is intentionally restricted to:
- `project_id == "McpSandbox"`
- `scene_name == "TestLoevel01"`
- non-empty `approval_token`
- current open scene must already be `TestLoevel01`

## Files
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_save_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-scene-save-handler-v1.py`

## Expected behavior
- typed request envelope required
- approval token required
- current scene must match expected scene
- invokes `general.save_level()`
- returns structured response

## Expected success result
- `tool_name: "scene_save"`
- `ok: true`
- `saved: true`
- `requires_approval: true`
- `approval_level: "confirm"`

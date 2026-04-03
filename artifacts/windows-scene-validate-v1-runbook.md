# Windows Scene Validate v1 Runbook

## Goal
Run the first narrow live `scene_validate` proof.

## Scope
This first validator is intentionally restricted to:
- `project_id == "McpSandbox"`
- `scene_name == "TestLoevel01"`
- one expected entity: `test entity`
- required components: `Camera`, `Mesh`

## Validates
- current scene identity
- entity existence
- Camera component presence
- Mesh component presence

## Files
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_validate_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-scene-validate-handler-v1.py`

## Expected output
Structured `scene_validate` result with:
- `valid`
- `issues`
- `entities[0].exists`
- `entities[0].has_camera`
- `entities[0].has_mesh`

## Note
This v1 validator intentionally does not attempt asset-assignment introspection yet.
That should come only after entity/component validation is stable.

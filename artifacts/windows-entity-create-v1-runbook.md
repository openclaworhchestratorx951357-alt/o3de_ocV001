# Windows Entity Create v1 Runbook

## Goal
Run the first narrow approval-gated live `entity_create` proof.

## Scope
This first handler is intentionally restricted to:
- `project_id == "McpSandbox"`
- `scene_name == "TestLoevel01"`
- `entity_name == "bridge_entity_01"`
- components limited to `Camera` and `Mesh`
- non-empty `approval_token`

## Files
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_entity_create_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-entity-create-handler-v1.py`

## Expected behavior
- typed request envelope required
- approval token required
- fails if `bridge_entity_01` already exists
- creates entity
- sets name
- adds Camera + Mesh
- returns structured response

## Expected success result
- `tool_name: "entity_create"`
- `ok: true`
- `entity_created: true`
- `components_added: ["Camera", "Mesh"]`
- `requires_approval: true`
- `approval_level: "confirm"`

## Important follow-up
After success, verify the new entity via a separate validation/probe step.
Do not rely only on the creation response.

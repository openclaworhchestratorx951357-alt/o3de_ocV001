# Windows Scene Open v1 Runbook

## Goal
Perform the first narrow, approval-gated live `scene_open` proof.

## Safety scope for v1
This first live handler is intentionally more restrictive than the general bridge contract.
It allows only:
- `project_id == "McpSandbox"`
- `scene_name == "TestLevel01"`
- non-empty `approval_token`
- `tool_name == "scene_open"`

## Canonical request shape
```json
{
  "meta": {
    "request_id": "scene-open-roundtrip-...",
    "tool_name": "scene_open",
    "dry_run": false,
    "approval_token": "approved-scene-open-v1",
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "TestLevel01"
}
```

## Files involved
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_open_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-scene-open-handler-v1.py`

## Expected behavior
The handler should:
- read the newest inbox request
- validate the typed envelope
- enforce approval token presence
- restrict to `McpSandbox` + `TestLevel01`
- call the editor-native `open_level_no_prompt` binding
- write a structured response to outbox
- archive the consumed request

## Expected success response
At minimum:
- `tool_name: "scene_open"`
- `ok: true`
- `data.project_id: "McpSandbox"`
- `data.scene_name: "TestLevel01"`
- `data.opened`
- `data.already_open`
- `requires_approval: true`
- `approval_level: "confirm"`

## Expected safe failure cases
- missing approval token -> `APPROVAL_REQUIRED`
- wrong project -> `INVALID_PROJECT_ID`
- wrong scene -> `INVALID_SCENE_NAME`
- wrong tool -> `TOOL_NOT_ALLOWED`

## First-run note
Before the first live attempt, ensure inbox/outbox are clean enough that the newest request rule is deterministic.

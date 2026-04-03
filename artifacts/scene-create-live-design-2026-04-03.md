# Scene Create Live Design — 2026-04-03

## Purpose
Define the first narrow approval-gated live `scene_create` bridge path to complete the approved six-tool surface.

## Why `scene_create` next
- it is the remaining approved core operation not yet live-proven
- O3DE exposes editor-native level creation surfaces
- it completes the current Phase 1 narrow surface

## Verified O3DE source grounding
The local O3DE source confirms editor-native creation surfaces exist:
- `EditorToolsApplication::CreateLevel`
- `EditorToolsApplication::CreateLevelNoPrompt`
- legacy general Python bindings:
  - `general.create_level(...)`
  - `general.create_level_no_prompt(...)`

## Safety stance for v1
The first live `scene_create` proof must remain:
- typed
- approval-gated
- narrow
- deterministic
- fail-closed

## Initial narrowing for the first live proof
Restrict the first live handler to:
- `project_id == "McpSandbox"`
- one specific scene name only
- one specific template only
- no terrain

Recommended first test scene name:
- `BridgeLevel01`

Recommended first template:
- `DefaultLevelPrefab`

Reason:
- explicit name
- easy to search for later
- avoids ambiguity with current validated scene `TestLoevel01`

## Proposed request shape
```json
{
  "meta": {
    "request_id": "scene-create-roundtrip-...",
    "tool_name": "scene_create",
    "dry_run": false,
    "approval_token": "approved-scene-create-v1",
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "BridgeLevel01",
  "template": "DefaultLevelPrefab"
}
```

## Expected creation result handling
O3DE returns an integer create-level result code.
For the first live bridge proof, treat result code `0` as success and anything else as failure.

## Recommendation
Proceed with a narrow `scene_create` v1 handler using `general.create_level_no_prompt(...)`, fixed to one approved test scene name and one template, then immediately follow with scene-open/validate if creation succeeds.

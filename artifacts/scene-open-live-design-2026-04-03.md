# Scene Open Live Design — 2026-04-03

## Purpose
Define the next low-risk live bridge operation after `project_scan`, grounded in verified O3DE editor source surfaces and the existing typed bridge contract.

## Why `scene_open` next
- Already part of the approved six-tool surface
- Naturally follows `project_scan`
- Mutating/editor-state-changing, but narrower than entity creation
- Gives us a real approval-gated operation without broadening scope

## Verified O3DE source grounding
The local O3DE source clone includes real editor-side level opening surfaces:

### Python bindings
In `Code/Editor/CryEditPy.cpp` the editor exposes:
- `open_level`
- `open_level_no_prompt`

These are bound into the editor Python surface under the legacy general module.

### Editor application API
In `Code/Editor/EditorToolsApplication.cpp` the editor provides:
- `OpenLevel`
- `OpenLevelNoPrompt`

This confirms there is a real editor-supported level-open path, not a made-up script hack.

## Safety stance for bridge v1
For the bridge, `scene_open` must remain:
- typed
- validated
- approval-gated
- narrow
- fail-closed

Do not expose generic editor command execution.
Do not expose arbitrary Python execution as the user-facing interface.

## Proposed request contract
Reuse the existing typed model already present in the bridge package:

```json
{
  "meta": {
    "request_id": "scene-open-roundtrip-...",
    "tool_name": "scene_open",
    "dry_run": false,
    "approval_token": "...",
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "TestLevel01"
}
```

Important:
- `approval_token` is required because `scene_open` is approval-gated in the bridge approval map
- `scene_name` remains identifier-validated by the current bridge validator

## Proposed response contract
Reuse the existing `SceneOpenData` shape already present in the bridge package:

```json
{
  "request_id": "scene-open-roundtrip-...",
  "tool_name": "scene_open",
  "ok": true,
  "data": {
    "project_id": "McpSandbox",
    "scene_name": "TestLevel01",
    "opened": true,
    "already_open": false
  },
  "warnings": [],
  "errors": [],
  "logs": [...],
  "requires_approval": true,
  "approval_level": "confirm"
}
```

## Narrow live implementation plan
### Phase A — read-only/source-safe preparation
1. Keep `project_scan` path unchanged.
2. Add a dedicated editor-side handler for `scene_open` only after request validation succeeds.
3. Validate:
   - typed `meta`
   - `tool_name == scene_open`
   - `project_id == McpSandbox` (for initial live proof if we want extra narrowing)
   - non-empty valid `scene_name`
   - non-empty `approval_token`

### Phase B — first live operation behavior
For the first live `scene_open` proof:
- prefer the editor-native no-prompt level open surface only if we explicitly decide that is the right operation for the already-saved known test level
- otherwise use the prompt-aware surface and observe behavior

My recommendation for the first controlled live proof:
- target only `TestLevel01`
- use the narrow known project `McpSandbox`
- use the source-grounded editor open-level binding
- log whether the current level already matches the requested level if detectable

## Initial extra guardrails
For the first live `scene_open` attempt, add temporary extra restrictions beyond the generic bridge validators:
- allow only `project_id == McpSandbox`
- allow only `scene_name == TestLevel01`
- reject any other scene name with a structured validation error

This is stricter than the long-term bridge contract, but appropriate for the first live mutation proof.

## Approval handling note
`scene_open` must not silently downgrade approval requirements.
Even if the editor-side implementation is technically simple, the bridge response must preserve:
- `requires_approval: true`
- `approval_level: confirm`

## Suggested first artifact additions
1. `artifacts/windows-file-transport-scene-open-handler-v1.py`
2. `artifacts/windows-scene-open-v1-runbook.md`
3. optional WSL helper mirroring the `project_scan` round-trip runner but for `scene_open`

## Success criteria
A first successful live `scene_open` proof should demonstrate:
- canonical typed request parsing
- required approval token enforcement
- deterministic structured response
- actual editor-native level open path invocation
- no broadening beyond `scene_open`

## Non-goals
- scene creation
- entity mutation
- generic command bus exposure
- multi-scene support on day one
- broad wildcard scene opening

## Recommendation
Proceed with a very narrow `scene_open` v1 design next, but keep the first live handler restricted to:
- `McpSandbox`
- `TestLevel01`
- typed request envelope
- required approval token
- structured response only

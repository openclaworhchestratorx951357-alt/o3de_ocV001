# Scene Validate Live Design — 2026-04-03

## Purpose
Define a narrow live `scene_validate` proof after the successful `project_scan` and approval-gated `scene_open` milestones.

## Why `scene_validate` next
`scene_validate` is a strong next step because it stays read-oriented while checking the exact persistence questions that matter for Phase 0 closeout:
- which scene is currently open
- whether the expected test entity exists
- whether Camera and Mesh are present
- later, whether the expected mesh asset assignment persisted

## Verified O3DE source grounding
### Current level inspection
`EditorToolsApplication` exposes:
- `GetCurrentLevelName`
- `GetCurrentLevelPath`

This gives a clean way to verify the currently open scene.

### Entity search
`AzToolsFramework::EditorEntitySearchComponent` exposes a behavior EBus with:
- `SearchEntities`
- `GetRootEditorEntities`

This confirms the editor has real entity search surfaces rather than forcing UI scraping.

### Component inspection
O3DE source also exposes editor-side component inspection helpers and APIs, including:
- `EditorComponentAPIBus::HasComponentOfType`
- `EditorComponentAPIBus::GetComponentsOfType`
- editor entity helper/component query paths

This is enough basis for a narrow first validator that checks component presence.

## Recommended v1 validation scope
Keep the first live validator narrower than the full long-term contract.

For the first proof, validate only:
1. current open scene identity
2. expected entity existence
3. presence of Camera component
4. presence of Mesh component

Do not block initial progress on asset assignment introspection if that requires deeper property-path work.
Treat asset assignment as a follow-up validation layer after entity/component presence is stable.

## Proposed first live target
Use the verified current saved level name:
- `scene_name == "TestLoevel01"`

And initially validate a single expected entity once its exact name is verified from the editor/project state.

## Request contract
Reuse the existing typed bridge request shape:

```json
{
  "meta": {
    "request_id": "scene-validate-roundtrip-...",
    "tool_name": "scene_validate",
    "dry_run": true,
    "approval_token": null,
    "timestamp": "..."
  },
  "project_id": "McpSandbox",
  "scene_name": "TestLoevel01",
  "expected_entities": [
    {
      "entity_name": "...",
      "required_components": ["Camera", "Mesh"],
      "expected_asset": null
    }
  ]
}
```

## Response contract
Reuse the existing `SceneValidateData` shape:
- `valid`
- `issues`
- `entities[]`
- each entity result includes:
  - `exists`
  - `has_camera`
  - `has_mesh`
  - optional asset assignment section later

## Immediate prerequisite
Before implementing the first live `scene_validate` handler, verify the exact expected entity name from the current level/editor state.

We should not guess the entity name.
We should inspect and use the real current name.

## Suggested implementation order
1. add a tiny editor-side probe to list root/editor entity names for the current level
2. identify the exact target entity name
3. implement a narrow `scene_validate` handler for:
   - `McpSandbox`
   - `TestLoevel01`
   - one expected entity name
4. check scene identity and component presence
5. add asset-assignment validation only after that works

## Recommendation
Proceed with `scene_validate`, but first do one tiny discovery probe to get the exact entity name rather than guessing.
That keeps the next step verification-first and avoids another avoidable naming mismatch.

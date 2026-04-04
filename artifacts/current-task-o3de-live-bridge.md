# Current Task — O3DE Live Bridge / MCP Preparation

## Current focus
Build the control artifacts that convert the proven six-tool live bridge into a capability-discovered, domain-based MCP v1.

## Right now
- active artifact: `entity_find`
- immediate next artifact: bridge-side typed request/response implementation and proof shape for `entity_find`

## Current execution requirements
- narrow mutation layer is complete enough to count as finished for: `component_add`, `entity_rename`, `entity_set_transform`, `mesh_set_model_asset`
- stable entity identifiers must remain primary
- mutation safety and allowlist boundaries must remain explicit in typed request/response structures
- `entity_find` is the explicitly selected next approved expansion and must follow the same typed/proved rollout pattern
- preserve approval-aware semantics and typed request/response design
- local pytest remains a non-blocking environment issue until the environment provides pytest

## After this file work
Implement `entity_find` bridge-side request/response and proof shape.
Do not stop at status-only updates.

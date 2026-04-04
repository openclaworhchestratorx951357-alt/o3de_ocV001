# Current Task — O3DE Live Bridge / MCP Preparation

## Current focus
Build the control artifacts that convert the proven six-tool live bridge into a capability-discovered, domain-based MCP v1.

## Right now
- active artifact: `entity_children`
- immediate next artifact: MCP exposure for `entity_children`

## Current execution requirements
- narrow mutation layer is complete enough to count as finished for: `component_add`, `entity_rename`, `entity_set_transform`, `mesh_set_model_asset`
- `entity_find` MCP exposure is complete
- `entity_list` MCP exposure is complete enough to count as finished
- stable identifiers must remain primary
- mutation safety and allowlist boundaries must remain explicit in typed request/response structures
- `entity_children` is the next adjacent read-only entity inspection slice selected from queue/control-file truth
- preserve approval-aware semantics and typed request/response design
- local pytest remains a non-blocking environment issue until the environment provides pytest

## After this file work
Advance from bridge-side `entity_children` implementation to MCP exposure.
Do not stop at status-only updates.

# Next Approved Expansion

## Status
Done for explicit selection.

## Selected next approved expansion
`entity_find`

## Why this is the next smallest unblocked artifact
- It is read-only and preserves the fail-closed safety posture.
- It directly strengthens stable-identifier-first workflows after the completed narrow mutation layer.
- It reduces ambiguity before any future widening by providing typed lookup from user-facing names or ids into stable entity records.
- It fits the existing MCP/domain shape without changing safety semantics.

## Scope of this artifact
Lock `entity_find` as the next approved bridge/MCP slice after:
- `component_add`
- `entity_rename`
- `entity_set_transform`
- `mesh_set_model_asset`

## Contract anchor
Use the already defined `entity_find` contract from `artifacts/mcp-v1-tool-contract.md`:
- purpose: typed entity search
- approval requirement: `none`
- dependency domain: `entities / components`
- proof status target for next implementation cycle: advance from `source_grounded` toward implementation/proof

## Required execution pattern for the next cycle
1. implement bridge-side typed request/response support for `entity_find`
2. preserve stable identifiers as primary output
3. keep deterministic ordering rules explicit
4. add fail-closed validation for missing search criteria and invalid match mode
5. wire MCP exposure only after bridge-side contract and proof shape are in place
6. update status files after execute → verify → report

## Not selected yet
The following remain valid future candidates but are not the selected next expansion in this artifact:
- `entity_list`
- `project_list_scenes`
- `list_supported_components`
- `list_scene_templates`
- `bridge_health` live-proof hardening
- `get_bridge_capabilities` live-proof hardening

## Validation
- selection is explicit
- selection is narrow
- selection does not widen mutation surface
- selection is unblocked by the known local pytest environment issue

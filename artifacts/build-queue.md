# O3DE MCP Build Queue

## 1. artifacts/bridge-capability-schema.md
- status: done
- purpose: define typed reporting for runtime/project/domain capability discovery
- done condition:
  - schema distinguishes:
    - installed in engine/editor
    - enabled in this project
    - discoverable at runtime
    - supported by bridge
    - exposed in MCP v1
    - planned for later
  - covers:
    - enabled Gems
    - supported domains
    - supported components
    - supported scene/template operations
    - supported asset operations
    - prefab support
    - White Box support
    - terrain support
    - scripting support
    - mutation safety class per operation
- validation:
  - schema fields are explicit and typed
  - no vague capability language
- next follow-on:
  - artifacts/mcp-v1-tool-contract.md

## 2. artifacts/mcp-v1-tool-contract.md
- status: done
- purpose: lock exact MCP v1 tool contracts
- done condition:
  - every v1 tool has:
    - purpose
    - request schema
    - response schema
    - side effects
    - approval requirement
    - preconditions
    - failure modes
    - determinism expectations
    - bridge handler mapping
    - dependency domain
    - proof status
    - expected test coverage
- validation:
  - tools are concrete and reviewable
  - no prose-only descriptions
- next follow-on:
  - bridge capability reporting implementation

## 3. bridge capability reporting implementation
- status: in progress
- purpose: implement runtime capability reporting in bridge code
- done condition:
  - capability schema is represented in code
  - bridge can return typed capability data
- validation:
  - output matches schema
- next follow-on:
  - MCP registration for bridge_health and get_bridge_capabilities

## 4. MCP registration for bridge_health and get_bridge_capabilities
- status: done
- purpose: expose foundational discovery tools first
- done condition:
  - both tools callable through MCP layer
- validation:
  - deterministic responses
- next follow-on:
  - wire proven six tools into MCP layer

## 5. wire the proven six tools into the MCP layer
- status: done
- purpose: connect live-proven bridge tools to MCP server
- done condition:
  - project_scan
  - scene_open
  - scene_create
  - scene_save
  - scene_validate
  - entity_create
    are exposed through MCP
- validation:
  - handlers route correctly
- next follow-on:
  - add entity_get

## 6. add entity_get
- status: done
- purpose: enable typed entity inspection
- done condition:
  - entity_get contract and implementation exist
- validation:
  - stable typed output
- next follow-on:
  - add asset_search and asset_resolve

## 7. add asset_search and asset_resolve
- status: done
- purpose: add safe asset introspection and resolution
- done condition:
  - both tools exist in contract and implementation
- validation:
  - result format is typed and deterministic
- next follow-on:
  - narrow mutation layer

## 8. narrow mutation layer
- status: done
- purpose: add first safe post-v1 mutation tools
- scope:
  - component_add
  - entity_rename
  - entity_set_transform
  - mesh_set_model_asset
- narrow mutation layer complete enough to count as finished: component_add, entity_rename, entity_set_transform, mesh_set_model_asset
- local pytest remains a non-blocking environment issue: `python3 -m pytest ...` fails with `No module named pytest`
- next approved expansion after narrow mutation layer: `entity_find`
- done condition:
  - each tool has explicit safety gating and contract coverage
- validation:
  - preconditions and failure modes are explicit
- next follow-on:
  - `entity_find`

## 9. entity_find
- status: done
- purpose: add safe typed entity lookup as the next smallest unblocked post-mutation expansion
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - deterministic ordering rules are explicit
  - fail-closed validation exists for missing search criteria and invalid match mode
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_find` or next adjacent read-only entity inspection slice

## 10. MCP exposure for entity_find
- status: done
- purpose: expose the completed bridge-side `entity_find` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_find`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
  - `python3 -m compileall` succeeded across MCP source and tests
- next follow-on:
  - `entity_list`

## 11. entity_list
- status: done
- purpose: add the next adjacent read-only entity inspection slice after `entity_find`
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - deterministic ordering rules are explicit
  - fail-closed validation exists for invalid scope values
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_list`

## 12. MCP exposure for entity_list
- status: done
- purpose: expose the completed bridge-side `entity_list` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_list`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
  - deterministic registry/server tests exist for `entity_list`
- next follow-on:
  - `entity_children`

## 13. entity_children
- status: done
- purpose: add the next adjacent read-only entity inspection slice after `entity_list`
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - parent/child relationship output is explicit and typed
  - fail-closed validation exists for missing parent lookup input
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_children`

## 14. MCP exposure for entity_children
- status: done
- purpose: expose the completed bridge-side `entity_children` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_children`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
  - deterministic registry/server tests exist for `entity_children`
- next follow-on:
  - `entity_parent`

## 15. entity_parent
- status: done
- purpose: add the next adjacent read-only entity inspection slice after `entity_children`
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - parent lookup output is explicit and typed
  - fail-closed validation exists for missing child lookup input
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_parent`

## 16. MCP exposure for entity_parent
- status: done
- purpose: expose the completed bridge-side `entity_parent` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_parent`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
  - deterministic registry/server tests exist for `entity_parent`
- next follow-on:
  - `entity_ancestors`

## 17. entity_ancestors
- status: done
- purpose: add the next adjacent read-only entity inspection slice after `entity_parent`
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - ancestor chain output is explicit and typed
  - fail-closed validation exists for missing child lookup input
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_ancestors`

## 18. MCP exposure for entity_ancestors
- status: done
- purpose: expose the completed bridge-side `entity_ancestors` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_ancestors`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
  - deterministic registry/server tests exist for `entity_ancestors`
- next follow-on:
  - `entity_descendants`

## 19. entity_descendants
- status: done
- purpose: add the next adjacent read-only entity inspection slice after `entity_ancestors`
- done condition:
  - bridge-side typed request/response support exists
  - stable identifiers remain primary in output
  - descendant tree/list output is explicit and typed
  - fail-closed validation exists for missing parent lookup input
  - proof shape exists before MCP exposure
- validation:
  - typed request validation is explicit
  - response shape is stable and reviewable
  - `python3 -m compileall` succeeded across bridge source and tests
- next follow-on:
  - MCP exposure for `entity_descendants`

## 20. MCP exposure for entity_descendants
- status: in progress
- purpose: expose the completed bridge-side `entity_descendants` slice through the MCP layer without widening mutation surface
- done condition:
  - MCP registration exists for `entity_descendants`
  - MCP routing preserves typed request/response shape
  - read-only approval semantics remain explicit
- validation:
  - handler routing is deterministic and reviewable
- next follow-on:
  - next adjacent read-only entity inspection slice after `entity_descendants`

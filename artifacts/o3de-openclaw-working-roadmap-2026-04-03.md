# O3DE + OpenClaw Working Roadmap — Post-Bring-up

Date: 2026-04-03  
Status: authoritative working roadmap after live bridge proof

---

## 1. Why this roadmap replaces the old planning center

The project is no longer in speculative bring-up mode.
The working setup has been proven live against the Windows-native O3DE editor.

That changes what should be considered “current truth.”

Older planning artifacts were useful during uncertainty, but they now risk slowing work down because they still emphasize:
- probe-first uncertainty that has already been resolved
- older transport assumptions that were corrected live
- earlier candidate paths that are no longer the best-known working path

This roadmap is the cleaned post-proof version.
It should be treated as the main planning center going forward.

---

## 2. Current verified working setup

## 2.1 Runtime model
- Windows-native O3DE Editor is the live editor runtime.
- OpenClaw running from WSL/Linux is the orchestration/support layer.
- Cross-boundary transport currently uses a narrow file-transport bridge through a shared Windows-visible folder.

## 2.2 Verified project/runtime targets
- Project: `McpSandbox`
- Verified saved scene name: `TestLoevel01`
- Verified validated entity: `test entity`
- Verified created bridge test entity: `bridge_entity_01`

## 2.3 Verified transport boundary
Windows:
- `C:\Users\topgu\O3DEBridge`

WSL:
- `/mnt/c/Users/topgu/O3DEBridge`

Subfolders:
- `inbox`
- `outbox`
- `archive`

## 2.4 Canonical contract rule
The typed request envelope is canonical:

```json
{
  "meta": {
    "request_id": "...",
    "tool_name": "...",
    "dry_run": false,
    "approval_token": null,
    "timestamp": "..."
  },
  "...": "tool-specific fields"
}
```

Do not reintroduce the legacy top-level-only request shape.

---

## 3. What is now live-proven

The full current approved six-tool surface is live-proven:
- `project_scan`
- `scene_open`
- `scene_create`
- `entity_create`
- `scene_save`
- `scene_validate`

Additional persistence proof completed:
- Mesh asset assignment on the validated entity resolves to:
  - `objects/_primitives/_box_1x1.fbx.azmodel`

Meaning:
- the current bridge is not hypothetical
- the narrow vertical slice is working in reality

---

## 4. New phase framing

The project should now be thought of in these phases:

## Phase A — Completed
### Live bridge feasibility and narrow workflow proof
Completed outcomes:
- editor Python execution proven
- file transport proven
- typed envelope hardened
- read operations proven
- approval-gated mutation operations proven
- persistence uncertainty resolved
- six-tool surface proven live

This phase is done.

## Phase B — Current phase
### Bridge consolidation and cleanup
Goal:
Turn the proven bridge from a collection of working handlers into a cleaner, more maintainable, reusable bridge layer.

This is the immediate next phase.

## Phase C — Next major step
### O3DE MCP server layer
Goal:
Wrap the proven narrow operations in a stable MCP server interface.

This should build on the now-proven operations rather than replacing them.

## Phase D — Orchestration layer refinement
Goal:
Teach OpenClaw to use the MCP layer cleanly and safely for structured workflows.

---

## 5. Immediate priorities for Phase B

These are ordered intentionally.

### Priority 1 — Consolidate the bridge runtime
Current issue:
- the live path is proven, but implementation still lives partly as individual operation-specific handlers and probes in `artifacts/`

Next work:
- move from ad hoc artifact handlers toward a cleaner runtime layout
- reduce duplication across:
  - request parsing
  - approval enforcement
  - response formatting
  - archive handling
  - entity/scene lookup helpers

Target outcome:
- fewer one-off scripts
- more reusable bridge runtime code
- same narrow behavior, cleaner implementation

### Priority 2 — Normalize operation contracts against the proven runtime reality
Current issue:
- some operations were initially written against guessed surfaces and later corrected during live testing
- example: `scene_create` needed retargeting from `general.create_level_no_prompt(...)` to `EditorToolsApplicationRequestBus(..., 'CreateLevelNoPrompt', ...)`

Next work:
- review each proven operation and encode the actual working runtime surface as canonical
- keep the working implementation path documented and centralized

Target outcome:
- no ambiguity about which runtime surface is authoritative for each operation

### Priority 3 — Separate durable bridge code from discovery probes
Current issue:
- some probe scripts are essential as references, but they are not the ideal permanent runtime shape

Next work:
- keep discovery probes for debugging/reference
- distinguish them clearly from production-intended bridge handlers

Target outcome:
- probes remain available without confusing the main implementation path

### Priority 4 — Clean the planning/documentation center
Current issue:
- older bring-up docs remain useful historically, but they should no longer function as the main roadmap

Next work:
- point future work to this roadmap + milestone handoff + key reference doc
- mark older planning docs as superseded where needed

Target outcome:
- less planning clash
- lower cognitive friction
- faster forward progress

---

## 6. What should be treated as canonical now

These should be considered the primary current truth sources:

### Primary current state docs
- `artifacts/o3de-openclaw-working-roadmap-2026-04-03.md`
- `artifacts/o3de-safe-bridge-milestone-handoff-2026-04-03.md`
- `reference/important-paths-and-facts-2026-04-03.md` (Dropbox copy)

### Primary current code paths
- `bridge/o3de-bridge/src/o3de_bridge/models.py`
- `bridge/o3de-bridge/src/o3de_bridge/validators.py`
- `bridge/o3de-bridge/src/o3de_bridge/approvals.py`
- round-trip helpers under `bridge/o3de-bridge/src/o3de_bridge/`
- verified Windows handlers under `artifacts/`

### Primary operational rule
- Dropbox checkpointing of important/successful artifacts is now part of the workflow, not optional cleanup

---

## 7. What should be considered superseded or secondary

These are not “wrong,” but they should no longer drive planning:
- early bring-up checklists once their uncertainty has been resolved
- older probe plans that assume the editor/runtime path is still unknown
- pre-proof milestone framing that stops at feasibility instead of consolidation

Keep them as historical reference only.

---

## 8. Concrete next work items

## Work Item 1 — Bridge consolidation pass
- identify duplicated logic across operation handlers
- factor shared request/response helper patterns
- centralize operation helper utilities where practical
- preserve live-proven behavior while reducing script sprawl

## Work Item 2 — Runtime layout cleanup
- decide which `artifacts/` handlers should remain reference/debug assets
- decide which logic should move into reusable bridge runtime modules
- keep external runbooks, but reduce internal duplication

## Work Item 3 — Prepare MCP wrapping plan from proven operations
- map each live-proven operation to future MCP tool semantics
- define how approvals flow through MCP safely
- define what remains editor-side vs orchestration-side

## Work Item 4 — Optional scene naming cleanup task later
- `TestLoevel01` is misspelled, but do not treat rename as part of bridge consolidation
- if renamed later, do it as a separate explicit content task

---

## 9. What not to do now

Do not:
- restart architecture
- widen the tool surface just because the current one works
- replace the bridge with unrestricted direct editor control
- discard the typed transport envelope
- collapse discovery, runtime, and orchestration concerns into one giant script
- let older speculative docs continue to steer current execution

---

## 10. One-sentence roadmap summary

The roadmap has now shifted from proving feasibility to consolidating the live-proven six-tool safe bridge into a cleaner, reusable foundation for the O3DE MCP server layer.

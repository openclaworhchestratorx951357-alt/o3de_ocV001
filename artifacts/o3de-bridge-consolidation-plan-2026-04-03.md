# O3DE Bridge Consolidation Plan — 2026-04-03

## Purpose
Turn the now-live-proven bridge from a successful bring-up collection into a cleaner, lower-conflict implementation baseline.

This document answers:
- what should remain runtime code
- what should remain reference/debug material
- what should stop acting like active planning
- what should be consolidated next before MCP work

---

## 1. Current situation

The bridge works.
That is no longer in question.

The current friction is structural:
- several operation-specific Windows handlers live under `artifacts/`
- several discovery probes also live under `artifacts/`
- some old bring-up docs and early probe plans remain nearby
- the runtime package already has shared models/validators/approvals/file-transport logic, but not enough operation helper centralization yet

So the cleanup target is not “make it work.”
It is:
- reduce duplication
- reduce ambiguity
- preserve what was learned
- keep the working path obvious

---

## 2. Keep / promote / archive classification

## 2.1 Keep as active runtime foundation
These are part of the real bridge base and should be treated as active implementation assets.

### Bridge runtime package
Keep active:
- `bridge/o3de-bridge/src/o3de_bridge/models.py`
- `bridge/o3de-bridge/src/o3de_bridge/errors.py`
- `bridge/o3de-bridge/src/o3de_bridge/approvals.py`
- `bridge/o3de-bridge/src/o3de_bridge/validators.py`
- `bridge/o3de-bridge/src/o3de_bridge/file_transport.py`
- `bridge/o3de-bridge/src/o3de_bridge/dispatch.py`

### Round-trip helpers
Keep active for now:
- `run_project_scan_roundtrip.py`
- `run_scene_open_roundtrip.py`
- `run_scene_create_roundtrip.py`
- `run_entity_create_roundtrip.py`
- `run_scene_save_roundtrip.py`
- `run_scene_validate_roundtrip.py`

These are still useful operationally even if they later get folded into a cleaner CLI surface.

---

## 2.2 Keep as active reference implementation (temporary)
These are working Windows-side handlers for the proven six-tool surface.
They should remain available, but should be treated as temporary reference implementations rather than the ideal final structure.

Keep active for now:
- `windows-file-transport-project-scan-handler-v3.py`
- `windows-file-transport-scene-open-handler-v1.py`
- `windows-file-transport-scene-create-handler-v1.py`
- `windows-file-transport-entity-create-handler-v1.py`
- `windows-file-transport-scene-save-handler-v1.py`
- `windows-file-transport-scene-validate-handler-v1.py`

Reason:
- they are the live-proven editor-side implementations
- they encode the real working editor API surfaces
- they should not be discarded before their shared logic is absorbed into cleaner runtime modules

---

## 2.3 Keep as reference/debug probes
These should be preserved, but clearly treated as discovery/debug assets rather than the normal bridge path.

Keep as reference/debug:
- `windows-list-root-entities-probe.py`
- `windows-list-level-children-probe.py`
- `windows-mesh-asset-validate-probe.py`
- `windows-mesh-asset-resolve-probe.py`
- `windows-validate-bridge-entity-01-probe.py`
- `windows-scene-create-direct-probe.py`
- `windows-o3de-project-scan-probe.py`
- `windows-python-editor-bindings-probe-script.py`

Reason:
- these were important in discovering the real runtime behavior
- they remain useful for debugging and future regression checks
- they should not be confused with the intended long-term runtime shape

---

## 2.4 Keep as primary planning/docs
These should remain easy to find and should act as the main current planning center.

Primary docs:
- `artifacts/o3de-openclaw-working-roadmap-2026-04-03.md`
- `artifacts/o3de-safe-bridge-milestone-handoff-2026-04-03.md`
- `artifacts/current-task-o3de-live-bridge.md`
- `artifacts/o3de-source-study-plan.md`
- Dropbox copies of roadmap / handoff / reference docs

---

## 2.5 Demote to historical / superseded reference
These should not be deleted right now, but they should no longer steer execution.

Historical/superseded:
- `windows-file-transport-project-scan-handler.py`
- `windows-file-transport-project-scan-handler-v2.py`
- `windows-file-transport-v1-plan.md`
- `windows-o3de-bridge-probe-plan-2026-04-03.md`
- `windows-probe-run-instructions-2026-04-03.md`
- `windows-project-scan-probe-run-instructions.md`
- `windows-bridge-bringup-checklist.md`
- older pre-proof scaffold/phase planning files used during uncertainty

Reason:
- they were useful during bring-up
- they now create planning and implementation noise if treated as current

---

## 3. Recommended directory-role cleanup

Without doing a big disruptive move yet, the conceptual directory roles should now be:

## 3.1 `bridge/o3de-bridge/src/o3de_bridge/`
This should hold:
- durable runtime models
- validators
- approvals
- transport helpers
- eventually shared operation helper code

## 3.2 `artifacts/`
This should hold:
- milestone docs
- runbooks
- proven Windows reference handlers
- debug/discovery probes

But `artifacts/` should no longer be treated as the main implementation home forever.
It is currently a staging/reference area.

## 3.3 Dropbox
This should continue to hold:
- milestone handoffs
- roadmap/reference docs
- selected high-value handlers/helpers/runbooks

Dropbox is now part of the checkpoint workflow.

---

## 4. First consolidation step to execute next

The next cleanup move should be small and low-risk.

### Recommended Step 1
Create shared bridge operation helper modules inside `bridge/o3de-bridge/src/o3de_bridge/` for the repeated editor-side logic patterns.

Examples of repeated patterns worth centralizing conceptually:
- strict typed envelope validation on the Windows side
- standard structured error/response formatting
- common scene/project restriction checks
- entity lookup helpers
- component type id lookup helpers
- archive/write response helpers

Goal:
- reduce duplicated logic across the six Windows handlers
- keep behavior identical while making the implementation easier to maintain

This should happen before trying to redesign everything at once.

---

## 5. Second consolidation step

### Recommended Step 2
Normalize the Windows handler family so they read like one system instead of six cousins.

That means aligning:
- naming
- response shapes
- error helper usage
- current-level checks
- approval enforcement patterns
- comments/docstrings

This is partly cosmetic, but mostly about reducing future bugs.

---

## 6. Third consolidation step

### Recommended Step 3
Create a clearer separation between:
- production-intended bridge handlers
- discovery/debug probes

Possible lightweight approach:
- keep current files, but adopt a stronger convention in docs and Dropbox packaging
- later, optionally move probes into a dedicated `artifacts/probes/` area and handlers into `artifacts/handlers/`

This does not need to be the first cleanup step.

---

## 7. What not to clean up yet

Do not do these immediately:
- do not rename the misspelled scene as part of bridge consolidation
- do not aggressively delete historical artifacts yet
- do not rewrite the entire bridge into a different architecture before harvesting the working patterns
- do not merge everything into one giant script/module

The right cleanup is incremental and preserving.

---

## 8. Immediate recommendation

Proceed next with:
1. shared helper extraction for repeated Windows handler logic
2. handler family normalization
3. clearer runtime vs probe separation
4. then MCP-layer planning from the stabilized bridge core

---

## 9. One-sentence conclusion

The right cleanup move now is not to throw away the working path, but to consolidate the proven six-tool bridge into a cleaner shared runtime while keeping probes and historical artifacts clearly demoted to reference-only status.

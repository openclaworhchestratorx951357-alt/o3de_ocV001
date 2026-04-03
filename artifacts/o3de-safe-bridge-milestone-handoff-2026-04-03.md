# O3DE + OpenClaw Safe Bridge Milestone Handoff — 2026-04-03

Prepared by: Agent Henderson  
Audience: Darrell / continuation agent / reviewer

---

## 1. Bottom line

The first real safe bridge milestone has been achieved.

This is no longer a theoretical scaffold or a one-off probe.
A typed, narrow, deterministic file-transport bridge between WSL/OpenClaw and the live Windows-native O3DE editor has now been proven across real editor operations.

Most importantly, the original Phase 0 persistence uncertainty has now been resolved by direct validation:
- the saved test scene persists after reopen
- the expected entity persists
- Camera persists
- Mesh persists
- the Mesh asset assignment persists to the expected Box_1x1 model asset

---

## 2. Locked direction remains unchanged

Still in force:
- Base engine/editor: **O3DE**
- Orchestration layer: OpenClaw
- First major deliverable: safe O3DE-focused MCP server
- Canonical sequence:
  1. O3DE fork
  2. safe bridge
  3. O3DE MCP server
  4. OpenClaw orchestration
  5. graybox prototype generation
  6. gradual expansion
- v1 bridge/runtime language: Python
- Windows-native O3DE Editor remains the primary interactive runtime
- WSL/OpenClaw remains orchestration/support, not the preferred live editor host
- Do **not** broaden into unrestricted editor control
- Do **not** expose arbitrary Python execution as the user-facing control interface
- Do **not** replace MCP-first sequencing with ad hoc direct control

---

## 3. Verified environment state

### OpenClaw workspace
- Workspace is active and being used as the bridge/orchestration repo.
- Bridge code, artifacts, logs, and continuity notes are present in the workspace.

### O3DE source
- Local O3DE fork clone verified at:
  - `/home/topgu/src/o3de_ocV001`
- Verified branch:
  - `development`
- Verified commit:
  - `3c0d28bc`

### Live editor runtime
- Windows-native O3DE Editor is working.
- Active project is `McpSandbox`.
- Editor-side Python execution is working.

---

## 4. Bridge/package state

Local bridge package work is now in place and runnable.

Verified local bridge status:
- typed request/response models
- approvals map
- validators
- whitelist-only dispatch
- file transport helpers
- narrow round-trip helpers
- tests

Test status at end of milestone work:
- `31 passed`

---

## 5. Live milestone proofs achieved

### 5.1 Live editor Python execution
Proven in the Windows editor.

### 5.2 `project_scan` live round-trip
Proven through the file transport path.

What was shown:
- typed request envelope consumed correctly
- structured response returned correctly
- project identified as `McpSandbox`
- repeatability verified from clean inbox/outbox state

### 5.3 `scene_open` live round-trip
Proven through an approval-gated narrow path.

What was shown:
- typed request envelope consumed correctly
- approval token requirement enforced
- structured response returned correctly
- live editor open-level path invoked successfully once the verified real level name was used

Important discovery:
- the saved level name on disk is misspelled:
  - `TestLoevel01`
- The first failed `scene_open` attempt against `TestLevel01` was therefore a correct fail based on a wrong requested identifier, not a transport failure.

### 5.4 `scene_validate` live round-trip
Proven through a narrow read-oriented validator path.

What was shown:
- current scene identity matched expected scene
- expected entity existed
- Camera component existed
- Mesh component existed

Validated entity:
- `test entity`

### 5.5 Final Mesh asset persistence resolution
Proven via direct Mesh component property inspection and asset-catalog resolution.

Verified Mesh property path (source-grounded from O3DE tests):
- `Controller|Configuration|Model Asset`

Resolved live result:
- assigned asset id:
  - `{C15CD465-9589-56ED-945F-8416FA4798A3}:10f216d9`
- resolved asset relative path:
  - `objects/_primitives/_box_1x1.fbx.azmodel`

This resolves the original persistence uncertainty.

### 5.6 `entity_create` live round-trip and verification
Proven through a narrow approval-gated mutation path.

What was shown:
- typed request envelope consumed correctly
- approval token requirement enforced
- entity `bridge_entity_01` created in `TestLoevel01`
- requested components `Camera` and `Mesh` added successfully
- structured response returned correctly
- follow-up validation probe confirmed `bridge_entity_01` exists and has both Camera and Mesh components

### 5.7 `scene_save` live round-trip
Proven through a narrow approval-gated save path.

What was shown:
- typed request envelope consumed correctly
- approval token requirement enforced
- current validated scene `TestLoevel01` saved successfully via editor-native save surface
- structured response returned correctly

### 5.8 `scene_create` live round-trip
Proven through a narrow approval-gated creation path.

What was shown:
- first attempt against `general.create_level_no_prompt(...)` failed with `result=None`, which exposed a binding/runtime mismatch rather than a capability gap
- direct probe confirmed the working creation surface is `EditorToolsApplicationRequestBus(..., 'CreateLevelNoPrompt', ...)`
- after retargeting to the working editor API and the real template path `Prefabs/Default_Level.prefab`, live creation of `BridgeLevel01` succeeded with result code `0`
- structured response returned correctly

---

## 6. Phase 0 closeout status

Original unresolved question was whether the intended box asset was actually assigned to the intended entity and persisted after save/reopen.

That is now resolved.

### Verified Phase 0 persistence answers
- saved scene reopened successfully
- correct scene identified: `TestLoevel01`
- expected entity exists: `test entity`
- Camera exists: yes
- Mesh exists: yes
- Box asset persisted: yes
  - resolved as `objects/_primitives/_box_1x1.fbx.azmodel`

So the Phase 0 closeout uncertainty is no longer open.

---

## 7. Important implementation lessons learned

### 7.1 Typed transport contract must stay canonical
A real mismatch was found between:
- legacy top-level request shape
- typed request envelope with `meta.request_id` and `meta.tool_name`

The bridge behaved correctly by failing closed.
The canonical transport path is now the typed request envelope.

### 7.2 Real on-disk/editor identifiers must be verified, not assumed
Two concrete examples:
- scene name turned out to be `TestLoevel01`, not `TestLevel01`
- expected entity had to be discovered from the live level hierarchy, not guessed

### 7.3 Live asset validation may require id resolution, not string matching
The Mesh component returned an asset id, not a human-readable path.
The final persistence answer required asset catalog resolution.

---

## 8. Artifacts that matter most

### Milestone and task tracking
- `artifacts/current-task-o3de-live-bridge.md`
- `artifacts/bridge-build-log-2026-04-03.md`
- `artifacts/o3de-safe-bridge-milestone-handoff-2026-04-03.md`

### Transport and live-operation design
- `artifacts/windows-file-transport-v3-runbook.md`
- `artifacts/scene-open-live-design-2026-04-03.md`
- `artifacts/scene-validate-live-design-2026-04-03.md`

### Windows handlers/probes
- `artifacts/windows-file-transport-project-scan-handler-v3.py`
- `artifacts/windows-file-transport-scene-open-handler-v1.py`
- `artifacts/windows-file-transport-scene-validate-handler-v1.py`
- `artifacts/windows-list-root-entities-probe.py`
- `artifacts/windows-list-level-children-probe.py`
- `artifacts/windows-mesh-asset-validate-probe.py`
- `artifacts/windows-mesh-asset-resolve-probe.py`

### WSL helpers
- `bridge/o3de-bridge/src/o3de_bridge/run_project_scan_roundtrip.py`
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_open_roundtrip.py`
- `bridge/o3de-bridge/src/o3de_bridge/run_scene_validate_roundtrip.py`

---

## 9. What should happen next

Recommended next step:
- move to the next narrow approved operation after this milestone checkpoint

Best candidate:
- `entity_create`

Reason:
- `project_scan` is proven
- `scene_open` is proven
- `scene_validate` is proven
- persistence of the known Mesh asset assignment is proven
- `entity_create` is the next mutation step that meaningfully advances the vertical slice without jumping too far ahead

Alternative reasonable next step:
- formal cleanup/refinement of the existing validator/response shapes before adding more operations

---

## 10. What must not drift now

Do not:
- restart architecture
- collapse the bridge into unrestricted direct editor control
- expose arbitrary Python execution as normal user-facing control
- broaden beyond the approved six-tool surface prematurely
- lose the typed request envelope as canonical transport

Do:
- keep the bridge narrow and deterministic
- keep using editor-native surfaces where available
- continue verification-first
- prefer structured outputs over ad hoc script behavior
- commit milestones as they are achieved

---

## 11. One-sentence conclusion

The safe bridge has crossed from planning into verified reality: `project_scan`, approval-gated `scene_open`, and `scene_validate` all work live against the Windows O3DE editor, and the Box_1x1 mesh assignment has been confirmed to persist after reopen.

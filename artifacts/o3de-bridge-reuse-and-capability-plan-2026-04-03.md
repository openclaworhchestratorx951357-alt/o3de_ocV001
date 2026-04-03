# O3DE Bridge Reuse and Capability Plan — 2026-04-03

## Purpose
Establish the next practical build direction for a safe O3DE control stack that reuses existing O3DE systems, Gems, and external tooling where possible instead of reinventing them.

This document is not a replacement for the approved narrow Phase 1 scaffold. It is a planning artifact that identifies what can be wrapped safely, what should stay approval-gated, and what should be deferred.

## Current verified base
- Approved bridge scaffold exists for:
  - `approvals.py`
  - `models.py`
  - `validators.py`
- Approved bridge surface remains exactly:
  - `project_scan`
  - `scene_open`
  - `scene_create`
  - `entity_create`
  - `scene_save`
  - `scene_validate`
- Windows-native O3DE editor is the intended interactive runtime.
- WSL/OpenClaw is the orchestration and support environment, not the preferred editor runtime.
- GitHub auth is working for the GitHub account `openclaworhchestratorx951357-alt`.

## Reuse-first findings

### 1. Editor automation
Best immediate bridge substrate.

O3DE documentation indicates editor automation support via the Python Editor Bindings Gem, including level management and interaction with editor functionality through Python and EBus-backed APIs.

Implication:
- The Windows-side bridge should target Python Editor Bindings first.
- Default bridge execution should be typed and whitelisted, not arbitrary Python from chat.

### 2. Materials
Strong native reuse path.

O3DE materials are JSON/data-driven (`.material`, `.materialtype`) and can be edited via Material Editor or generated through tool/script workflows. Material Canvas can generate material/shader source artifacts.

Implication:
- We should not invent a custom material format.
- Bridge capability should focus on search, inspect, assign, and limited property mutation first.
- Higher-level material generation can be layered later through external tools plus import/validation.

### 3. Lighting
Good native reuse path.

O3DE has Atom light components and documented scene/cinematic lighting workflows.

Implication:
- Lighting control belongs in a future adapter/tool family, not in the initial six-tool batch.
- Future safe operations can include light creation, property edits, preset application, and validation.

### 4. Animation / characters
Substantial native tooling exists, but this is not a first bridge batch.

O3DE EMotion FX and related animation tooling support actor setup, skeletons, motion blending, anim graphs, and related animation workflows.

Implication:
- Character and movement work should reuse EMotion FX and asset import pipelines.
- Bridge exposure should begin with setup/inspection/configuration helpers, not broad character-generation claims.

### 5. Navigation / NPC movement substrate
Viable native base exists.

O3DE documentation points to Recast Navigation for navmesh generation and pathfinding.

Implication:
- NPC realism should not be framed as one feature.
- We can build on existing navigation components for locomotion/pathing foundations, then layer project-specific behavior systems later.

### 6. Gems / downloadable integrations
Important strategic direction.

O3DE Gems are the natural extension mechanism. This aligns with the project rule to extend heavily and patch core lightly.

Implication:
- Before writing custom subsystems, survey relevant Gems and external integrations.
- The bridge should expose stable project capabilities, not hardcode assumptions that belong to optional integrations.

## Safe capability envelope

### Safe-now / near-term bridge control
These are realistic bridge targets after the current six-tool runtime layer:
- project inspection
- scene open/create/save/validate
- entity create/find/list
- transform get/set
- component add/remove/list
- component property get/set
- mesh/material assignment
- prefab instantiate
- selection/query helpers
- structured logs and validation reports

### Approval-gated future operations
These should require explicit approval or confirmation gates:
- entity deletion
- scene overwrite / save-as overwrite
- bulk rename or move operations
- bulk property rewrites
- asset reassignment across many entities
- multi-step recipes that mutate many objects

### Dangerous / disabled-by-default lane
Not part of normal architecture. If ever introduced, keep local-only, explicit, and separately gated.
- allowlisted debug scripts
- special maintenance actions
- migration helpers for controlled development use

Not recommended as the default interface:
- arbitrary Python execution from chat
- generic editor command execution
- raw UI automation as the primary control mechanism

## Proposed layered architecture

### Layer A — Windows-side safe editor bridge
- Python runtime
- Python Editor Bindings based
- static tool whitelist
- typed request/response models
- approval-aware execution
- structured log records per operation

### Layer B — Domain adapters
Separate adapters behind the bridge for:
- scenes/entities/components
- materials
- lighting
- prefabs/assets
- navigation
- animation/character setup

### Layer C — Reuse/download integrations
Adapters or workflows for:
- official/third-party Gems
- asset libraries
- external material/content tools
- optional MCP servers where they add value without weakening safety boundaries

### Layer D — OpenClaw orchestration
- planning and sequencing
- approval capture
- report synthesis
- multi-agent role separation if adopted later

## Proposed capability phases

### Phase 1A — finish current narrow bridge runtime
- dispatch layer for the approved six-tool surface
- deterministic stub handlers
- tests for whitelist dispatch behavior

### Phase 1B — Windows-side bridge probe
- verify Python Editor Bindings availability on the Windows editor setup
- create a minimal bridge execution harness on Windows
- prove one read-only or low-risk operation end to end

### Phase 2 — broaden editor-safe operations
- entity query/list/find
- transform operations
- component inspection
- mesh/material assignment
- richer validation output

### Phase 3 — content/lookdev helpers
- material search/inspect/assign
- lighting presets and light property tools
- prefab placement helpers

### Phase 4 — movement/behavior foundations
- navigation area setup helpers
- navmesh update/validate hooks
- character setup helpers
- animation graph inspection/config support

### Phase 5 — higher-level orchestration
- recipes
- task decomposition
- optional A2A role separation
- selective MCP ecosystem integrations

## Questions to resolve next
1. Where will the Windows-side bridge live relative to the editor/project installation?
2. Is Python Editor Bindings already enabled for the active project/editor setup?
3. Should the first live bridge transport be local HTTP, named pipe, or file-backed command polling?
4. Which read-only live operation should be the first end-to-end proof:
   - project scan
   - scene open state inspection
   - entity listing in current scene

## Recommended next build step
Continue from the approved scaffold and generate the next reviewable bridge runtime file(s) for dispatch and deterministic stub operations, while separately planning the Windows-side live bridge probe.

## References consulted
- O3DE editor automation docs
- O3DE Python Editor Bindings docs
- O3DE material system / Material Editor / Material Canvas docs
- O3DE animation overview docs
- O3DE navigation / Recast Navigation docs

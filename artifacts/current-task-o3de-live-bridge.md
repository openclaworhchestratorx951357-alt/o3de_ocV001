# Current Task — O3DE Live Bridge Bring-up

## Objective
Build toward the first real safe end-to-end O3DE control loop from OpenClaw/WSL to the Windows-native O3DE editor.

## Active milestone
Milestone A: first live bridge proof.

## Immediate subgoals
1. Verify and document the approved bridge scaffold currently on disk.
2. Materialize the approved scaffold into a working source tree inside the workspace so implementation can continue from real package files instead of artifact-only copies.
3. Normalize the copied approved bridge source files into runnable Python so the test suite can collect.
4. Generate/approve the next narrow bridge runtime files needed for dispatch/runtime proof.
5. Prepare a Windows-side bridge probe plan for Python Editor Bindings.

## Current milestone focus
- Local bridge skeleton is runnable and passing tests.
- Windows-side generic Python execution and O3DE-aware read-only probe execution have been proven in the live editor environment.
- First manual file-transport round-trip has been completed successfully.
- Canonical typed `project_scan` round-trip has now been repeated successfully with the v3 handler.
- Next action: clean remaining legacy transport debris, then decide the next low-risk live operation.

## Notes
- Persist progress here and in dated memory as work advances.
- Do not assume Windows editor-side binding availability until verified.
- Keep implementation narrow and reviewable.
- Transport hardening note: the shared Windows bridge directories previously contained legacy files from earlier handler attempts (`windows-project-scan-request-001.json`, prior response files, and `unknown-request.response.json`). These have now been archived so inbox/outbox are clean again for the next repeatability check.

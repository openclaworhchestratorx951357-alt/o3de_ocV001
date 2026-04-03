# O3DE Editor Persistent Runner Plan — 2026-04-03

## Goal
Reduce or eliminate manual per-handler pasting into the O3DE Python console by introducing a single safe editor-side bootstrap/runner.

## Immediate design target
A single editor-side script should be pasted/run once in the O3DE Python console and then remain available as the dispatch entrypoint for typed bridge requests.

## Safety goals
The persistent runner must preserve the same properties as the manual handler path:
- typed requests only
- explicit tool dispatch
- approval enforcement preserved
- structured responses preserved
- fail-closed behavior
- no arbitrary Python execution surface

## Preferred near-term design
### Option A — one-time bootstrap + per-request dispatch file
1. Run one editor-side bootstrap script once.
2. That bootstrap loads shared bridge code from a Windows-visible directory.
3. The bootstrap exposes a single function or rerunnable dispatch script that reads the newest inbox request and dispatches to the correct operation handler.
4. Future requests only need one stable runner file in the editor, not one pasted command per operation-specific script.

This is the best immediate step because it reduces paste overhead without prematurely building a complicated always-on loop.

## Why not jump immediately to an always-on polling loop?
Possible, but riskier because:
- persistent loops inside the editor need careful lifecycle behavior
- debugging is harder if the first version is too magical
- a single stable dispatch runner gives most of the benefit with less fragility

## Recommended implementation shape
### 1. Shared Windows bridge module
Create a Windows-visible shared module set that contains:
- common helpers
- operation dispatch table
- individual operation functions or imported handler entrypoints

### 2. Single dispatch runner
Create a script such as:
- `windows-o3de-bridge-dispatch.py`

Behavior:
- read newest inbox request
- inspect `meta.tool_name`
- route to the correct proven handler logic
- write response
- archive request

### 3. One stable console command
Then the O3DE console step becomes only:
```python
import runpy
runpy.run_path(r"C:\Users\topgu\O3DEBridge\windows-o3de-bridge-dispatch.py", run_name="__main__")
```

That is already a major reduction in friction.

## After that
Only after the single dispatch runner is stable should we consider:
- timer-based polling
- editor-start bootstrap auto-registration
- deeper persistent resident behavior

## Recommendation
Implement the shared Windows dispatch runner next.
That gives a strong step toward “connected to the O3DE Python console” without skipping the safety model.

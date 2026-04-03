# Windows Level Children Probe Runbook

## Goal
List the level root entity and its immediate children so we can discover the exact test entity name for `scene_validate`.

## Script
- `artifacts/windows-list-level-children-probe.py`

## Suggested execution
Copy to a Windows-visible path, for example:
- `C:\Users\topgu\O3DEBridge\windows-list-level-children-probe.py`

Then run in the O3DE Python Console:

```python
import runpy
runpy.run_path(r"C:\Users\topgu\O3DEBridge\windows-list-level-children-probe.py", run_name="__main__")
```

## Expected output
Structured JSON including:
- current level name/path
- root entity names
- each root entity's immediate child ids/names

## Purpose
Use the discovered child entity name as the exact expected entity for the first narrow `scene_validate` path.

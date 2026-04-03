# Windows Root Entity Probe Runbook

## Goal
List the current root editor entity names from the currently open level so the next `scene_validate` step can use the exact verified entity name.

## Script
- `artifacts/windows-list-root-entities-probe.py`

## Suggested execution
Copy the script to a Windows-visible path, for example:
- `C:\Users\topgu\O3DEBridge\windows-list-root-entities-probe.py`

Then run in the O3DE Python Console:

```python
import runpy
runpy.run_path(r"C:\Users\topgu\O3DEBridge\windows-list-root-entities-probe.py", run_name="__main__")
```

## Expected output
Structured JSON including:
- current level name
- current level path
- root entity ids
- root entity names

## Purpose
Use the exact returned entity name in the first narrow `scene_validate` implementation.
Do not guess the entity name.

# Windows O3DE Bridge Bootstrap Runbook

## Goal
Run one bootstrap command in the O3DE Python console so the editor polls for typed bridge requests automatically.

## What this bootstrap does
- starts a lightweight Qt timer inside the editor runtime
- every poll interval, runs the single bridge dispatcher:
  - `C:\Users\topgu\O3DEBridge\windows-o3de-bridge-dispatch.py`
- if no request exists, nothing meaningful happens
- if a typed request is present, it gets dispatched automatically

## Bootstrap file
- `artifacts/windows-o3de-bridge-bootstrap.py`

## Suggested deployment
Copy to:
- `C:\Users\topgu\O3DEBridge\windows-o3de-bridge-bootstrap.py`

## First-time install in O3DE Python Console
```python
import runpy
runpy.run_path(r"C:\Users\topgu\O3DEBridge\windows-o3de-bridge-bootstrap.py", run_name="__main__")
```

## Expected result
Printed message like:
- `O3DE bridge bootstrap installed. Poll interval: 1500 ms`

## After installation
You should not need to manually run the dispatcher for each request.
Instead, you stage requests from WSL/OpenClaw and the installed timer should pick them up automatically.

## Status file
The bootstrap also writes lightweight status to:
- `C:\Users\topgu\O3DEBridge\bootstrap-status.json`

This is useful for checking whether the bootstrap believes it is installed and what dispatch path/poll interval it is using.

## Notes
- this is the first safe bootstrap version, not the final polished persistent bridge
- the script exposes `install()`, `uninstall()`, and `status()` functions
- restart of the O3DE editor still requires reinstalling the bootstrap unless a startup hook is added later

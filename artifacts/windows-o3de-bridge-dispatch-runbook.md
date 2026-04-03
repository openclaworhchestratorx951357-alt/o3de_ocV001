# Windows O3DE Bridge Dispatch Runbook

## Goal
Replace manual per-operation handler pasting with one stable editor-side dispatch script.

## What this changes
Instead of running a different handler file for each request type, the editor console runs one stable dispatch file:
- `windows-o3de-bridge-dispatch.py`

That dispatch file:
- reads the newest typed request from inbox
- inspects `meta.tool_name`
- routes to the correct proven handler
- lets that handler generate the structured response

## Current handler source location
For now, the dispatch script loads handlers from the Dropbox checkpoint folder:
- `C:\Users\topgu\Dropbox\O3DE-OpenClaw\handlers`

This keeps the dispatcher stable while reusing the already checkpointed handler set.

## Suggested execution
Copy the dispatcher to a Windows-visible path, for example:
- `C:\Users\topgu\O3DEBridge\windows-o3de-bridge-dispatch.py`

Then in the O3DE Python Console run:

```python
import runpy
runpy.run_path(r"C:\Users\topgu\O3DEBridge\windows-o3de-bridge-dispatch.py", run_name="__main__")
```

## Expected benefit
You no longer need to remember which specific handler file to run for each tool.
You only run the one dispatcher.

## Future step after this
If this proves stable, the next evolution is an editor-start bootstrap or persistent polling/trigger mechanism so even this one manual dispatch step can be reduced further.

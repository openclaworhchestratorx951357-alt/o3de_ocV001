# Windows File Transport v3 Runbook

## Goal
Run one clean `project_scan` round-trip using the canonical typed request envelope.

## Canonical request contract
The request JSON in inbox must use the typed bridge shape:

```json
{
  "meta": {
    "request_id": "project-scan-roundtrip-...",
    "tool_name": "project_scan",
    "dry_run": true,
    "approval_token": null,
    "timestamp": "..."
  },
  "project_id": "McpSandbox"
}
```

Important:
- `request_id` lives under `meta.request_id`
- `tool_name` lives under `meta.tool_name`
- do not use the older top-level-only request shape

## Files involved
### WSL-side helper
- `bridge/o3de-bridge/src/o3de_bridge/run_project_scan_roundtrip.py`

### Windows editor-side handler
- `artifacts/windows-file-transport-project-scan-handler-v3.py`

## Prep
Ensure these directories exist:
- `C:\Users\topgu\O3DEBridge\inbox`
- `C:\Users\topgu\O3DEBridge\outbox`
- `C:\Users\topgu\O3DEBridge\archive`

Recommended cleanup before run:
- move any stale `*.json` request files out of inbox if they are unrelated
- keep outbox clean enough that the new response is obvious

## Step 1 — Stage the request from WSL
From the workspace venv/package context:

```bash
source /home/topgu/.openclaw/workspace/.venv/bin/activate
cd /home/topgu/.openclaw/workspace/bridge/o3de-bridge
PYTHONPATH=src python -m o3de_bridge.run_project_scan_roundtrip
```

This will:
- create a unique request id
- write a typed request into inbox
- wait for the response file
- print the response
- archive the consumed request and response after reading

## Step 2 — Run the handler in the live Windows O3DE editor
Execute the v3 handler from the O3DE Python console or via the known script path.

Handler file:
- `artifacts/windows-file-transport-project-scan-handler-v3.py`

Expected behavior:
- reads newest inbox request
- validates typed `meta` envelope
- accepts only `project_scan`
- writes `<request_id>.response.json` to outbox
- archives the consumed request

## Expected success result
The response should include at least:
- `request_id`
- `tool_name: "project_scan"`
- `ok: true`
- `data.project_id: "McpSandbox"`
- `data.project_found`
- `data.project_name_guess`
- `requires_approval: false`
- `approval_level: "none"`

## Expected failure mode
If an old request shape is consumed, the handler should fail closed with structured error output such as:
- `code: "INVALID_REQUEST"`
- target like `meta` or `meta.tool_name`

That is preferred over silently accepting the wrong contract.

## Meaning of a successful run
A successful v3 run means:
- WSL and Windows editor agree on one request contract
- `project_scan` file transport is now repeatable, inspectable, and safe-failing
- the first live bridge loop is no longer a one-off proof only

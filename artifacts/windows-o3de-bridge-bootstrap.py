"""Persistent-ish O3DE bridge bootstrap using a self-rescheduling Qt timer.

Run this once in the O3DE Python console. It installs a lightweight timer that
periodically invokes the single-dispatch bridge runner.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

try:
    from PySide2 import QtCore
except Exception as exc:  # pragma: no cover - runtime-only bootstrap
    print(f"Failed to import PySide2.QtCore: {exc}")
    raise

DISPATCH_PATH = Path(r"C:\Users\topgu\O3DEBridge\windows-o3de-bridge-dispatch.py")
POLL_INTERVAL_MS = 1500
STATE_PATH = Path(r"C:\Users\topgu\O3DEBridge\bootstrap-status.json")
_TIMER = None
_RUNNING = False


def _write_state(installed: bool) -> None:
    payload = {
        'installed': installed,
        'dispatch_path': str(DISPATCH_PATH),
        'poll_interval_ms': POLL_INTERVAL_MS,
        'running': _RUNNING,
    }
    STATE_PATH.write_text(__import__('json').dumps(payload, indent=2, sort_keys=True), encoding='utf-8')


def _tick() -> None:
    global _RUNNING
    if _RUNNING:
        return
    _RUNNING = True
    _write_state(installed=True)
    try:
        if DISPATCH_PATH.exists():
            runpy.run_path(str(DISPATCH_PATH), run_name="__main__")
    except Exception as exc:
        print(f"O3DE bridge bootstrap tick error: {exc}")
    finally:
        _RUNNING = False
        _write_state(installed=True)


def install() -> None:
    global _TIMER
    if _TIMER is not None:
        print("O3DE bridge bootstrap already installed.")
        return

    app = QtCore.QCoreApplication.instance()
    if app is None:
        raise RuntimeError("No Qt application instance found in O3DE editor runtime.")

    timer = QtCore.QTimer()
    timer.setInterval(POLL_INTERVAL_MS)
    timer.timeout.connect(_tick)
    timer.start()
    _TIMER = timer
    _write_state(installed=True)
    print(f"O3DE bridge bootstrap installed. Poll interval: {POLL_INTERVAL_MS} ms")


def uninstall() -> None:
    global _TIMER
    if _TIMER is None:
        print("O3DE bridge bootstrap is not installed.")
        return
    _TIMER.stop()
    _TIMER.deleteLater()
    _TIMER = None
    _write_state(installed=False)
    print("O3DE bridge bootstrap uninstalled.")


def status() -> None:
    installed = _TIMER is not None
    payload = {
        'installed': installed,
        'dispatch_path': str(DISPATCH_PATH),
        'poll_interval_ms': POLL_INTERVAL_MS,
        'running': _RUNNING,
        'state_path': str(STATE_PATH),
    }
    print(payload)
    _write_state(installed=installed)


if __name__ == '__main__':
    install()

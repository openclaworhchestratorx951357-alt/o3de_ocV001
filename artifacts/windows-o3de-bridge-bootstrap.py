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
_TIMER = None
_RUNNING = False


def _tick() -> None:
    global _RUNNING
    if _RUNNING:
        return
    _RUNNING = True
    try:
        if DISPATCH_PATH.exists():
            runpy.run_path(str(DISPATCH_PATH), run_name="__main__")
    except Exception as exc:
        print(f"O3DE bridge bootstrap tick error: {exc}")
    finally:
        _RUNNING = False


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
    print(f"O3DE bridge bootstrap installed. Poll interval: {POLL_INTERVAL_MS} ms")


def uninstall() -> None:
    global _TIMER
    if _TIMER is None:
        print("O3DE bridge bootstrap is not installed.")
        return
    _TIMER.stop()
    _TIMER.deleteLater()
    _TIMER = None
    print("O3DE bridge bootstrap uninstalled.")


def status() -> None:
    installed = _TIMER is not None
    print({
        'installed': installed,
        'dispatch_path': str(DISPATCH_PATH),
        'poll_interval_ms': POLL_INTERVAL_MS,
    })


if __name__ == '__main__':
    install()

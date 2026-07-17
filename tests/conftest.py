"""Shared test setup for the Windows-focused TimePulse module."""

import ctypes
import os
import sys
from pathlib import Path

# Avoid loading a real tray backend in headless test environments.
os.environ.setdefault("PYSTRAY_BACKEND", "dummy")

# TimePulse is Windows-only. This compatibility alias allows its pure utility
# logic to be imported and tested on non-Windows CI runners.
if not hasattr(ctypes, "WINFUNCTYPE"):
    ctypes.WINFUNCTYPE = ctypes.CFUNCTYPE

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

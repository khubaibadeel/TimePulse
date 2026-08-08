# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files


PROJECT_DIR = Path(SPECPATH)

# Use the application's actual icon file.
ICON_PATH = PROJECT_DIR / "newico.ico"
if not ICON_PATH.is_file():
    raise FileNotFoundError(
        f"Required application icon not found: {ICON_PATH}"
    )

datas = collect_data_files("customtkinter")

datas.append((str(ICON_PATH), "."))

RINGTONES_PATH = PROJECT_DIR / "ringtones"
if RINGTONES_PATH.is_dir():
    datas.append((str(RINGTONES_PATH), "ringtones"))


a = Analysis(
    [str(PROJECT_DIR / "Alarm.py")],
    pathex=[str(PROJECT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Alarm",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_PATH),
)

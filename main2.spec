# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main2.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\AchuAbu\\Desktop\\SIH\\solid-umbrella/rep.py', '.')],
    hiddenimports=[],
    hiddenimports=[
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebChannel',
        # Add any additional modules you may use
    ],
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
    [],
    exclude_binaries=True,
    name='main2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main2',
)

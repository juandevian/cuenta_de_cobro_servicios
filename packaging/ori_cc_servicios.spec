# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para compilar ori-cc-servicios.exe (aplicación principal)
GUI de importación de facturas con conexión a MySQL.

Compilar desde la raíz del proyecto:
    pyinstaller packaging/ori_cc_servicios.spec --clean

Salida:
    dist/ori-cc-servicios/ (carpeta con ejecutable y dependencias)
"""

block_cipher = None

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../assets/database_schema.sql', 'assets'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'mysql.connector',
        'pandas',
        'openpyxl',
        'pydantic',
        'colorlog',
        'dateutil',
        'keyring',
        'keyring.backends',
        'keyring.backends.Windows',
        'win32ctypes',
        'win32ctypes.core',
        'win32ctypes.win32cred',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ori-cc-servicios',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No mostrar consola, solo GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un .ico aquí si tienes
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ori-cc-servicios',
)

# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para compilar set_password.exe
Herramienta standalone para registrar contraseñas en Windows Credential Manager.

Compilar desde la raíz del proyecto:
    pyinstaller packaging/set_password.spec --clean

Salida:
    dist/set_password.exe (ejecutable único sin dependencias externas)
"""

block_cipher = None

a = Analysis(
    ['../src/tools/set_password_tool.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
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
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PyQt5',
        'openpyxl',
        'mysql',
        'dotenv',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='set_password',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un icono si lo deseas
)

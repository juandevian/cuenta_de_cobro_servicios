# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para compilar ori-cc-servicios.exe (aplicación principal)
GUI de importación de facturas con conexión a MySQL.

Compilar desde la raíz del proyecto:
    pyinstaller packaging/ori_cc_servicios.spec --clean

Salida:
    dist/ori-cc-servicios/ (carpeta con ejecutable y dependencias)
"""
import os
import sys

# Detectar ruta de mysql.connector dinámicamente
try:
    import mysql.connector
    mysql_base_path = os.path.dirname(mysql.connector.__file__)
    mysql_locales_src = os.path.join(mysql_base_path, 'locales')
    mysql_locales_exists = os.path.isdir(mysql_locales_src)
except ImportError:
    mysql_locales_exists = False
    mysql_locales_src = None

block_cipher = None

# Preparar datas dinámicamente
datas_list = [
    ('../assets/database_schema.sql', 'assets'),
]

# Incluir archivos de localización de MySQL si existen
if mysql_locales_exists:
    datas_list.append((mysql_locales_src, 'mysql/connector/locales'))

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'mysql.connector',
        'mysql.connector.locales.eng',
        'mysql.connector.plugins',
        'mysql.connector.plugins.mysql_native_password',
        'mysql.connector.plugins.caching_sha2_password',
        'mysql.connector.plugins.sha256_password',
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

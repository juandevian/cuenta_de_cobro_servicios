# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para compilar ori-cc-servicios.exe (aplicación principal)
GUI de importación de facturas con conexión a MySQL.

Compilar desde la raíz del proyecto con entorno virtual activado:
    pyinstaller packaging/ori_cc_servicios.spec --clean

Salida:
    dist/ori-cc-servicios/ (carpeta con ejecutable y dependencias)
"""
import os
import sys
from PyInstaller.utils.hooks import collect_all

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

# CRITICAL: Recolectar numpy/pandas con collect_all y filtrar _distributor_init.py
# Este archivo hace que numpy piense que está en modo desarrollo, causando el error:
# "you should not try to import numpy from its source directory"
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')

# Filtrar _distributor_init.py de numpy para evitar detección de "development mode"
numpy_datas = [(src, dst) for src, dst in numpy_datas if '_distributor_init' not in src]

# Preparar datas dinámicamente
datas_list = [
    ('../assets/database_schema.sql', 'assets'),
]

# Incluir archivos de localización de MySQL si existen
if mysql_locales_exists:
    datas_list.append((mysql_locales_src, 'mysql/connector/locales'))

# Agregar numpy y pandas data files filtrados
datas_list.extend(numpy_datas)
datas_list.extend(pandas_datas)

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=numpy_binaries + pandas_binaries,
    datas=datas_list,
    hiddenimports=[
        # PyQt5
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',

        # MySQL
        'mysql.connector',
        'mysql.connector.locales.eng',
        'mysql.connector.plugins',
        'mysql.connector.plugins.mysql_native_password',
        'mysql.connector.plugins.caching_sha2_password',
        'mysql.connector.plugins.sha256_password',

        # OpenPyXL
        'openpyxl',

        # Pydantic
        'pydantic',

        # colorlog
        'colorlog',

        # Dateutil
        'dateutil',

        # Keyring
        'keyring',
        'keyring.backends',
        'keyring.backends.Windows',

        # Win32ctypes
        'win32ctypes',
        'win32ctypes.core',
        'win32ctypes.win32cred',

    ] + numpy_hiddenimports + pandas_hiddenimports,  # Agregar imports auto-detectados
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir módulos de testing y desarrollo
        'numpy.tests',
        'numpy.testing',
        'pandas.tests',
        'pandas._testing',
        'pandas.conftest',
        'matplotlib.tests',
        'PIL.tests',
        'test',
        'tests',
        'testing',
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
    [],
    exclude_binaries=True,
    name='ori-cc-servicios',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../assets/icon.ico' if os.path.exists('../assets/icon.ico') else None,
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

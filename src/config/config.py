"""
Configuración de la aplicación Panorama_net
"""
import os
import sys
from typing import Optional
import json
from dotenv import load_dotenv


def _load_env_priority() -> None:
    """Carga variables de entorno desde distintas ubicaciones con prioridad.

    Prioridad (primero que exista):
    1) Carpeta del ejecutable (cuando está empaquetado con PyInstaller)
    2) Directorio de trabajo actual (fallback por defecto)

    Nota: Las variables ya presentes en el entorno NO se sobrescriben.
    """
    candidates = []

    # 1) Carpeta del ejecutable cuando está 'frozen'
    try:
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            candidates.append(os.path.join(exe_dir, '.env'))
    except Exception:
        pass

    # 2) Directorio de trabajo actual
    candidates.append(os.path.join(os.getcwd(), '.env'))

    for path in candidates:
        try:
            if os.path.isfile(path):
                # Only override if not set (override=False)
                print(f"Cargando variables de entorno desde: {path}")   
                load_dotenv(path, override=False)
        except Exception:
            # Silencioso: no bloquear la app por problemas de lectura
            continue


_load_env_priority()


def _load_config_json_priority() -> None:
    """Carga config.json (sin secretos) y exporta valores a ENV si no están definidos.

    Ubicación: Siempre busca en la carpeta raíz donde se ejecuta el programa.
    - En producción (PyInstaller): carpeta del .exe
    - En desarrollo: directorio de trabajo actual
    """
    # Determinar la carpeta raíz del ejecutable
    if getattr(sys, 'frozen', False):
        # Producción: carpeta donde está el .exe
        root_dir = os.path.dirname(sys.executable)
    else:
        root_dir = os.getcwd()
    
    config_path = os.path.join(root_dir, 'config.json')
    
    try:
        if os.path.isfile(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Mapear claves esperadas
            mapping = {
                'host': 'DB_HOST',
                'port': 'DB_PORT',
                'username': 'DB_USERNAME',
                'database': 'DB_NAME',
            }
            for k, envk in mapping.items():
                if k in data and not os.getenv(envk):
                    os.environ[envk] = str(data[k])
    except Exception:
        # Silencioso: no bloquear la app si no hay config.json
        pass

_load_config_json_priority()

class Config:
    """Configuración de la aplicación"""

    # Configuración de la base de datos
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    DB_USERNAME: str = os.getenv('DB_USERNAME', '')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'panorama_net')

    # Configuración de la aplicación
    APP_NAME: str = "Importación de Facturas de servicios con consumos"
    APP_VERSION: str = "0.1.0"
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600

    # Configuración de archivos
    SUPPORTED_EXCEL_FORMATS: tuple = ('.xlsx', '.xls')
    MAX_FILE_SIZE_MB: int = 50

    # Configuración de logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Servicio de keyring para recuperar contraseña en Windows Credential Manager
    KEYRING_SERVICE: str = os.getenv('KEYRING_SERVICE', 'ori-cc-servicios')

    @classmethod
    def get_database_url(cls) -> str:
        """Genera la URL de conexión a la base de datos (solo para referencia/logs)."""
        user = cls.DB_USERNAME or '<user>'
        host = cls.DB_HOST or '<host>'
        name = cls.DB_NAME or '<db>'
        return f"mysql://{user}:***@{host}:{cls.DB_PORT}/{name}"

    @classmethod
    def validate_config(cls) -> bool:
        """Valida la configuración mínima de la base de datos."""
        required_vars = ['DB_HOST', 'DB_USERNAME', 'DB_NAME']
        for var in required_vars:
            if not getattr(cls, var):
                return False
        return True
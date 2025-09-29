"""
Configuración de la aplicación Panorama_net
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde un archivo .env

class Config:
    """Configuración de la aplicación"""

    # Configuración de la base de datos
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    DB_USER: str = os.getenv('DB_USERNAME', '')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'panorama_net')

    # Configuración de la aplicación
    APP_NAME: str = "Importación de Facturas de Servicios con Consumos"
    APP_VERSION: str = "1.0.0"
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600

    # Configuración de archivos
    SUPPORTED_EXCEL_FORMATS: tuple = ('.xlsx', '.xls')
    MAX_FILE_SIZE_MB: int = 50

    # Configuración de logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @classmethod
    def get_database_url(cls) -> str:
        """Genera la URL de conexión a la base de datos"""
        return f"mysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

    @classmethod
    def validate_config(cls) -> bool:
        """Valida la configuración de la aplicación"""
        required_vars = ['DB_HOST', 'DB_USER', 'DB_NAME']
        for var in required_vars:
            if not getattr(cls, var):
                return False
        return True
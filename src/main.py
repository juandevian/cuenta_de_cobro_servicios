#!/usr/bin/env python3
"""
Sistema de Importación de Facturas de servicios con consumos
Programa de escritorio multiplataforma para importar items a cobrar desde Excel a Orión Plus
"""
import os
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import colorlog

from src.ui.main_window import MainWindow
from src.config.config import Config
from src.services.database import DatabaseConnection
from src.utils import resource_path

def setup_logging():
    """Configura el sistema de logging"""
    # Crear logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # Crear formato para consola con colores
    console_format = colorlog.ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Handler para archivo (Archivo de Log)
    try:
        file_handler = logging.FileHandler('ori_cc_servicios.log', encoding='utf-8')
        file_format = logging.Formatter(Config.LOG_FORMAT)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logging.warning(f"No se pudo crear archivo de log: {e}")

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    required_modules = [    
        'colorlog',
        'dateutil',
        'dotenv',
        'keyring',
        'mysql.connector',
        'openpyxl',
        'pandas',
        'pydantic',
        'PyQt5',
        'pytest'
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            logging.info(f"✓ {module} disponible")
        except ImportError:
            missing_modules.append(module)
            logging.error(f"✗ {module} no encontrado")

    if missing_modules:
        logging.error(f"Módulos faltantes: {', '.join(missing_modules)}")
        logging.error("Instale las dependencias con: pip install -r requirements.txt")
        return False

    return True

def create_database_schema():
    """Crea el esquema de la base de datos si no existe"""
    try:
        logging.info("Verificando esquema de base de datos...")

        db = DatabaseConnection()

        if not db.connection:
            logging.warning("No se pudo conectar a la base de datos")
            logging.warning("La aplicación continuará, pero las funciones de BD no estarán disponibles")
            return False
            
        if not db.connection.is_connected():
            logging.warning("Conexión a BD no está activa")
            logging.info("La aplicación no se iniciará")
            return False

        # Leer archivo SQL (opcional)
        schema_file = resource_path('assets/database_schema.sql')
        
        if not os.path.exists(schema_file):
            logging.info("Archivo de esquema SQL no encontrado, omitiendo verificación")
            db.disconnect()
            return True
                   
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()      

        # Dividir el script en comandos individuales
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

        # Disponer cursor para ejecutar comandos
        cursor = db.connection.cursor()

        for command in commands:
            if command:
                try:
                    cursor.execute(command)
                    logging.debug(f"Comando ejecutado: {command[:50]}...")
                except Exception as e:
                    logging.warning(f"Error ejecutando comando: {e}")

        db.connection.commit()
        cursor.close()
        db.disconnect()

        logging.info("Esquema de base de datos verificado/creado exitosamente")
        return True

    except Exception as e:
        logging.error(f"Error creando esquema de base de datos: {e}")
        return False

def validate_database_schema():
    """Valida que el esquema de la base de datos sea correcto"""
    try:
        logging.info("Validando esquema de base de datos...")

        db = DatabaseConnection()

        if not db.connection:
            logging.warning("No se pudo conectar a la base de datos")
            return False
            
        if not db.connection.is_connected():
            logging.warning("Conexión a BD no está activa")
            return False

        is_valid = db.validate_database_schema()

        db.disconnect()

        if is_valid:
            logging.info("Esquema de base de datos es válido")
        else:
            logging.warning("Esquema de base de datos no es válido")

        return is_valid

    except Exception as e:
        logging.error(f"Error validando esquema de base de datos: {e}")
        return False

def main():
    """Función principal de la aplicación"""
    # Configurar logging
    setup_logging()
    logging.info("Iniciando Sistema de Importación de Facturas Orión Plus")
    logging.info(f"Versión: {Config.APP_VERSION}")

    # Verificar dependencias
    if not check_requirements():
        logging.critical("Error de Dependencias: Faltan dependencias requeridas. Instale con: pip install -r requirements.txt")
        sys.exit(1)

    # Crear esquema de base de datos
    if not create_database_schema():
        logging.warning("No se pudo verificar/crear el esquema de base de datos")
        logging.warning("Asegúrese de que la base de datos esté configurada correctamente")

    if not validate_database_schema():
        logging.critical("El esquema de la base de datos no es válido")
        logging.warning("Error de Base de Datos\nVerifique la versión de Orión Plus, recuerde que debe ser V17.383.419 o superior.")
        sys.exit(1)

    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)
    app.setApplicationVersion(Config.APP_VERSION)

    # Configurar fuente por defecto
    default_font = QFont("Arial", 10)
    app.setFont(default_font)

    # Crear ventana principal
    try:
        main_window = MainWindow()
        main_window.show()

        logging.info("Aplicación iniciada exitosamente")
        logging.info(f"Interfaz de usuario: {Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # Ejecutar aplicación
        sys.exit(app.exec_())

    except Exception as e:
        logging.critical(f"Error fatal al iniciar la aplicación: {e}")
        QMessageBox.critical(
            None,
            "Error Fatal",
            f"No se pudo iniciar la aplicación: {str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
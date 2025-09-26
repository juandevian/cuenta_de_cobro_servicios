#!/usr/bin/env python3
"""
Sistema de Importación de Facturas Panorama_net - Versión SQLite
Programa de escritorio multiplataforma para importar facturas desde Excel a SQLite
"""
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import colorlog

from main_window import MainWindow
from config import Config
from database_sqlite import SQLiteConnection

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

    # Handler para archivo (opcional)
    try:
        file_handler = logging.FileHandler('panorama_net_sqlite.log', encoding='utf-8')
        file_format = logging.Formatter(Config.LOG_FORMAT)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except Exception as e:
        logging.warning(f"No se pudo crear archivo de log: {e}")

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    required_modules = [
        'PyQt5',
        'pandas',
        'openpyxl',
        'pydantic',
        'python_dateutil',
        'colorlog'
    ]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module.replace('_', '.'))  # Para manejar módulos con guiones bajos
            logging.info(f"[OK] {module} disponible")
        except ImportError:
            missing_modules.append(module)
            logging.error(f"[ERROR] {module} no encontrado")

    if missing_modules:
        logging.error(f"Módulos faltantes: {', '.join(missing_modules)}")
        logging.error("Instale las dependencias con: pip install -r requirements.txt")
        return False

    return True

def create_database_schema():
    """Crea el esquema de la base de datos SQLite si no existe"""
    try:
        logging.info("Verificando esquema de base de datos SQLite...")

        db = SQLiteConnection()

        if not db.connection:
            logging.error("No se pudo conectar a la base de datos SQLite")
            return False

        # Crear tablas
        if db.create_tables():
            logging.info("Esquema de base de datos SQLite verificado/creado exitosamente")
        else:
            logging.error("Error creando esquema de base de datos SQLite")
            return False

        # Insertar datos de ejemplo si no hay datos
        invoices_count = db.get_invoices_count()
        if invoices_count == 0:
            logging.info("Insertando datos de ejemplo...")
            db.insert_sample_data()

        db.disconnect()
        return True

    except Exception as e:
        logging.error(f"Error creando esquema de base de datos SQLite: {e}")
        return False

def main():
    """Función principal de la aplicación"""
    # Configurar logging
    setup_logging()
    logging.info("Iniciando Sistema de Importación de Facturas Panorama_net (SQLite)")
    logging.info(f"Versión: {Config.APP_VERSION}")

    # Verificar dependencias
    if not check_requirements():
        QMessageBox.critical(
            None,
            "Error de Dependencias",
            "Faltan dependencias requeridas. Instale con: pip install -r requirements.txt"
        )
        sys.exit(1)

    # Crear esquema de base de datos
    if not create_database_schema():
        logging.warning("No se pudo verificar/crear el esquema de base de datos SQLite")
        logging.warning("Ejecutando init_sqlite.py para configurar la base de datos...")

        # Intentar ejecutar el script de inicialización
        result = subprocess.run([sys.executable, 'init_sqlite.py'],
                              capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            logging.error("Error ejecutando init_sqlite.py")
            logging.error(result.stderr)

            QMessageBox.warning(
                None,
                "Base de Datos",
                "No se pudo configurar automáticamente la base de datos SQLite.\n"
                "Ejecute manualmente: python init_sqlite.py"
            )

    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName(f"{Config.APP_NAME} (SQLite)")
    app.setApplicationVersion(Config.APP_VERSION)

    # Configurar fuente por defecto
    default_font = QFont("Arial", 10)
    app.setFont(default_font)

    # Crear ventana principal con SQLite
    try:
        # Modificar la ventana principal para usar SQLite
        main_window = MainWindow()

        # Reemplazar el procesador de MySQL con SQLite
        from invoice_processor_sqlite import InvoiceProcessorSQLite
        main_window.processor = InvoiceProcessorSQLite()

        main_window.show()

        logging.info("Aplicación SQLite iniciada exitosamente")
        logging.info(f"Interfaz de usuario: {Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        logging.info("Base de datos: SQLite (panorama_net.db)")

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
    import subprocess
    main()
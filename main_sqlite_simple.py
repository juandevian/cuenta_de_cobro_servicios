#!/usr/bin/env python3
"""
Sistema de Importación de Facturas Panorama_net - Versión SQLite Simplificada
Programa de escritorio multiplataforma para importar facturas desde Excel a SQLite
"""
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from main_window import MainWindow
from config import Config
from database_sqlite import SQLiteConnection
from invoice_processor_sqlite import InvoiceProcessorSQLite

def main():
    """Función principal de la aplicación"""
    # Configurar logging básico
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Iniciando Sistema de Importación de Facturas Panorama_net (SQLite)")
    logger.info(f"Versión: {Config.APP_VERSION}")

    # Verificar que las dependencias básicas estén disponibles
    try:
        import PyQt5
        import pandas
        import openpyxl
        import sqlite3
        logger.info("Dependencias verificadas correctamente")
    except ImportError as e:
        logger.error(f"Error de dependencias: {e}")
        QMessageBox.critical(
            None,
            "Error de Dependencias",
            f"Faltan dependencias requeridas: {e}\nInstale con: pip install -r requirements.txt"
        )
        sys.exit(1)

    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName(f"{Config.APP_NAME} (SQLite)")
    app.setApplicationVersion(Config.APP_VERSION)

    # Configurar fuente por defecto
    default_font = QFont("Arial", 10)
    app.setFont(default_font)

    # Crear ventana principal con SQLite
    try:
        main_window = MainWindow()
        main_window.processor = InvoiceProcessorSQLite()
        main_window.show()

        logger.info("Aplicación SQLite iniciada exitosamente")
        logger.info(f"Interfaz de usuario: {Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        logger.info("Base de datos: SQLite (panorama_net.db)")

        # Ejecutar aplicación
        sys.exit(app.exec_())

    except Exception as e:
        logger.critical(f"Error fatal al iniciar la aplicación: {e}")
        QMessageBox.critical(
            None,
            "Error Fatal",
            f"No se pudo iniciar la aplicación: {str(e)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
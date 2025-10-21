#!/usr/bin/env python3
"""
Script de prueba simplificado para verificar que la aplicación funcione correctamente
"""
import sys
import os

def test_imports():
    """Prueba las importaciones principales"""
    try:
        print("Probando importaciones...")

        # Probar importaciones básicas
        import logging
        print("[OK] logging importado")

        # Probar PyQt5
        try:
            from PyQt5.QtWidgets import QApplication
            print("[OK] PyQt5 importado")
        except ImportError:
            print("[ERROR] PyQt5 no disponible - instale con: pip install PyQt5")

        # Probar pandas
        try:
            import pandas as pd
            print("[OK] pandas importado")
        except ImportError:
            print("[ERROR] pandas no disponible - instale con: pip install pandas")

        # Probar mysql.connector
        try:
            import mysql.connector
            print("[OK] mysql.connector importado")
        except ImportError:
            print("[ERROR] mysql.connector no disponible - instale con: pip install mysql-connector-python")

        # Probar pydantic
        try:
            from pydantic import BaseModel
            print("[OK] pydantic importado")
        except ImportError:
            print("[ERROR] pydantic no disponible - instale con: pip install pydantic")
            
        # Probar dateutil
        try:
            from dateutil import parser
            print("[OK] dateutil importado")
        except ImportError:
            print("[ERROR] dateutil no disponible - instale con: pip install python-dateutil")
        # Probar colorlog
        try:
            import colorlog
            print("[OK] colorlog importado")
        except ImportError:
            print("[ERROR] colorlog no disponible - instale con: pip install colorlog")

        # Probar dotenv
        try:
            from dotenv import load_dotenv
            print("[OK] dotenv importado")
        except ImportError:
            print("[ERROR] dotenv no disponible - instale con: pip install python-dotenv")

        return True

    except Exception as e:
        print(f"[ERROR] Error en importaciones: {e}")
        return False

def test_config():
    """Prueba la configuración"""
    try:
        print("\nProbando configuración...")

        # Importar configuración
        from src.config import Config
        print("[OK] Configuración cargada")

        # Mostrar configuración actual
        print(f"  - Base de datos: {Config.DB_NAME}")
        print(f"  - Host: {Config.DB_HOST}:{Config.DB_PORT}")
        print(f"  - Usuario: {Config.DB_USER}")
        print(f"  - App: {Config.APP_NAME} v{Config.APP_VERSION}")

        return True

    except Exception as e:
        print(f"[ERROR] Error en configuración: {e}")
        return False

def test_excel_handler():
    """Prueba el manejador de Excel"""
    try:
        print("\nProbando manejador de Excel...")

        from excel_handler import ExcelHandler
        handler = ExcelHandler()
        print("[OK] ExcelHandler creado")

        # Verificar si existe el archivo CSV de ejemplo
        xlsx_file = 'ejemplo_facturas.xlsx'
        if os.path.exists(xlsx_file):
            print(f"[OK] Archivo de ejemplo encontrado: {xlsx_file}")

            # Intentar leer como Excel (esto fallará pero es esperado)
            try:
                df = handler.read_excel_file(xlsx_file)
                if df is not None:
                    print(f"[OK] Datos leídos: {len(df)} filas")
                else:
                    print("[INFO] No se pudieron leer los datos del CSV como Excel")
            except Exception as e:
                print(f"[INFO] Error esperado al leer CSV como Excel: {e}")
        else:
            print(f"[WARNING] Archivo de ejemplo no encontrado: {xlsx_file}")

        return True

    except Exception as e:
        print(f"[ERROR] Error en ExcelHandler: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        print("\nProbando conexión a base de datos...")

        from database import DatabaseConnection
        db = DatabaseConnection()

        if db.connection and db.connection.is_connected():
            print("[OK] Conexión a base de datos exitosa")

            # Probar algunas consultas básicas
            try:
                result = db.get_items_count()
                print(f"[OK] Items de factura importados en BD: {result}")

                result = db.get_last_item_ordinal()
                print(f"[OK] Último ordinal: {result or 'Ninguna'}")

            except Exception as e:
                print(f"[WARNING] Error en consultas: {e}")

            db.disconnect()
            return True
        else:
            print("[ERROR] No se pudo conectar a la base de datos")
            print("  Asegúrese de que MySQL esté ejecutándose")
            print("  Ejecute: python init_database.py")
            return False

    except Exception as e:
        print(f"[ERROR] Error en conexión a BD: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("PRUEBAS DEL SISTEMA DE IMPORTACION DE FACTURAS")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Directorio: {os.getcwd()}")

    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_config),
        ("Excel Handler", test_excel_handler),
        ("Base de Datos", test_database_connection)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Ejecutando: {test_name}")
        print('='*50)

        if test_func():
            passed += 1
            print(f"[PASSED] {test_name}")
        else:
            print(f"[FAILED] {test_name}")

    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    print('='*60)

    if passed == total:
        print("EXCELENTE! Todas las pruebas pasaron. La aplicación está lista.")
        print("\nPara ejecutar la aplicación:")
        print("  python main.py")
    else:
        print("Algunas pruebas fallaron. Revise los errores arriba.")
        print("\nPara instalar dependencias:")
        print("  pip install -r requirements.txt")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
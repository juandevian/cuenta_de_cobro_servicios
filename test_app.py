#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funcione correctamente
"""
import sys
import os

def test_imports():
    """Prueba las importaciones principales"""
    try:
        print("Probando importaciones...")

        # Probar importaciones básicas
        import logging
        print("✓ logging importado")

        # Probar PyQt5 (esto puede fallar si no está instalado)
        try:
            from PyQt5.QtWidgets import QApplication
            print("✓ PyQt5 importado")
        except ImportError:
            print("⚠ PyQt5 no disponible - instale con: pip install PyQt5")

        # Probar pandas (puede fallar si no está instalado)
        try:
            import pandas as pd
            print("✓ pandas importado")
        except ImportError:
            print("⚠ pandas no disponible - instale con: pip install pandas")

        # Probar mysql.connector (puede fallar si no está instalado)
        try:
            import mysql.connector
            print("✓ mysql.connector importado")
        except ImportError:
            print("⚠ mysql.connector no disponible - instale con: pip install mysql-connector-python")

        return True

    except Exception as e:
        print(f"✗ Error en importaciones: {e}")
        return False

def test_config():
    """Prueba la configuración"""
    try:
        print("\nProbando configuración...")

        # Importar configuración
        from config import Config
        print("✓ Configuración cargada")

        # Mostrar configuración actual
        print(f"  - Base de datos: {Config.DB_NAME}")
        print(f"  - Host: {Config.DB_HOST}:{Config.DB_PORT}")
        print(f"  - Usuario: {Config.DB_USER}")
        print(f"  - App: {Config.APP_NAME} v{Config.APP_VERSION}")

        return True

    except Exception as e:
        print(f"✗ Error en configuración: {e}")
        return False

def test_excel_handler():
    """Prueba el manejador de Excel"""
    try:
        print("\nProbando manejador de Excel...")

        from excel_handler import ExcelHandler
        handler = ExcelHandler()
        print("✓ ExcelHandler creado")

        # Verificar si existe el archivo CSV de ejemplo
        csv_file = 'ejemplo_facturas.csv'
        if os.path.exists(csv_file):
            print(f"✓ Archivo de ejemplo encontrado: {csv_file}")

            # Intentar leer como Excel (esto fallará pero es esperado)
            try:
                df = handler.read_excel_file(csv_file)
                if df is not None:
                    print(f"✓ Datos leídos: {len(df)} filas")
                else:
                    print("⚠ No se pudieron leer los datos del CSV como Excel")
            except Exception as e:
                print(f"⚠ Error esperado al leer CSV como Excel: {e}")
        else:
            print(f"⚠ Archivo de ejemplo no encontrado: {csv_file}")

        return True

    except Exception as e:
        print(f"✗ Error en ExcelHandler: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        print("\nProbando conexión a base de datos...")

        from database import DatabaseConnection
        db = DatabaseConnection()

        if db.connection and db.connection.is_connected():
            print("✓ Conexión a base de datos exitosa")

            # Probar algunas consultas básicas
            try:
                result = db.get_invoices_count()
                print(f"✓ Facturas en BD: {result}")

                result = db.get_last_invoice_number()
                print(f"✓ Última factura: {result or 'Ninguna'}")

            except Exception as e:
                print(f"⚠ Error en consultas: {e}")

            db.disconnect()
            return True
        else:
            print("⚠ No se pudo conectar a la base de datos")
            print("  Asegúrese de que MySQL esté ejecutándose")
            print("  Ejecute: python init_database.py")
            return False

    except Exception as e:
        print(f"✗ Error en conexión a BD: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=== PRUEBAS DEL SISTEMA DE IMPORTACIÓN DE FACTURAS ===")
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
            print(f"✓ {test_name}: PASSED")
        else:
            print(f"✗ {test_name}: FAILED")

    print(f"\n{'='*60}")
    print(f"RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    print('='*60)

    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista.")
        print("\nPara ejecutar la aplicación:")
        print("  python main.py")
    else:
        print("⚠ Algunas pruebas fallaron. Revise los errores arriba.")
        print("\nPara instalar dependencias:")
        print("  pip install -r requirements.txt")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
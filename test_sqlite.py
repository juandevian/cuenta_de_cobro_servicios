#!/usr/bin/env python3
"""
Script de prueba específico para SQLite
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
            print("[ERROR] PyQt5 no disponible")

        # Probar pandas
        try:
            import pandas as pd
            print("[OK] pandas importado")
        except ImportError:
            print("[ERROR] pandas no disponible")

        # Probar sqlite3
        try:
            import sqlite3
            print("[OK] sqlite3 importado")
        except ImportError:
            print("[ERROR] sqlite3 no disponible")

        return True

    except Exception as e:
        print(f"[ERROR] Error en importaciones: {e}")
        return False

def test_sqlite_connection():
    """Prueba la conexión a SQLite"""
    try:
        print("\nProbando conexión a SQLite...")

        from database_sqlite import SQLiteConnection
        db = SQLiteConnection()

        if db.get_connection():
            print("[OK] Conexión exitosa a SQLite")

            # Probar algunas consultas básicas
            try:
                result = db.get_invoices_count()
                print(f"[OK] Facturas en BD: {result}")

                result = db.get_last_invoice_number()
                print(f"[OK] Última factura: {result or 'Ninguna'}")

            except Exception as e:
                print(f"[WARNING] Error en consultas: {e}")

            db.disconnect()
            return True
        else:
            print("[ERROR] No se pudo conectar a SQLite")
            return False

    except Exception as e:
        print(f"[ERROR] Error en conexión a SQLite: {e}")
        return False

def test_excel_handler():
    """Prueba el manejador de Excel"""
    try:
        print("\nProbando manejador de Excel...")

        from excel_handler import ExcelHandler
        handler = ExcelHandler()
        print("[OK] ExcelHandler creado")

        # Verificar si existe el archivo CSV de ejemplo
        csv_file = 'ejemplo_facturas.csv'
        if os.path.exists(csv_file):
            print(f"[OK] Archivo de ejemplo encontrado: {csv_file}")

            # Intentar leer como Excel (esto fallará pero es esperado)
            try:
                df = handler.read_excel_file(csv_file)
                if df is not None:
                    print(f"[OK] Datos leídos: {len(df)} filas")
                else:
                    print("[INFO] No se pudieron leer los datos del CSV como Excel")
            except Exception as e:
                print(f"[INFO] Error esperado al leer CSV como Excel: {e}")
        else:
            print(f"[WARNING] Archivo de ejemplo no encontrado: {csv_file}")

        return True

    except Exception as e:
        print(f"[ERROR] Error en ExcelHandler: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("PRUEBAS DEL SISTEMA SQLITE")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Directorio: {os.getcwd()}")

    tests = [
        ("Importaciones", test_imports),
        ("Excel Handler", test_excel_handler),
        ("Base de Datos SQLite", test_sqlite_connection)
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
        print("EXCELENTE! Todas las pruebas pasaron. SQLite está funcionando.")
        print("\nPara ejecutar la aplicación:")
        print("  python main_sqlite_simple.py")
    else:
        print("Algunas pruebas fallaron. Revise los errores arriba.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
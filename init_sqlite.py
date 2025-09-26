#!/usr/bin/env python3
"""
Script de inicialización de base de datos SQLite para Panorama_net
Versión alternativa para desarrollo y pruebas sin necesidad de MySQL
"""
import sys
import logging
import os
from database_sqlite import SQLiteConnection

def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('database_sqlite_init.log', encoding='utf-8')
        ]
    )

def main():
    """Función principal"""
    setup_logging()
    logging.info("Iniciando configuración de base de datos SQLite para Panorama_net")

    print("CONFIGURACION DE SQLITE PARA EL SISTEMA DE FACTURACION")
    print("="*60)

    # Crear conexión SQLite
    db = SQLiteConnection()

    if not db.connection:
        logging.error("No se pudo conectar a SQLite")
        return False

    try:
        # Crear tablas
        print("Creando tablas...")
        if db.create_tables():
            print("[OK] Tablas creadas exitosamente")
        else:
            print("[ERROR] Error creando tablas")
            return False

        # Insertar datos de ejemplo
        print("Insertando datos de ejemplo...")
        if db.insert_sample_data():
            print("[OK] Datos de ejemplo insertados")
        else:
            print("[WARNING] Error insertando datos de ejemplo")

        # Verificar datos
        print("\nVerificando datos insertados...")

        # Contar clientes
        clients_query = "SELECT COUNT(*) as count FROM clientes"
        clients_result = db.execute_query(clients_query)
        clients_count = clients_result[0]['count'] if clients_result else 0
        print(f"[OK] Clientes en la base de datos: {clients_count}")

        # Contar facturas
        invoices_query = "SELECT COUNT(*) as count FROM facturas"
        invoices_result = db.execute_query(invoices_query)
        invoices_count = invoices_result[0]['count'] if invoices_result else 0
        print(f"[OK] Facturas en la base de datos: {invoices_count}")

        # Mostrar información de la base de datos
        db_info = {
            'database_path': db.db_path,
            'size_mb': os.path.getsize(db.db_path) / (1024 * 1024) if os.path.exists(db.db_path) else 0
        }

        print("\nINFORMACION DE LA BASE DE DATOS:")
        print(f"  - Archivo: {db_info['database_path']}")
        print(f"  - Tamaño: {db_info['size_mb']:.2f} MB")

        # Mostrar facturas de ejemplo
        print("\nFACTURAS DE EJEMPLO:")
        sample_invoices = db.execute_query("SELECT * FROM facturas LIMIT 3")
        for invoice in sample_invoices:
            print(f"  - {invoice['numero_factura']}: ${invoice['total']:.2f} - Estado: {invoice['estado']}")

    except Exception as e:
        logging.error(f"Error en la configuración: {e}")
        return False
    finally:
        db.disconnect()

    print("\n" + "="*60)
    print("CONFIGURACION SQLITE COMPLETADA!")
    print("="*60)
    print("Base de datos SQLite configurada exitosamente.")
    print("Puede ejecutar la aplicación con: python main_sqlite.py")
    print("="*60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
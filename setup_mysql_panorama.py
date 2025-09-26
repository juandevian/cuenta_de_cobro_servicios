#!/usr/bin/env python3
"""
Script para configurar MySQL y la base de datos panorama_net
Verifica existencia de base de datos y tablas, crea lo que falte
"""
import sys
import os
import subprocess
import mysql.connector
from mysql.connector import Error
from config import Config

def check_mysql_installed():
    """Verifica si MySQL está instalado"""
    try:
        result = subprocess.run(['mysql', '--version'],
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"[OK] MySQL instalado: {result.stdout.strip()}")
            return True
        else:
            print("[ERROR] MySQL no parece estar instalado o no está en el PATH")
            return False
    except Exception as e:
        print(f"[ERROR] Error verificando MySQL: {e}")
        return False

def check_mysql_running():
    """Verifica si MySQL está ejecutándose"""
    try:
        result = subprocess.run(['sc', 'query', 'MySQL'],
                              capture_output=True, text=True, shell=True)
        if 'RUNNING' in result.stdout:
            print("[OK] Servicio MySQL está ejecutándose")
            return True
        else:
            print("[WARNING] Servicio MySQL no está ejecutándose")
            return False
    except Exception as e:
        print(f"[ERROR] Error verificando servicio MySQL: {e}")
        return False

def start_mysql_service():
    """Intenta iniciar el servicio MySQL"""
    try:
        print("Intentando iniciar MySQL...")
        result = subprocess.run(['net', 'start', 'MySQL'],
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("[OK] MySQL iniciado exitosamente")
            return True
        else:
            print(f"[ERROR] No se pudo iniciar MySQL: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error iniciando MySQL: {e}")
        return False

def test_mysql_connection():
    """Prueba la conexión a MySQL"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        if connection.is_connected():
            print("[OK] Conexión exitosa a MySQL")
            connection.close()
            return True
        else:
            print("[ERROR] No se pudo conectar a MySQL")
            return False
    except Error as e:
        print(f"[ERROR] Error de conexión a MySQL: {e}")
        return False

def check_database_exists():
    """Verifica si la base de datos panorama_net existe"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{Config.DB_NAME}'")
        result = cursor.fetchone()

        if result:
            print(f"[OK] Base de datos '{Config.DB_NAME}' existe")
            cursor.close()
            connection.close()
            return True
        else:
            print(f"[WARNING] Base de datos '{Config.DB_NAME}' NO existe")
            cursor.close()
            connection.close()
            return False

    except Error as e:
        print(f"[ERROR] Error verificando base de datos: {e}")
        return False

def create_database():
    """Crea la base de datos panorama_net"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        connection.commit()

        print(f"[OK] Base de datos '{Config.DB_NAME}' creada exitosamente")

        cursor.close()
        connection.close()
        return True

    except Error as e:
        print(f"[ERROR] Error creando base de datos: {e}")
        return False

def check_tables_exist():
    """Verifica si las tablas existen en la base de datos"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        cursor = connection.cursor()

        # Verificar tablas requeridas
        required_tables = ['clientes', 'facturas', 'pagos']
        existing_tables = []
        missing_tables = []

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table in tables:
            existing_tables.append(table[0])

        for required_table in required_tables:
            if required_table in existing_tables:
                print(f"[OK] Tabla '{required_table}' existe")
            else:
                print(f"[WARNING] Tabla '{required_table}' NO existe")
                missing_tables.append(required_table)

        cursor.close()
        connection.close()

        return missing_tables

    except Error as e:
        print(f"[ERROR] Error verificando tablas: {e}")
        return []

def create_tables():
    """Crea las tablas necesarias en MySQL"""
    try:
        # Leer el archivo SQL
        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        cursor = connection.cursor()

        # Dividir el script en comandos individuales
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

        executed_commands = 0
        for command in commands:
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    executed_commands += 1
                except Error as e:
                    print(f"[WARNING] Error ejecutando comando: {e}")

        connection.commit()
        cursor.close()
        connection.close()

        print(f"[OK] Esquema de base de datos creado: {executed_commands} comandos ejecutados")
        return True

    except Error as e:
        print(f"[ERROR] Error creando tablas: {e}")
        return False

def verify_mysql_setup():
    """Verifica la configuración completa de MySQL"""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        cursor = connection.cursor()

        # Obtener información del servidor
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"[OK] Versión de MySQL: {version}")

        # Verificar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"[OK] Tablas encontradas: {len(tables)}")

        for table in tables:
            print(f"  - {table[0]}")

        # Verificar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM clientes")
        clients_count = cursor.fetchone()[0]
        print(f"[OK] Clientes en la base de datos: {clients_count}")

        cursor.execute("SELECT COUNT(*) FROM facturas")
        invoices_count = cursor.fetchone()[0]
        print(f"[OK] Facturas en la base de datos: {invoices_count}")

        cursor.close()
        connection.close()

        return True

    except Error as e:
        print(f"[ERROR] Error verificando configuración: {e}")
        return False

def show_mysql_options():
    """Muestra opciones para configurar MySQL"""
    print("\n" + "="*70)
    print("OPCIONES PARA CONFIGURAR MYSQL:")
    print("="*70)
    print("1. Si MySQL no está instalado:")
    print("   - Descargue MySQL Community Server desde:")
    print("     https://dev.mysql.com/downloads/mysql/")
    print("   - O instale XAMPP/WAMP que incluye MySQL")
    print("")
    print("2. Si MySQL está instalado pero no ejecutándose:")
    print("   - Inicie MySQL manualmente desde el panel de servicios")
    print("   - O ejecute: net start MySQL (como administrador)")
    print("")
    print("3. Si necesita configurar usuario/contraseña:")
    print("   - Abra MySQL Command Line Client")
    print("   - Ejecute: ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   - Luego actualice config.py con la nueva contraseña")
    print("")
    print("4. Configuración actual en config.py:")
    print(f"   - Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"   - Usuario: {Config.DB_USER}")
    print(f"   - Base de datos: {Config.DB_NAME}")
    print("="*70)

def main():
    """Función principal"""
    print("CONFIGURACION DE MYSQL Y BASE DE DATOS panorama_net")
    print("="*70)

    # Verificar si MySQL está instalado
    if not check_mysql_installed():
        show_mysql_options()
        return False

    # Verificar si MySQL está ejecutándose
    if not check_mysql_running():
        if not start_mysql_service():
            show_mysql_options()
            return False

    # Probar conexión básica
    if not test_mysql_connection():
        print("\n[ERROR] No se puede conectar a MySQL con la configuración actual")
        show_mysql_options()
        return False

    print("\n" + "="*70)
    print("VERIFICANDO BASE DE DATOS panorama_net")
    print("="*70)

    # Verificar si la base de datos existe
    database_exists = check_database_exists()

    if not database_exists:
        print(f"\n[INFO] La base de datos '{Config.DB_NAME}' no existe")
        print("[INFO] Creando base de datos...")

        if not create_database():
            print("[ERROR] No se pudo crear la base de datos")
            return False

    print("\n" + "="*70)
    print("VERIFICANDO TABLAS EN panorama_net")
    print("="*70)

    # Verificar tablas
    missing_tables = check_tables_exist()

    if missing_tables:
        print(f"\n[INFO] Tablas faltantes: {', '.join(missing_tables)}")
        print("[INFO] Creando tablas...")

        if not create_tables():
            print("[ERROR] No se pudieron crear las tablas")
            return False

    print("\n" + "="*70)
    print("VERIFICACION FINAL")
    print("="*70)

    # Verificación final
    if verify_mysql_setup():
        print("\n" + "="*70)
        print("CONFIGURACION MYSQL COMPLETADA EXITOSAMENTE!")
        print("="*70)
        print("MySQL y base de datos panorama_net configurados correctamente.")
        print("Puede ejecutar la aplicación con: python main.py")
        print("="*70)
        return True
    else:
        print("\n[ERROR] Error en la verificación final")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
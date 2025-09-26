#!/usr/bin/env python3
"""
Script de inicialización de base de datos para Panorama_net
Este script crea la base de datos y tablas necesarias para el sistema
"""
import sys
import logging
import mysql.connector
from mysql.connector import Error
from config import Config

def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('database_init.log', encoding='utf-8')
        ]
    )

def create_database_connection(host, user, password, database=None):
    """Crea una conexión a MySQL"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        logging.error(f"Error conectando a MySQL: {e}")
        return None

def execute_sql_file(connection, sql_file_path):
    """Ejecuta un archivo SQL"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        cursor = connection.cursor()

        # Dividir el script en comandos individuales
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

        executed_commands = 0
        for command in commands:
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    executed_commands += 1
                    logging.debug(f"Comando ejecutado: {command[:50]}...")
                except Error as e:
                    logging.warning(f"Error ejecutando comando: {e}")
                    logging.warning(f"Comando: {command}")

        connection.commit()
        cursor.close()

        logging.info(f"Archivo SQL ejecutado exitosamente: {executed_commands} comandos")
        return True

    except FileNotFoundError:
        logging.error(f"Archivo SQL no encontrado: {sql_file_path}")
        return False
    except Exception as e:
        logging.error(f"Error ejecutando archivo SQL: {e}")
        return False

def test_database_connection(host, port, user, password, database):
    """Prueba la conexión a la base de datos"""
    try:
        connection = create_database_connection(host, user, password, database)
        if connection and connection.is_connected():
            logging.info("✓ Conexión a base de datos exitosa")

            # Obtener información del servidor
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            logging.info(f"✓ Versión de MySQL: {version}")

            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            logging.info(f"✓ Base de datos actual: {db_name}")

            cursor.close()
            connection.close()
            return True
        else:
            logging.error("✗ No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        logging.error(f"✗ Error probando conexión: {e}")
        return False

def main():
    """Función principal"""
    setup_logging()
    logging.info("Iniciando script de inicialización de base de datos Panorama_net")

    # Obtener parámetros de conexión
    host = input(f"Host MySQL (default: {Config.DB_HOST}): ") or Config.DB_HOST
    port = input(f"Puerto MySQL (default: {Config.DB_PORT}): ") or str(Config.DB_PORT)
    user = input(f"Usuario MySQL (default: {Config.DB_USER}): ") or Config.DB_USER
    password = input("Contraseña MySQL: ") or Config.DB_PASSWORD
    database = input(f"Nombre de base de datos (default: {Config.DB_NAME}): ") or Config.DB_NAME

    # Verificar que el archivo SQL existe
    sql_file = 'database_schema.sql'
    if not os.path.exists(sql_file):
        logging.error(f"Archivo {sql_file} no encontrado")
        sys.exit(1)

    logging.info("=== PRUEBA DE CONEXIÓN ===")
    if not test_database_connection(host, int(port), user, password, None):
        logging.error("No se puede continuar sin conexión a MySQL")
        sys.exit(1)

    logging.info("=== CREANDO BASE DE DATOS Y TABLAS ===")

    # Conectar sin especificar base de datos para poder crearla
    connection = create_database_connection(host, user, password, None)
    if not connection:
        logging.error("No se pudo conectar para crear la base de datos")
        sys.exit(1)

    try:
        cursor = connection.cursor()

        # Crear base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        logging.info(f"✓ Base de datos '{database}' creada o ya existe")

        # Usar la base de datos
        cursor.execute(f"USE {database}")
        logging.info(f"✓ Usando base de datos '{database}'")

        # Ejecutar script SQL
        if execute_sql_file(connection, sql_file):
            logging.info("✓ Esquema de base de datos creado exitosamente")
        else:
            logging.error("✗ Error creando esquema de base de datos")
            sys.exit(1)

        cursor.close()

    except Error as e:
        logging.error(f"Error en operaciones de base de datos: {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            connection.close()

    logging.info("=== VERIFICACIÓN FINAL ===")

    # Verificar que las tablas se crearon correctamente
    connection = create_database_connection(host, user, password, database)
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            expected_tables = ['clientes', 'facturas', 'pagos']
            created_tables = [table[0] for table in tables]

            logging.info(f"✓ Tablas encontradas: {created_tables}")

            for table in expected_tables:
                if table in created_tables:
                    logging.info(f"✓ Tabla '{table}' creada correctamente")
                else:
                    logging.warning(f"⚠ Tabla '{table}' no encontrada")

            # Verificar datos de ejemplo
            cursor.execute("SELECT COUNT(*) FROM clientes")
            clients_count = cursor.fetchone()[0]
            logging.info(f"✓ Clientes en la base de datos: {clients_count}")

            cursor.execute("SELECT COUNT(*) FROM facturas")
            invoices_count = cursor.fetchone()[0]
            logging.info(f"✓ Facturas en la base de datos: {invoices_count}")

            cursor.close()

        except Error as e:
            logging.error(f"Error verificando base de datos: {e}")
        finally:
            connection.close()

    logging.info("=== INICIALIZACIÓN COMPLETADA ===")
    logging.info("✓ Base de datos Panorama_net inicializada exitosamente")
    logging.info("✓ Puede ejecutar la aplicación con: python main.py")

if __name__ == "__main__":
    import os
    main()
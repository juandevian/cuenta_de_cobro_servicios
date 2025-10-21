#!/usr/bin/env python3
"""
Script para probar la conexión directa a MySQL
"""
import mysql.connector
from mysql.connector import Error
from src.config import Config

def test_connection():
    """Prueba diferentes formas de conectar a MySQL"""
    print("PROBANDO CONEXION A MYSQL")
    print("="*50)

    # Método 1: Conexión sin especificar base de datos
    try:
        print("1. Probando conexion basica...")
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )

        if connection.is_connected():
            print("[OK] Conexion exitosa a MySQL")

            # Obtener información del servidor
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"[OK] Version de MySQL: {version}")

            # Verificar bases de datos existentes
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"[OK] Bases de datos encontradas: {len(databases)}")

            db_names = [db[0] for db in databases]
            print("Bases de datos disponibles:")
            for db in db_names:
                if Config.DB_NAME.lower() in db.lower():
                    print(f"  - {db} (contiene '{Config.DB_NAME}')")
                else:
                    print(f"  - {db}")

            # Verificar si panorama_net existe
            if Config.DB_NAME in db_names:
                print(f"\n[OK] Base de datos '{Config.DB_NAME}' existe")

                # Cambiar a la base de datos
                cursor.execute(f"USE {Config.DB_NAME}")

                # Verificar tablas
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"[OK] Tablas en '{Config.DB_NAME}': {len(tables)}")

                if tables:
                    print("Tablas encontradas:")
                    for table in tables:
                        print(f"  - {table[0]}")
                else:
                    print("[INFO] No hay tablas en la base de datos")
                    print("[INFO] Se necesitan crear las tablas")

            else:
                print(f"\n[WARNING] Base de datos '{Config.DB_NAME}' NO existe")
                print("[INFO] Se necesita crear la base de datos")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"[ERROR] Error de conexion: {e}")
        return False

def show_connection_options():
    """Muestra opciones de conexión"""
    print("\n" + "="*70)
    print("OPCIONES DE CONEXION MYSQL:")
    print("="*70)
    print("1. Verificar credenciales:")
    print("   - Usuario: root")
    print("   - Contraseña: (vacía en config.py)")
    print("   - Host: localhost:3306")
    print("")
    print("2. Si la contraseña está configurada:")
    print("   - Edite config.py y configure DB_PASSWORD")
    print("   - O pruebe con diferentes contraseñas")
    print("")
    print("3. Si MySQL requiere autenticación:")
    print("   - Abra MySQL Command Line Client")
    print("   - Ejecute: ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   - Actualice config.py con la nueva contraseña")
    print("")
    print("4. Si usa XAMPP/WAMP:")
    print("   - Usuario por defecto: root")
    print("   - Contraseña por defecto: (vacía)")
    print("="*70)

def main():
    """Función principal"""
    print("PRUEBA DE CONEXION DIRECTA A MYSQL")
    print("="*70)

    if test_connection():
        print("\n" + "="*70)
        print("CONEXION MYSQL EXITOSA!")
        print("="*70)
        print("Puede proceder con:")
        print("python setup_mysql_panorama.py")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("PROBLEMAS DE CONEXION MYSQL")
        print("="*70)
        show_connection_options()

if __name__ == "__main__":
    main()
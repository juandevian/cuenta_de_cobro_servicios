#!/usr/bin/env python3
"""
Script para configurar la contraseña de MySQL
"""
import sys
import os
import subprocess
import mysql.connector
from mysql.connector import Error

def check_mysql_command_line():
    """Verifica si podemos acceder a MySQL Command Line"""
    print("VERIFICANDO ACCESO A MYSQL COMMAND LINE...")
    print("="*50)

    try:
        # Intentar ejecutar mysql sin contraseña
        result = subprocess.run(['mysql', '-u', 'root', '-e', 'SELECT VERSION();'],
                              capture_output=True, text=True, shell=True, timeout=10)

        if result.returncode == 0:
            print("[OK] MySQL Command Line accesible sin contraseña")
            return True, ""
        else:
            print("[INFO] MySQL requiere contraseña o autenticacion")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print("[ERROR] MySQL Command Line no responde")
        return False, "Timeout"
    except Exception as e:
        print(f"[ERROR] Error ejecutando MySQL Command Line: {e}")
        return False, str(e)

def try_common_passwords():
    """Prueba contraseñas comunes de MySQL"""
    print("\nPROBANDO CONTRASEÑAS COMUNES...")
    print("="*50)

    common_passwords = ['', 'root', 'password', '123456', 'admin', 'mysql', '1234']

    for password in common_passwords:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password=password
            )

            if connection.is_connected():
                print(f"[OK] Conexion exitosa con contraseña: '{password}'")
                connection.close()
                return password

        except Error:
            continue

    print("[INFO] Ninguna contraseña comun funciono")
    return None

def show_mysql_reset_instructions():
    """Muestra instrucciones para resetear contraseña de MySQL"""
    print("\n" + "="*70)
    print("INSTRUCCIONES PARA RESETEAR CONTRASEÑA MYSQL:")
    print("="*70)
    print("OPCION 1: Usando MySQL Command Line Client")
    print("1. Abra MySQL Command Line Client como administrador")
    print("2. Ejecute estos comandos:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   FLUSH PRIVILEGES;")
    print("3. Actualice config.py con la nueva contraseña")
    print("")
    print("OPCION 2: Usando Windows Services")
    print("1. Detenga el servicio MySQL:")
    print("   net stop MySQL")
    print("2. Inicie MySQL en modo seguro:")
    print("   mysqld --skip-grant-tables --skip-networking")
    print("3. Conectese sin contraseña:")
    print("   mysql -u root")
    print("4. Ejecute:")
    print("   UPDATE mysql.user SET authentication_string = PASSWORD('nueva_contraseña') WHERE User = 'root';")
    print("   UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root';")
    print("   FLUSH PRIVILEGES;")
    print("5. Reinicie MySQL normalmente:")
    print("   net stop MySQL")
    print("   net start MySQL")
    print("")
    print("OPCION 3: Si usa XAMPP")
    print("1. Abra XAMPP Control Panel")
    print("2. Haga clic en 'Shell'")
    print("3. Ejecute: mysql -u root -p")
    print("4. Presione Enter (contraseña vacia)")
    print("5. Ejecute los comandos ALTER USER arriba")
    print("="*70)

def create_config_with_password():
    """Crea un script para configurar la contraseña"""
    print("\nCREANDO SCRIPT DE CONFIGURACION...")
    print("="*50)

    script_content = '''
#!/usr/bin/env python3
"""
Script para probar diferentes contraseñas de MySQL
Edite este script con su contraseña y ejecútelo
"""
import mysql.connector
from mysql.connector import Error

def test_password(password):
    """Prueba una contraseña específica"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=password
        )

        if connection.is_connected():
            print(f"[OK] Contraseña correcta: '{password}'")

            # Verificar bases de datos
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()

            print(f"Bases de datos disponibles: {len(databases)}")
            for db in databases:
                print(f"  - {db[0]}")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"[ERROR] Contraseña '{password}': {e}")
        return False

# PRUEBE SU CONTRASEÑA AQUI:
# Reemplace 'SU_CONTRASEÑA' con la contraseña real de MySQL
test_password('SU_CONTRASEÑA')
'''

    with open('test_password.py', 'w', encoding='utf-8') as f:
        f.write(script_content)

    print("[OK] Script 'test_password.py' creado")
    print("[INFO] Edite el script con su contraseña de MySQL y ejecútelo")

def main():
    """Función principal"""
    print("CONFIGURACION DE CONTRASEÑA MYSQL")
    print("="*70)

    # Verificar acceso a MySQL Command Line
    can_access_cli, error_msg = check_mysql_command_line()

    if can_access_cli:
        print("[OK] MySQL Command Line accesible sin contraseña")
        print("[INFO] Puede configurar la contraseña usando los comandos SQL")

        # Probar conexión con contraseña vacía
        working_password = try_common_passwords()
        if working_password is not None:
            print(f"\n[OK] Contraseña de trabajo: '{working_password}'")
            print("[INFO] Actualice config.py con esta contraseña")
        else:
            print("\n[INFO] Necesita configurar una contraseña")

    else:
        print(f"[INFO] MySQL Command Line no accesible: {error_msg}")

        # Probar contraseñas comunes
        working_password = try_common_passwords()
        if working_password is not None:
            print(f"\n[OK] Contraseña encontrada: '{working_password}'")
            print("[INFO] Actualice config.py con esta contraseña")
        else:
            print("\n[INFO] No se pudo determinar la contraseña")

    # Mostrar instrucciones
    show_mysql_reset_instructions()

    # Crear script de prueba
    create_config_with_password()

    print("\n" + "="*70)
    print("PROXIMOS PASOS:")
    print("="*70)
    print("1. Determine la contraseña de MySQL")
    print("2. Edite config.py y configure DB_PASSWORD")
    print("3. Ejecute: python setup_mysql_panorama.py")
    print("")
    print("O use SQLite (ya funcionando):")
    print("python main_sqlite_simple.py")
    print("="*70)

if __name__ == "__main__":
    main()
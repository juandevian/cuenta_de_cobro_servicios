#!/usr/bin/env python3
"""
Script para resetear la contraseña de MySQL
"""
import sys
import os
import subprocess
import time
import mysql.connector
from mysql.connector import Error

def stop_mysql_service():
    """Detiene el servicio MySQL"""
    print("DETENIENDO SERVICIO MYSQL...")
    try:
        result = subprocess.run(['net', 'stop', 'MySQL'],
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("[OK] MySQL detenido exitosamente")
            return True
        else:
            print(f"[WARNING] No se pudo detener MySQL: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error deteniendo MySQL: {e}")
        return False

def start_mysql_safe():
    """Inicia MySQL en modo seguro"""
    print("INICIANDO MYSQL EN MODO SEGURO...")
    try:
        # Iniciar MySQL en modo seguro
        mysql_process = subprocess.Popen(
            ['mysqld', '--skip-grant-tables', '--skip-networking'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        print("[OK] MySQL iniciado en modo seguro")
        time.sleep(3)  # Esperar a que inicie
        return mysql_process

    except Exception as e:
        print(f"[ERROR] Error iniciando MySQL en modo seguro: {e}")
        return None

def reset_mysql_password():
    """Resetea la contraseña de MySQL"""
    try:
        print("CONECTANDO A MYSQL SIN CONTRASEÑA...")
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''  # Sin contraseña en modo seguro
        )

        if connection.is_connected():
            print("[OK] Conexion exitosa sin contraseña")

            cursor = connection.cursor()

            # Resetear contraseña del usuario root
            print("RESETEANDO CONTRASEÑA...")
            cursor.execute("UPDATE mysql.user SET authentication_string = PASSWORD('') WHERE User = 'root' AND Host = 'localhost';")
            cursor.execute("UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root' AND Host = 'localhost';")
            cursor.execute("FLUSH PRIVILEGES;")

            print("[OK] Contraseña reseteada exitosamente")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"[ERROR] Error reseteando contraseña: {e}")
        return False

def start_mysql_normal():
    """Inicia MySQL normalmente"""
    print("INICIANDO MYSQL NORMALMENTE...")
    try:
        result = subprocess.run(['net', 'start', 'MySQL'],
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("[OK] MySQL iniciado normalmente")
            return True
        else:
            print(f"[ERROR] No se pudo iniciar MySQL: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error iniciando MySQL: {e}")
        return False

def test_new_connection():
    """Prueba la conexión con la nueva contraseña"""
    print("PROBANDO CONEXION CON CONTRASEÑA VACIA...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''  # Contraseña vacía
        )

        if connection.is_connected():
            print("[OK] Conexion exitosa con contraseña vacia")

            # Verificar bases de datos
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()

            print(f"[OK] Bases de datos encontradas: {len(databases)}")
            for db in databases:
                print(f"  - {db[0]}")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"[ERROR] Error de conexion: {e}")
        return False

def show_manual_instructions():
    """Muestra instrucciones manuales"""
    print("\n" + "="*70)
    print("INSTRUCCIONES MANUALES (si el script no funciona):")
    print("="*70)
    print("1. Abra CMD como ADMINISTRADOR")
    print("2. Detenga MySQL:")
    print("   net stop MySQL")
    print("3. Inicie MySQL en modo seguro:")
    print("   mysqld --skip-grant-tables --skip-networking")
    print("4. Abra otra CMD y ejecute:")
    print("   mysql -u root")
    print("5. En MySQL ejecute:")
    print("   UPDATE mysql.user SET authentication_string = PASSWORD('') WHERE User = 'root';")
    print("   UPDATE mysql.user SET plugin = 'mysql_native_password' WHERE User = 'root';")
    print("   FLUSH PRIVILEGES;")
    print("   EXIT;")
    print("6. En la primera CMD presione Ctrl+C")
    print("7. Inicie MySQL normalmente:")
    print("   net start MySQL")
    print("="*70)

def main():
    """Función principal"""
    print("RESETEO DE CONTRASEÑA MYSQL")
    print("="*70)

    # Detener MySQL
    if not stop_mysql_service():
        print("[WARNING] No se pudo detener MySQL, continuando...")

    # Iniciar en modo seguro
    mysql_process = start_mysql_safe()
    if not mysql_process:
        print("[ERROR] No se pudo iniciar MySQL en modo seguro")
        show_manual_instructions()
        return False

    try:
        # Resetear contraseña
        if reset_mysql_password():
            print("[OK] Contraseña reseteada exitosamente")
        else:
            print("[ERROR] No se pudo resetear la contraseña")
            show_manual_instructions()
            return False

        # Detener el proceso en modo seguro
        mysql_process.terminate()
        time.sleep(2)

        # Iniciar MySQL normalmente
        if start_mysql_normal():
            print("[OK] MySQL iniciado normalmente")
        else:
            print("[ERROR] No se pudo iniciar MySQL normalmente")
            return False

        # Esperar a que inicie
        print("ESPERANDO A QUE MYSQL INICIE...")
        time.sleep(5)

        # Probar conexión
        if test_new_connection():
            print("\n" + "="*70)
            print("RESETEO COMPLETADO EXITOSAMENTE!")
            print("="*70)
            print("MySQL ahora acepta conexión con:")
            print("  Usuario: root")
            print("  Contraseña: (vacía)")
            print("")
            print("Puede ejecutar:")
            print("python setup_mysql_panorama.py")
            print("="*70)
            return True
        else:
            print("[ERROR] No se pudo verificar la conexión")
            return False

    except Exception as e:
        print(f"[ERROR] Error durante el proceso: {e}")
        show_manual_instructions()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
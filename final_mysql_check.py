#!/usr/bin/env python3
"""
Verificación final de MySQL y opciones disponibles
"""
import sys
import os
import subprocess
import mysql.connector
from mysql.connector import Error

def try_mysql_connection_methods():
    """Prueba diferentes métodos de conexión a MySQL"""
    print("PROBANDO METODOS DE CONEXION MYSQL...")
    print("="*50)

    methods_tried = []
    successful_connection = None

    # Método 1: Conexión directa con contraseña vacía
    try:
        print("1. Probando conexión con contraseña vacía...")
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''
        )
        if conn.is_connected():
            print("[OK] Conexión exitosa con contraseña vacía")
            successful_connection = ('', 'contraseña vacía')
            conn.close()
    except Error as e:
        print(f"[ERROR] {e}")
        methods_tried.append("Contraseña vacía")

    # Método 2: Conexión con usuario diferente
    try:
        print("2. Probando con usuario 'debian-sys-maint'...")
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='debian-sys-maint',
            password=''
        )
        if conn.is_connected():
            print("[OK] Conexión exitosa con debian-sys-maint")
            successful_connection = ('debian-sys-maint', 'usuario del sistema')
            conn.close()
    except Error as e:
        print(f"[ERROR] {e}")
        methods_tried.append("Usuario debian-sys-maint")

    # Método 3: Conexión con socket
    try:
        print("3. Probando conexión con socket...")
        conn = mysql.connector.connect(
            unix_socket='/tmp/mysql.sock',
            user='root',
            password=''
        )
        if conn.is_connected():
            print("[OK] Conexión exitosa con socket")
            successful_connection = ('socket', '/tmp/mysql.sock')
            conn.close()
    except Error as e:
        print(f"[ERROR] {e}")
        methods_tried.append("Socket /tmp/mysql.sock")

    return successful_connection, methods_tried

def check_mysql_workbench():
    """Verifica si MySQL Workbench está instalado"""
    print("\nVERIFICANDO MYSQL WORKBENCH...")
    print("="*50)

    workbench_paths = [
        r"C:\Program Files\MySQL\MySQL Workbench*",
        r"C:\Program Files (x86)\MySQL\MySQL Workbench*",
        r"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\MySQL\MySQL Workbench*"
    ]

    for path in workbench_paths:
        try:
            result = subprocess.run(['dir', path],
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"[OK] MySQL Workbench encontrado en: {path}")
                return True
        except:
            pass

    print("[INFO] MySQL Workbench no encontrado")
    return False

def show_final_options():
    """Muestra las opciones finales"""
    print("\n" + "="*70)
    print("OPCIONES FINALES PARA CONTINUAR:")
    print("="*70)

    print("OPCION 1: Usar SQLite (INMEDIATO)")
    print("   python main_sqlite_simple.py")
    print("   - Ya configurado y funcionando")
    print("   - Base de datos lista")
    print("   - 2 facturas de ejemplo incluidas")
    print("   - Interfaz gráfica operativa")
    print("")

    print("OPCION 2: Configurar MySQL (REQUIERE TIEMPO)")
    print("   a) Instalar MySQL Workbench:")
    print("      - Descargue de: https://dev.mysql.com/downloads/workbench/")
    print("      - Herramienta gráfica para gestionar MySQL")
    print("      - Puede resetear contraseña visualmente")
    print("")
    print("   b) Usar comandos manuales:")
    print("      - Abra CMD como ADMINISTRADOR")
    print("      - Ejecute: mysql -u root -p")
    print("      - Si pide contraseña, presione Enter")
    print("      - Ejecute: ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva';")
    print("      - Actualice config.py con la contraseña")
    print("")
    print("   c) Usar XAMPP (más fácil):")
    print("      - Descargue de: https://www.apachefriends.org/")
    print("      - Instale y ejecute")
    print("      - Use las instrucciones del script anterior")
    print("")

    print("OPCION 3: Docker (avanzado)")
    print("   docker run --name mysql -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 -d mysql:8.0")
    print("   - Luego configure config.py con contraseña 'pass'")
    print("="*70)

def main():
    """Función principal"""
    print("VERIFICACION FINAL DE MYSQL")
    print("="*70)

    # Probar métodos de conexión
    successful_connection, methods_tried = try_mysql_connection_methods()

    # Verificar MySQL Workbench
    workbench_installed = check_mysql_workbench()

    print("\n" + "="*70)
    print("RESUMEN DE LA SITUACION:")
    print("="*70)

    if successful_connection:
        print(f"[OK] Conexión exitosa encontrada: {successful_connection[1]}")
        print("[INFO] Puede configurar MySQL con esta conexión")
    else:
        print("[INFO] Ningún método de conexión funcionó")
        print(f"[INFO] Métodos probados: {len(methods_tried)}")

    if workbench_installed:
        print("[OK] MySQL Workbench instalado - puede usarlo para configurar")

    print("\n" + "="*70)
    print("RECOMENDACION FINAL:")
    print("="*70)
    print("Para comenzar INMEDIATAMENTE, use SQLite:")
    print("python main_sqlite_simple.py")
    print("")
    print("SQLite está completamente configurado y funcionando.")
    print("Incluye base de datos, tablas y datos de ejemplo.")
    print("La interfaz gráfica está lista para usar.")
    print("="*70)

    # Mostrar opciones finales
    show_final_options()

if __name__ == "__main__":
    main()
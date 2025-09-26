#!/usr/bin/env python3
"""
Script para verificar alternativas de MySQL y opciones de instalación
"""
import sys
import os
import subprocess

def check_common_mysql_installations():
    """Verifica instalaciones comunes de MySQL"""
    print("VERIFICANDO INSTALACIONES COMUNES DE MYSQL...")
    print("="*50)

    # Posibles ubicaciones de MySQL
    possible_paths = [
        r"C:\Program Files\MySQL\MySQL Server*\bin\mysql.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"C:\xampp\mysql\bin\mysql.exe",
        r"C:\wamp\bin\mysql\*\bin\mysql.exe",
        r"C:\Program Files (x86)\MySQL\MySQL Server*\bin\mysql.exe",
    ]

    found_installations = []

    for path in possible_paths:
        try:
            result = subprocess.run(['where', path],
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                found_installations.append(path)
                print(f"[ENCONTRADO] {path}")
        except:
            pass

    if not found_installations:
        print("[NO ENCONTRADO] No se encontraron instalaciones de MySQL")

    return found_installations

def check_mysql_services():
    """Verifica servicios MySQL ejecutándose"""
    print("\nVERIFICANDO SERVICIOS MYSQL...")
    print("="*50)

    try:
        # Verificar servicios MySQL
        result = subprocess.run(['sc', 'query', 'MySQL*'],
                              capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("[INFO] No se encontraron servicios MySQL")

    except Exception as e:
        print(f"[ERROR] Error verificando servicios: {e}")

def check_mysql_ports():
    """Verifica puertos MySQL comunes"""
    print("\nVERIFICANDO PUERTOS MYSQL...")
    print("="*50)

    common_ports = [3306, 3307, 3308, 3309]

    for port in common_ports:
        try:
            result = subprocess.run(['netstat', '-an'],
                                  capture_output=True, text=True, shell=True)

            if f":{port}" in result.stdout and "LISTENING" in result.stdout:
                print(f"[OK] Puerto {port} está escuchando (posible MySQL)")
            else:
                print(f"[INFO] Puerto {port} no está activo")
        except:
            print(f"[ERROR] No se pudo verificar puerto {port}")

def show_installation_options():
    """Muestra opciones de instalación"""
    print("\n" + "="*70)
    print("OPCIONES DE INSTALACIÓN DE MYSQL:")
    print("="*70)
    print("1. MySQL Community Server (Recomendado):")
    print("   - Descargar desde: https://dev.mysql.com/downloads/mysql/")
    print("   - Instalador completo con herramientas")
    print("   - Configuración guiada")
    print("")
    print("2. XAMPP (Más fácil para desarrollo):")
    print("   - Descargar desde: https://www.apachefriends.org/")
    print("   - Incluye MySQL, PHP, Apache")
    print("   - Panel de control fácil de usar")
    print("")
    print("3. WAMP Server:")
    print("   - Descargar desde: https://www.wampserver.com/")
    print("   - Similar a XAMPP para Windows")
    print("")
    print("4. Docker (Avanzado):")
    print("   - docker run --name mysql -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 -d mysql:8.0")
    print("="*70)

def show_alternatives():
    """Muestra alternativas a MySQL"""
    print("\n" + "="*70)
    print("ALTERNATIVAS A MYSQL:")
    print("="*70)
    print("1. SQLite (Ya configurado y funcionando):")
    print("   - python main_sqlite_simple.py")
    print("   - No requiere instalación")
    print("   - Perfecto para desarrollo")
    print("")
    print("2. PostgreSQL:")
    print("   - Más avanzado que MySQL")
    print("   - Mejor para aplicaciones grandes")
    print("")
    print("3. MariaDB:")
    print("   - Compatible con MySQL")
    print("   - Desarrollado por la comunidad")
    print("")
    print("4. SQL Server Express:")
    print("   - Gratuito de Microsoft")
    print("   - Integración con Windows")
    print("="*70)

def check_system_info():
    """Verifica información del sistema"""
    print("INFORMACION DEL SISTEMA:")
    print("="*50)
    print(f"Python: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")

    # Verificar si hay archivos de configuración MySQL
    config_files = [
        r"C:\ProgramData\MySQL\my.ini",
        r"C:\xampp\mysql\my.ini",
        r"C:\wamp\bin\mysql\*\my.ini"
    ]

    print("\nVERIFICANDO ARCHIVOS DE CONFIGURACION MYSQL...")
    for config in config_files:
        try:
            result = subprocess.run(['dir', config],
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"[ENCONTRADO] {config}")
        except:
            pass

def main():
    """Función principal"""
    print("VERIFICACION DE MYSQL Y ALTERNATIVAS")
    print("="*70)

    # Verificar información del sistema
    check_system_info()

    # Verificar instalaciones comunes
    found_mysql = check_common_mysql_installations()

    # Verificar servicios
    check_mysql_services()

    # Verificar puertos
    check_mysql_ports()

    print("\n" + "="*70)
    print("RESUMEN:")
    print("="*70)

    if found_mysql:
        print("✓ Se encontraron instalaciones de MySQL")
        print("  Intente ejecutar: python setup_mysql_panorama.py")
    else:
        print("✗ No se encontraron instalaciones de MySQL")
        show_installation_options()
        show_alternatives()

    print("\n" + "="*70)
    print("RECOMENDACIONES:")
    print("="*70)
    print("1. Para desarrollo rápido: Use SQLite (ya funcionando)")
    print("   python main_sqlite_simple.py")
    print("")
    print("2. Para producción: Instale MySQL Community Server")
    print("   - Siga las instrucciones de instalación")
    print("   - Ejecute: python setup_mysql_panorama.py")
    print("")
    print("3. Para desarrollo web: Use XAMPP")
    print("   - Incluye MySQL, PHP, Apache")
    print("   - Panel de control fácil")
    print("="*70)

if __name__ == "__main__":
    main()
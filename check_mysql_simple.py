#!/usr/bin/env python3
"""
Script simplificado para verificar MySQL sin caracteres Unicode
"""
import sys
import os
import subprocess

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
                print(f"[OK] Puerto {port} esta escuchando (posible MySQL)")
            else:
                print(f"[INFO] Puerto {port} no esta activo")
        except:
            print(f"[ERROR] No se pudo verificar puerto {port}")

def show_mysql_status():
    """Muestra el estado actual de MySQL"""
    print("ESTADO ACTUAL DE MYSQL:")
    print("="*50)

    # Verificar si hay procesos MySQL ejecutandose
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq mysql*'],
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0 and 'mysql' in result.stdout.lower():
            print("[OK] Procesos MySQL encontrados:")
            print(result.stdout)
        else:
            print("[INFO] No se encontraron procesos MySQL ejecutandose")
    except:
        print("[ERROR] No se pudo verificar procesos MySQL")

def show_options():
    """Muestra opciones disponibles"""
    print("\n" + "="*70)
    print("OPCIONES DISPONIBLES:")
    print("="*70)
    print("1. SQLite (YA FUNCIONANDO):")
    print("   - python main_sqlite_simple.py")
    print("   - Base de datos: panorama_net.db")
    print("   - Listo para usar inmediatamente")
    print("")
    print("2. Instalar MySQL Community Server:")
    print("   - Visite: https://dev.mysql.com/downloads/mysql/")
    print("   - Descargue el instalador MSI")
    print("   - Ejecute el instalador")
    print("   - Configure usuario y contrasena")
    print("")
    print("3. Instalar XAMPP (Recomendado para desarrollo):")
    print("   - Visite: https://www.apachefriends.org/")
    print("   - Descargue XAMPP para Windows")
    print("   - Ejecute el instalador")
    print("   - Inicie MySQL desde el panel de control")
    print("")
    print("4. Docker (Avanzado):")
    print("   - docker run --name mysql -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 -d mysql:8.0")
    print("="*70)

def main():
    """Función principal"""
    print("VERIFICACION DE MYSQL - VERSION SIMPLIFICADA")
    print("="*70)

    # Verificar puertos
    check_mysql_ports()

    # Verificar procesos
    show_mysql_status()

    # Mostrar opciones
    show_options()

    print("\n" + "="*70)
    print("RECOMENDACION:")
    print("="*70)
    print("Para comenzar inmediatamente, use SQLite:")
    print("python main_sqlite_simple.py")
    print("")
    print("SQLite ya esta configurado y funcionando perfectamente.")
    print("Incluye base de datos con datos de ejemplo.")
    print("="*70)

if __name__ == "__main__":
    main()
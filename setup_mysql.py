#!/usr/bin/env python3
"""
Script para configurar MySQL para el sistema de facturación
"""
import sys
import os
import subprocess

def check_mysql_installed():
    """Verifica si MySQL está instalado"""
    try:
        # Intentar ejecutar mysql --version
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
        # En Windows, verificar si el servicio MySQL está ejecutándose
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
        from database import DatabaseConnection
        print("\nProbando conexión a MySQL...")

        db = DatabaseConnection()
        if db.connection and db.connection.is_connected():
            print("[OK] Conexión exitosa a MySQL")
            db.disconnect()
            return True
        else:
            print("[ERROR] No se pudo conectar a MySQL")
            return False
    except Exception as e:
        print(f"[ERROR] Error de conexión: {e}")
        return False

def setup_database():
    """Configura la base de datos"""
    try:
        print("\nConfigurando base de datos...")
        result = subprocess.run([sys.executable, 'init_database.py'],
                              capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            print("[OK] Base de datos configurada exitosamente")
            print(result.stdout)
            return True
        else:
            print("[ERROR] Error configurando base de datos")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando init_database.py: {e}")
        return False

def show_mysql_options():
    """Muestra opciones para configurar MySQL"""
    print("\n" + "="*60)
    print("OPCIONES PARA CONFIGURAR MYSQL:")
    print("="*60)
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
    print("4. Para desarrollo/pruebas, puede usar SQLite:")
    print("   - Instale: pip install pysqlite3")
    print("   - Modifique database.py para usar SQLite")
    print("="*60)

def main():
    """Función principal"""
    print("CONFIGURACION DE MYSQL PARA EL SISTEMA DE FACTURACION")
    print("="*60)

    # Verificar si MySQL está instalado
    if not check_mysql_installed():
        show_mysql_options()
        return False

    # Verificar si MySQL está ejecutándose
    if not check_mysql_running():
        if not start_mysql_service():
            show_mysql_options()
            return False

    # Probar conexión
    if not test_mysql_connection():
        print("\nProblemas de conexión detectados.")
        show_mysql_options()
        return False

    # Configurar base de datos
    if not setup_database():
        return False

    print("\n" + "="*60)
    print("CONFIGURACION COMPLETADA EXITOSAMENTE!")
    print("="*60)
    print("MySQL está configurado y funcionando correctamente.")
    print("Puede ejecutar la aplicación con: python main.py")
    print("="*60)

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
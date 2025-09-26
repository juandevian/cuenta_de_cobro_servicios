#!/usr/bin/env python3
"""
Script con instrucciones manuales para configurar MySQL
"""
import sys
import os
import subprocess

def check_xampp():
    """Verifica si XAMPP está instalado"""
    print("VERIFICANDO XAMPP...")
    xampp_paths = [
        r"C:\xampp",
        r"C:\Program Files\xampp",
        r"C:\Program Files (x86)\xampp"
    ]

    for path in xampp_paths:
        if os.path.exists(path):
            print(f"[OK] XAMPP encontrado en: {path}")
            return path

    print("[INFO] XAMPP no encontrado")
    return None

def check_wamp():
    """Verifica si WAMP está instalado"""
    print("VERIFICANDO WAMP...")
    wamp_paths = [
        r"C:\wamp",
        r"C:\wamp64",
        r"C:\Program Files\wamp",
        r"C:\Program Files (x86)\wamp"
    ]

    for path in wamp_paths:
        if os.path.exists(path):
            print(f"[OK] WAMP encontrado en: {path}")
            return path

    print("[INFO] WAMP no encontrado")
    return None

def show_xampp_instructions():
    """Muestra instrucciones para XAMPP"""
    print("\n" + "="*70)
    print("INSTRUCCIONES PARA XAMPP:")
    print("="*70)
    print("1. Abra XAMPP Control Panel")
    print("2. Inicie MySQL (haga clic en 'Start' junto a MySQL)")
    print("3. Haga clic en 'Shell' en XAMPP Control Panel")
    print("4. En la terminal que se abre, ejecute:")
    print("   mysql -u root -p")
    print("5. Presione Enter (contraseña vacía por defecto)")
    print("6. Ejecute estos comandos:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   FLUSH PRIVILEGES;")
    print("   EXIT;")
    print("7. Edite config.py y configure:")
    print("   DB_PASSWORD = 'nueva_contraseña'")
    print("8. Ejecute: python setup_mysql_panorama.py")
    print("="*70)

def show_wamp_instructions():
    """Muestra instrucciones para WAMP"""
    print("\n" + "="*70)
    print("INSTRUCCIONES PARA WAMP:")
    print("="*70)
    print("1. Abra WAMP Control Panel")
    print("2. Inicie MySQL (haga clic en 'Start' junto a MySQL)")
    print("3. Haga clic izquierdo en el icono de WAMP en la barra de tareas")
    print("4. Seleccione 'MySQL' > 'MySQL Console'")
    print("5. En la consola, ejecute:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   FLUSH PRIVILEGES;")
    print("   EXIT;")
    print("6. Edite config.py y configure:")
    print("   DB_PASSWORD = 'nueva_contraseña'")
    print("7. Ejecute: python setup_mysql_panorama.py")
    print("="*70)

def show_mysql_installer_instructions():
    """Muestra instrucciones para MySQL Installer"""
    print("\n" + "="*70)
    print("INSTRUCCIONES PARA MYSQL INSTALLER:")
    print("="*70)
    print("1. Abra MySQL Command Line Client desde el menu Inicio")
    print("2. Ejecute como ADMINISTRADOR")
    print("3. Ejecute estos comandos:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';")
    print("   FLUSH PRIVILEGES;")
    print("   EXIT;")
    print("4. Edite config.py y configure:")
    print("   DB_PASSWORD = 'nueva_contraseña'")
    print("5. Ejecute: python setup_mysql_panorama.py")
    print("="*70)

def show_alternatives():
    """Muestra alternativas"""
    print("\n" + "="*70)
    print("ALTERNATIVAS RECOMENDADAS:")
    print("="*70)
    print("OPCION 1: Usar SQLite (YA FUNCIONANDO)")
    print("   python main_sqlite_simple.py")
    print("   - No requiere configuración")
    print("   - Base de datos lista")
    print("   - Interfaz funcionando")
    print("")
    print("OPCION 2: Instalar XAMPP (Más fácil)")
    print("   - Descargue de: https://www.apachefriends.org/")
    print("   - Incluye MySQL, PHP, Apache")
    print("   - Panel de control gráfico")
    print("   - Siga las instrucciones arriba")
    print("")
    print("OPCION 3: Instalar MySQL Workbench")
    print("   - Descargue de: https://dev.mysql.com/downloads/workbench/")
    print("   - Herramienta gráfica para MySQL")
    print("   - Puede resetear contraseña visualmente")
    print("="*70)

def main():
    """Función principal"""
    print("CONFIGURACION MANUAL DE MYSQL")
    print("="*70)

    # Verificar XAMPP
    xampp_path = check_xampp()

    # Verificar WAMP
    wamp_path = check_wamp()

    print("\n" + "="*70)
    print("DETECTANDO TIPO DE INSTALACION MYSQL:")
    print("="*70)

    if xampp_path:
        print(f"[OK] XAMPP detectado en: {xampp_path}")
        show_xampp_instructions()
    elif wamp_path:
        print(f"[OK] WAMP detectado en: {wamp_path}")
        show_wamp_instructions()
    else:
        print("[INFO] No se detectó XAMPP ni WAMP")
        print("[INFO] Probablemente MySQL Installer o Docker")
        show_mysql_installer_instructions()

    # Mostrar alternativas
    show_alternatives()

    print("\n" + "="*70)
    print("RESUMEN:")
    print("="*70)
    print("1. Siga las instrucciones específicas para su instalación")
    print("2. Configure la contraseña en config.py")
    print("3. Ejecute: python setup_mysql_panorama.py")
    print("")
    print("O use SQLite inmediatamente:")
    print("python main_sqlite_simple.py")
    print("="*70)

if __name__ == "__main__":
    main()
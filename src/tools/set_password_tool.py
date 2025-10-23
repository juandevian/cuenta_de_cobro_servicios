#!/usr/bin/env python3
"""
Herramienta standalone para registrar la contraseña de la base de datos
en el Almacén de Credenciales de Windows (Credential Manager).

Esta herramienta se compila como ejecutable independiente (.exe) y
se distribuye con el instalador para facilitar la configuración sin
requerir Python en la máquina de destino.

Uso:
    set_password.exe

El programa pedirá:
- Usuario de la base de datos (DB_USERNAME del config.json)
- Contraseña (se oculta al escribir)

Guarda la contraseña de forma segura en el keyring de Windows.
"""
import sys
import os
import getpass

# Banner de bienvenida
BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║        Orión CC Servicios - Configuración de Contraseña       ║
║                   Almacén de Credenciales                     ║
╚═══════════════════════════════════════════════════════════════╝
"""

SERVICE_NAME = 'ori-cc-servicios'


def print_error(message):
    """Imprime un mensaje de error en rojo."""
    print(f"\n❌ ERROR: {message}\n")


def print_success(message):
    """Imprime un mensaje de éxito en verde."""
    print(f"\n✓ {message}\n")


def print_info(message):
    """Imprime un mensaje informativo."""
    print(f"ℹ {message}")


def main():
    """Función principal."""
    print(BANNER)
    print("Esta herramienta guardará la contraseña de la base de datos")
    print("en el Almacén de Credenciales de Windows de forma segura.")
    print(f"\nServicio: {SERVICE_NAME}")
    print("-" * 63)
    
    # Verificar que keyring está disponible
    try:
        import keyring
    except ImportError:
        print_error(
            "No se pudo cargar el módulo de credenciales.\n"
            "Esta herramienta requiere la librería 'keyring'.\n"
            "Contacte con soporte técnico."
        )
        input("\nPresione ENTER para salir...")
        return 1
    
    # Solicitar usuario
    print("\n1. Usuario de la base de datos")
    print("   (Debe coincidir con 'username' en config.json)")
    username = input("\n   Usuario: ").strip()
    
    if not username:
        print_error("El usuario no puede estar vacío.")
        input("Presione ENTER para salir...")
        return 2
    
    # Solicitar contraseña
    print("\n2. Contraseña de la base de datos")
    print("   (La contraseña no se mostrará mientras la escribe)")
    
    try:
        password = getpass.getpass("\n   Contraseña: ")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        return 3
    
    if not password:
        print_error("La contraseña no puede estar vacía.")
        input("Presione ENTER para salir...")
        return 4
    
    # Confirmar contraseña
    try:
        password_confirm = getpass.getpass("   Confirmar contraseña: ")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        return 3
    
    if password != password_confirm:
        print_error("Las contraseñas no coinciden.")
        input("Presione ENTER para salir...")
        return 5
    
    # Guardar en keyring
    print("\n3. Guardando credenciales...")
    
    try:
        keyring.set_password(SERVICE_NAME, username, password)
        print_success(
            "Contraseña guardada correctamente en el Almacén de Credenciales.\n"
            f"   • Servicio: {SERVICE_NAME}\n"
            f"   • Usuario: {username}"
        )
        print_info(
            "La aplicación Orión CC Servicios podrá ahora conectarse\n"
            "  a la base de datos de forma segura."
        )
        print("\n" + "=" * 63)
        print("CONFIGURACIÓN COMPLETADA")
        print("=" * 63)
        
    except Exception as e:
        print_error(f"No se pudo guardar la contraseña: {e}")
        input("\nPresione ENTER para salir...")
        return 6
    
    input("\nPresione ENTER para salir...")
    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        input("\nPresione ENTER para salir...")
        sys.exit(99)

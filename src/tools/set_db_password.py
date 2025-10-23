#!/usr/bin/env python3
"""
Script para registrar la contraseña de la base de datos en el Credential Manager (keyring).
Uso (interactivo):
  python -m src.tools.set_db_password

Variables controlables por entorno:
  KEYRING_SERVICE (por defecto: 'ori-cc-servicios')
  DB_USERNAME (si no se proporciona por prompt)

Nota: Este script requiere tener instalado 'keyring'.
"""
import getpass
import os
import sys

try:
    import keyring
except Exception as e:
    print("Error: 'keyring' no está instalado.")
    print("Instala dependencias con: pip install -r requirements.txt")
    sys.exit(1)

SERVICE = os.getenv('KEYRING_SERVICE', 'ori-cc-servicios')


def main():
    print("Configurar contraseña de la BD en keyring (Windows Credential Manager)")
    print(f"Servicio: {SERVICE}")
    username = os.getenv('DB_USERNAME') or input("Usuario DB (DB_USERNAME): ").strip()
    if not username:
        print("Usuario no proporcionado. Abortando.")
        sys.exit(2)
    password = getpass.getpass("Contraseña DB: ")
    if not password:
        print("Contraseña vacía. Abortando.")
        sys.exit(3)
    try:
        keyring.set_password(SERVICE, username, password)
        print("Contraseña guardada correctamente en el keyring.")
    except Exception as e:
        print(f"Error guardando contraseña en keyring: {e}")
        sys.exit(4)


if __name__ == '__main__':
    main()

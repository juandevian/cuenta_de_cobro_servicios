
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

# También probar contraseñas comunes
print("\nPROBANDO CONTRASEÑAS COMUNES...")
common_passwords = ['', 'root', 'password', '123456', 'admin', 'mysql', '1234', 'xampp', 'wamp']

for pwd in common_passwords:
    if test_password(pwd):
        print(f"\n[EXITO] Contraseña encontrada: '{pwd}'")
        break
else:
    print("\n[INFO] Ninguna contraseña común funcionó")
    print("[INFO] Necesita resetear la contraseña de MySQL")

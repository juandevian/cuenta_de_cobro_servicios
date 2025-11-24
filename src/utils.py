#!/usr/bin/env python3
"""
Utilidades varias para la aplicación
"""
import os
import sys  

def resource_path(relative_path: str) -> str:
    """Devuelve la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller."""
    if getattr(sys, '_MEIPASS', False):
        # PyInstaller crea una carpeta temporal y guarda el path en _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


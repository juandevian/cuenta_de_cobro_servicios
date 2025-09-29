#!/usr/bin/env python3
"""
Script para crear un archivo Excel de plantilla para importación de cobros
"""
import pandas as pd
from datetime import datetime, timedelta
import os

def create_sample_excel():
    """Crea un archivo Excel de ejemplo con datos de facturas"""

    # Crear datos de ejemplo
    data = {
        'id_carpeta': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'id_servicio': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        'id_predio': ['', 'APT 102', 'APT 103', 'APT 201', 'APT 202', 'PAR 001', 'PAR 002', '', 'PAR 004', 'PAR 005'],
        'id_tercero_cliente': [10999000, 0, 0, 0, 0, 0, 0, 1053700700, 0, 0],
        'periodo_inicio_cobro': ['202609', '202609', '202609', '202609', '202609', '202609', '202609', '202609', '202609', '202609'],
        'lectura_anterior': [1000, 2500, 800, 1150, 3200, 500, 1500, 2000, 4000, 6000],
        'lectura_actual': [1150, 2750, 950, 1320, 3450, 650, 1650, 2200, 4300, 6300],
        'valor_unitario': [850, 920, 780, 850, 950, 800, 900, 870, 960, 990]
    }

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear archivo Excel
    filename = 'ejemplo_facturas.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')

    print(f"✓ Archivo Excel de ejemplo creado: {filename}")
    print(f"✓ Filas: {len(df)}")
    print(f"✓ Columnas: {list(df.columns)}")
    print("\nDatos de ejemplo incluidos:")
    print(df.to_string(index=False))

    return filename

def create_excel_import_template():
    """Crea una plantilla en Excel para la importación de cobros de servicios con consumo"""
    filename = 'plantilla_importacion_facturas_servicios.xlsx'
    
    columns = [
        'id_carpeta',
        'id_servicio',
        'id_predio',
        'id_tercero_cliente',
        'periodo_inicio_cobro',
        'lectura_anterior',
        'lectura_actual',
        'valor_unitario'
    ]

    df = pd.DataFrame(columns)
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"✓ Archivo de plantilla Excel creado: {filename}")
    print(f"✓ Columnas: {list(df.columns)}")
    return filename

if __name__ == "__main__":
    create_sample_excel()
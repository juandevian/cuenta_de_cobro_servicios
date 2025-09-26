#!/usr/bin/env python3
"""
Script para crear un archivo Excel de ejemplo para pruebas
"""
import pandas as pd
from datetime import datetime, timedelta
import os

def create_sample_excel():
    """Crea un archivo Excel de ejemplo con datos de facturas"""

    # Crear datos de ejemplo
    data = {
        'numero_factura': ['FAC001', 'FAC002', 'FAC003', 'FAC004', 'FAC005'],
        'codigo_cliente': ['CLI001', 'CLI002', 'CLI003', 'CLI001', 'CLI004'],
        'fecha_emision': [
            '2024-01-15',
            '2024-01-20',
            '2024-01-25',
            '2024-02-01',
            '2024-02-05'
        ],
        'fecha_vencimiento': [
            '2024-02-15',
            '2024-02-20',
            '2024-02-25',
            '2024-03-01',
            '2024-03-05'
        ],
        'lectura_anterior': [1000.50, 2500.00, 800.00, 1150.75, 3200.00],
        'lectura_actual': [1150.75, 2750.25, 950.50, 1320.25, 3450.75],
        'consumo': [150.25, 250.25, 150.50, 169.50, 250.75],
        'valor_unitario': [850.00, 920.00, 780.00, 850.00, 950.00]
    }

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Calcular columnas adicionales
    df['subtotal'] = df['consumo'] * df['valor_unitario']
    df['iva'] = df['subtotal'] * 0.19
    df['total'] = df['subtotal'] + df['iva']

    # Crear archivo Excel
    filename = 'ejemplo_facturas.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')

    print(f"✓ Archivo Excel de ejemplo creado: {filename}")
    print(f"✓ Filas: {len(df)}")
    print(f"✓ Columnas: {list(df.columns)}")
    print("\nDatos de ejemplo incluidos:")
    print(df.to_string(index=False))

    return filename

if __name__ == "__main__":
    create_sample_excel()
#!/usr/bin/env python3
"""
Script TEMPORAL para crear un Excel de prueba profesional con datos realistas.

IMPORTANTE: Este script es solo para desarrollo y pruebas.
Después de completar las pruebas, eliminar este archivo y limpiar tests/test_data/
"""
import pandas as pd
import os

def create_test_excel():
    """Crear un Excel de prueba con datos realistas para validación"""

    # Datos de prueba realistas con más casos de uso
    test_data = [
        # Caso válido 1: id_predio definido
        {
            'id_carpeta': 1,
            'id_servicio': 1,
            'id_predio': 'PRED001',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 100.50,
            'lectura_actual': 150.75,
            'valor_unitario': 25.0
        },
        # Caso válido 2: id_tercero_cliente definido
        {
            'id_carpeta': 1,
            'id_servicio': 1,
            'id_predio': '',
            'id_tercero_cliente': 12345,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 200.00,
            'lectura_actual': 250.25,
            'valor_unitario': 30.0
        },
        # Caso válido 3: Valores límite
        {
            'id_carpeta': 99,
            'id_servicio': 99,
            'id_predio': 'PRED999',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '204012',  # Último año posible (2040)
            'lectura_anterior': 0.01,
            'lectura_actual': 999999.99,
            'valor_unitario': 999999.0
        },
        # Caso válido 4: valor_unitario mínimo (0)
        {
            'id_carpeta': 1,
            'id_servicio': 2,
            'id_predio': 'PRED000',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 0.0  # Valor mínimo permitido
        },
        # Caso inválido 1: id_carpeta fuera de rango
        {
            'id_carpeta': 150,
            'id_servicio': 1,
            'id_predio': 'PRED003',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 50.0,
            'lectura_actual': 75.0,
            'valor_unitario': 20.0
        },
        # Caso inválido 2: id_servicio fuera de rango
        {
            'id_carpeta': 1,
            'id_servicio': 150,
            'id_predio': 'PRED004',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 25.0,
            'lectura_actual': 50.0,
            'valor_unitario': 15.0
        },
        # Caso inválido 3: periodo_inicio_cobro mal formateado
        {
            'id_carpeta': 2,
            'id_servicio': 2,
            'id_predio': 'PRED005',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '20251',  # 5 dígitos en lugar de 6
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 10.0
        },
        # Caso inválido 3b: año fuera de rango (antes de 2024)
        {
            'id_carpeta': 2,
            'id_servicio': 3,
            'id_predio': 'PRED005B',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202312',  # Año 2023 - fuera de rango
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 10.0
        },
        # Caso inválido 3c: año fuera de rango (después de 2040)
        {
            'id_carpeta': 2,
            'id_servicio': 4,
            'id_predio': 'PRED005C',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '204112',  # Año 2041 - fuera de rango
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 10.0
        },
        # Caso inválido 3d: mes inválido
        {
            'id_carpeta': 2,
            'id_servicio': 5,
            'id_predio': 'PRED005D',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202513',  # Mes 13 - inválido
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 10.0
        },
        # Caso inválido 3e: valor_unitario negativo
        {
            'id_carpeta': 2,
            'id_servicio': 6,
            'id_predio': 'PRED005E',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': -5.0  # Negativo - inválido
        },
        # Caso inválido 6: Ambos id_predio e id_tercero_cliente definidos
        {
            'id_carpeta': 3,
            'id_servicio': 3,
            'id_predio': 'PRED006',
            'id_tercero_cliente': 67890,  # Ambos definidos - ERROR
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 5.0,
            'lectura_actual': 15.0,
            'valor_unitario': 5.0
        },
        # Caso inválido 7: Ninguno definido
        {
            'id_carpeta': 4,
            'id_servicio': 4,
            'id_predio': '',  # Vacío
            'id_tercero_cliente': None,  # Ninguno definido - ERROR
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 0.0,
            'lectura_actual': 10.0,
            'valor_unitario': 1.0
        },
        # Caso con NaN 8: lectura_anterior faltante
        {
            'id_carpeta': 5,
            'id_servicio': 5,
            'id_predio': 'PRED007',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': None,  # NaN
            'lectura_actual': 100.0,
            'valor_unitario': 15.0
        },
        # Caso con NaN 9: valor_unitario faltante
        {
            'id_carpeta': 6,
            'id_servicio': 6,
            'id_predio': 'PRED008',
            'id_tercero_cliente': None,
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 50.0,
            'lectura_actual': 75.0,
            'valor_unitario': None  # NaN
        }
    ]

    # Crear DataFrame
    df = pd.DataFrame(test_data)

    # Crear directorio de pruebas en tests/
    test_dir = '../test_data'
    os.makedirs(test_dir, exist_ok=True)

    # Guardar Excel
    excel_path = os.path.join(test_dir, 'test_importacion_servicios.xlsx')
    df.to_excel(excel_path, index=False, engine='openpyxl')

    print(f"✅ Excel de prueba creado: {excel_path}")
    print(f"📊 Datos incluidos: {len(df)} filas")
    print("\n📋 Columnas:")
    for col in df.columns:
        print(f"   - {col}")

    print("\n📝 Casos de prueba incluidos:")
    print("   - 4 casos válidos (id_predio, id_tercero_cliente, límites, valor_unitario mínimo)")
    print("   - 8 casos inválidos (rangos, formato, exclusividad, período, valor_unitario)")
    print("   - Casos edge (valores límite, NaN en diferentes campos)")

    return excel_path

if __name__ == "__main__":
    create_test_excel()
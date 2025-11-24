"""
Módulo para manejar la importación de archivos Excel
"""
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from .excel_data_validator import ExcelValidator
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class ExcelHandler:
    """Clase para manejar la importación y procesamiento de archivos Excel"""

    def __init__(self):
        self.clear = [
            'id_carpeta', 'id_servicio', 'id_predio', 'id_tercero_cliente', 'periodo_inicio_cobro',
            'lectura_anterior', 'lectura_actual', 'valor_unitario'
        ]
        

    def read_excel_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Lee el archivo Excel y retorna un DataFrame"""
        try:
            if not ExcelValidator.validate_file(file_path):
                return None

            # Leer el archivo Excel 
            df = pd.read_excel(file_path, engine='openpyxl')

            # Limpiar nombres de columnas (quitar espacios y convertir a minúsculas)
            df.columns = df.columns.str.strip().str.lower()

            logger.info(f"Archivo Excel leído exitosamente: {len (df)} filas")
            return df

        except Exception as e:
            logger.error(f"Error al leer archivo Excel: {e}")
            return None       

    def process_excel_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Procesa los datos del Excel y los prepara para insertar en la BD"""
        processed_data = []

        try:
            # Redondear valores de entrada antes de cálculos
            df['lectura_anterior'] = df['lectura_anterior'].astype(float).round(2)
            df['lectura_actual'] = df['lectura_actual'].astype(float).round(2)
            df['valor_unitario'] = df['valor_unitario'].astype(float).round(0)

            # Calcular consumo, saldo y valor_periodo
            if 'consumo' not in df.columns:
                df['consumo'] = df['lectura_actual'] - df['lectura_anterior']
                
            if 'valor_periodo' not in df.columns:
                df['valor_periodo'] = round(df['valor_unitario'] * df['consumo'])

            if 'saldo' not in df.columns:
                df['saldo'] = df['valor_periodo']

            # Crear lista de diccionarios para cada fila
            for _, row in df.iterrows():
                # Manejar valores que pueden ser NaN
                id_carpeta_val = row.get('id_carpeta', 0)
                if pd.isna(id_carpeta_val):
                    id_carpeta_val = 0
                else:
                    id_carpeta_val = int(id_carpeta_val)
                
                id_servicio_val = row.get('id_servicio', 0)
                if pd.isna(id_servicio_val):
                    id_servicio_val = 0
                else:
                    id_servicio_val = int(id_servicio_val)
                
                id_tercero_cliente_val = row.get('id_tercero_cliente')
                if pd.isna(id_tercero_cliente_val):
                    id_tercero_cliente_val = 0  # Valor por defecto cuando no hay id_tercero_cliente
                else:
                    id_tercero_cliente_val = int(id_tercero_cliente_val)
                
                invoice_data = {
                    'consumo': float(row.get('consumo', 0)),
                    'id_carpeta': id_carpeta_val,
                    'id_servicio': id_servicio_val,
                    'id_predio': str(row.get('id_predio', '')),
                    'id_tercero_cliente': id_tercero_cliente_val,
                    'periodo_inicio_cobro': str(row.get('periodo_inicio_cobro', '')),
                    'lectura_anterior': float(row.get('lectura_anterior', 0)),
                    'lectura_actual': float(row.get('lectura_actual', 0)),
                    'saldo': float(row.get('saldo', 0)),
                    'valor_periodo': float(row.get('valor_periodo', 0)),
                    'valor_unitario': float(row.get('valor_unitario', 0))
                }
                processed_data.append(invoice_data)

            logger.info(f"Datos procesados exitosamente: {len(processed_data)} registros")
            return processed_data

        except Exception as e:
            logger.error(f"Error procesando datos: {e}")
            return []

    def get_excel_preview(self, file_path: str) -> Dict[str, Any]:
        """Obtiene una vista previa del archivo Excel"""
        try:
            df = self.read_excel_file(file_path)
            if df is None:
                return {}

            preview = {
                'filename': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'total_rows': len(df),
                'columns': list(df.columns),
                'preview_data': df.head(10).to_dict('records')
            }

            return preview

        except Exception as e:
            logger.error(f"Error obteniendo vista previa: {e}")
            return {}
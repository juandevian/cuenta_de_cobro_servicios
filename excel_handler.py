"""
Módulo para manejar la importación de archivos Excel
"""
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class ExcelHandler:
    """Clase para manejar la importación y procesamiento de archivos Excel"""

    def __init__(self):
        self.supported_extensions = ('.xlsx', '.xls')

    def validate_file(self, file_path: str) -> bool:
        """Valida si el archivo es un Excel válido"""
        if not os.path.exists(file_path):
            logger.error(f"Archivo no encontrado: {file_path}")
            return False

        if not file_path.lower().endswith(self.supported_extensions):
            logger.error(f"Formato no soportado: {file_path}")
            return False

        # Verificar tamaño del archivo (máximo 50MB)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > 50:
            logger.error(f"Archivo demasiado grande: {file_size:.2f}MB")
            return False

        return True

    def read_excel_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Lee el archivo Excel y retorna un DataFrame"""
        try:
            if not self.validate_file(file_path):
                return None

            # Leer el archivo Excel
            df = pd.read_excel(file_path, engine='openpyxl')

            # Limpiar nombres de columnas (quitar espacios y convertir a minúsculas)
            df.columns = df.columns.str.strip().str.lower()

            logger.info(f"Archivo Excel leído exitosamente: {len(df)} filas")
            return df

        except Exception as e:
            logger.error(f"Error al leer archivo Excel: {e}")
            return None

    def validate_excel_structure(self, df: pd.DataFrame) -> List[str]:
        """Valida que el Excel tenga la estructura requerida"""
        errors = []
        required_columns = [
            'numero_factura', 'codigo_cliente', 'fecha_emision', 'fecha_vencimiento',
            'lectura_anterior', 'lectura_actual', 'consumo', 'valor_unitario'
        ]

        # Verificar columnas requeridas
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")

        # Verificar que haya datos
        if df.empty:
            errors.append("El archivo Excel está vacío")

        # Verificar tipos de datos
        if 'fecha_emision' in df.columns:
            try:
                pd.to_datetime(df['fecha_emision'])
            except:
                errors.append("Formato de fecha inválido en columna 'fecha_emision'")

        if 'fecha_vencimiento' in df.columns:
            try:
                pd.to_datetime(df['fecha_vencimiento'])
            except:
                errors.append("Formato de fecha inválido en columna 'fecha_vencimiento'")

        return errors

    def process_excel_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Procesa los datos del Excel y los prepara para insertar en la BD"""
        processed_data = []

        try:
            # Convertir fechas a string
            if 'fecha_emision' in df.columns:
                df['fecha_emision'] = pd.to_datetime(df['fecha_emision']).dt.strftime('%Y-%m-%d')
            if 'fecha_vencimiento' in df.columns:
                df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento']).dt.strftime('%Y-%m-%d')

            # Calcular subtotal, IVA y total si no están presentes
            if 'subtotal' not in df.columns:
                df['subtotal'] = df['consumo'] * df['valor_unitario']

            if 'iva' not in df.columns:
                df['iva'] = df['subtotal'] * 0.19  # IVA del 19%

            if 'total' not in df.columns:
                df['total'] = df['subtotal'] + df['iva']

            # Crear lista de diccionarios para cada fila
            for _, row in df.iterrows():
                invoice_data = {
                    'numero_factura': str(row.get('numero_factura', '')),
                    'codigo_cliente': str(row.get('codigo_cliente', '')),
                    'fecha_emision': row.get('fecha_emision', ''),
                    'fecha_vencimiento': row.get('fecha_vencimiento', ''),
                    'lectura_anterior': float(row.get('lectura_anterior', 0)),
                    'lectura_actual': float(row.get('lectura_actual', 0)),
                    'consumo': float(row.get('consumo', 0)),
                    'valor_unitario': float(row.get('valor_unitario', 0)),
                    'subtotal': float(row.get('subtotal', 0)),
                    'iva': float(row.get('iva', 0)),
                    'total': float(row.get('total', 0)),
                    'estado': 'pendiente'
                }
                processed_data.append(invoice_data)

            logger.info(f"Datos procesados exitosamente: {len(processed_data)} registros")
            return processed_data

        except Exception as e:
            logger.error(f"Error procesando datos del Excel: {e}")
            return []

    def get_excel_preview(self, file_path: str, max_rows: int = 5) -> Optional[Dict[str, Any]]:
        """Obtiene una vista previa del archivo Excel"""
        try:
            df = self.read_excel_file(file_path)
            if df is None:
                return None

            # Obtener información del archivo
            file_info = {
                'filename': os.path.basename(file_path),
                'total_rows': len(df),
                'columns': list(df.columns),
                'preview_data': df.head(max_rows).to_dict('records'),
                'file_size': os.path.getsize(file_path)
            }

            return file_info

        except Exception as e:
            logger.error(f"Error obteniendo vista previa: {e}")
            return None
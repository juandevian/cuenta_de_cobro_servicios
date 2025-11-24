"""
Validador de archivos Excel y datos antes de la inserción en la base de datos.
"""
import pandas as pd
from typing import List, Dict
import os
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class ExcelValidator:
    """Clase para validar archivos Excel"""
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        supported_extensions = ('.xls', '.xlsx', '.xlsm')
        
        """Valida si el archivo existe""" 
        if not os.path.exists(file_path):
            logger.error(f"Archivo no encontrado: {file_path}")
            return False

        """Valida si el archivo es un Excel válido"""
        if not file_path.lower().endswith(supported_extensions):
            logger.error(f"Formato no soportado: {file_path}")
            return False

        # Verificar tamaño del archivo (máximo 20MB)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > 20:
            logger.error(f"Archivo demasiado grande: {file_size}MB")
            return False

        return True

    @staticmethod
    def validate_excel_structure(df: pd.DataFrame, required_columns: List[str]) -> Dict[str, List[str]]:
        """Valida que el Excel tenga la estructura requerida"""
        errors = []
        warnings = []
        
        # Verificar columnas requeridas
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Columnas faltantes: {', '.join(missing_columns)}")
        
        # Verificar que haya datos (vacío o solo encabezados)
        if df.empty or df.dropna(how='all').empty:
            errors.append("El documento seleccionado está vacío")

        # Validar tipos de datos específicos
        data_validation = ExcelValidator.validate_data_types(df)
        errors.extend(data_validation['errors'])
        warnings.extend(data_validation['warnings'])

        # Validar consistencia de id_carpeta e id_servicio
        consistency_errors = ExcelValidator.validate_consistency(df)
        errors.extend(consistency_errors) 
            
        return {'errors': errors, 'warnings': warnings}

    @staticmethod
    def validate_data_types(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Valida los tipos de datos en las columnas requeridas"""
        errors = []
        warnings = []
        
        for idx, row in df.iterrows():
            # Validar id_carpeta: Integer entre 1 y 99
            try:
                id_carpeta = int(row.get('id_carpeta', 0))
                if not (1 <= id_carpeta <= 99):
                    errors.append(f"Fila {idx + 1}: 'id_carpeta' debe ser un entero entre 1 y 99 (valor actual: {row.get('id_carpeta')})")
            except (ValueError, TypeError):
                errors.append(f"Fila {idx + 1}: 'id_carpeta' debe ser un número entero válido (valor actual: {row.get('id_carpeta')})")

            # Validar id_servicio: Integer entre 1 y 99
            try:
                id_servicio = int(row.get('id_servicio', 0))
                if not (1 <= id_servicio <= 99):
                    errors.append(f"Fila {idx + 1}: 'id_servicio' debe ser un entero entre 1 y 99 (valor actual: {row.get('id_servicio')})")
            except (ValueError, TypeError):
                errors.append(f"Fila {idx + 1}: 'id_servicio' debe ser un número entero válido (valor actual: {row.get('id_servicio')})")
            
            # Validar exclusividad mutua: id_predio (varchar) e id_tercero_cliente (integer)
            id_predio = str(row.get('id_predio', '')).strip() 
            id_predio_defined = bool(id_predio) # Definido si no es vacío

            id_tercero_cliente = row.get('id_tercero_cliente')
            id_tercero_cliente_defined = (
                id_tercero_cliente is not None and 
                not pd.isna(id_tercero_cliente) and
                str(id_tercero_cliente).strip()
            ) # Definido si no es None, NaN y no es vacío
            
            if id_predio_defined and id_tercero_cliente_defined:
                errors.append(f"Fila {idx + 1}: 'id_predio' e 'id_tercero_cliente' no pueden tener valores al mismo tiempo")
            elif not id_predio_defined and not id_tercero_cliente_defined:
                errors.append(f"Fila {idx + 1}: Debe haber un valor en 'id_predio' o 'id_tercero_cliente', pero no en ambos")
            elif id_tercero_cliente_defined and id_predio_defined is False:
                try:
                    int(id_tercero_cliente)  # Verificar que sea convertible a int
                except (ValueError, TypeError):
                    errors.append(f"Fila {idx + 1}: 'id_tercero_cliente' debe ser un número entero válido (valor actual: {id_tercero_cliente})")

            # Validar periodo_inicio_cobro: String de 6 dígitos 'AAAAMM'
            periodo = str(row.get('periodo_inicio_cobro', '')).strip()
            if not re.match(r'^\d{6}$', periodo):
                errors.append(f"Fila {idx + 1}: 'periodo_inicio_cobro' debe ser una cadena de exactamente 6 dígitos numéricos (valor actual: '{periodo}')")
            else:
                # Verificar formato AAAAMM (año entre año_actual-1 y 2040, mes 01-12)
                year = int(periodo[:4])
                month = int(periodo[4:])
                
                current_year = datetime.now().year
                min_year = current_year - 1
                max_year = 2040
                
                if not (min_year <= year <= max_year):
                    errors.append(f"Fila {idx + 1}: el año del periodo ingresado no es válido (debe estar entre {min_year} y {max_year})")
                elif not (1 <= month <= 12):
                    errors.append(f"Fila {idx + 1}: el mes del periodo ingresado no es válido (debe estar entre 01 y 12)")

            # Validar valor_unitario: Float entre 0 y 999999
            try:
                valor_unitario = float(row.get('valor_unitario', 0))
                if not (0 <= valor_unitario <= 999999):
                    errors.append(f"Fila {idx + 1}: 'valor_unitario' debe ser un número entre 0 y 999999 (valor actual: {row.get('valor_unitario')})")
            except (ValueError, TypeError):
                errors.append(f"Fila {idx + 1}: 'valor_unitario' debe ser un número válido (valor actual: {row.get('valor_unitario')})")

            # Validar lecturas y consumo
            lectura_anterior = row.get('lectura_anterior')
            lectura_actual = row.get('lectura_actual')
            
            # Convertir NaN a 0
            if pd.isna(lectura_anterior):
                lectura_anterior = 0
            if pd.isna(lectura_actual):
                lectura_actual = 0
            
            # Validar que sean numéricos
            try:
                lectura_anterior = float(lectura_anterior)
                lectura_actual = float(lectura_actual)
            except (ValueError, TypeError):
                errors.append(f"Fila {idx + 1}: 'lectura_anterior' y 'lectura_actual' deben ser números válidos")
                continue
            
            # No permitir lecturas negativas
            if lectura_anterior < 0 or lectura_actual < 0:
                errors.append(f"Fila {idx + 1}: Las lecturas no pueden ser negativas")
                continue
            
            # Validar lectura_actual >= lectura_anterior
            if lectura_actual < lectura_anterior:
                errors.append(f"Fila {idx + 1}: lectura_actual debe ser mayor o igual a lectura_anterior")
            
            # Calcular consumo
            consumo = lectura_actual - lectura_anterior
            
            # Validar límites de consumo
            if consumo < 0:
                errors.append(f"Fila {idx + 1}: El consumo no puede ser negativo")
            elif consumo > 999999:
                errors.append(f"Fila {idx + 1}: El consumo no puede exceder 999999")
            
            # Advertencia si lectura_anterior == 0 y lectura_actual > 0
            if lectura_anterior == 0 and lectura_actual > 0:
                warnings.append(f"Fila {idx + 1}: lectura_anterior es 0, verificar y corregir si es el caso")
            
            # Advertencia para diferencias muy grandes (ej. > 10000)
            if consumo > 10000:
                warnings.append(f"Fila {idx + 1}: Consumo muy alto ({consumo}), revisar datos")

        return {'errors': errors, 'warnings': warnings}

    @staticmethod
    def validate_consistency(df: pd.DataFrame) -> List[str]:
        """Valida consistencia de id_carpeta, id_servicio, periodo_inicio_cobro y valor_unitario (no null/vacío, y algunos deben ser iguales en todas las filas)"""
        errors = []
        
        # Validar id_carpeta: No null/vacío y igual en todas las filas
        id_carpeta_values = df['id_carpeta'].dropna()
        if id_carpeta_values.empty:
            errors.append("La columna 'id_carpeta' no puede estar vacía en todas las filas")
        elif len(id_carpeta_values.unique()) > 1:
            errors.append(f"'id_carpeta' debe ser igual en todas las filas (valores encontrados: {list(id_carpeta_values.unique())})")
        elif pd.isna(df['id_carpeta']).any():
            errors.append("'id_carpeta' no puede contener valores null o vacíos")
        
        # Validar id_servicio: No null/vacío y igual en todas las filas
        id_servicio_values = df['id_servicio'].dropna()
        if id_servicio_values.empty:
            errors.append("La columna 'id_servicio' no puede estar vacía en todas las filas")
        elif len(id_servicio_values.unique()) > 1:
            errors.append(f"'id_servicio' debe ser igual en todas las filas (valores encontrados: {list(id_servicio_values.unique())})")
        elif pd.isna(df['id_servicio']).any():
            errors.append("'id_servicio' no puede contener valores null o vacíos")
        
        # Validar periodo_inicio_cobro: No null/vacío y igual en todas las filas
        periodo_values = df['periodo_inicio_cobro'].dropna()
        if periodo_values.empty:
            errors.append("La columna 'periodo_inicio_cobro' no puede estar vacía en todas las filas")
        elif len(periodo_values.unique()) > 1:
            errors.append(f"'periodo_inicio_cobro' debe ser igual en todas las filas (valores encontrados: {list(periodo_values.unique())})")
        elif pd.isna(df['periodo_inicio_cobro']).any():
            errors.append("'periodo_inicio_cobro' no puede contener valores null o vacíos")
        
        # Validar valor_unitario: No null/vacío (puede variar entre filas)
        if pd.isna(df['valor_unitario']).any():
            errors.append("'valor_unitario' no puede contener valores null o vacíos")
    
        return errors

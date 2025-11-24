"""
Validador de base de datos para verificar concordancia de IDs en tablas de Orión Plus
"""
import pandas as pd
from typing import List
import logging
from .database import DatabaseConnection

logger = logging.getLogger(__name__)

class DatabaseValidator:
    """Clase para validar existencia de IDs en la base de datos"""

    def __init__(self):
        self.db = DatabaseConnection()

    def validate_ids(self, df: pd.DataFrame) -> List[str]:
        """
        Valida que los IDs del DataFrame existan en las tablas correspondientes de la BD
        """
        errors = []

        try:
            for idx, row in df.iterrows():
                # Manejar id_carpeta
                id_carpeta_val = row.get('id_carpeta', 0)
                if pd.isna(id_carpeta_val) or id_carpeta_val is None:
                    id_carpeta_val = 0
                else:
                    try:
                        id_carpeta_val = int(float(id_carpeta_val))
                    except (ValueError, TypeError, OverflowError):
                        id_carpeta_val = 0
                
                # Manejar id_servicio
                id_servicio_val = row.get('id_servicio', 0)
                if pd.isna(id_servicio_val) or id_servicio_val is None:
                    id_servicio_val = 0
                else:
                    try:
                        id_servicio_val = int(float(id_servicio_val))
                    except (ValueError, TypeError, OverflowError):
                        id_servicio_val = 0
                
                id_predio = str(row.get('id_predio', '')).strip()
                id_tercero_cliente = row.get('id_tercero_cliente')

                # Convertir id_tercero_cliente a int si es válido
                if id_tercero_cliente is not None and not pd.isna(id_tercero_cliente):
                    try:
                        id_tercero_cliente = int(float(id_tercero_cliente))
                    except (ValueError, TypeError, OverflowError):
                        id_tercero_cliente = 0  # Valor por defecto si no es convertible
                else:
                    id_tercero_cliente = 0  # Valor por defecto cuando es None/NaN

                # Usar las variables val
                id_carpeta = id_carpeta_val
                id_servicio = id_servicio_val

                # Validar id_carpeta en oriitemsprogramafact
                query_carpeta = "SELECT COUNT(*) FROM oriitemsprogramafact WHERE IdCarpeta = %s"
                result_carpeta = self.db.execute_query(query_carpeta, (id_carpeta,))
                if result_carpeta and result_carpeta[0]['COUNT(*)'] == 0:
                    errors.append(f"Fila {idx + 1}: 'id_carpeta' {id_carpeta} no existe en oriitemsprogramafact")

                # Validar id_servicio en oriservicios con clave (id_carpeta, idano=0, id_servicio)
                query_servicio = "SELECT COUNT(*) FROM oriservicios WHERE IdCarpeta = %s AND IdAno = 0 AND IdServicio = %s"
                result_servicio = self.db.execute_query(query_servicio, (id_carpeta, id_servicio))
                if result_servicio and result_servicio[0]['COUNT(*)'] == 0:
                    errors.append(f"Fila {idx + 1}: 'id_servicio' {id_servicio} no existe en oriservicios para id_carpeta {id_carpeta}")

                # Validar id_predio en oripredios (solo si id_tercero_cliente está vacío)
                if id_predio and (id_tercero_cliente is None):
                    query_predio = "SELECT COUNT(*) FROM oripredios WHERE IdCarpeta = %s AND IdPredio = %s"
                    result_predio = self.db.execute_query(query_predio, (id_carpeta, id_predio))
                    if result_predio and result_predio[0]['COUNT(*)'] == 0:
                        errors.append(f"Fila {idx + 1}: 'id_predio' {id_predio} no existe en oripredios para id_carpeta {id_carpeta}")

                # Validar id_tercero_cliente en oriclientes (solo si id_predio está vacío)
                if id_tercero_cliente is not None and not id_predio:
                    query_cliente = "SELECT COUNT(*) FROM oriclientes WHERE IdCarpeta = %s AND IdTerceroCliente = %s"
                    result_cliente = self.db.execute_query(query_cliente, (id_carpeta, id_tercero_cliente))
                    if result_cliente and result_cliente[0]['COUNT(*)'] == 0:
                        errors.append(f"Fila {idx + 1}: 'id_tercero_cliente' {id_tercero_cliente} no existe en oriclientes para id_carpeta {id_carpeta}")

            logger.info(f"Validación de BD completada: {len(errors)} errores encontrados")
            return errors

        except Exception as e:
            logger.error(f"Error en validación de BD: {e}")
            return [f"Error interno en validación de base de datos: {str(e)}"]
        finally:
            self.db.disconnect()

    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.db:
            self.db.disconnect()
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
                id_carpeta = int(row.get('id_carpeta', 0))
                id_servicio = int(row.get('id_servicio', 0))
                id_predio = str(row.get('id_predio', '')).strip()
                id_tercero_cliente = row.get('id_tercero_cliente')

                # Convertir id_tercero_cliente a int si no es None/vacío
                if id_tercero_cliente is not None and str(id_tercero_cliente).strip():
                    id_tercero_cliente = int(id_tercero_cliente)
                else:
                    id_tercero_cliente = None

                # Validar id_carpeta en oriitemsprogramafact
                query_carpeta = "SELECT COUNT(*) FROM oriitemsprogramafact WHERE id_carpeta = %s"
                result_carpeta = self.db.execute_query(query_carpeta, (id_carpeta,))
                if result_carpeta and result_carpeta[0][0] == 0:
                    errors.append(f"Fila {idx + 1}: 'id_carpeta' {id_carpeta} no existe en oriitemsprogramafact")

                # Validar id_servicio en oriservicios con clave (id_carpeta, idano=0, id_servicio)
                query_servicio = "SELECT COUNT(*) FROM oriservicios WHERE id_carpeta = %s AND idano = 0 AND id_servicio = %s"
                result_servicio = self.db.execute_query(query_servicio, (id_carpeta, id_servicio))
                if result_servicio and result_servicio[0][0] == 0:
                    errors.append(f"Fila {idx + 1}: 'id_servicio' {id_servicio} no existe en oriservicios para id_carpeta {id_carpeta}")

                # Validar id_predio en oripredios (solo si id_tercero_cliente está vacío)
                if id_predio and id_tercero_cliente is None:
                    query_predio = "SELECT COUNT(*) FROM oripredios WHERE id_carpeta = %s AND id_predio = %s"
                    result_predio = self.db.execute_query(query_predio, (id_carpeta, id_predio))
                    if result_predio and result_predio[0][0] == 0:
                        errors.append(f"Fila {idx + 1}: 'id_predio' {id_predio} no existe en oripredios para id_carpeta {id_carpeta}")

                # Validar id_tercero_cliente en oriclientes (solo si id_predio está vacío)
                if id_tercero_cliente is not None and not id_predio:
                    query_cliente = "SELECT COUNT(*) FROM oriclientes WHERE id_carpeta = %s AND id_tercero_cliente = %s"
                    result_cliente = self.db.execute_query(query_cliente, (id_carpeta, id_tercero_cliente))
                    if result_cliente and result_cliente[0][0] == 0:
                        errors.append(f"Fila {idx + 1}: 'id_tercero_cliente' {id_tercero_cliente} no existe en oriclientes para id_carpeta {id_carpeta}")

            logger.info(f"Validación de BD completada: {len(errors)} errores encontrados")
            return errors

        except Exception as e:
            logger.error(f"Error en validación de BD: {e}")
            return [f"Error interno en validación de base de datos: {str(e)}"]
        finally:
            self.db.close()

    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.db:
            self.db.close()
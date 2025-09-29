"""
Módulo de conexión y operaciones con base de datos MySQL
"""
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
import logging
from config import Config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Clase para manejar la conexión con la base de datos MySQL"""

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self) -> bool:
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if self.connection.is_connected():
                logger.info("Conexión exitosa a la base de datos MySQL")
                return True
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            return False

    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión cerrada")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Ejecuta una consulta SELECT"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Error ejecutando consulta: {e}")
            return None

    def execute_insert(self, query: str, params: tuple = None) -> Optional[int]:
        """Ejecuta una consulta INSERT y retorna el ID insertado"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            last_id = cursor.rowcount
            cursor.close()
            return last_id
        except Error as e:
            logger.error(f"Error ejecutando insert: {e}")
            self.connection.rollback()
            return None

    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Ejecuta una consulta UPDATE"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Error ejecutando update: {e}")
            self.connection.rollback()
            return False

    def insert_item_program_invoice(
            self,
            CantidadPeriodos: int,
            Consumo: int,
            IdAno: int,
            IdCarpeta: int,
            IdCentroUtil: int,
            IdPredio: str,
            IdServicio: int,
            IdTerceroCliente: float,
            LecturaActual: float,
            LecturaAnterior: float,
            Ordinal: int,
            Origen: str,
            PeriodoInicioFact: str,
            Saldo: float,
            ValorPeriodo: float,
            ValorUnitario: float) -> Optional[int]:
        """Inserta una nueva factura"""
        query = """
            INSERT INTO oriitemsprogramafact(CantidadPeriodos, Consumo, IdAno, IdCarpeta, IdCentroUtil, IdPredio, IdServicio, IdTerceroCliente, LecturaAnterior, LecturaActual, Ordinal, Origen, PeriodoInicioFact, Saldo, ValorPeriodo, ValorUnitario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (CantidadPeriodos, Consumo, IdAno, IdCarpeta, IdCentroUtil, IdPredio, IdServicio, IdTerceroCliente, LecturaAnterior, LecturaActual, Ordinal, Origen, PeriodoInicioFact, Saldo, ValorPeriodo,  ValorUnitario)
        return self.execute_insert(query, params)

    # TODO: Revisar si se usan estos métodos get_invoices_count y get_last_invoice_number
    def get_items_count(self) -> int:
        """Obtiene el conteo total de items"""
        query = "SELECT COUNT(*) as count FROM oriitemsprogramafact WHERE Origen = '3'"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0

    def get_last_item_ordinal(self) -> Optional[str]:
        """Obtiene el último ordinal de item de factura"""
        query = "SELECT ordinal FROM oriitemsprogramafact ORDER BY ordinal DESC LIMIT 1"
        result = self.execute_query(query)
        return result[0]['ordinal'] if result else None

    def get_client_by_id(self, client_id: float) -> Optional[Dict[str, Any]]:
        """Obtiene un cliente por su ID"""
        query = "SELECT * FROM oriclientes WHERE idTerceroCliente = %s"
        params = (client_id,)
        result = self.execute_query(query, params)
        return result[0] if result else None
    
    def get_property_by_id(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un predio por su ID"""
        query = "SELECT * FROM oripredios WHERE idPredio = %s"
        params = (property_id,)
        result = self.execute_query(query, params)
        return result[0] if result else None
    
    def delete_items_by_service(self, folder_id: int, service_id: int) -> bool:
        """Elimina items de factura por IdServicio"""
        query = "DELETE FROM oriitemsprogramafact WHERE IdCarpeta = %s AND IdAno = '0' AND IdServicio = %s"
        params = (folder_id, service_id,)
        return self.execute_update(query, params)
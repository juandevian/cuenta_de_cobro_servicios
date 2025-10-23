"""
Módulo de conexión y operaciones con base de datos MySQL
"""
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Clase para manejar la conexión con la base de datos MySQL"""

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self) -> bool:
        """Establece conexión con la base de datos"""
        # Validar configuración mínima antes de intentar conectar
        if not Config.validate_config():
            logger.error(
                "Configuración de base de datos incompleta. Defina DB_HOST, DB_USERNAME y DB_NAME via variables de entorno (.env)."
            )
            self.connection = None
            return False
        try:
            # Resolver contraseña: ENV primero; si no, intentar keyring
            password = Config.DB_PASSWORD
            if not password:
                try:
                    import keyring  # type: ignore
                    password = keyring.get_password(Config.KEYRING_SERVICE, Config.DB_USER) or ''
                    if not password:
                        logger.error(
                            "No se encontró contraseña en keyring (servicio=%s, usuario=%s).",
                            Config.KEYRING_SERVICE,
                            Config.DB_USER,
                        )
                        self.connection = None
                        return False
                except ImportError:
                    logger.error("El paquete 'keyring' no está instalado y no hay DB_PASSWORD en el entorno.")
                    self.connection = None
                    return False

            # Usar use_pure=True para evitar extensiones C que pueden causar access violations
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=password,
                database=Config.DB_NAME,
                use_pure=True
            )
            if self.connection.is_connected():
                logger.info("Conexión exitosa a la base de datos MySQL")
                return True
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            self.connection = None
            return False
        except Exception as e:
            logger.error(f"Error inesperado al conectar a MySQL: {e}")
            self.connection = None
            return False

    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexión cerrada")

    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Ejecuta una consulta SELECT"""
        if not self.connection or not self.connection.is_connected():
            logger.error("No hay conexión a la base de datos. Imposible ejecutar consulta.")
            return None
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
        if not self.connection or not self.connection.is_connected():
            logger.error("No hay conexión a la base de datos. Imposible ejecutar insert.")
            return None
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
        if not self.connection or not self.connection.is_connected():
            logger.error("No hay conexión a la base de datos. Imposible ejecutar update.")
            return False
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
            INSERT INTO oriitemsprogramafact(
                CantidadPeriodos, Consumo, IdAno, IdCarpeta, IdCentroUtil,
                IdPredio, IdServicio, IdTerceroCliente, LecturaAnterior,
                LecturaActual, Ordinal, Origen, PeriodoInicioFact,
                Saldo, ValorPeriodo, ValorUnitario
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        params = (
            CantidadPeriodos, Consumo, IdAno, IdCarpeta, IdCentroUtil,
            IdPredio, IdServicio, IdTerceroCliente, LecturaAnterior,
            LecturaActual, Ordinal, Origen, PeriodoInicioFact,
            Saldo, ValorPeriodo, ValorUnitario
        )
        return self.execute_insert(query, params)
    
    def get_last_item_ordinal(self) -> Optional[int]:
        """Obtiene el último ordinal usado en los items de factura"""
        query = "SELECT MAX(Ordinal) AS last_ordinal FROM oriitemsprogramafact"
        result = self.execute_query(query)
        if result and len(result) > 0:
            return result[0]['last_ordinal'] or 0
        return None
    
    def delete_items_by_service(self, IdCarpeta: int, IdServicio: int) -> bool:
        """Elimina items de factura por IdCarpeta e IdServicio"""
        query = """
            DELETE FROM oriitemsprogramafact
            WHERE IdCarpeta = %s AND IdServicio = %s
        """
        params = (IdCarpeta, IdServicio)
        return self.execute_update(query, params)
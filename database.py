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
            last_id = cursor.lastrowid
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

    def get_client_by_code(self, codigo_cliente: str) -> Optional[Dict]:
        """Obtiene un cliente por su código"""
        query = "SELECT * FROM clientes WHERE codigo_cliente = %s"
        result = self.execute_query(query, (codigo_cliente,))
        return result[0] if result else None

    def insert_client(self, codigo_cliente: str, nombre: str, direccion: str = None,
                     telefono: str = None, email: str = None) -> Optional[int]:
        """Inserta un nuevo cliente"""
        query = """
            INSERT INTO clientes (codigo_cliente, nombre, direccion, telefono, email)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (codigo_cliente, nombre, direccion, telefono, email)
        return self.execute_insert(query, params)

    def insert_invoice(self, numero_factura: str, id_cliente: int, fecha_emision: str,
                      fecha_vencimiento: str, lectura_anterior: float, lectura_actual: float,
                      consumo: float, valor_unitario: float, subtotal: float,
                      iva: float, total: float, estado: str = 'pendiente') -> Optional[int]:
        """Inserta una nueva factura"""
        query = """
            INSERT INTO facturas (numero_factura, id_cliente, fecha_emision, fecha_vencimiento,
                                lectura_anterior, lectura_actual, consumo, valor_unitario,
                                subtotal, iva, total, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (numero_factura, id_cliente, fecha_emision, fecha_vencimiento,
                 lectura_anterior, lectura_actual, consumo, valor_unitario,
                 subtotal, iva, total, estado)
        return self.execute_insert(query, params)

    def get_invoices_count(self) -> int:
        """Obtiene el conteo total de facturas"""
        query = "SELECT COUNT(*) as count FROM facturas"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0

    def get_last_invoice_number(self) -> Optional[str]:
        """Obtiene el último número de factura"""
        query = "SELECT numero_factura FROM facturas ORDER BY id DESC LIMIT 1"
        result = self.execute_query(query)
        return result[0]['numero_factura'] if result else None
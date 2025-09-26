"""
Módulo principal para procesar facturas desde Excel a SQLite
"""
from typing import List, Dict, Any, Optional
import logging
from database_sqlite import SQLiteConnection
from excel_handler import ExcelHandler

logger = logging.getLogger(__name__)

class InvoiceProcessorSQLite:
    """Clase principal para procesar la importación de facturas con SQLite"""

    def __init__(self):
        self.db = SQLiteConnection()
        self.excel_handler = ExcelHandler()

    def process_excel_import(self, file_path: str) -> Dict[str, Any]:
        """Procesa la importación completa de un archivo Excel"""
        result = {
            'success': False,
            'message': '',
            'processed': 0,
            'errors': [],
            'warnings': []
        }

        try:
            # Validar conexión a base de datos
            if not self.db.connection:
                result['message'] = 'Error de conexión a la base de datos SQLite'
                return result

            # Leer archivo Excel
            df = self.excel_handler.read_excel_file(file_path)
            if df is None:
                result['message'] = 'Error al leer el archivo Excel'
                return result

            # Validar estructura del Excel
            validation_errors = self.excel_handler.validate_excel_structure(df)
            if validation_errors:
                result['message'] = 'Errores de validación en el archivo Excel'
                result['errors'] = validation_errors
                return result

            # Procesar datos
            processed_data = self.excel_handler.process_excel_data(df)
            if not processed_data:
                result['message'] = 'No se pudieron procesar los datos del Excel'
                return result

            # Insertar datos en la base de datos
            success_count = 0
            error_count = 0

            for invoice_data in processed_data:
                try:
                    # Verificar si el cliente existe
                    client = self.db.get_client_by_code(invoice_data['codigo_cliente'])

                    if not client:
                        # Crear nuevo cliente
                        client_id = self.db.insert_client(
                            codigo_cliente=invoice_data['codigo_cliente'],
                            nombre=f"Cliente {invoice_data['codigo_cliente']}",
                            telefono=None,
                            email=None
                        )

                        if not client_id:
                            result['errors'].append(f"Error al crear cliente {invoice_data['codigo_cliente']}")
                            error_count += 1
                            continue
                    else:
                        client_id = client['id']

                    # Insertar factura
                    invoice_id = self.db.insert_invoice(
                        numero_factura=invoice_data['numero_factura'],
                        id_cliente=client_id,
                        fecha_emision=invoice_data['fecha_emision'],
                        fecha_vencimiento=invoice_data['fecha_vencimiento'],
                        lectura_anterior=invoice_data['lectura_anterior'],
                        lectura_actual=invoice_data['lectura_actual'],
                        consumo=invoice_data['consumo'],
                        valor_unitario=invoice_data['valor_unitario'],
                        subtotal=invoice_data['subtotal'],
                        iva=invoice_data['iva'],
                        total=invoice_data['total'],
                        estado=invoice_data['estado']
                    )

                    if invoice_id:
                        success_count += 1
                    else:
                        result['errors'].append(f"Error al insertar factura {invoice_data['numero_factura']}")
                        error_count += 1

                except Exception as e:
                    logger.error(f"Error procesando factura {invoice_data.get('numero_factura', 'desconocida')}: {e}")
                    error_count += 1

            # Preparar resultado final
            result['success'] = success_count > 0
            result['processed'] = success_count
            result['message'] = f"Procesamiento completado: {success_count} facturas importadas exitosamente"

            if error_count > 0:
                result['message'] += f", {error_count} errores"
                result['warnings'].append(f"{error_count} facturas no pudieron ser procesadas")

            logger.info(f"Importación completada: {success_count} exitosas, {error_count} errores")

        except Exception as e:
            logger.error(f"Error general en el procesamiento: {e}")
            result['message'] = f"Error general: {str(e)}"

        return result

    def get_import_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen de las importaciones realizadas"""
        try:
            total_invoices = self.db.get_invoices_count()
            last_invoice = self.db.get_last_invoice_number()

            return {
                'total_invoices': total_invoices,
                'last_invoice_number': last_invoice,
                'database_status': 'connected' if self.db.connection else 'disconnected',
                'database_type': 'SQLite',
                'database_path': self.db.db_path
            }
        except Exception as e:
            logger.error(f"Error obteniendo resumen: {e}")
            return {'error': str(e)}

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.db.disconnect()
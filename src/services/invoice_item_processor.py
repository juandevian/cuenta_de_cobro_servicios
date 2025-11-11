"""
Módulo principal para procesar facturas desde Excel a MySQL
"""
from typing import List, Dict, Any, Optional
import logging
from services.database import DatabaseConnection
from services.excel_handler import ExcelHandler
from services.database_validator import DatabaseValidator

logger = logging.getLogger(__name__)

class InvoiceItemProcessor:
    """Clase principal para procesar la importación de item de facturas"""

    def __init__(self):
        self.db = DatabaseConnection()
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
            if not self.db.connection or not self.db.connection.is_connected():
                result['message'] = 'Error de conexión a la base de datos'
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
            
            # Validar BD con DatabaseValidator
            db_validator = DatabaseValidator()
            db_errors = db_validator.validate_ids(df)
            db_validator.close()  # Cerrar conexión
            if db_errors:
                result['message'] = 'Errores de validación en la base de datos'
                result['errors'].extend(validation_errors)  # Incluir errores previos si los hay
                result['errors'].extend(db_errors)
                return result

            # Procesar datos
            processed_data = self.excel_handler.process_excel_data(df)
            if not processed_data:
                result['message'] = 'No se pudieron procesar los datos del Excel'
                return result
            
            # Obtener el último ordinal
            last_ordinal = self.db.get_last_item_ordinal()
            if last_ordinal is None:
                last_ordinal = 0

            # Insertar datos en la base de datos
            success_count = 0
            error_count = 0
            
            # Eliminar items existentes para el IdCarpeta y el IdServicio
            delete_items = self.db.delete_items_by_service(processed_data[0]['id_carpeta'], processed_data[0]['id_servicio'])
            
            if not delete_items:
                logger.warning(f"No se pudieron eliminar items existentes para IdCarpeta {processed_data[0]['id_carpeta']} e IdServicio {processed_data[0]['id_servicio']}")

            for invoice_data in processed_data:
                try:
                    last_ordinal += 1  # Incrementar el ordinal para cada nuevo item

                    # Insertar items de factura
                    invoice_item_id = self.db.insert_item_program_invoice(
                        CantidadPeriodos=1,
                        Consumo=invoice_data['consumo'],
                        IdAno=0,
                        IdCarpeta=invoice_data['id_carpeta'],
                        IdCentroUtil=1,
                        IdPredio=invoice_data['id_predio'],
                        IdServicio=invoice_data['id_servicio'],
                        IdTerceroCliente=invoice_data['id_tercero_cliente'],
                        LecturaActual=invoice_data['lectura_actual'],
                        LecturaAnterior=invoice_data['lectura_anterior'],
                        Ordinal=last_ordinal,
                        Origen='3',  # Origen 3 = Importación desde Excel
                        PeriodoInicioFact=invoice_data['periodo_inicio_cobro'],
                        Saldo=invoice_data['saldo'],
                        ValorPeriodo=invoice_data['valor_periodo'],
                        ValorUnitario=invoice_data['valor_unitario']
                    )

                    if invoice_item_id:
                        success_count += 1
                    else:
                        result['errors'].append(f"Error al insertar item del predio {invoice_data['id_predio']} en la base de datos")
                        error_count += 1

                except Exception as e:
                    logger.error(f"Error procesando item de factura {invoice_data.get('id_predio', 'desconocido')}: {e}")
                    error_count += 1

            # Actualizar resultado
            result['success'] = success_count > 0
            result['processed'] = success_count
            result['message'] = f"Importación completada. {success_count} registros insertados."
            
            if error_count > 0:
                result['message'] += f" {error_count} errores encontrados."

        except Exception as e:
            logger.error(f"Error en el proceso de importación: {e}")
            result['message'] = f"Error en el proceso de importación: {str(e)}"
            result['errors'].append(str(e))

        return result

    def close(self):
        """Cierra las conexiones"""
        if self.db:
            self.db.disconnect()
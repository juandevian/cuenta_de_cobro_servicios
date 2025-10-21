#!/usr/bin/env python3
"""
Suite de pruebas unitarias para el sistema de importación de facturas
Usa pytest para ejecutar: pytest test_app.py -v
"""
import pytest
import sys
import os
import tempfile
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos a testear
from src.config import Config
from database import DatabaseConnection
from excel_handler import ExcelHandler
from invoice_item_processor import InvoiceItemProcessor
from create_excels import create_sample_excel, create_excel_import_template


class TestConfig:
    """Pruebas para la clase Config"""

    def test_config_attributes(self):
        """Verifica que todos los atributos de configuración existan"""
        assert hasattr(Config, 'DB_HOST')
        assert hasattr(Config, 'DB_PORT')
        assert hasattr(Config, 'DB_USER')
        assert hasattr(Config, 'DB_PASSWORD')
        assert hasattr(Config, 'DB_NAME')
        assert hasattr(Config, 'APP_NAME')
        assert hasattr(Config, 'APP_VERSION')
        assert hasattr(Config, 'WINDOW_WIDTH')
        assert hasattr(Config, 'WINDOW_HEIGHT')
        assert hasattr(Config, 'LOG_LEVEL')

    def test_config_types(self):
        """Verifica los tipos de datos de la configuración"""
        assert isinstance(Config.DB_HOST, str)
        assert isinstance(Config.DB_PORT, int)
        assert isinstance(Config.DB_USER, str)
        assert isinstance(Config.DB_PASSWORD, str)
        assert isinstance(Config.DB_NAME, str)
        assert isinstance(Config.APP_NAME, str)
        assert isinstance(Config.APP_VERSION, str)

    @patch.dict(os.environ, {'DB_HOST': 'test_host', 'DB_PORT': '3307'})
    def test_env_variables(self):
        """Verifica que las variables de entorno se carguen correctamente"""
        # Recargar el módulo para capturar variables de entorno
        import importlib
        import src.config as config
        importlib.reload(config)
        from src.config import Config as TestConfig

        assert TestConfig.DB_HOST == 'test_host'
        assert TestConfig.DB_PORT == 3307


class TestDatabaseConnection:
    """Pruebas para la clase DatabaseConnection"""

    @patch('database.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """Verifica conexión exitosa a la base de datos"""
        mock_connection = Mock()
        mock_connection.is_connected.return_value = True
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        assert db.connect() is True
        assert db.connection == mock_connection

    @patch('database.mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """Verifica manejo de error en conexión"""
        mock_connect.side_effect = Exception("Connection failed")

        db = DatabaseConnection()
        assert db.connect() is False
        assert db.connection is None

    def test_disconnect(self):
        """Verifica desconexión de la base de datos"""
        db = DatabaseConnection()
        db.connection = Mock()
        db.connection.is_connected.return_value = True

        db.disconnect()
        db.connection.close.assert_called_once()

    @patch('database.mysql.connector.connect')
    def test_execute_query(self, mock_connect):
        """Verifica ejecución de consultas SELECT"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'test'}]
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.execute_query("SELECT * FROM test")
        assert result == [{'id': 1, 'name': 'test'}]
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test", ())

    @patch('database.mysql.connector.connect')
    def test_execute_insert(self, mock_connect):
        """Verifica ejecución de consultas INSERT"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.lastrowid = 123
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.execute_insert("INSERT INTO test VALUES (?)", ("value",))
        assert result == 123
        mock_connection.commit.assert_called_once()

    @patch('database.mysql.connector.connect')
    def test_execute_update(self, mock_connect):
        """Verifica ejecución de consultas UPDATE"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.execute_update("UPDATE test SET name = ?", ("new_name",))
        assert result is True
        mock_connection.commit.assert_called_once()

    @patch('database.mysql.connector.connect')
    def test_insert_item_program_invoice(self, mock_connect):
        """Verifica inserción de items de factura"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.lastrowid = 456
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.insert_item_program_invoice(
            CantidadPeriodos=1,
            IdAno=2023,
            IdTerceroCliente=123,
            IdCarpeta=1,
            IdCentroUtil=1,
            IdPredio="PRED001",
            IdServicio=1,
            LecturaActual=100.0,
            LecturaAnterior=90.0,
            Origen="Test",
            PeriodoInicioFact="2023-01-01",
            Saldo=10.0,
            ValorPeriodo=10.0,
            ValorUnitario=1.0
        )
        assert result == 456

    @patch('database.mysql.connector.connect')
    def test_get_invoices_count(self, mock_connect):
        """Verifica conteo de facturas"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [{'count': 5}]
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.get_invoices_count()
        assert result == 5

    @patch('database.mysql.connector.connect')
    def test_get_last_invoice_number(self, mock_connect):
        """Verifica obtención del último número de factura"""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [{'numero_factura': 'F001'}]
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        db.connection = mock_connection

        result = db.get_last_invoice_number()
        assert result == 'F001'


class TestExcelHandler:
    """Pruebas para la clase ExcelHandler"""

    def test_init(self):
        """Verifica inicialización del ExcelHandler"""
        handler = ExcelHandler()
        assert handler.supported_extensions == ('.xlsx', '.xls')

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_validate_file_valid(self, mock_getsize, mock_exists):
        """Verifica validación de archivo válido"""
        mock_exists.return_value = True
        mock_getsize.return_value = 1024 * 1024  # 1MB

        handler = ExcelHandler()
        result = handler.validate_file('test.xlsx')
        assert result is True

    @patch('os.path.exists')
    def test_validate_file_not_exists(self, mock_exists):
        """Verifica validación de archivo inexistente"""
        mock_exists.return_value = False

        handler = ExcelHandler()
        result = handler.validate_file('nonexistent.xlsx')
        assert result is False

    def test_validate_file_wrong_extension(self):
        """Verifica validación de archivo con extensión incorrecta"""
        handler = ExcelHandler()
        result = handler.validate_file('test.txt')
        assert result is False

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_validate_file_too_large(self, mock_getsize, mock_exists):
        """Verifica validación de archivo demasiado grande"""
        mock_exists.return_value = True
        mock_getsize.return_value = 60 * 1024 * 1024  # 60MB

        handler = ExcelHandler()
        result = handler.validate_file('large.xlsx')
        assert result is False

    @patch('pandas.read_excel')
    @patch.object(ExcelHandler, 'validate_file')
    def test_read_excel_file(self, mock_validate, mock_read_excel):
        """Verifica lectura de archivo Excel"""
        mock_validate.return_value = True
        mock_df = Mock()
        mock_df.columns = pd.Index(['col1', 'col2'])
        mock_read_excel.return_value = mock_df

        handler = ExcelHandler()
        result = handler.read_excel_file('test.xlsx')
        assert result == mock_df

    def test_validate_excel_structure_valid(self):
        """Verifica validación de estructura Excel válida"""
        df = pd.DataFrame({
            'id_carpeta': [1, 2],
            'id_servicio': [1, 2],
            'id_predio': ['P1', 'P2'],
            'id_tercero_cliente': [1, 2],
            'periodo_inicio_cobro': ['2023-01', '2023-02'],
            'lectura_anterior': [10.0, 20.0],
            'lectura_actual': [15.0, 25.0],
            'valor_unitario': [1.0, 2.0]
        })

        handler = ExcelHandler()
        errors = handler.validate_excel_structure(df)
        assert len(errors) == 0

    def test_validate_excel_structure_missing_columns(self):
        """Verifica validación con columnas faltantes"""
        df = pd.DataFrame({'col1': [1, 2]})

        handler = ExcelHandler()
        errors = handler.validate_excel_structure(df)
        assert len(errors) > 0
        assert 'Columnas faltantes' in errors[0]

    def test_process_excel_data(self):
        """Verifica procesamiento de datos Excel"""
        df = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['P1'],
            'id_tercero_cliente': [1],
            'periodo_inicio_cobro': ['2023-01-01'],
            'lectura_anterior': [10.0],
            'lectura_actual': [15.0],
            'valor_unitario': [1.0]
        })

        handler = ExcelHandler()
        result = handler.process_excel_data(df)
        assert len(result) == 1
        assert result[0]['consumo'] == 5.0
        assert result[0]['valor_periodo'] == 5.0
        assert result[0]['saldo'] == 5.0

    @patch.object(ExcelHandler, 'read_excel_file')
    @patch('os.path.basename')
    @patch('os.path.getsize')
    def test_get_excel_preview(self, mock_getsize, mock_basename, mock_read):
        """Verifica obtención de vista previa Excel"""
        mock_df = pd.DataFrame({'col1': [1, 2, 3]})
        mock_read.return_value = mock_df
        mock_basename.return_value = 'test.xlsx'
        mock_getsize.return_value = 1024

        handler = ExcelHandler()
        result = handler.get_excel_preview('path/test.xlsx')
        assert result is not None
        assert result['filename'] == 'test.xlsx'
        assert result['total_rows'] == 3


class TestInvoiceItemProcessor:
    """Pruebas para la clase InvoiceItemProcessor"""

    def test_init(self):
        """Verifica inicialización del InvoiceItemProcessor"""
        with patch('invoice_item_processor.DatabaseConnection'), \
             patch('invoice_item_processor.ExcelHandler'):
            processor = InvoiceItemProcessor()
            assert processor.db is not None
            assert processor.excel_handler is not None

    @patch('invoice_item_processor.DatabaseConnection')
    @patch('invoice_item_processor.ExcelHandler')
    def test_process_excel_import(self, mock_excel_handler, mock_db):
        """Verifica procesamiento de importación Excel"""
        # Mock de datos procesados
        processed_data = [{
            'id_carpeta': 1,
            'id_servicio': 1,
            'id_predio': 'P1',
            'id_tercero_cliente': 1,
            'consumo': 5.0,
            'periodo_inicio_cobro': '2023-01-01',
            'lectura_anterior': 10.0,
            'lectura_actual': 15.0,
            'saldo': 5.0,
            'valor_periodo': 5.0,
            'valor_unitario': 1.0
        }]

        # Mock de ExcelHandler
        mock_excel_instance = Mock()
        mock_excel_handler.return_value = mock_excel_instance
        mock_excel_instance.process_excel_data.return_value = processed_data

        # Mock de DatabaseConnection
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        mock_db_instance.get_client_by_id.return_value = {'id': 1}
        mock_db_instance.get_property_by_id.return_value = {'id': 'P1'}
        mock_db_instance.insert_item_program_invoice.return_value = 123

        processor = InvoiceItemProcessor()
        result = processor.process_excel_import('test.xlsx')

        assert result['success'] is True
        assert result['processed'] == 1
        assert result['errors'] == []

    @patch('invoice_item_processor.DatabaseConnection')
    @patch('invoice_item_processor.ExcelHandler')
    def test_get_import_summary(self, mock_excel_handler, mock_db):
        """Verifica obtención de resumen de importación"""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        mock_db_instance.get_invoices_count.return_value = 10

        processor = InvoiceItemProcessor()
        summary = processor.get_import_summary()

        assert 'total_invoices' in summary
        assert summary['total_invoices'] == 10

    @patch('invoice_item_processor.DatabaseConnection')
    def test_close(self, mock_db):
        """Verifica cierre del procesador"""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance

        processor = InvoiceItemProcessor()
        processor.close()

        mock_db_instance.disconnect.assert_called_once()


class TestCreateExcels:
    """Pruebas para funciones de creación de Excels"""

    @patch('pandas.DataFrame.to_excel')
    def test_create_sample_excel(self, mock_to_excel):
        """Verifica creación de Excel de ejemplo"""
        with patch('builtins.print'):  # Suprimir prints
            filename = create_sample_excel()
            assert filename.endswith('.xlsx')
            mock_to_excel.assert_called()

    @patch('pandas.DataFrame.to_excel')
    def test_create_excel_import_template(self, mock_to_excel):
        """Verifica creación de plantilla Excel"""
        with patch('builtins.print'):  # Suprimir prints
            filename = create_excel_import_template()
            assert 'plantilla' in filename
            assert filename.endswith('.xlsx')
            mock_to_excel.assert_called()


if __name__ == "__main__":
    # Ejecutar pruebas con pytest
    pytest.main([__file__, "-v"])
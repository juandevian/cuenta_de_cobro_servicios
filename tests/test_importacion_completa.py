import pytest
import pandas as pd
import os
from src.services.excel_handler import ExcelHandler
from src.services.excel_data_validator import ExcelValidator
from src.services.database_validator import DatabaseValidator


class TestImportacionCompleta:
    """Tests de integración para la importación completa de Excel"""

    @pytest.fixture
    def test_excel_path(self):
        """Fixture que crea y retorna el path del Excel de prueba"""
        # Importar el script de creación
        import sys
        sys.path.append('.')
        from tests.fixtures.create_test_excel import create_test_excel

        # Crear el Excel si no existe
        excel_path = create_test_excel()
        return excel_path

    @pytest.fixture
    def test_data_df(self, test_excel_path):
        """Fixture que carga el DataFrame de prueba"""
        return pd.read_excel(test_excel_path, engine='openpyxl')

    def test_excel_structure_validation(self, test_data_df):
        """Test que valida la estructura completa del Excel"""
        validator = ExcelValidator()
        required_columns = [
            'id_carpeta', 'id_servicio', 'id_predio', 'id_tercero_cliente',
            'periodo_inicio_cobro', 'lectura_anterior', 'lectura_actual', 'valor_unitario'
        ]

        errors = ExcelValidator.validate_excel_structure(test_data_df, required_columns)

        # Debería haber errores porque incluimos casos inválidos intencionalmente
        assert len(errors) > 0
        print(f"Errores encontrados: {errors}")

    def test_excel_reading_and_processing(self, test_excel_path):
        """Test que valida la lectura y procesamiento del Excel"""
        handler = ExcelHandler()

        # Leer Excel
        df = handler.read_excel_file(test_excel_path)
        assert df is not None
        assert len(df) == 15  # 15 filas de prueba (actualizado con casos adicionales)

        # Procesar datos
        processed_data = handler.process_excel_data(df)
        assert len(processed_data) > 0

        # Verificar estructura de datos procesados
        first_item = processed_data[0]
        required_keys = [
            'consumo', 'id_carpeta', 'id_servicio', 'id_predio', 'id_tercero_cliente',
            'periodo_inicio_cobro', 'lectura_anterior', 'lectura_actual', 'saldo',
            'valor_periodo', 'valor_unitario'
        ]

        for key in required_keys:
            assert key in first_item

    def test_validation_cases(self, test_data_df):
        """Test específico para validar casos individuales"""
        validator = ExcelValidator()

        # Caso 1: Válido con id_predio
        valid_row = test_data_df.iloc[0]
        single_row_df = pd.DataFrame([valid_row])
        result = ExcelValidator.validate_data_types(single_row_df)
        assert len(result['errors']) == 0, f"No debería haber errores en caso válido: {result['errors']}"

        # Caso 4: Inválido - id_carpeta fuera de rango
        invalid_row = test_data_df.iloc[4]  # id_carpeta = 150 (actualizado por nuevos casos)
        single_row_df = pd.DataFrame([invalid_row])
        result = ExcelValidator.validate_data_types(single_row_df)
        assert len(result['errors']) > 0
        assert "id_carpeta" in str(result['errors'][0])

        # Caso 6: Inválido - periodo mal formateado
        invalid_row = test_data_df.iloc[6]  # periodo = '20251' (actualizado por nuevos casos)
        single_row_df = pd.DataFrame([invalid_row])
        result = ExcelValidator.validate_data_types(single_row_df)
        assert len(result['errors']) > 0
        assert "periodo_inicio_cobro" in str(result['errors'][0])

    def test_nan_handling(self, test_data_df):
        """Test específico para validar manejo de NaN"""
        validator = ExcelValidator()

        # Caso con NaN en lectura_anterior (fila 8)
        nan_row = test_data_df.iloc[8]
        single_row_df = pd.DataFrame([nan_row])
        result = validator.validate_data_types(single_row_df)

        # No debería fallar por NaN, debería manejarse correctamente
        # (aunque puede haber otros errores de validación)
        # Lo importante es que no crashee
        assert isinstance(result, dict)

    def test_consistency_validation(self, test_data_df):
        """Test de validación de consistencia"""
        validator = ExcelValidator()

        # Tomar filas 0 y 1 (ambas con id_carpeta=1, id_servicio=1, periodo=202511)
        consistent_df = test_data_df.iloc[0:2]
        errors = ExcelValidator.validate_consistency(consistent_df)

        # Debería pasar la validación de consistencia
        consistency_errors = [e for e in errors if 'igual en todas las filas' in e]
        assert len(consistency_errors) == 0, f"Errores de consistencia: {consistency_errors}"

    def test_exclusivity_validation(self, test_data_df):
        """Test de validación de exclusividad mutua"""
        validator = ExcelValidator()

        # Caso de exclusividad: Ambos definidos (debería fallar)
        both_defined_row = test_data_df.iloc[11]  # Ambos id_predio e id_tercero_cliente (actualizado por nuevos casos)
        single_row_df = pd.DataFrame([both_defined_row])
        result = ExcelValidator.validate_data_types(single_row_df)
        assert len(result['errors']) > 0
        assert "no pueden tener valores al mismo tiempo" in str(result['errors'][0])

        # Crear un caso específico donde ninguno está definido
        none_defined_data = {
            'id_carpeta': 10,
            'id_servicio': 10,
            'id_predio': '',  # Vacío
            'id_tercero_cliente': None,  # None
            'periodo_inicio_cobro': '202511',
            'lectura_anterior': 10.0,
            'lectura_actual': 20.0,
            'valor_unitario': 5.0
        }
        none_defined_df = pd.DataFrame([none_defined_data])
        result = ExcelValidator.validate_data_types(none_defined_df)
        assert len(result['errors']) > 0
        # Buscar el error específico de exclusividad
        exclusivity_errors = [e for e in result['errors'] if "Debe haber un valor" in e]
        assert len(exclusivity_errors) > 0, f"No se encontró error de exclusividad. Errores: {result['errors']}"
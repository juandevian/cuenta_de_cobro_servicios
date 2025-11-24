import pytest
import pandas as pd
from src.services.excel_handler import ExcelHandler
from src.services.excel_data_validator import ExcelValidator

class TestExcelHandler:
    def test_validate_file_nonexistent(self):
        """Prueba que validate_file retorne False para archivo inexistente"""
        result = ExcelValidator.validate_file("nonexistent.xlsx")
        assert result == False

    def test_validate_file_invalid_extension(self):
        """Prueba que validate_file retorne False para extensión inválida"""
        result = ExcelValidator.validate_file("../requirements.txt")  # Crea un archivo dummy si es necesario
        assert result == False

    def test_validate_data_types_valid(self):
        """Prueba validate_data_types con datos válidos"""
        validator = ExcelValidator()
        df = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [5],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202511'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df)
        assert len(result['errors']) == 0  # No debe haber errores

    def test_validate_data_types_invalid_id_carpeta(self):
        """Prueba validate_data_types con id_carpeta inválido"""
        df = pd.DataFrame({
            'id_carpeta': [150],  # Fuera de rango (1-99)
            'id_servicio': [5],
            'id_predio': [''],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202311'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df)
        assert len(result['errors']) > 0
        assert "id_carpeta" in result['errors'][0] and "entre 1 y 99" in result['errors'][0]

    def test_validate_data_types_nan_tercero_cliente(self):
        """Prueba eclusividad mutua con NaN en id_tercero_cliente (debe permitir id_predio)"""
        validator = ExcelValidator()
        df = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [5],
            'id_predio': ['PRED001'],  # Definido
            'id_tercero_cliente': [float('nan')],  # NaN, no definido
            'periodo_inicio_cobro': ['202511'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df)
        assert len(result['errors']) == 0  # No debe haber error de exclusividad

    def test_validate_period_range(self):
        """Prueba validación de rango de período"""
        # Caso válido: dentro del rango
        df_valid = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202412'],  # Año 2024 (mínimo actual)
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df_valid)
        assert len(result['errors']) == 0

        # Caso inválido: año antes del rango
        df_invalid_year_low = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202311'],  # Año 2023 - inválido
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df_invalid_year_low)
        assert len(result['errors']) > 0
        assert "año del periodo ingresado no es válido" in result['errors'][0]

        # Caso inválido: año después del rango
        df_invalid_year_high = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['204112'],  # Año 2041 - inválido
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df_invalid_year_high)
        assert len(result['errors']) > 0
        assert "año del periodo ingresado no es válido" in result['errors'][0]

        # Caso inválido: mes fuera de rango
        df_invalid_month = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202513'],  # Mes 13 - inválido
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [10.0]
        })
        result = ExcelValidator.validate_data_types(df_invalid_month)
        assert len(result['errors']) > 0
        assert "mes del periodo ingresado no es válido" in result['errors'][0]

    def test_validate_valor_unitario_range(self):
        """Prueba validación de rango de valor_unitario"""
        # Caso válido: valor_unitario = 0 (mínimo permitido)
        df_valid_zero = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202511'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [0.0]  # Valor mínimo válido
        })
        result = ExcelValidator.validate_data_types(df_valid_zero)
        assert len(result['errors']) == 0

        # Caso válido: valor_unitario positivo
        df_valid_positive = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202511'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [100.5]  # Será redondeado a 101
        })
        result = ExcelValidator.validate_data_types(df_valid_positive)
        assert len(result['errors']) == 0

        # Caso inválido: valor_unitario negativo
        df_invalid_negative = pd.DataFrame({
            'id_carpeta': [1],
            'id_servicio': [1],
            'id_predio': ['PRED001'],
            'id_tercero_cliente': [None],
            'periodo_inicio_cobro': ['202511'],
            'lectura_anterior': [100.0],
            'lectura_actual': [150.0],
            'valor_unitario': [-5.0]  # Negativo - inválido
        })
        result = ExcelValidator.validate_data_types(df_invalid_negative)
        assert len(result['errors']) > 0
        assert "valor_unitario" in result['errors'][0] and "entre 0 y 999999" in result['errors'][0]
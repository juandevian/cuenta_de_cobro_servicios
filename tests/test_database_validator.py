import pytest
import pandas as pd
from src.services.database_validator import DatabaseValidator

class TestDatabaseValidator:
    def test_validate_ids_existing_carpeta(self, mocker):
        """Prueba validación cuando id_carpeta existe"""
        validator = DatabaseValidator()
        # Mock del objeto db
        mock_db = mocker.patch.object(validator, 'db')
        mock_db.execute_query.return_value = [{'COUNT(*)': 1}]  # Simula resultado existente

        df = pd.DataFrame({'id_carpeta': [1], 'id_servicio': [1], 'id_predio': [''], 'id_tercero_cliente': [None]})
        errors = validator.validate_ids(df)
        
        assert len(errors) == 0  # No errores si existe

    def test_validate_ids_missing_carpeta(self, mocker):
        """Prueba validación cuando id_carpeta no existe"""
        validator = DatabaseValidator()
        mock_db = mocker.patch.object(validator, 'db')
        mock_db.execute_query.return_value = [{'COUNT(*)': 0}]  # Simula no encontrado

        df = pd.DataFrame({'id_carpeta': [999], 'id_servicio': [1], 'id_predio': [''], 'id_tercero_cliente': [None]})
        errors = validator.validate_ids(df)
        
        assert len(errors) > 0  # Debe haber error
        assert "no existe en oriitemsprogramafact" in errors[0]
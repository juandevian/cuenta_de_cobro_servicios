#!/usr/bin/env python3
"""
Script para probar la importación completa usando el Excel de prueba
"""
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from services.invoice_item_processor import InvoiceItemProcessor

def test_full_import():
    """Probar la importación completa con el Excel de prueba"""

    # Ruta al Excel de prueba
    excel_path = '../test_data/test_importacion_servicios.xlsx'

    if not os.path.exists(excel_path):
        print(f"❌ Excel de prueba no encontrado: {excel_path}")
        assert False, f"Excel de prueba no encontrado: {excel_path}"

    print(f"📄 Usando Excel de prueba: {excel_path}")

    # Crear procesador
    processor = InvoiceItemProcessor()

    try:
        # Ejecutar importación completa
        print("🚀 Iniciando importación completa...")
        result = processor.process_excel_import(excel_path)

        print("\n📊 Resultados de la importación:")
        print(f"   ✅ Éxito: {result['success']}")
        print(f"   📝 Mensaje: {result['message']}")
        print(f"   🔢 Procesados: {result['processed']}")
        print(f"   ⚠️  Advertencias: {len(result['warnings'])}")
        print(f"   ❌ Errores: {len(result['errors'])}")

        if result['errors']:
            print("\n🚨 Errores encontrados:")
            for error in result['errors']:
                print(f"   - {error}")

        if result['warnings']:
            print("\n⚠️  Advertencias:")
            for warning in result['warnings']:
                print(f"   - {warning}")

        # Validación final - este Excel tiene errores intencionalmente
        assert not result['success'], "La importación debería fallar debido a errores de validación"
        assert result['processed'] == 0, "No deberían procesarse registros con errores"
        assert len(result['errors']) > 0, "Deberían detectarse errores de validación"
        assert len(result['warnings']) >= 0, "Pueden haber advertencias"

        print("\n✅ Validaciones funcionando correctamente!")
        print(f"   Se detectaron {len(result['errors'])} errores como esperado.")
        print(f"   Se detectaron {len(result['warnings'])} advertencias.")

    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        assert False, f"Error durante la importación: {e}"
    finally:
        # Cerrar conexiones si es necesario
        pass  # DatabaseConnection maneja la conexión automáticamente

if __name__ == "__main__":
    try:
        test_full_import()
        print("\n✅ Test completado exitosamente!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test falló: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
# Sistema de Importación de Facturas Panorama_net

Programa de escritorio multiplataforma para importar facturas desde archivos Excel a una base de datos MySQL.

## Características

- ✅ Interfaz gráfica intuitiva con PyQt5
- ✅ Importación automática desde archivos Excel (.xlsx, .xls)
- ✅ Conexión a base de datos MySQL
- ✅ Validación de datos antes de la importación
- ✅ Procesamiento en segundo plano
- ✅ Log detallado de operaciones
- ✅ Vista previa de archivos Excel
- ✅ Configuración de conexión a base de datos
- ✅ Manejo de errores robusto

## Requisitos del Sistema

### Software Requerido
- Python 3.7 o superior
- MySQL Server 5.7 o superior

### Dependencias de Python
```bash
pip install -r requirements.txt
```

## Instalación

### 1. Clonar o descargar el proyecto
```bash
git clone <url-del-repositorio>
cd ori_cc_servicios
```

### 2. Instalar dependencias
```bash
# Si pip no está instalado, instálalo primero:
python -m ensurepip --upgrade

# Luego instala las dependencias:
pip install -r requirements.txt

# O instala manualmente los paquetes principales:
pip install PyQt5 pandas openpyxl mysql-connector-python pydantic python-dateutil colorlog
```

### 3. Configurar base de datos
Ejecutar el script de inicialización:
```bash
python init_database.py
```

O manualmente:
- Crear una base de datos MySQL llamada `Panorama_net`
- Ejecutar el contenido del archivo `database_schema.sql`

### 4. Configurar variables de entorno (opcional pero recomendado)
Copia el archivo de ejemplo y configura tus credenciales:
```bash
cp .env.example .env
# Edita .env con tus valores reales
```

### 5. Ejecutar pruebas
Antes de usar la aplicación, ejecuta las pruebas unitarias:
```bash
# Instalar dependencias de desarrollo
pip install pytest python-dotenv

# Ejecutar todas las pruebas
pytest test_app.py -v

# O ejecutar con reporte detallado
pytest test_app.py --tb=short
```

### 6. Ejecutar la aplicación

**Opción A: Con MySQL (requiere MySQL instalado)**
```bash
python main.py
```

## Uso de la Aplicación

### 1. Importación de items de facturas de servicios con datos de consumo.
- Ve a la pestaña "Importar Cobro de Servicios"
- Haz clic en "Seleccionar Archivo Excel"
- Elige un archivo Excel con el formato correcto
- Opcionalmente, haz clic en "Vista Previa" para ver los datos
- Haz clic en "Importar Servicio" para comenzar la importación

### 2. Monitoreo
- Observa el progreso en la barra de progreso
- Revisa el log de operaciones para detalles
- Al finalizar, se mostrará un resumen de la importación

## Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas obligatorias:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id_carpeta | Número | Número de la carpeta de la copropiedad en Orión |
| id_servicio | Número | Número de servicio en Servicios Permanentes |
| id_predio | Texto | Identificación del predio en Orión (Si se va a cobrar a una persona sin predio se deja vacío) |
| id_tercero_cliente | Número | Si se le va a cobrar a un cliente sin predio, se agrega la identificación |
| periodo_inicio_cobro | Texto | Año y mes en el que se realizará el cobro, (YYYYMM) Ej. '202603' (Marzo de 2026) |
| lectura_anterior | Número | Lectura anterior del medidor |
| lectura_actual | Número | Lectura actual del medidor |
| valor_unitario | Número | Valor por unidad |

### Columnas Opcionales
- saldo: Se calcula automáticamente si no está presente
- consumo: Se calcula automáticamente (lectura_actual - lectura_anterior)

## Estructura de la Base de Datos

### Tabla: itemsprogramafact
- CantidadPeriodos: Meses de cobro - 1 (automático)
- Consumo: Consumo calculado
- IdAno: Servicio permanente - 0 (automático) (KEY)
- IdTerceroCliente: Identificación del cliente - (Sólo si no se cobra a un predio)
- IdCarpeta: Número de carpeta de la copropiedad asignado en Orión
- IdCentroUtil: Centro de utilidad - 1 (automático) (KEY)
- IdPredio: Nombre del predio al que se va a cobrar - Exactamente como está en Orión
- IdServicio: Servicio permanente creado para este cobro.
- LecturaActual: Lectura actual del medidor
- LecturaAnterior: Lectura anterior del medidor
- Ordinal: Número consecutivo (KEY)
- Origen: Generación: 1-Calculado, 2-Usuario, 3-Importado
- PeriodoInicioFact: Periodo YYYYMM (202602 = Feb/2026).
- Saldo: Automático (Valor Periodo * Cantidad de Periodos)
- ValorPeriodo: Automático
- ValorUnitario: Precio por unidad de consumo

## Archivos del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `main_window.py`: Ventana principal con interfaz gráfica
- `database.py`: Conexión y operaciones con MySQL
- `excel_handler.py`: Manejo de archivos Excel
- `invoice_item_processor.py`: Lógica de procesamiento de items de facturas
- `config.py`: Configuración de la aplicación
- `database_schema.sql`: Esquema de la base de datos
- `init_database.py`: Script de inicialización de BD
- `test_app.py`: Suite completa de pruebas unitarias
- `create_excels.py`: Scripts para generar archivos Excel de ejemplo
- `requirements.txt`: Dependencias de Python
- `.env.example`: Plantilla de variables de entorno

## Pruebas Unitarias

El proyecto incluye una suite completa de pruebas unitarias usando pytest:

### Ejecutar Pruebas
```bash
# Todas las pruebas
pytest test_app.py -v

# Pruebas específicas
pytest test_app.py::TestDatabaseConnection::test_connect_success -v

# Con cobertura
pytest test_app.py --cov=. --cov-report=html
```

### Cobertura de Pruebas
- **Config**: Validación de configuración y variables de entorno
- **DatabaseConnection**: Todos los métodos de conexión y consultas
- **ExcelHandler**: Validación, lectura y procesamiento de Excel
- **InvoiceItemProcessor**: Procesamiento completo de importaciones
- **Funciones auxiliares**: Creación de archivos Excel

### Mocks y Fixtures
Las pruebas usan mocks para:
- Conexiones de base de datos
- Archivos del sistema
- Dependencias externas
- Evitar efectos secundarios en pruebas

## Ejemplo de Uso

1. **Preparar datos de ejemplo**:
   - Crea un archivo Excel con el formato especificado
   - Incluye al menos las columnas obligatorias
   - Guarda como `facturas_ejemplo.xlsx`

2. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

3. **Importar datos**:
   - Selecciona el archivo Excel
   - Revisa la vista previa
   - Ejecuta la importación

## Solución de Problemas

### Error de conexión a MySQL
- Verifica que MySQL esté ejecutándose
- Comprueba las credenciales en `config.py`
- Asegúrate de que la base de datos exista

### Error al leer archivo Excel
- Verifica que el archivo no esté corrupto
- Asegúrate de que tenga las columnas requeridas
- Comprueba que los datos estén en el formato correcto

### Error de permisos
- Verifica que tengas permisos de escritura en la base de datos
- Asegúrate de que el usuario de MySQL tenga los privilegios necesarios

## Logging

La aplicación genera logs detallados en:
- Consola: Con colores para diferentes niveles
- Archivo: `panorama_net.log` (si se puede crear)

Niveles de log:
- DEBUG: Información detallada para desarrollo
- INFO: Información general de operaciones
- WARNING: Advertencias
- ERROR: Errores
- CRITICAL: Errores críticos

## Desarrollo

### Agregar nuevas características
1. Edita los archivos correspondientes
2. Actualiza las dependencias en `requirements.txt`
3. Prueba los cambios
4. Actualiza este README

### Estructura del código
- Sigue las convenciones PEP 8
- Usa type hints
- Incluye docstrings
- Maneja excepciones apropiadamente

## Soporte

Para soporte técnico o reportar bugs:
1. Revisa los logs de la aplicación
2. Verifica la configuración
3. Consulta la documentación
4. Reporta el problema con detalles específicos

## Licencia

Este proyecto es desarrollado para uso interno de la organización.

---

**Versión**: 1.0.0
**Fecha**: Septiembre 2025
**Auto**: DevIan (Sebas Villegas)
**Desarrollado con**: Python 3.7+, PyQt5, MySQL
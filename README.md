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
- Git (opcional)

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

### 4. Configurar conexión (opcional)
Editar el archivo `config.py` si es necesario cambiar los parámetros de conexión:
```python
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'tu_contraseña'
DB_NAME = 'Panorama_net'
```

### 5. Ejecutar la aplicación

**Opción A: Con MySQL (requiere MySQL instalado)**
```bash
python main.py
```

**Opción B: Con SQLite (recomendado para desarrollo/pruebas)**
```bash
# Configurar base de datos SQLite
python init_sqlite.py

# Ejecutar aplicación con SQLite (versión completa)
python main_sqlite.py

# O ejecutar versión simplificada (recomendada)
python main_sqlite_simple.py
```

## Uso de la Aplicación

### 1. Configuración de Base de Datos
- Ve a la pestaña "Configuración"
- Modifica los parámetros de conexión si es necesario
- Haz clic en "Probar Conexión" para verificar
- Guarda la configuración

### 2. Importación de Facturas
- Ve a la pestaña "Importar Facturas"
- Haz clic en "Seleccionar Archivo Excel"
- Elige un archivo Excel con el formato correcto
- Opcionalmente, haz clic en "Vista Previa" para ver los datos
- Haz clic en "Importar Facturas" para comenzar la importación

### 3. Monitoreo
- Observa el progreso en la barra de progreso
- Revisa el log de operaciones para detalles
- Al finalizar, se mostrará un resumen de la importación

## Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas obligatorias:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| numero_factura | Texto | Número único de la factura |
| codigo_cliente | Texto | Código del cliente |
| fecha_emision | Fecha | Fecha de emisión (YYYY-MM-DD) |
| fecha_vencimiento | Fecha | Fecha de vencimiento (YYYY-MM-DD) |
| lectura_anterior | Número | Lectura anterior del medidor |
| lectura_actual | Número | Lectura actual del medidor |
| consumo | Número | Consumo calculado |
| valor_unitario | Número | Valor por unidad |

### Columnas Opcionales
- subtotal: Se calcula automáticamente si no está presente
- iva: Se calcula automáticamente (19%) si no está presente
- total: Se calcula automáticamente si no está presente

## Estructura de la Base de Datos

### Tabla: clientes
- id: Identificador único
- codigo_cliente: Código del cliente
- nombre: Nombre del cliente
- direccion: Dirección
- telefono: Teléfono
- email: Correo electrónico
- fecha_registro: Fecha de registro

### Tabla: facturas
- id: Identificador único
- numero_factura: Número de factura
- id_cliente: Referencia al cliente
- fecha_emision: Fecha de emisión
- fecha_vencimiento: Fecha de vencimiento
- lectura_anterior: Lectura anterior
- lectura_actual: Lectura actual
- consumo: Consumo
- valor_unitario: Valor unitario
- subtotal: Subtotal
- iva: IVA (19%)
- total: Total a pagar
- estado: Estado de la factura
- fecha_pago: Fecha de pago
- metodo_pago: Método de pago
- observaciones: Observaciones

### Tabla: pagos
- id: Identificador único
- id_factura: Referencia a la factura
- monto_pagado: Monto pagado
- fecha_pago: Fecha de pago
- metodo_pago: Método de pago
- referencia: Referencia del pago
- observaciones: Observaciones

## Archivos del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `main_window.py`: Ventana principal con interfaz gráfica
- `database.py`: Conexión y operaciones con MySQL
- `excel_handler.py`: Manejo de archivos Excel
- `invoice_processor.py`: Lógica de procesamiento de facturas
- `config.py`: Configuración de la aplicación
- `database_schema.sql`: Esquema de la base de datos
- `init_database.py`: Script de inicialización de BD
- `requirements.txt`: Dependencias de Python

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
**Fecha**: Septiembre 2024
**Desarrollado con**: Python 3.7+, PyQt5, MySQL
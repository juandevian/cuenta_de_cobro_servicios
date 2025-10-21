
# Changelog

> Todos los cambios importantes en este repositorio se documentan en este archivo.

El formato sigue: https://keepachangelog.com/es/1.0.0/

## [Unreleased]

### Added

- **Estructura de paquete Python estándar**: Migración completa a estructura `src/` siguiendo las mejores prácticas de Python.
  - Organización modular en paquetes: `config/`, `services/`, `ui/`, `models/`
  - Archivo `setup.py` para instalación editable del paquete
  - Archivos `__init__.py` en todos los paquetes para correcta importación
  
- **Scripts de desarrollo multiplataforma**:
  - `dev.ps1`: Script PowerShell para Windows con comandos `-install`, `-run`, `-test`
  - `dev.sh`: Script Bash para Git Bash/Linux con las mismas funcionalidades
  - Carga automática de variables de entorno desde `.env.development`

- **Módulo de utilidades** (`src/utils.py`):
  - Función `resource_path()` para manejo de rutas en desarrollo y producción (compatible con PyInstaller)
  - Evita importaciones circulares moviendo funciones compartidas

- **Esquema de base de datos**: Archivo `assets/database_schema.sql` con definición completa de la tabla `oriitemsprogramafact`

- **Configuración de pruebas**: 
  - `tests/pytest.ini` con configuración estándar de pytest
  - Tests simplificados en `tests/test_app_simple.py`

### Changed

- **Reestructuración completa del proyecto**:
  - Todo el código fuente movido de raíz a `src/`
  - Imports actualizados para usar rutas de paquete (`from src.config import Config`)
  - Imports relativos en módulos internos (`from ..services import`)

- **Simplificación de `.gitignore`**:
  - Reducido de 179 líneas a 41 líneas manteniendo solo lo esencial
  - Categorización clara: entornos virtuales, archivos sensibles, compilación, IDE, sistema operativo
  - Eliminación de reglas redundantes o innecesarias

- Actualización de la pestaña de "Información" en `main_window.py`: se dividió el contenido informativo en dos bloques (resumen rápido con acciones y enlace a documentación detallada). Se mejoró la redacción de la guía rápida y se añadió soporte para enlaces externos.

- Nueva documentación en formato Markdown: `docs/guia-importacion-servicios.md` creada con la guía completa de usuario para la importación de servicios por consumo (incluye estructura del Excel, validaciones, proceso paso a paso y resolución de problemas). Esta documentación está pensada para publicarse en Notion.

### Fixed

- **Crash crítico de MySQL** (Segmentation fault / Access violation):
  - Agregado `use_pure=True` en la conexión MySQL para forzar implementación Python pura
  - Evita problemas con la extensión C (`_mysql_connector.pyd`) que causaba crashes en Windows
  - Manejo robusto de errores de conexión sin detener la aplicación
  
- **Importaciones circulares**:
  - Movida función `resource_path()` de `main.py` a módulo independiente `utils.py`
  - Resuelto ciclo de importación entre `main.py` y `ui/main_window.py`

- **Gestión de ventanas PyQt**:
  - Guardada referencia a ventana de vista previa (`self.preview_window`) para evitar garbage collection prematuro
  - Previene crashes y comportamiento inestable de la UI

- **Manejo opcional del esquema SQL**:
  - La aplicación ya no falla si `database_schema.sql` no existe
  - Verificación de existencia del archivo antes de intentar cargarlo
  - Logs informativos en lugar de errores críticos

### Removed

- Archivos obsoletos eliminados:
  - `init_database.py` (funcionalidad integrada en `main.py`)
  - `ejemplo_facturas.xlsx` de raíz (ahora se genera dinámicamente)
  - Código duplicado y archivos de prueba antiguos

## [0.1.0] - 2025-10-19

### Changed

- Eliminación de Tab de configuración; ajustes en módulos requeridos y varias mejoras de optimización y limpieza de código.
  - commit 5ec5bc8 — Eliminación de Tab de configuración, se realizan ajustes en los módulos reqeuridos y se realizan modificaciones varias de optimización y mejora de código. (Ian Dev Villegas, 2025-10-19)
  - Archivos afectados: create_excels.py, database_schema.sql, main.py, main_window.py, plantilla_importacion_servicios.xlsx, test_database_schema.sql

- Correcciones en README, cambios en la estructura del archivo Excel (estilos), y adición de nuevas librerías.
  - commit ed7591db — Se realizan algunas correcciones en el README, cambios en la estructura del archivo de excel con estilos, se agregan nuevas librerías de python, y se realiza una rapida depuración del código. (Ian Dev Villegas, 2025-10-16)
  - Archivos afectados: create_excels.py, ejemplo_facturas.xlsx, main_window.py, plantilla_importacion_servicios.xlsx

---
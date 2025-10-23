
# Changelog

> Todos los cambios importantes en este repositorio se documentan en este archivo.

El formato sigue: https://keepachangelog.com/es/1.0.0/

## [Unreleased]

Nada por ahora.

## [0.1.0] - 2025-10-22

### Added

- **Sistema de configuración segura para producción**:
  - Soporte de `config.json` (sin secretos) para almacenar host, puerto, usuario y base de datos
  - Integración con Windows Credential Manager mediante librería `keyring` para almacenar contraseñas de forma segura
  - Búsqueda prioritaria de configuración: `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\config.json`, carpeta del ejecutable (PyInstaller), directorio actual
  - Contraseñas nunca almacenadas en archivos de texto plano

- **Herramienta standalone de configuración** (`set_password.exe`):
  - Ejecutable independiente compilado con PyInstaller (no requiere Python instalado)
  - Interfaz de consola amigable con banner y validación de entrada
  - Registro de credenciales en Windows Credential Manager
  - Confirmación de contraseña para evitar errores
  - Incluido automáticamente en el instalador

- **Script SQL para usuario MySQL con privilegios mínimos** (`docs/setup_mysql_user.sql`):
  - Crea usuario de base de datos con permisos restringidos (SELECT, INSERT, UPDATE, DELETE únicamente)
  - Limitado a tabla específica (`oriitemsprogramafact`)
  - Sin permisos para modificar estructura, crear tablas o acceder a otras bases de datos
  - Documentación detallada línea por línea en el script
  - Instrucciones de personalización (host, contraseña, permisos adicionales)

- **Documentación completa de despliegue**:
  - Nueva sección "Despliegue en Producción (Windows)" en `README.md` con flujo de 3 pasos
  - `docs/GUIA_DESPLIEGUE.md`: Guía rápida con diagrama visual de flujo completo
  - `docs/CHECKLIST_VALIDACION.md`: Lista de verificación paso a paso para instalación
  - Instrucciones para DBA y administrador de sistemas separadas
  - Solución de problemas comunes documentada

- **Plantilla de configuración unificada**:
  - Se usa `config.example.json` (en la raíz) como plantilla JSON sin secretos
  - El instalador copia esta plantilla como `config.json` si no existe
  - Comentarios integrados e incluye valores por defecto (localhost, 3306, panorama_net)

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

- **Instalador mejorado con seguridad y automatización** (`installer.iss`):
  - Copia automática de `set_password.exe` a la carpeta de instalación
  - Generación de `config.json` desde plantilla (solo si no existe)
  - Inclusión de `setup_mysql_user.sql` en carpeta `docs` para referencia del DBA
  - Permisos NTFS restrictivos en carpeta de instalación (solo Admin/SYSTEM)
  - Generación automática de `INSTRUCCIONES_CONFIGURACION.txt` con guía completa post-instalación
  - Mensaje informativo al finalizar con pasos de configuración
  - Apertura automática de instrucciones en Notepad
  - **Eliminación de accesos directos**: La aplicación se ejecuta únicamente desde VB.NET (no desde menú inicio ni escritorio)

- **Carga de configuración con prioridad** (`src/config/config.py`):
  - Nueva función `_load_config_json_priority()` para lectura de config.json desde múltiples ubicaciones
  - Función `_load_env_priority()` mejorada para buscar `.env` en: ProgramData, carpeta ejecutable, directorio actual, `.env.development`
  - Exportación automática de valores JSON a variables de entorno si no están definidas
  - Validación de configuración mínima antes de intentar conexión
  - URL de base de datos ofuscada en logs (contraseña reemplazada por `***`)

- **Conexión a base de datos con recuperación segura de contraseñas** (`src/services/database.py`):
  - Intentar primero contraseña desde variable de entorno `DB_PASSWORD`
  - Fallback a Windows Credential Manager usando `keyring` si la variable no existe
  - Validación previa de configuración antes de intentar conectar
  - Verificación de estado de conexión antes de ejecutar cualquier consulta
  - Mensajes de error claros y específicos para cada fallo
  - Importación de `keyring` con manejo de excepciones (aviso si no está instalado)

- **Reestructuración completa del proyecto**:
  - Todo el código fuente movido de raíz a `src/`
  - Imports actualizados para usar rutas de paquete (`from src.config import Config`)
  - Imports relativos en módulos internos (`from ..services import`)

- **Reorganización de archivos de compilación**:
  - Creada carpeta `packaging/` para agrupar archivos de PyInstaller
  - Movidos `ori_cc_servicios.spec` y `set_password.spec` de raíz a `packaging/`
  - Actualizados paths relativos en archivos `.spec` (`../src/`, `../assets/`)
  - Creado `packaging/README.md` con instrucciones completas de compilación
  - Actualizada toda la documentación con nuevos comandos: `pyinstaller packaging/*.spec`

- **Simplificación y actualización de `.gitignore`**:
  - Reducido de 179 líneas a 41 líneas manteniendo solo lo esencial
  - Categorización clara: entornos virtuales, archivos sensibles, compilación, IDE, sistema operativo
  - Eliminación de reglas redundantes o innecesarias
  - **Nuevas exclusiones**: `config.json` y `setup_mysql_user.sql` para evitar versionar archivos con credenciales
  - Permitidos archivos `.spec` en `packaging/` (se versionan correctamente)

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

### Documentation

- **Nueva documentación completa de desarrollo y compilación**:
  - `docs/RECETA_COMPILACION.md`: Guía paso a paso completa ("receta") para desarrolladores
  - Incluye: configuración inicial, desarrollo local, ejecución, pruebas, compilación e instalador
  - Comandos para PowerShell y Git Bash/Linux
  - Cheat sheet con comandos rápidos
  - Solución de problemas comunes con ejemplos
  - Flujo completo de trabajo diario y generación de versiones

### Security

- **Sistema de múltiples capas de seguridad implementado**:
  - **Capa 1 - Base de datos**: Usuario MySQL con privilegios mínimos (solo operaciones básicas en una tabla específica)
  - **Capa 2 - Almacenamiento de credenciales**: Contraseñas en Windows Credential Manager (nunca en archivos de texto)
  - **Capa 3 - Permisos de archivos**: Carpeta de instalación con permisos NTFS restrictivos (Admin/SYSTEM únicamente)
  - **Capa 4 - Logs**: Contraseñas no expuestas en logs (URL de conexión ofuscada)
  - **Capa 5 - Control de versiones**: Archivos con credenciales excluidos de Git

- **Separación de responsabilidades**:
  - DBA configura usuario MySQL (credenciales de root nunca salen del equipo)
  - Instalador no ejecuta comandos de base de datos ni solicita credenciales sensibles
  - Administrador de sistema solo configura conexión con credenciales del usuario restringido

- **Dependencias de seguridad**:
  - `keyring==24.3.1`: Manejo seguro de credenciales en sistemas operativos
  - `pywin32-ctypes==0.2.2`: Backend de Windows para acceso al Credential Manager

### Removed

- **Accesos directos eliminados del instalador**:
  - No se crean íconos en el menú inicio ni escritorio
  - Aplicación diseñada para ejecutarse únicamente desde VB.NET
  - Simplifica el flujo de instalación y evita ejecución accidental directa

- Archivos obsoletos eliminados:
  - `init_database.py` (funcionalidad integrada en `main.py`)
  - `ejemplo_facturas.xlsx` de raíz (ahora se genera dinámicamente)
  - Código duplicado y archivos de prueba antiguos

### Changed (también incluye mejoras previas del 19/oct/2025)

- Eliminación de Tab de configuración; ajustes en módulos requeridos y varias mejoras de optimización y limpieza de código.
  - commit 5ec5bc8 — Eliminación de Tab de configuración, se realizan ajustes en los módulos reqeuridos y se realizan modificaciones varias de optimización y mejora de código. (Ian Dev Villegas, 2025-10-19)
  - Archivos afectados: create_excels.py, database_schema.sql, main.py, main_window.py, plantilla_importacion_servicios.xlsx, test_database_schema.sql

- Correcciones en README, cambios en la estructura del archivo Excel (estilos), y adición de nuevas librerías.
  - commit ed7591db — Se realizan algunas correcciones en el README, cambios en la estructura del archivo de excel con estilos, se agregan nuevas librerías de python, y se realiza una rapida depuración del código. (Ian Dev Villegas, 2025-10-16)
  - Archivos afectados: create_excels.py, ejemplo_facturas.xlsx, main_window.py, plantilla_importacion_servicios.xlsx
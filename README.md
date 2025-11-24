# 🧾 Orión CC Servicios

**Sistema de importación de servicios de facturación desde Excel hacia Orión Plus** - Módulo complementario que permite importar masivamente ítems de cobro por consumo desde archivos Excel a la base de datos de Panorama_net (Orión Plus).

---

## 📥 Descarga e Instalación Rápida

### ⬇️ Descargar Instalador

<div align="center">

**[📦 Descargar ori-cc-servicios-setup.exe v0.2.0](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/latest/download/ori-cc-servicios-setup.exe)**

*Windows 10/11 (64-bit) | ~50 MB*

</div>

### � Instalación en 3 Pasos

1. **Descarga** el instalador desde el botón de arriba.
2. **Ejecuta** `ori-cc-servicios-setup.exe` como **Administrador** (clic derecho > Ejecutar como administrador).
3. **Sigue** las instrucciones del asistente y espera confirmación.
4. **Contacta** a soporte técnico de Orión Plus para:
   - Crear tu usuario en la base de datos MySQL.
   - Configurar el archivo `config.json` con los datos de conexión.

### ✅ Verificación de Instalación

1. Abre **Orión Plus** con tu usuario y contraseña.
2. Navega a: **Cobranza** > **Cobranza Automática** > **Programación de cobros automáticos** > **Importar Cobros por Consumo**.
3. Al abrir el módulo, debe aparecer un **mensaje de conexión exitosa** en el histórico de operaciones.

### ⚠️ Problema Común: SmartScreen de Windows

**Al descargar**, Windows SmartScreen puede mostrar una advertencia como "ori-cc-servicios-setup.exe no se descarga habitualmente" o "Editor desconocido". Esto es normal en aplicaciones sin firma digital (certificado de código).

**Solución rápida**:
- Haz clic en **"Más información"** o **"..."** en la advertencia.
- Selecciona **"Conservar de todos modos"** o **"Ejecutar de todos modos"**.
- Confirma que confías en el archivo.

� **Guía detallada**: [Solución a SmartScreen y VirusTotal](docs/guias/GUÍA_USUARIO_INSTALADOR.md#smartscreen)

---

## 📚 Documentación Adicional

- 📖 **[Guía Completa de Usuario Final](docs/guias/GUÍA_USUARIO_INSTALADOR.md)** - Instrucciones detalladas de instalación, uso y solución de problemas.
- 🛠️ **[Guía de Despliegue](docs/GUIA_DESPLIEGUE.md)** - Para administradores que configuran el entorno de producción.
- 🐛 **[Solución de Problemas (Troubleshooting)](docs/guias/TROUBLESHOOTING.md)** - Errores comunes y cómo resolverlos.
- 🔧 **[Guía para Desarrolladores](#-para-desarrolladores)** - Si quieres modificar o contribuir al código (ver más abajo).

---

## 🐛 Problemas Conocidos (v0.2.0 Beta)

- **SmartScreen/Antivirus**: Algunos antivirus pueden marcar el instalador como sospechoso (falso positivo). Ver [solución arriba](#️-problema-común-smartscreen-de-windows).
- **Configuración MySQL**: El usuario de base de datos debe tener permisos sobre la tabla `oriitemsprogramafact`. Contacta a soporte técnico si hay errores de conexión.

---

## ✨ Características Principales

- 🖥️ **Interfaz gráfica integrada** con Orión Plus (PyQt5).
- 📊 **Importación masiva** desde archivos Excel (`.xlsx`, `.xls`).
- 🔒 **Conexión segura** a MySQL con credenciales en Windows Credential Manager.
- ✅ **Validación automática completa** antes de la importación:
  - 📁 **Validación de archivo**: existencia, formato, tamaño máximo 20MB
  - 📋 **Validación de estructura**: columnas requeridas, datos no vacíos
  - 🔢 **Validación de tipos de datos**: rangos específicos por campo
  - 🔗 **Validación de consistencia**: campos que deben ser iguales en todas las filas
  - 🗄️ **Validación de base de datos**: existencia de IDs en tablas de Orión Plus
  - ⚡ **Validación de lógica**: consumo, lecturas, exclusividad mutua de IDs
- � **Histórico de operaciones** con log detallado.
- 👁️ **Vista previa** de archivos Excel antes de importar.

---

## 🔍 Validaciones Implementadas

La aplicación realiza **6 niveles de validación** antes de importar datos:

### 📁 **1. Validación de Archivo**
- ✅ Archivo existe y es accesible
- ✅ Formato soportado: `.xlsx`, `.xls`, `.xlsm`
- ✅ Tamaño máximo: 20MB
- ✅ Archivo no está vacío

### 📋 **2. Validación de Estructura**
- ✅ Columnas requeridas presentes:
  - `id_carpeta`, `id_servicio`, `id_predio`, `id_tercero_cliente`
  - `periodo_inicio_cobro`, `lectura_anterior`, `lectura_actual`, `valor_unitario`
- ✅ Archivo contiene datos (no solo encabezados)

### 🔢 **3. Validación de Tipos de Datos**
- ✅ **`id_carpeta`**: Entero entre 1-99
- ✅ **`id_servicio`**: Entero entre 1-99
- ✅ **`id_predio`**: Texto (varchar) - exclusivo con `id_tercero_cliente`
- ✅ **`id_tercero_cliente`**: Entero - exclusivo con `id_predio`
- ✅ **`periodo_inicio_cobro`**: Formato AAAAMM (año actual-1 a 2040, mes 01-12)
- ✅ **`valor_unitario`**: Número entre 0-999999
- ✅ **`lectura_anterior/actual`**: Números no negativos

### 🔗 **4. Validación de Consistencia**
- ✅ **`id_carpeta`**: Igual en todas las filas
- ✅ **`id_servicio`**: Igual en todas las filas
- ✅ **`periodo_inicio_cobro`**: Igual en todas las filas
- ✅ **`valor_unitario`**: No nulo/vacío (puede variar)

### 🗄️ **5. Validación de Base de Datos**
- ✅ **`id_carpeta`**: Existe en tabla correspondiente
- ✅ **`id_servicio`**: Existe en tabla correspondiente
- ✅ **`id_predio/id_tercero_cliente`**: Existe en tabla correspondiente

### ⚡ **6. Validación de Lógica de Negocio**
- ✅ **Consumo**: `lectura_actual ≥ lectura_anterior`, máximo 999999
- ✅ **Exclusividad mutua**: Solo uno de `id_predio` o `id_tercero_cliente` por fila
- ✅ **Lecturas**: No negativas, `lectura_actual ≥ lectura_anterior`
- ⚠️ **Advertencias**: Consumo alto (>10000), lectura_anterior = 0

---

## 👨‍💻 Para Desarrolladores

Si quieres **desarrollar, modificar o contribuir** al código fuente:

#### 1️⃣ **Requisitos Previos**

- **Python 3.13+** instalado
- **MySQL Server 5.7+** con la base de datos `panorama_net` ya creada
- **Git** (para clonar el repositorio)
- Acceso a la tabla `oriitemsprogramafact` en MySQL

#### 2️⃣ **Clonar el Proyecto**

```powershell
git clone https://github.com/juandevian/cuenta_de_cobro_servicios.git
cd ori_cc_servicios
```

#### 3️⃣ **Crear Entorno Virtual e Instalar Dependencias**

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

#### 4️⃣ **Configurar Conexión a Base de Datos**

La base de datos **debe existir previamente** con la estructura correcta.

**Opción A - Variables de Entorno** (desarrollo local):

```powershell
# Crear archivo .env en la raíz del proyecto
@"
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=panorama_net
"@ | Out-File -FilePath .env -Encoding utf8
```

**Opción B - config.json + Keyring** (simula producción):

```powershell
# 1. Crear config.json
@"
{
  "host": "localhost",
  "port": 3306,
  "username": "tu_usuario",
  "database": "panorama_net"
}
"@ | Out-File -FilePath config.json -Encoding utf8

# 2. Registrar contraseña en Credential Manager
python -m src.tools.set_db_password
```

#### 5️⃣ **Ejecutar la Aplicación**

```powershell
python -m src.main
```

📖 **Guías adicionales**:
- [`docs/guias/COMENZAR.md`](docs/guias/COMENZAR.md) - Guía detallada para nuevos desarrolladores
- [`docs/guias/TESTING.md`](docs/guias/TESTING.md) - Cómo ejecutar pruebas
- [`docs/guias/TROUBLESHOOTING.md`](docs/guias/TROUBLESHOOTING.md) - Solución de problemas comunes

---

## 📦 Compilación y Distribución

Para generar ejecutables y el instalador de Windows:

### 1️⃣ **Compilar la Aplicación Principal**

```powershell
pyinstaller packaging/ori_cc_servicios.spec --clean
```

Resultado: `dist/ori-cc-servicios/ori-cc-servicios.exe`

### 2️⃣ **Compilar Herramienta de Configuración**

```powershell
pyinstaller packaging/set_password.spec --clean
```

Resultado: `dist/set_password.exe`

### 3️⃣ **Generar Instalador con Inno Setup**

```powershell
# Requiere Inno Setup 6 instalado
iscc packaging/installer.iss
```

Resultado: `Output/ori-cc-servicios-setup.exe`

📖 **Documentación completa**: [`packaging/GUIA_COMPILACION.md`](packaging/GUIA_COMPILACION.md)

---

## 🔐 Verificación de Integridad (Hashes SHA256)

Cada release publica el archivo `RELEASE-<version>-SHA256.txt` con los hashes de los artefactos principales:

```
<SHA256> dist/ori-cc-servicios/ori-cc-servicios.exe
<SHA256> installer/ori-cc-servicios-setup.exe
```

### ✅ Verificación Automática (Windows PowerShell)

Se incluye el script `verify_release_hashes.ps1` que compara los hashes calculados con el archivo publicado.

```powershell
# En la raíz del proyecto (o carpeta donde estén artefactos y archivo de hashes)
pwsh ./verify_release_hashes.ps1 -ReleaseVersion 0.2.0 -HashFile RELEASE-0.2.0-SHA256.txt
```

Salida esperada:
```
OK  dist/ori-cc-servicios/ori-cc-servicios.exe
OK  installer/ori-cc-servicios-setup.exe

Todos los hashes coinciden para release v0.2.0.
```

Código de salida:
- `0`: Todo coincide
- `1`: Algún hash no coincide / falta archivo
- `2`: No se encontró el archivo de hashes

### 🔍 Verificación Manual (Windows sin script)

```powershell
Get-FileHash -Algorithm SHA256 dist\ori-cc-servicios\ori-cc-servicios.exe
Get-FileHash -Algorithm SHA256 installer\ori-cc-servicios-setup.exe
```
Comparar las columnas `Hash` con el contenido de `RELEASE-0.2.0-SHA256.txt`.

### 🐧 Verificación en Linux / macOS

Copiar (SCP / descarga) los artefactos y el archivo de hashes, luego:

```bash
sha256sum dist/ori-cc-servicios/ori-cc-servicios.exe
sha256sum installer/ori-cc-servicios-setup.exe
```
Si se quiere automatizar:
```bash
grep -v '^#' RELEASE-0.2.0-SHA256.txt | while read hash path; do \
  calc=$(sha256sum "$path" | awk '{print $1}'); \
  [ "$calc" = "$hash" ] && echo "OK  $path" || echo "FAIL $path"; \
done
```

### 🌐 Validación en Equipo Remoto (Buenas Prácticas)
1. Descargar ejecutable e instalador desde la página de releases.
2. Descargar también el archivo de hashes correspondiente.
3. Verificar integridad con uno de los métodos anteriores antes de ejecutar.
4. Conservar el archivo de hashes junto al instalador para auditoría futura.

### 🛡️ ¿Por qué Verificar?
Garantiza que:
- No hubo corrupción de descarga.
- No hubo modificación maliciosa intermedia.
- El artefacto corresponde exactamente al release etiquetado.

---

## 🗂️ Estructura del Proyecto

```
ori_cc_servicios/
├── src/                          # Código fuente
│   ├── main.py                   # Punto de entrada
│   ├── config/                   # Gestión de configuración
│   ├── models/                   # Modelos de datos
│   ├── services/                 # Lógica de negocio
│   │   ├── database.py           # Conexión MySQL
│   │   ├── excel_handler.py      # Lectura de Excel
│   │   └── invoice_item_processor.py  # Procesamiento
│   ├── ui/                       # Interfaz gráfica PyQt5
│   └── tools/                    # Herramientas auxiliares
├── packaging/                    # Scripts de compilación
│   ├── ori_cc_servicios.spec     # Spec PyInstaller (app)
│   ├── set_password.spec         # Spec PyInstaller (tool)
│   └── installer.iss             # Script Inno Setup
├── docs/                         # Documentación
│   ├── GUIA_DESPLIEGUE.md        # Guía de instalación
│   ├── setup_mysql_user.sql      # Script SQL para DBA
│   └── guias/                    # Guías adicionales
├── assets/                       # Recursos (SQL, imágenes)
├── tests/                        # Pruebas unitarias
├── requirements.txt              # Dependencias Python
├── config.example.json           # Plantilla de configuración
└── README.md                     # Este archivo
```
---

## 🔐 Seguridad y Buenas Prácticas

### ✅ Usuario MySQL con Privilegios Mínimos

La aplicación se conecta con un usuario que **solo** tiene permisos sobre la tabla `oriitemsprogramafact`:
- `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- **NO** puede modificar estructura ni acceder a otras tablas

📄 Script: [`docs/setup_mysql_user.sql`](docs/setup_mysql_user.sql)

### ✅ Credenciales Fuera del Código

- **Desarrollo**: Variables de entorno (`.env`)
- **Producción**: `config.json` + Windows Credential Manager (Keyring)
- **Nunca** se incluyen contraseñas en archivos versionados

### ✅ Permisos NTFS Restrictivos (Producción)

El instalador configura automáticamente:
- `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\` accesible solo por Administradores/SYSTEM
- Los archivos de configuración no son legibles por usuarios estándar

---

## 🧪 Pruebas

```powershell
# Ejecutar todas las pruebas
pytest

# Con cobertura n
pytest --cov=src --cov-report=html

# Solo un archivo específico
pytest tests/test_database.py
```

---

## 📋 Requisitos del Sistema

### Producción
- **OS**: Windows 10/11 o Windows Server 2016+
- **MySQL**: Server 5.7+ (con base de datos `panorama_net` existente)
- **RAM**: 512 MB mínimo, 1 GB recomendado
- **Disco**: 200 MB para la aplicación

### Desarrollo
- **OS**: Windows, Linux o macOS
- **Python**: 3.13 o superior
- **MySQL**: Server 5.7+ o compatible (MariaDB)
- **Espacio**: 500 MB (incluye dependencias y entorno virtual)

---

## 🤝 Contribuir

1. Crea un branch desde `dev`: `git checkout -b feature/nueva-funcionalidad`
2. Realiza tus cambios y haz commit: `git commit -m "Descripción"`
3. Push al repositorio: `git push origin feature/nueva-funcionalidad`
4. Abre un Pull Request hacia `dev`

---

## 📄 Licencia

Proyecto propietario - OPTIMUSOFT © 2025

---

## 🆘 Soporte

**Problemas comunes**: [`docs/guias/TROUBLESHOOTING.md`](docs/guias/TROUBLESHOOTING.md)

**Documentación completa**: Carpeta [`docs/`](docs/)

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de cambios |
| [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md) | Instalación en producción (paso a paso) |
| [`docs/guias/COMENZAR.md`](docs/guias/COMENZAR.md) | Primeros pasos para desarrolladores |
| [`packaging/GUIA_COMPILACION.md`](packaging/GUIA_COMPILACION.md) | Generar ejecutables e instalador |
| [`docs/setup_mysql_user.sql`](docs/setup_mysql_user.sql) | Script para configurar usuario MySQL |

---

## 🚀 Despliegue en Producción (Resumen)

```
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: DBA - Configurar Usuario MySQL                     │
│ ▸ Ejecutar: docs/setup_mysql_user.sql                      │
│ ▸ Editar contraseña antes de ejecutar                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: Admin Windows - Instalar Aplicación                │
│ ▸ Verificar: C:\ProgramData\OPTIMUSOFT                         │
│ ▸ Ejecutar: ori-cc-servicios-setup.exe                     │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 3: Admin Windows - Configurar                         │
│ ▸ Editar: config.json (host, usuario, BD)                  │
│ ▸ Ejecutar: set_password.exe (registrar contraseña)        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ ✓ LISTO - Ejecutar desde Menú Inicio                       │
└─────────────────────────────────────────────────────────────┘
```

📖 **Documentación completa**: [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md)

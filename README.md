# 🧾 Orión CC Servicios

**Sistema de importación de servicios de facturación desde Excel hacia Orión Plus** - Módulo complementario que permite importar masivamente ítems de cobro por consumo desde archivos Excel a la base de datos de Panorama_net (Orión Plus).

---

## 📥 Descarga e Instalación Rápida

### ⬇️ Descargar Instalador

<div align="center">

**[📦 Descargar ori-cc-servicios-setup.exe v0.1.0 (Beta)](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/latest/download/ori-cc-servicios-setup.exe)**

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

## 🐛 Problemas Conocidos (v0.1.0 Beta)

- **Versión Beta**: Esta es una versión de prueba y puede contener errores menores. Reporta cualquier problema en [Issues](https://github.com/juandevian/cuenta_de_cobro_servicios/issues).
- **Permisos de Administrador**: Asegúrate de ejecutar el instalador como administrador para evitar problemas de permisos.
- **SmartScreen/Antivirus**: Algunos antivirus pueden marcar el instalador como sospechoso (falso positivo). Ver [solución arriba](#️-problema-común-smartscreen-de-windows).
- **Configuración MySQL**: El usuario de base de datos debe tener permisos sobre la tabla `oriitemsprogramafact`. Contacta a soporte técnico si hay errores de conexión.

---

## ✨ Características Principales

- 🖥️ **Interfaz gráfica integrada** con Orión Plus (PyQt5).
- 📊 **Importación masiva** desde archivos Excel (`.xlsx`, `.xls`).
- 🔒 **Conexión segura** a MySQL con credenciales en Windows Credential Manager.
- ✅ **Validación automática** de datos antes de la importación.
- � **Histórico de operaciones** con log detallado.
- 👁️ **Vista previa** de archivos Excel antes de importar.

---

## 👨‍💻 Para Desarrolladores

## 👨‍💻 Para Desarrolladores

Si quieres **desarrollar, modificar o contribuir** al código fuente:

### Para Desarrolladores (Entorno Local)

Si quieres **desarrollar o modificar** la aplicación:

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

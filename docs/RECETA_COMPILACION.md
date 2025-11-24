# 🧑‍💻 Receta de Desarrollo y Compilación - Orión CC Servicios

> Guía completa paso a paso para desarrolladores. Sigue esta "receta" para trabajar en el proyecto, compilar ejecutables y generar instaladores.

**Última actualización**: 22 de octubre de 2025

---

## 📋 Índice

1. [Configuración Inicial del Entorno](#1-configuración-inicial-del-entorno)
2. [Desarrollo Local](#2-desarrollo-local)
3. [Ejecución de la Aplicación](#3-ejecución-de-la-aplicación)
4. [Pruebas](#4-pruebas)
5. [Compilación de Ejecutables](#5-compilación-de-ejecutables)
6. [Generación del Instalador](#6-generación-del-instalador)
7. [Validación Completa](#7-validación-completa)
8. [Solución de Problemas Comunes](#8-solución-de-problemas-comunes)

---

## 1. Configuración Inicial del Entorno

### Pre-requisitos

- **Python 3.10+** instalado
- **Git** instalado
- **MySQL Server** instalado y ejecutándose
- **Inno Setup 6+** instalado (para generar instalador Windows)

### 1.1 Clonar el Repositorio

```bash
git clone https://github.com/juandevian/cuenta_de_cobro_servicios.git
cd cuenta_de_cobro_servicios
```

### 1.2 Crear Entorno Virtual

```powershell
# PowerShell (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Git Bash / Linux
python -m venv .venv
source .venv/bin/activate
```

### 1.3 Instalar Dependencias

```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Instalar en modo editable (desarrollo)
pip install -e .
```

### 1.4 Configurar Variables de Entorno para Desarrollo

#### Opción A: Usando `.env.development` (Recomendado para desarrollo)

```powershell
# Copiar plantilla
Copy-Item .env.example -Destination .env.development

# Editar .env.development
notepad .env.development
```

Contenido de `.env.development`:
```bash
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=tu_password_desarrollo
DB_NAME=panorama_net
LOG_LEVEL=DEBUG
```

#### Opción B: Usando `config.json` (Opcional, simula producción)

```powershell
# Copiar plantilla
Copy-Item config.example.json -Destination config.json

# Editar config.json
notepad config.json
```

Contenido de `config.json`:
```json
{
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "database": "panorama_net"
}
```

Y registrar contraseña en keyring:
```powershell
python -c "import keyring; keyring.set_password('ori-cc-servicios','root','tu_password')"
```

---

## 2. Desarrollo Local

### 2.1 Estructura del Proyecto

```
ori_cc_servicios/
├── .venv/                      # Entorno virtual (no versionar)
├── .env.development            # Variables desarrollo (no versionar)
├── .env.example                # Plantilla de variables (versionar)
├── config.json                 # Config local (no versionar)
├── config.example.json         # Plantilla config (versionar)
├── dev.ps1                     # Script desarrollo PowerShell
├── dev.sh                      # Script desarrollo Bash
├── installer.iss               # Script Inno Setup
├── requirements.txt            # Dependencias Python
├── setup.py                    # Configuración del paquete
├── assets/                     # Recursos (SQL, imágenes)
├── build/                      # Temporales PyInstaller (no versionar)
├── dist/                       # Ejecutables compilados (no versionar)
├── docs/                       # Documentación
├── installer/                  # Instalador generado (no versionar)
├── packaging/                  # Archivos .spec de PyInstaller
│   ├── ori_cc_servicios.spec
│   ├── set_password.spec
│   └── README.md
├── src/                        # Código fuente
│   ├── config/
│   ├── models/
│   ├── services/
│   ├── tools/
│   └── ui/
└── tests/                      # Pruebas unitarias
```

### 2.2 Inicializar Base de Datos (Primera vez)

```powershell
# Conectar a MySQL como root
mysql -u root -p

# Crear base de datos
CREATE DATABASE IF NOT EXISTS panorama_net;

# Ejecutar schema (opcional, la app lo puede hacer)
USE panorama_net;
SOURCE assets/database_schema.sql;
```

---

## 3. Ejecución de la Aplicación

### Opción A: Scripts de Desarrollo (Recomendado)

#### PowerShell (Windows)

```powershell
# Instalar dependencias
.\dev.ps1 -install

# Ejecutar aplicación
.\dev.ps1 -run

# Ejecutar tests
.\dev.ps1 -test

# Ver ayuda
.\dev.ps1
```

#### Git Bash / Linux

```bash
# Dar permisos de ejecución (primera vez)
chmod +x dev.sh

# Instalar dependencias
./dev.sh install

# Ejecutar aplicación
./dev.sh run

# Ejecutar tests
./dev.sh test

# Ver ayuda
./dev.sh
```

### Opción B: Ejecución Manual

```powershell
# Activar entorno virtual (si no está activo)
.\.venv\Scripts\Activate.ps1

# Ejecutar aplicación
python -m src.main

# O con variables de entorno específicas
$env:DB_PASSWORD="mi_password"; python -m src.main
```

---

## 4. Pruebas

### 4.1 Ejecutar Tests Unitarios

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar todos los tests
pytest

# Tests con verbose
pytest -v

# Tests específicos
pytest tests/test_app.py -v

# Con cobertura
pytest --cov=src --cov-report=html
```

### 4.2 Verificar Conexión a Base de Datos

```powershell
python tests/test_mysql_connection.py
```

---

## 5. Compilación de Ejecutables

### 5.1 Pre-compilación

```powershell
# 1. Asegurar que el entorno virtual está activado
.\.venv\Scripts\Activate.ps1

# 2. Verificar que todas las dependencias están instaladas
pip install -r requirements.txt

# 3. Cerrar cualquier instancia de los ejecutables
taskkill /IM ori-cc-servicios.exe /F
taskkill /IM set_password.exe /F
```

### 5.2 Compilar Herramienta de Contraseña

```powershell
# Desde la raíz del proyecto
pyinstaller packaging/set_password.spec --clean
```

**Salida esperada**: `dist/set_password.exe`

**Tiempo estimado**: 1-2 minutos

### 5.3 Compilar Aplicación Principal

```powershell
# Desde la raíz del proyecto
pyinstaller packaging/ori_cc_servicios.spec --clean
```

**Salida esperada**: `dist/ori-cc-servicios/` (carpeta con ejecutable y dependencias)

**Tiempo estimado**: 2-3 minutos

### 5.4 Verificar Compilaciones

```powershell
# Listar salidas
ls dist/

# Debería mostrar:
# - ori-cc-servicios/ (carpeta)
# - set_password.exe (archivo)

# Probar set_password.exe
.\dist\set_password.exe

# Probar aplicación
.\dist\ori-cc-servicios\ori-cc-servicios.exe
```

---

## 6. Generación del Instalador

### 6.1 Pre-requisitos

- **Ejecutables compilados** (Paso 5 completo)
- **Inno Setup** instalado
- Comando `iscc` disponible en PATH

### 6.2 Verificar Archivos Necesarios

```powershell
# Verificar que existen:
Test-Path dist/ori-cc-servicios/ori-cc-servicios.exe
Test-Path dist/set_password.exe
Test-Path config.example.json
Test-Path docs/setup_mysql_user.sql

# Todos deben devolver: True
```

### 6.3 Compilar Instalador

```powershell
# Desde la raíz del proyecto
iscc installer.iss
```

**Salida esperada**: `installer/ori-cc-servicios-setup.exe`

**Tiempo estimado**: 30 segundos

### 6.4 Verificar Instalador Generado

```powershell
# Verificar que existe
Test-Path installer/ori-cc-servicios-setup.exe

# Ver tamaño
Get-Item installer/ori-cc-servicios-setup.exe | Select-Object Name, Length
```

---

## 7. Validación Completa

### 7.1 Validar Instalador (Entorno de Prueba)

#### Pre-requisitos de la Máquina de Prueba

- Windows 10/11 o Windows Server 2016+
- MySQL Server instalado
- Carpeta `C:\ProgramData\OPTIMUSOFT` existente
- Permisos de Administrador

#### Pasos de Validación

1. **Crear directorio base**:
```powershell
New-Item -Path "C:\ProgramData\OPTIMUSOFT" -ItemType Directory -Force
```

2. **Ejecutar instalador**:
```powershell
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs
```

3. **Verificar instalación**:
```powershell
# Verificar archivos instalados
ls "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\"

# Debería mostrar:
# - ori-cc-servicios.exe
# - set_password.exe
# - config.json
# - INSTRUCCIONES_CONFIGURACION.txt
# - docs/setup_mysql_user.sql
```

4. **Configurar aplicación**:

   a. Configurar usuario MySQL (como DBA):
   ```powershell
   # Editar script SQL
   notepad "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\docs\setup_mysql_user.sql"
   
   # Ejecutar en MySQL
   mysql -u root -p < "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\docs\setup_mysql_user.sql"
   ```

   b. Editar config.json:
   ```powershell
   notepad "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\config.json"
   ```

   c. Registrar contraseña:
   ```powershell
   & "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\set_password.exe"
   ```

5. **Ejecutar aplicación**:
```powershell
& "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\ori-cc-servicios.exe"
```

6. **Verificar conexión**:
   - La aplicación debe abrir sin errores
   - Debe conectar a MySQL exitosamente
   - Los logs deben mostrar: "Conexión exitosa a la base de datos MySQL"

### 7.2 Checklist de Validación Completo

Consulta: [`docs/CHECKLIST_VALIDACION.md`](./CHECKLIST_VALIDACION.md)

---

## 8. Solución de Problemas Comunes

### Error: "No se pudo cargar el módulo de credenciales" (set_password.exe)

**Causa**: Falta `keyring` o `pywin32-ctypes` en el ejecutable.

**Solución**:
```powershell
# Reinstalar dependencias
pip install keyring==24.3.1 pywin32-ctypes==0.2.2

# Recompilar
pyinstaller packaging/set_password.spec --clean
```

### Error: "PermissionError: [WinError 5] Acceso denegado" al compilar

**Causa**: El ejecutable está en uso.

**Solución**:
```powershell
# Cerrar procesos
taskkill /IM ori-cc-servicios.exe /F
taskkill /IM set_password.exe /F

# Eliminar ejecutables viejos
Remove-Item dist/set_password.exe -Force -ErrorAction SilentlyContinue

# Recompilar
pyinstaller packaging/set_password.spec --clean
```

### Error: "No such file or directory" al compilar

**Causa**: Ejecutando PyInstaller desde carpeta incorrecta.

**Solución**:
```powershell
# Verificar que estás en la raíz del proyecto
pwd
# Debe mostrar: C:\Users\...\ori_cc_servicios

# Ejecutar desde la raíz
pyinstaller packaging/ori_cc_servicios.spec --clean
```

### Error: "Configuración de base de datos incompleta"

**Causa**: Falta configuración en `.env`, `.env.development` o `config.json`.

**Solución**:
```powershell
# Verificar que existe configuración
Test-Path .env.development
# O
Test-Path config.json

# Si no existe, crear desde ejemplo
Copy-Item .env.example -Destination .env.development
# Editar y agregar credenciales
notepad .env.development
```

### Error: "No se encontró contraseña en keyring"

**Causa**: No se ha registrado la contraseña en Credential Manager.

**Solución**:
```powershell
# Opción 1: Con Python
python -c "import keyring; keyring.set_password('ori-cc-servicios','tu_usuario','tu_password')"

# Opción 2: Con la herramienta
.\dist\set_password.exe
```

### Aplicación no conecta a MySQL

**Verificaciones**:

1. **MySQL corriendo**:
```powershell
Get-Service MySQL* | Where-Object {$_.Status -eq 'Running'}
```

2. **Usuario existe**:
```sql
SELECT User, Host FROM mysql.user WHERE User='ori_app_user';
```

3. **Permisos correctos**:
```sql
SHOW GRANTS FOR 'ori_app_user'@'localhost';
```

4. **Firewall** (si MySQL está en servidor remoto):
```powershell
Test-NetConnection -ComputerName servidor_mysql -Port 3306
```

---

## 📚 Documentación Adicional

- [Guía de Despliegue en Producción](./GUIA_DESPLIEGUE.md)
- [Checklist de Validación](./CHECKLIST_VALIDACION.md)
- [Instrucciones de Compilación (packaging/)](../packaging/README.md)
- [README Principal](../README.md)

---

## 🔄 Flujo Completo de Trabajo

### Para Desarrollo Diario

```powershell
# 1. Activar entorno
.\.venv\Scripts\Activate.ps1

# 2. Actualizar código (git pull, editar archivos, etc.)

# 3. Ejecutar aplicación
.\dev.ps1 -run
# O
python -m src.main

# 4. Ejecutar tests antes de commit
pytest -v

# 5. Commit y push
git add .
git commit -m "Descripción de cambios"
git push
```

### Para Generar Nueva Versión

```powershell
# 1. Actualizar versión en installer.iss
#    Cambiar: #define MyAppVersion "0.2.1"

# 2. Actualizar CHANGELOG.md
notepad CHANGELOG.md

# 3. Compilar ejecutables
pyinstaller packaging/set_password.spec --clean
pyinstaller packaging/ori_cc_servicios.spec --clean

# 4. Generar instalador
iscc installer.iss

# 5. Validar instalador
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs

# 6. Etiquetar versión en Git
git tag v0.2.1
git push --tags
```

---

## 🎯 Comandos Rápidos (Cheat Sheet)

```powershell
# Desarrollo
.\dev.ps1 -install      # Instalar dependencias
.\dev.ps1 -run          # Ejecutar app
.\dev.ps1 -test         # Ejecutar tests

# Compilación
pyinstaller packaging/set_password.spec --clean
pyinstaller packaging/ori_cc_servicios.spec --clean
iscc installer.iss

# Verificación
.\dist\set_password.exe
.\dist\ori-cc-servicios\ori-cc-servicios.exe
Test-Path installer/ori-cc-servicios-setup.exe

# Limpieza
Remove-Item -Recurse -Force build, dist
taskkill /IM ori-cc-servicios.exe /F
taskkill /IM set_password.exe /F

# Git
git status
git add .
git commit -m "mensaje"
git push
```

---

**¿Dudas o problemas?** Consulta la documentación completa o abre un issue en el repositorio.

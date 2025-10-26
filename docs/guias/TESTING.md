# ✅ Guía de Testing - Validación y Verificación

## 1. Validación Pre-Compilación

### Checklist Rápido

```powershell
# Ejecutar antes de compilar
.\Build-Installer.ps1 -BuildMode Validate
```

**Validaciones que verifica:**
- ✅ Inno Setup 6 instalado y en PATH
- ✅ Spanish.isl disponible
- ✅ ori_cc_servicios.spec existe y es válido
- ✅ set_password.spec existe y es válido
- ✅ config.example.json es JSON válido
- ✅ Archivos requeridos presentes
- ✅ Versiones consistentes
- ✅ Permisos de escritura en directorios

---

## 2. Testing de Compilación

### Build Completo con Verificación

```powershell
# Paso 1: Compilar ejecutables
Write-Host "=== Compilando con PyInstaller ===" -ForegroundColor Cyan
pyinstaller packaging/ori_cc_servicios.spec --clean
pyinstaller packaging/set_password.spec --clean

# Verificar que se crearon
$mainExe = "dist\ori-cc-servicios\ori-cc-servicios.exe"
$pwdExe = "dist\set_password.exe"

if (-not (Test-Path $mainExe)) {
    throw "FALLO: $mainExe no encontrado"
}
Write-Host "✓ $mainExe creado ($(((Get-Item $mainExe).Length) / 1MB) MB)" -ForegroundColor Green

if (-not (Test-Path $pwdExe)) {
    throw "FALLO: $pwdExe no encontrado"
}
Write-Host "✓ $pwdExe creado ($(((Get-Item $pwdExe).Length) / 1MB) MB)" -ForegroundColor Green

# Paso 2: Compilar instalador
Write-Host "`n=== Compilando Instalador ===" -ForegroundColor Cyan
.\Build-Installer.ps1 -BuildMode Full

# Verificar que se creó
$installer = "installer\ori-cc-servicios-setup.exe"
if (-not (Test-Path $installer)) {
    throw "FALLO: $installer no encontrado"
}
Write-Host "✓ $installer creado ($(((Get-Item $installer).Length) / 1MB) MB)" -ForegroundColor Green
```

### Testing Modo Rápido

```powershell
# Para desarrollo iterativo
.\Build-Installer.ps1 -BuildMode QuickBuild
```

---

## 3. Testing de Instalación

### Entorno de Testing

**Sistema recomendado:**
- Windows 10/11 64-bit
- 2+ GB RAM
- 500 MB espacio libre
- Conexión MySQL funcional (opcional)

### Pre-Testing: Preparar VM

```powershell
# 1. Crear directorio base (IMPORTANTE)
New-Item -ItemType Directory -Path "C:\ProgramData\OPTIMUSOFT" -Force
New-Item -ItemType Directory -Path "C:\ProgramData\OPTIMUSOFT\Temp" -Force

# 2. Crear usuario MySQL de prueba (si es necesario)
$sqlSetup = @"
CREATE USER 'panorama_usr'@'localhost' IDENTIFIED BY 'prueba123';
GRANT ALL PRIVILEGES ON panorama_net.* TO 'panorama_usr'@'localhost';
FLUSH PRIVILEGES;
"@
$sqlSetup | mysql -u root -p
```

### Prueba 1: Instalación Normal

```powershell
# Ejecutar instalador con interfaz
.\installer\ori-cc-servicios-setup.exe

# Durante la instalación, verificar:
# ✓ Se muestra en español
# ✓ Acepta directorio C:\ProgramData\OPTIMUSOFT\ori-cc-servicios
# ✓ Pregunta credenciales MySQL
# ✓ Crea atajo en Menú Inicio (No debe crear)
# ✓ No hay errores de permiso

# Después de instalar, verificar:
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\ori-cc-servicios.exe"  # True
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\config.json"           # True
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\INSTRUCCIONES_CONFIGURACION.txt"  # True
```

### Prueba 2: Instalación Silenciosa

```powershell
# Instalar sin interfaz
.\installer\ori-cc-servicios-setup.exe /SILENT

# Verificar
Get-Service | Where-Object { $_.Name -like "*ori*" }  # Si hay servicio
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"  # True
```

### Prueba 3: Actualización/Reinstalación

```powershell
# Instalar una primera vez
.\installer\ori-cc-servicios-setup.exe /SILENT

# Instalar nuevamente (simular actualización)
.\installer\ori-cc-servicios-setup.exe /SILENT

# Verificar que config.json se conservó
$config1 = Get-Content "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\config.json"
$config1 | ConvertFrom-Json  # Debe ser válido

# Instalar tercera vez
.\installer\ori-cc-servicios-setup.exe /SILENT

# Verificar que sigue siendo igual
$config2 = Get-Content "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\config.json"
$config1 -eq $config2  # True (no cambió)
```

### Prueba 4: Desinstalación

```powershell
# Desinstalar
.\installer\ori-cc-servicios-setup.exe /UNINSTALL /SILENT

# Verificar que se removió
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"  # False o con archivos de config

# Verificar que se removieron accesos directos
Test-Path "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Ori CC Servicios"  # False
```

---

## 4. Testing de Funcionalidad

### Test 1: Ejecutar Aplicación Principal

```powershell
# Iniciar aplicación
$exe = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\ori-cc-servicios.exe"
Start-Process $exe

# Verificar en Task Manager que el proceso está corriendo
Get-Process | Where-Object { $_.MainWindowTitle -like "*Orión*" }
```

### Test 2: Tool de Cambio de Contraseña

```powershell
# Ejecutar set_password
$pwdExe = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\set_password.exe"
Start-Process $pwdExe

# Debe abrir interfaz para cambiar contraseña
```

### Test 3: Validar config.json

```powershell
$configPath = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\config.json"
$config = Get-Content $configPath | ConvertFrom-Json

# Verificar estructura
$config.host       # Debe existir
$config.port       # Debe ser número
$config.username   # Debe existir
$config.database   # Debe existir

# Verificar conexión MySQL (si está disponible)
$connString = "Server=$($config.host);Port=$($config.port);Uid=$($config.username)"
Write-Host "Conexión: $connString"
```

---

## 5. Testing de Archivos

### Integridad de Archivos Instalados

```powershell
$installDir = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"

# Archivos que DEBEN existir
$requiredFiles = @(
    "ori-cc-servicios.exe",
    "set_password.exe",
    "config.json",
    "config.example.json",
    "INSTRUCCIONES_CONFIGURACION.txt"
)

$requiredFiles | ForEach-Object {
    $file = Join-Path $installDir $_
    if (Test-Path $file) {
        Write-Host "✓ $_" -ForegroundColor Green
    } else {
        Write-Host "✗ $_ FALTA" -ForegroundColor Red
    }
}
```

### Permisos de Archivos

```powershell
$installDir = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"

# Verificar que el usuario actual puede leer/escribir
$acl = Get-Acl $installDir
$acl.Access | Format-Table -AutoSize

# Todos deben poder leer
# Usuario debe poder escribir en config
```

---

## 6. Testing de Reglas de Negocio

### Test 1: Procesamiento de Excel

```powershell
# Crear Excel de prueba con estructura correcta
# Luego procesarlo con la aplicación

# Verificar que:
# ✓ Se detectan todos los ítems
# ✓ Se calculan totales correctamente
# ✓ Se generan informes correctamente
```

### Test 2: Generación de Reportes

```powershell
# En la aplicación:
# 1. Procesar documento
# 2. Generar reporte
# 3. Verificar que Excel se crea correctamente
# 4. Abrir en Excel y verificar fórmulas
```

---

## 7. Performance Testing

### Tamaño de Instalador

```powershell
$installer = "installer\ori-cc-servicios-setup.exe"
$sizeMB = (Get-Item $installer).Length / 1MB
Write-Host "Tamaño: $sizeMB MB"

# Aceptable: 50-100 MB
# Sospechoso: < 30 MB (falta código) o > 150 MB (inflado)
```

### Tiempo de Instalación

```powershell
# Medir tiempo de instalación silenciosa
$startTime = Get-Date
.\installer\ori-cc-servicios-setup.exe /SILENT
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds
Write-Host "Tiempo de instalación: $duration segundos"

# Aceptable: 30-120 segundos
```

### Tiempo de Ejecución

```powershell
# Medir tiempo de inicio de aplicación
$process = Start-Process -FilePath "$installDir\ori-cc-servicios.exe" -PassThru

# Esperar a que esté lista
Start-Sleep -Seconds 5

# Verificar si está respondiendo
if ($process.Responding) {
    Write-Host "✓ Aplicación responsiva en 5 segundos" -ForegroundColor Green
} else {
    Write-Host "✗ Aplicación no responsiva" -ForegroundColor Red
}

$process.Kill()
```

---

## 8. Testing de Compatibilidad

### Windows Compatibility

```powershell
# Obtener versión
$osVersion = [System.Environment]::OSVersion.Version
Write-Host "Windows: $osVersion"

# Debe funcionar en:
# ✓ Windows 7 SP1+
# ✓ Windows 8+
# ✓ Windows 10 (todas las versiones)
# ✓ Windows 11+
```

### Arquitectura

```powershell
# Verificar si es 64-bit
[Environment]::Is64BitOperatingSystem  # True

# Los ejecutables compilados deben ser compatibles
# Usar: pyinstaller --onefile --windowed ori_cc_servicios.spec
```

---

## 9. Script de Testing Automatizado

```powershell
# ============================================
# SCRIPT: Test-Installation.ps1
# ============================================

param(
    [ValidateSet("Validate", "Install", "Execute", "Uninstall", "Full")]
    [string]$TestMode = "Full"
)

function Test-Validation {
    Write-Host "🔍 Ejecutando validación..." -ForegroundColor Cyan
    .\Build-Installer.ps1 -BuildMode Validate
}

function Test-Install {
    Write-Host "📦 Ejecutando instalación..." -ForegroundColor Cyan
    $installer = "installer\ori-cc-servicios-setup.exe"
    if (-not (Test-Path $installer)) {
        throw "Instalador no encontrado"
    }
    Start-Process $installer -Verb RunAs
    Write-Host "⏳ Esperando instalación..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

function Test-Execute {
    Write-Host "▶️ Ejecutando aplicación..." -ForegroundColor Cyan
    $exe = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\ori-cc-servicios.exe"
    Start-Process $exe
    Start-Sleep -Seconds 10
}

function Test-Uninstall {
    Write-Host "🗑️ Desinstalando..." -ForegroundColor Cyan
    $installer = "installer\ori-cc-servicios-setup.exe"
    Start-Process $installer -ArgumentList "/UNINSTALL /SILENT" -Verb RunAs
    Start-Sleep -Seconds 10
}

switch ($TestMode) {
    "Validate" { Test-Validation }
    "Install" { Test-Install }
    "Execute" { Test-Execute }
    "Uninstall" { Test-Uninstall }
    "Full" {
        Test-Validation
        Test-Install
        Test-Execute
        Test-Uninstall
    }
}
```

---

## 10. Matriz de Casos de Prueba

| # | Caso | Pasos | Resultado Esperado | Estado |
|---|------|-------|-------------------|--------|
| 1 | Validación | Ejecutar Validate | Todos checkmarks | ⬜ |
| 2 | Instalación Normal | Ejecutar .exe | Sin errores | ⬜ |
| 3 | Reinstalación | Ejecutar .exe 2 veces | Config conservado | ⬜ |
| 4 | Desinstalación | Ejecutar /UNINSTALL | Directorio removido | ⬜ |
| 5 | App Principal | Ejecutar ori-cc-servicios.exe | Ventana abierta | ⬜ |
| 6 | Set Password | Ejecutar set_password.exe | Diálogo abierto | ⬜ |
| 7 | Config válido | Validar JSON | Sin errores | ⬜ |
| 8 | Permisos | Verificar ACL | Usuario tiene acceso | ⬜ |

---

## 📝 Reportar Resultado de Test

Al completar un ciclo de testing, documentar:

```
Fecha: 2024-XX-XX
Versión: X.X.X
Sistema: Windows 10/11, Python 3.X, Inno Setup 6
Resultados: 
  - Validación: ✓
  - Compilación: ✓
  - Instalación: ✓
  - Funcionalidad: ✓
  - Desinstalación: ✓
Problemas encontrados: Ninguno / [Detallar]
```

---

**Versión**: 0.1.0 | **Última actualización**: Oct 2025

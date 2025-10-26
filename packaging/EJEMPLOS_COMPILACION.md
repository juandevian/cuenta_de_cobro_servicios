# Ejemplos de Compilación - Build-Installer.ps1

## Tabla de Contenidos
1. [Compilación Completa](#compilación-completa)
2. [Solo Validación](#solo-validación)
3. [Compilación Rápida](#compilación-rápida)
4. [Limpieza y Reconstrucción](#limpieza-y-reconstrucción)
5. [Salida Esperada](#salida-esperada)
6. [Troubleshooting](#troubleshooting)

---

## Compilación Completa

Modo recomendado para compilaciones de producción. Ejecuta todas las validaciones + compilación.

### Comando
```powershell
# Modo "Full" - Compilación completa con validaciones
.\Build-Installer.ps1 -BuildMode Full

# O simplemente (Full es el valor por defecto)
.\Build-Installer.ps1
```

### Qué Valida
1. ✅ Inno Setup 6 instalado
2. ✅ Spanish.isl disponible
3. ✅ Archivos requeridos presentes
4. ✅ JSON válido en config.example.json
5. ✅ Versiones consistentes (0.1.0)
6. ✅ Integridad de archivos
7. ✅ Directorio base existe
8. ✅ Compilación exitosa

### Salida Esperada
```
════════════════════════════════════════════════════════════════════
  Build-Installer.ps1 - Orión CC Servicios
                        v0.1.0
════════════════════════════════════════════════════════════════════

ℹ Modo: Full
ℹ Directorio: C:\Users\juanv\dev\work\ori_cc_servicios
ℹ Perfil: DESKTOP\usuario

══════════════════════════════════════════════════════════════════════════
  Validando Instalación de Inno Setup
══════════════════════════════════════════════════════════════════════════
✓ Inno Setup 6 encontrado
✓ Compilador iscc.exe encontrado
✓ Spanish.isl disponible

══════════════════════════════════════════════════════════════════════════
  Validando Archivos Requeridos
══════════════════════════════════════════════════════════════════════════
✓ config.example.json
✓ setup_mysql_user.sql
✓ ori-cc-servicios.exe
✓ set_password.exe
✓ installer.iss

══════════════════════════════════════════════════════════════════════════
  Validando Integridad de Archivos
══════════════════════════════════════════════════════════════════════════
✓ config.example.json es JSON válido
ℹ  Campos: host, port, username, database
✓ Sección [Setup] encontrada
✓ Sección [Files] encontrada
✓ Sección [Code] encontrada
✓ Sección [Languages] encontrada

══════════════════════════════════════════════════════════════════════════
  Validando Directorio Base ProgramData
══════════════════════════════════════════════════════════════════════════
✓ Directorio base existe: C:\ProgramData\OPTIMUSOFT
✓ Permisos verificados

══════════════════════════════════════════════════════════════════════════
  Validando Consistencia de Versiones
══════════════════════════════════════════════════════════════════════════
✓ setup.py: 0.1.0
✓ installer.iss: 0.1.0

══════════════════════════════════════════════════════════════════════════
  Limpiando Archivos Anteriores
══════════════════════════════════════════════════════════════════════════
ℹ Eliminando directorio: C:\installer
✓ Directorio limpiado
✓ Directorio de salida creado

══════════════════════════════════════════════════════════════════════════
  Compilando Instalador Inno Setup
══════════════════════════════════════════════════════════════════════════
ℹ Script: C:\packaging\installer.iss
ℹ Salida: C:\installer

Inno Setup 6 Compiler Copyright (c) 1997-2024
[Compilation successful]

✓ Compilación completada
✓ Instalador generado: ori-cc-servicios-setup.exe
ℹ  Tamaño: 45.23 MB

✓ Tamaño dentro de límites esperados

══════════════════════════════════════════════════════════════════════════
COMPILACIÓN EXITOSA
══════════════════════════════════════════════════════════════════════════
✓ Instalador listo en: C:\installer\ori-cc-servicios-setup.exe
ℹ Siguiente paso: Ejecutar como administrador en máquina destino
```

---

## Solo Validación

Modo para verificar que todo está listo ANTES de compilar. Útil para CI/CD pipelines.

### Comando
```powershell
# Modo "Validate" - Solo validaciones, sin compilar
.\Build-Installer.ps1 -BuildMode Validate
```

### Qué Hace
- Ejecuta todas las validaciones
- NO compila nada
- Reporta estado de cada validación
- Útil para pre-flight checks

### Salida Esperada
```
════════════════════════════════════════════════════════════════════
  Build-Installer.ps1 - Orión CC Servicios
                        v0.1.0
════════════════════════════════════════════════════════════════════

ℹ Modo: Validate
ℹ Directorio: C:\Users\juanv\dev\work\ori_cc_servicios

[... todas las validaciones ...]

══════════════════════════════════════════════════════════════════════════
RESULTADO DE VALIDACIÓN
══════════════════════════════════════════════════════════════════════════
✓ Todas las validaciones pasaron
```

### Casos de Uso
```powershell
# Pre-compilación check
.\Build-Installer.ps1 -BuildMode Validate

# En script de CI/CD
if ($LASTEXITCODE -eq 0) {
    Write-Host "Proceder a compilar"
    .\Build-Installer.ps1 -BuildMode Full
} else {
    Write-Host "Fallos detectados"
    exit 1
}
```

---

## Compilación Rápida

Modo para desarrollo iterativo. Omite validaciones para compilar más rápido.

### Comando
```powershell
# Modo "QuickBuild" - Omite validaciones
.\Build-Installer.ps1 -BuildMode QuickBuild

# O con verbose
.\Build-Installer.ps1 -BuildMode QuickBuild -Verbose
```

### Qué Hace
- Verifica solo existencia de iscc.exe
- Limpia compilaciones anteriores
- Compila inmediatamente
- Reporta resultado

### Salida Esperada
```
════════════════════════════════════════════════════════════════════
  Build-Installer.ps1 - Orión CC Servicios
                        v0.1.0
════════════════════════════════════════════════════════════════════

ℹ Modo: QuickBuild
ℹ Omitiendo validaciones detalladas...

══════════════════════════════════════════════════════════════════════════
  Limpiando Archivos Anteriores
══════════════════════════════════════════════════════════════════════════
ℹ Eliminando directorio: C:\installer
✓ Directorio limpiado
✓ Directorio de salida creado

══════════════════════════════════════════════════════════════════════════
  Compilando Instalador Inno Setup
══════════════════════════════════════════════════════════════════════════

[Compilation successful]

✓ Compilación completada
✓ Instalador generado: ori-cc-servicios-setup.exe
ℹ  Tamaño: 45.23 MB
✓ Tamaño dentro de límites esperados
```

### Casos de Uso
```powershell
# Desarrollo iterativo
.\Build-Installer.ps1 -BuildMode QuickBuild

# Loop de desarrollo
for ($i = 1; $i -le 5; $i++) {
    .\Build-Installer.ps1 -BuildMode QuickBuild
    if ($LASTEXITCODE -ne 0) { break }
}
```

---

## Limpieza y Reconstrucción

Modo para hacer limpieza profunda y reconstruir desde cero.

### Comando
```powershell
# Modo "Clean" - Elimina compilaciones anteriores
.\Build-Installer.ps1 -BuildMode Clean
```

### Qué Hace
1. Elimina directorio `dist/` completo
2. Elimina directorio `installer/` completo
3. Muestra instrucciones para reconstruir

### Salida Esperada
```
════════════════════════════════════════════════════════════════════
  Build-Installer.ps1 - Orión CC Servicios
                        v0.1.0
════════════════════════════════════════════════════════════════════

ℹ Modo: Clean

⚠ Esto eliminará compilaciones anteriores

══════════════════════════════════════════════════════════════════════════
  LIMPIEZA Y RECONSTRUCCIÓN
══════════════════════════════════════════════════════════════════════════

ℹ Limpiando: C:\dist
✓ Directorio limpiado

ℹ Limpiando: C:\installer
✓ Directorio limpiado

ℹ Ahora debe:
ℹ 1. Compilar ejecutables: pyinstaller packaging/ori_cc_servicios.spec
ℹ 2. Ejecutar nuevamente: Build-Installer.ps1 -BuildMode Full
```

### Workflow Completo
```powershell
# 1. Limpiar todo
.\Build-Installer.ps1 -BuildMode Clean

# 2. Recompilar ejecutables de Python
pyinstaller packaging/ori_cc_servicios.spec --clean

# 3. Compilar instalador
.\Build-Installer.ps1 -BuildMode Full

# 4. Resultado
ls installer\ori-cc-servicios-setup.exe
```

---

## Salida Esperada

### Estructura de Directorios Resultante

```
proyecto/
├── installer/
│   └── ori-cc-servicios-setup.exe          ← AQUÍ está el instalador
├── dist/
│   ├── ori-cc-servicios/
│   │   └── ori-cc-servicios.exe
│   └── set_password.exe
├── packaging/
│   ├── installer.iss
│   ├── Build-Installer.ps1
│   └── ...
└── ...
```

### Información del Archivo

```powershell
# Verificar archivo generado
$setupFile = "installer\ori-cc-servicios-setup.exe"
$file = Get-Item $setupFile

Write-Host "Información del instalador:"
Write-Host "  Nombre: $($file.Name)"
Write-Host "  Ruta: $($file.FullName)"
Write-Host "  Tamaño: $([Math]::Round($file.Length / 1MB, 2)) MB"
Write-Host "  Creado: $($file.CreationTime)"
Write-Host "  Modificado: $($file.LastWriteTime)"
```

---

## Troubleshooting

### Problema 1: "iscc.exe no encontrado"

```powershell
# Error
✗ iscc.exe no encontrado

# Solución
$innoPath = "C:\Program Files (x86)\Inno Setup 6"
$isccExe = Join-Path $innoPath "iscc.exe"
if (Test-Path $isccExe) {
    Write-Host "✓ iscc.exe encontrado en: $isccExe"
} else {
    Write-Host "Instalar Inno Setup desde: https://www.innosetup.com"
}
```

### Problema 2: "Permisos insuficientes"

```powershell
# Error
Access denied: C:\ProgramData\OPTIMUSOFT

# Solución: Ejecutar como administrador
# PowerShell > Menú Inicio > Click derecho > "Ejecutar como administrador"

# O mediante comando
Start-Process powershell -Verb RunAs
.\Build-Installer.ps1 -BuildMode Full
```

### Problema 3: "config.example.json es JSON inválido"

```powershell
# Error
✗ config.example.json es JSON inválido

# Solución: Verificar sintaxis
$config = Get-Content "config.example.json" | ConvertFrom-Json

# Ejemplo de config válida
@{
    host = "localhost"
    port = 3306
    username = "mi_usuario"
    database = "panorama_net"
} | ConvertTo-Json | Out-File "config.example.json"
```

### Problema 4: "Archivos requeridos incompletos"

```powershell
# Error
✗ FALTA: ori-cc-servicios.exe

# Solución: Compilar ejecutables primero
pyinstaller packaging/ori_cc_servicios.spec --clean
pyinstaller packaging/set_password.spec --clean

# Verificar
Test-Path "dist\ori-cc-servicios\ori-cc-servicios.exe"  # Debe ser True
Test-Path "dist\set_password.exe"                        # Debe ser True
```

### Problema 5: Compilación sale antes de completar

```powershell
# Verificar exit code del último comando
Write-Host "Exit code: $LASTEXITCODE"

# 0 = exitoso
# 1 = error

# Para capturar error:
try {
    .\Build-Installer.ps1 -BuildMode Full
    if ($LASTEXITCODE -ne 0) {
        throw "Compilación fallida"
    }
} catch {
    Write-Host "Error: $_"
}
```

---

## Ejemplos Avanzados

### Script de Compilación Automática

```powershell
# script-compilacion-auto.ps1
# Compila automáticamente cada vez que cambian los archivos

$rootDir = (Get-Location).Path
$packagingDir = Join-Path $rootDir "packaging"

# Monitorear cambios
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $packagingDir
$watcher.Filter = "installer.iss"
$watcher.IncludeSubdirectories = $false

$action = {
    Write-Host "Cambio detectado - recompilando..."
    & "$packagingDir\Build-Installer.ps1" -BuildMode Quick
}

Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action

Write-Host "Monitorando cambios en: $packagingDir"
Write-Host "Presiona Ctrl+C para salir..."

# Mantener script ejecutando
while ($true) { Start-Sleep -Seconds 1 }
```

### CI/CD Pipeline

```powershell
# build-pipeline.ps1
# Ejecutar en GitHub Actions, Azure Pipelines, etc.

param([string]$BuildMode = "Full")

Write-Host "════════════════════════════════════════"
Write-Host "Pipeline de Compilación - Orión CC"
Write-Host "════════════════════════════════════════"

# 1. Validar
Write-Host "`n[1/4] Validando..."
.\packaging\Build-Installer.ps1 -BuildMode Validate
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Compilar ejecutables
Write-Host "`n[2/4] Compilando ejecutables..."
pyinstaller packaging/ori_cc_servicios.spec --clean
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. Compilar instalador
Write-Host "`n[3/4] Compilando instalador..."
.\packaging\Build-Installer.ps1 -BuildMode Full
if ($LASTEXITCODE -ne 0) { exit 1 }

# 4. Crear artefacto
Write-Host "`n[4/4] Preparando artefacto..."
$setupFile = "installer\ori-cc-servicios-setup.exe"
if (Test-Path $setupFile) {
    Write-Host "✓ Pipeline exitoso"
    Write-Host "Artefacto: $setupFile"
    exit 0
} else {
    Write-Host "✗ Pipeline fallido"
    exit 1
}
```

### Testing Automático

```powershell
# test-instalador.ps1
# Validar instalador en máquina de pruebas

param(
    [string]$InstallerPath = "installer\ori-cc-servicios-setup.exe"
)

Write-Host "Iniciando testing del instalador..."

# 1. Verificar archivo existe
if (-not (Test-Path $InstallerPath)) {
    Write-Host "✗ Instalador no encontrado: $InstallerPath"
    exit 1
}
Write-Host "✓ Instalador encontrado"

# 2. Verificar tamaño
$size = (Get-Item $InstallerPath).Length / 1MB
if ($size -lt 20 -or $size -gt 150) {
    Write-Host "✗ Tamaño sospechoso: $size MB"
    exit 1
}
Write-Host "✓ Tamaño válido: $size MB"

# 3. Ejecutar instalador
Write-Host "ℹ Iniciando instalación de prueba..."
Start-Process $InstallerPath

# 4. Esperar completación
Start-Sleep -Seconds 30

# 5. Validar instalación
$appDir = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"
if (Test-Path $appDir) {
    Write-Host "✓ Instalación exitosa"
    Write-Host "  Directorio: $appDir"
    exit 0
} else {
    Write-Host "✗ Instalación fallida"
    exit 1
}
```

---

## Mejores Prácticas

```powershell
# ✅ HACER
.\Build-Installer.ps1 -BuildMode Full              # Completo
.\Build-Installer.ps1 -BuildMode Validate          # Pre-check
.\Build-Installer.ps1 -BuildMode QuickBuild        # Desarrollo

# ❌ NO HACER
.\Build-Installer.ps1 -BuildMode full              # Sensible a casos
"C:\iscc.exe" installer.iss                        # Evitar llamadas directas
cd packaging; iscc.exe installer.iss               # Evitar rutas hardcodeadas
```

---

**Versión**: 0.1.0  
**Actualizado**: Octubre 2025

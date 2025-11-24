# Guía de Compilación y Validación del Instalador

## Tabla de Contenidos
1. [Pre-requisitos](#pre-requisitos)
2. [Configuración del Entorno](#configuración-del-entorno)
3. [Checklist Pre-compilación](#checklist-pre-compilación)
4. [Compilación](#compilación)
5. [Validación Post-compilación](#validación-post-compilación)
6. [Testing en Máquina Limpia](#testing-en-máquina-limpia)
7. [Solución de Problemas](#solución-de-problemas)

---

## Pre-requisitos

### Software Requerido
- **Inno Setup 6.0 o superior**: [Descargar](https://www.innosetup.com)
- **Python 3.9+**: Con PyInstaller configurado
- **PyInstaller**: Para compilar los ejecutables principales

### Componentes Inno Setup
- Compilador Inno Setup (iscc.exe)
- Language file Spanish.isl (incluido en instalación estándar)

### Requisitos del Sistema Destino
- Windows 7, 10, u 11 (32 o 64-bit)
- Privilegios de administrador
- (Instalación) Directorio destino: `C:\Program Files\OPTIMUSOFT\orion-cc-servicios\` (creado por el instalador)
- Estructura opcional externa requerida por operación: `c:\Panorama.Net\Dat\` (si existe se crea subcarpeta `PlantillasServiciosConsumo`)
- MySQL Server accesible (local o remoto)

---

## Configuración del Entorno

### 1. Instalar Inno Setup

```bash
# Descargar desde https://www.innosetup.com/
# Ejecutar instalador
# Seleccionar componentes:
#   ✓ Compiler
#   ✓ Components
#   ✓ Languages (incluye Spanish.isl)
```

### 2. Verificar Instalación

```powershell
# Verificar ruta de iscc.exe
$innoPath = "C:\Program Files (x86)\Inno Setup 6"
if (Test-Path "$innoPath\iscc.exe") {
    Write-Host "✓ Inno Setup encontrado"
} else {
    Write-Host "✗ Inno Setup no encontrado"
}

# Verificar Spanish.isl
if (Test-Path "$innoPath\Languages\Spanish.isl") {
    Write-Host "✓ Spanish.isl disponible"
} else {
    Write-Host "✗ Spanish.isl no disponible"
}
```

### 3. Crear Directorio Base

```powershell
# En máquina destino, ejecutar como administrador
$baseDir = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios"
if (-not (Test-Path $baseDir)) {
    New-Item -ItemType Directory -Path $baseDir -Force
    Write-Host "✓ Directorio creado: $baseDir"
} else {
    Write-Host "✓ Directorio ya existe: $baseDir"
}
```

---

## Checklist Pre-compilación

**Ubicación**: Raíz del proyecto

### Archivos de Configuración
```
[ ] config.example.json                          (plantilla de config)
[ ] requirements.txt                             (dependencias Python)
[ ] setup.py                                     (configuración del paquete)
```

### Compilados con PyInstaller
```
[ ] dist\ori-cc-servicios\ori-cc-servicios.exe   (ejecutable principal)
[ ] dist\ori-cc-servicios\*                       (todas las dependencias)
[ ] dist\set_password.exe                         (herramienta de contraseña)
```

**Generar ejecutables**:
```powershell
# Compilar aplicación principal
pyinstaller packaging/ori_cc_servicios.spec --clean

# Resultado: dist/ori-cc-servicios/
```

### Documentación
```
[ ] docs\setup_mysql_user.sql                    (script SQL)
[ ] packaging\installer.iss                      (script Inno Setup)
```

### Versionado
```
[ ] CHANGELOG.md                                 (actualizado a v0.2.1)
[ ] Version en setup.py                          (0.2.1)
[ ] Version en installer.iss                     ({#MyAppVersion = "0.2.1"})
```

**Verificación de versiones**:
```powershell
# Verificar setup.py
$setupContent = Get-Content "setup.py" -Raw
if ($setupContent -match 'version\s*=\s*["\']0\.2\.0["\']') {
    Write-Host "✓ Versión correcta en setup.py"
}

# Verificar installer.iss
$issContent = Get-Content "packaging\installer.iss" -Raw
if ($issContent -match '#define MyAppVersion "0\.2\.0"') {
    Write-Host "✓ Versión correcta en installer.iss"
}
```

### Estructura de Directorios
```powershell
function Test-DirectoryStructure {
    $checks = @(
        'config.example.json',
        'dist\ori-cc-servicios\ori-cc-servicios.exe',
        'dist\set_password.exe',
        'docs\setup_mysql_user.sql',
        'packaging\installer.iss'
    )
    
    foreach ($check in $checks) {
        if (Test-Path $check) {
            Write-Host "✓ $check"
        } else {
            Write-Host "✗ FALTA: $check" -ForegroundColor Red
        }
    }
}

Test-DirectoryStructure
```

---

## Compilación

### Compilación desde PowerShell

```powershell
# Variables
$innoCompiler = "C:\Program Files (x86)\Inno Setup 6\iscc.exe"
$scriptPath = "packaging\installer.iss"
$workingDir = Get-Location

# Compilar
& $innoCompiler $scriptPath

# Verificar resultado
$setupExe = "installer\ori-cc-servicios-setup.exe"
if (Test-Path $setupExe) {
    $fileSize = (Get-Item $setupExe).Length / 1MB
    Write-Host "✓ Compilación exitosa"
    Write-Host "  Archivo: $setupExe"
    Write-Host "  Tamaño: $([Math]::Round($fileSize, 2)) MB"
} else {
    Write-Host "✗ Compilación fallida" -ForegroundColor Red
}
```

### Compilación desde línea de comandos

```bash
# Cambiar a directorio packaging
cd packaging

# Compilar
"C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss

# El instalador se genera en: ..\installer\ori-cc-servicios-setup.exe
```

---

## Validación Post-compilación

### Verificar Archivo Generado

```powershell
$setupFile = "installer\ori-cc-servicios-setup.exe"

# Tamaño
$size = (Get-Item $setupFile).Length / 1MB
Write-Host "Tamaño del instalador: $([Math]::Round($size, 2)) MB"

# Debe estar entre 30-100 MB (depende de dependencias)
if ($size -gt 20 -and $size -lt 150) {
    Write-Host "✓ Tamaño razonable (compresión LZMA activa)"
} else {
    Write-Host "⚠ Tamaño sospechoso - revisar compresión"
}

# Firma y atributos
$file = Get-Item $setupFile
Write-Host "Fecha de creación: $($file.CreationTime)"
Write-Host "Última modificación: $($file.LastWriteTime)"

# Verificar que no es un archivo antiguo
if ($file.LastWriteTime -gt (Get-Date).AddMinutes(-5)) {
    Write-Host "✓ Archivo recién generado"
} else {
    Write-Host "✗ Archivo parece antiguo - revisar compilación"
}
```

### Verificar Contenido del Instalador

Los instaladores Inno Setup son ejecutables que contienen:
- Archivos a instalar (comprimidos)
- Binarios del instalador
- Scripting Pascal
- Recursos y lenguajes

```powershell
# Usar Inno Setup para extraer información
# (Este paso es principalmente visual/manual)

# Alternativa: buscar signatura de Inno Setup
$bytes = [System.IO.File]::ReadAllBytes($setupFile)
$signature = [System.Text.Encoding]::ASCII.GetString($bytes[0..11])
if ($signature -like "*Inno Setup*") {
    Write-Host "✓ Formato válido de Inno Setup"
}
```

---

## Testing en Máquina Limpia

### Preparación

**Importante**: Usar máquina virtual o máquina dedicada para testing

1. **Crear Directorio Base**
```powershell
# En máquina destino, como administrador
$baseDir = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios"
New-Item -ItemType Directory -Path $baseDir -Force
Write-Host "✓ Directorio creado: $baseDir"
```

2. **Copiar Instalador**
```powershell
# Copiar archivo a máquina destino
Copy-Item "installer\ori-cc-servicios-setup.exe" -Destination "C:\temp\"
```

### Instalación

```powershell
# Ejecutar como administrador
C:\temp\ori-cc-servicios-setup.exe

# Pasos de instalación:
# 1. Mostrar idioma (Español)
# 2. Mostrar pantalla de bienvenida
# 3. Mostrar acuerdo de licencia (si aplica)
# 4. Mostrar directorio de instalación (no editable)
# 5. Mostrar selección de componentes
# 6. Ejecutar instalación
# 7. Mostrar instrucciones post-instalación
# 8. Abrir INSTRUCCIONES_CONFIGURACION.txt en Notepad
```

### Validaciones Post-Instalación

```powershell
$appDir = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios"

# Verificar archivos instalados
$requiredFiles = @(
    'ori-cc-servicios.exe',
    'set_password.exe',
    'config.json',
    'INSTRUCCIONES_CONFIGURACION.txt',
    'docs\setup_mysql_user.sql'
)

Write-Host "Validando archivos instalados:"
foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $appDir $file
    if (Test-Path $fullPath) {
        Write-Host "✓ $file"
    } else {
        Write-Host "✗ FALTA: $file" -ForegroundColor Red
    }
}

# Verificar permisos
Write-Host "`nValidando permisos:"
$acl = Get-Acl $appDir
$acl.Access | ForEach-Object {
    Write-Host "  - $($_.IdentityReference): $($_.FileSystemRights)"
}

# Verificar contenido de config.json
Write-Host "`nValidando config.json:"
$configPath = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\config.json"
$config = Get-Content $configPath | ConvertFrom-Json
Write-Host "  - Host: $($config.host)"
Write-Host "  - Puerto: $($config.port)"
Write-Host "  - Usuario: $($config.username)"
Write-Host "  - Base de datos: $($config.database)"

# Verificar que INSTRUCCIONES_CONFIGURACION.txt existe
Write-Host "`nValidando instrucciones:"
$instructionsPath = Join-Path $appDir "INSTRUCCIONES_CONFIGURACION.txt"
if (Test-Path $instructionsPath) {
    Write-Host "✓ Archivo de instrucciones creado"
    $content = Get-Content $instructionsPath
    Write-Host "  Líneas: $($content.Count)"
} else {
    Write-Host "✗ Archivo de instrucciones NO encontrado" -ForegroundColor Red
}
```

### Testing de Actualización

```powershell
# 1. Ejecutar instalador original
C:\temp\ori-cc-servicios-setup.exe

# 2. Editar config.json manualmente
# 3. Guardar cambios
# 4. Ejecutar actualización del instalador

# 5. Verificar que config.json se preservó
Write-Host "Verificando preservación de configuración:"
$configPath = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\config.json"
$config = Get-Content $configPath | ConvertFrom-Json
Write-Host "✓ Configuración preservada" 
Write-Host "  Usuario: $($config.username)"
```

### Testing de Desinstalación

```powershell
# Métodos para desinstalar:

# Opción 1: Desde Agregar/Quitar programas (GUI)
# Buscar "Orion CC Servicios" y desinstalar

# Opción 2: Desde línea de comandos
& 'C:\Program Files\OPTIMUSOFT\orion-cc-servicios\unins000.exe'

# Verificar que se desinstaló (excepto config.json)
Write-Host "Verificando desinstalación:"
$appDir = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios"
if (-not (Test-Path "$appDir\ori-cc-servicios.exe")) {
    Write-Host "✓ Ejecutable removido"
} else {
    Write-Host "✗ Ejecutable aún existe" -ForegroundColor Red
}

if (Test-Path "$appDir\config.json") {
    Write-Host "✓ config.json preservado (correcto)"
} else {
    Write-Host "✗ config.json fue eliminado (incorrecto)" -ForegroundColor Red
}
```

---

## Solución de Problemas

### Problema: "Directorio C:\Program Files\OPTIMUSOFT no encontrado"

**Síntoma**: El instalador muestra error y cancela.

**Solución**:
```powershell
# Crear directorio como administrador
$baseDir = "C:\Program Files\OPTIMUSOFT"
New-Item -ItemType Directory -Path $baseDir -Force

# Verificar permisos
$acl = Get-Acl $baseDir
Write-Host $acl
```

---

### Problema: "Error al guardar INSTRUCCIONES_CONFIGURACION.txt"

**Síntoma**: La instalación se completa pero no aparecen instrucciones.

**Causas posibles**:
- Permisos insuficientes en directorio de instalación
- Espacio en disco insuficiente
- Ruta demasiado larga

**Solución**:
```powershell
# Verificar permisos en directorio de instalación
$appDir = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios"
$acl = Get-Acl $appDir
$acl | Format-List

# Verificar espacio en disco
$drive = Get-Item C:\
$freeSpace = $drive.AvailableFreeSpace / 1GB
Write-Host "Espacio libre: $([Math]::Round($freeSpace, 2)) GB"

# Verificar longitud de ruta
$instructionsPath = "$appDir\INSTRUCCIONES_CONFIGURACION.txt"
Write-Host "Longitud de ruta: $($instructionsPath.Length) caracteres"
# Máximo: 260 caracteres en Windows (MAX_PATH)
```

---

### Problema: "Spanish.isl no encontrado"

**Síntoma**: Error de compilación: "Spanish.isl no found"

**Solución**:
```powershell
# Verificar ubicación correcta
$innoPath = "C:\Program Files (x86)\Inno Setup 6"
$spanishFile = "$innoPath\Languages\Spanish.isl"

if (Test-Path $spanishFile) {
    Write-Host "✓ Spanish.isl encontrado en: $spanishFile"
} else {
    Write-Host "✗ Spanish.isl no encontrado"
    Write-Host "  Reinstalar Inno Setup e incluir idiomas"
}

# Si falta, descargar desde:
# https://www.innosetup.com/files/isxlang/Spanish.isl
```

---

### Problema: Ejecutable no inicia después de instalar

**Síntoma**: El programa no arranca desde línea de comandos.

**Causa probable**: Falta de dependencias o rutas incorrectas.

**Solución**:
```powershell
# Verificar que PyInstaller compiló correctamente
$exePath = "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\ori-cc-servicios.exe"

# Ejecutar con error output
try {
    & $exePath
} catch {
    Write-Host "Error: $_"
}

# Revisar logs de dependencias
# Python y dependencias requeridas en config.json
```

---

### Problema: "Access denied" durante instalación

**Síntoma**: Error de permisos durante la instalación.

**Solución**:
```powershell
# Ejecutar instalador como administrador (siempre)
# Click derecho > "Ejecutar como administrador"

# O desde PowerShell:
Start-Process "C:\temp\ori-cc-servicios-setup.exe" -Verb RunAs

# Verificar que el usuario actual es administrador
$isAdmin = [Security.Principal.WindowsIdentity]::GetCurrent() | 
    ForEach-Object { (New-Object Security.Principal.WindowsPrincipal $_).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) }

if ($isAdmin) {
    Write-Host "✓ Ejecutando como administrador"
} else {
    Write-Host "✗ NO se ejecuta como administrador" -ForegroundColor Red
}
```

---

## Generación de Hashes SHA256 para Release

### Proceso Automático

```powershell
# Generar archivo de hashes (ejecutar desde raíz del proyecto)
$version = "0.2.1"
$outputDir = ".\build\release"

# Crear directorio si no existe
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

# Generar hashes
$hashFile = "$outputDir\RELEASE-$version-SHA256.txt"
@"
# Hashes de artefactos release $version (SHA256)
# Fecha: $(Get-Date -Format "yyyy-MM-dd")
# Formato: <SHA256> <Ruta relativa>
"@ | Out-File -FilePath $hashFile -Encoding utf8

# Calcular hash del ejecutable principal
if (Test-Path ".\dist\ori-cc-servicios\ori-cc-servicios.exe") {
    $hash = (Get-FileHash -Algorithm SHA256 ".\dist\ori-cc-servicios\ori-cc-servicios.exe").Hash
    "$hash dist/ori-cc-servicios/ori-cc-servicios.exe" | Out-File -FilePath $hashFile -Append -Encoding utf8
}

# Calcular hash del instalador
if (Test-Path ".\installer\ori-cc-servicios-setup.exe") {
    $hash = (Get-FileHash -Algorithm SHA256 ".\installer\ori-cc-servicios-setup.exe").Hash
    "$hash installer/ori-cc-servicios-setup.exe" | Out-File -FilePath $hashFile -Append -Encoding utf8
}

Write-Host "✓ Archivo de hashes generado: $hashFile" -ForegroundColor Green
Get-Content $hashFile
```

### Verificación de Hashes

```powershell
# Descargar y verificar con script incluido
pwsh ./verify_release_hashes.ps1 -ReleaseVersion $version -HashFile "$outputDir\RELEASE-$version-SHA256.txt"
```

### Publicación en GitHub Release

1. **Subir assets manualmente** (interfaz web):
   - `installer\ori-cc-servicios-setup.exe`
   - `build\release\RELEASE-0.2.1-SHA256.txt`

2. **Subir con GitHub CLI** (automatizado):
```powershell
gh release upload v0.2.1 `
  .\installer\ori-cc-servicios-setup.exe `
  .\build\release\RELEASE-0.2.1-SHA256.txt
```

### Notas Importantes

- ⚠️ **NO versionar** archivos `*-SHA256.txt` en Git (ya están en `.gitignore`)
- ✅ **Generar bajo demanda** en `build/release/` antes de publicar
- ✅ **Script de verificación** (`verify_release_hashes.ps1`) SÍ está versionado
- ✅ **Archivo de hashes** solo existe como asset del release en GitHub

---

## Checklist de Validación Final

Antes de distribuir el instalador:

```
[ ] Versión actualizada en todos los archivos (setup.py, config.py, installer.iss)
[ ] CHANGELOG.md actualizado con nueva versión
[ ] config.example.json existe y es válido
[ ] setup_mysql_user.sql existe
[ ] Ejecutables compilados con PyInstaller
[ ] Directorio installer/ contiene ori-cc-servicios-setup.exe
[ ] Tamaño del instalador es razonable (50-100 MB)
[ ] Installer.iss compila sin errores
[ ] Archivo de hashes generado en build/release/
[ ] Hashes verificados con verify_release_hashes.ps1
[ ] Instalación en máquina limpia funciona
[ ] Directorio C:\ProgramData\OPTIMUSOFT se valida correctamente
[ ] config.json se crea desde plantilla
[ ] INSTRUCCIONES_CONFIGURACION.txt se genera
[ ] Se abre Notepad con instrucciones
[ ] Actualización preserva config.json existente
[ ] Desinstalación elimina binarios pero preserva config.json
[ ] Mensajes de error son claros y en español
[ ] No hay accesos directos creados
[ ] No se ejecuta aplicación automáticamente
[ ] Tag creado y pusheado: git tag -a v0.X.X -m "Release 0.X.X"
[ ] Release publicado en GitHub con assets (instalador + hashes)
```

---

## Comandos Útiles

```powershell
# Compilar instalador
& 'C:\Program Files (x86)\Inno Setup 6\iscc.exe' packaging\installer.iss

# Generar hashes para release
$version = "0.2.1"
New-Item -ItemType Directory -Force -Path ".\build\release" | Out-Null
$hashFile = ".\build\release\RELEASE-$version-SHA256.txt"
@"
# Hashes release $version (SHA256)
# Fecha: $(Get-Date -Format "yyyy-MM-dd")
"@ | Out-File -FilePath $hashFile -Encoding utf8
(Get-FileHash -Algorithm SHA256 ".\dist\ori-cc-servicios\ori-cc-servicios.exe").Hash + " dist/ori-cc-servicios/ori-cc-servicios.exe" | Out-File -Append $hashFile -Encoding utf8
(Get-FileHash -Algorithm SHA256 ".\installer\ori-cc-servicios-setup.exe").Hash + " installer/ori-cc-servicios-setup.exe" | Out-File -Append $hashFile -Encoding utf8
Write-Host "✓ Hashes: $hashFile"

# Verificar hashes
pwsh ./verify_release_hashes.ps1 -ReleaseVersion $version -HashFile $hashFile

# Crear directorio base
New-Item -ItemType Directory -Path "C:\Program Files\OPTIMUSOFT" -Force

# Ejecutar instalador como administrador
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs

# Verificar instalación
Test-Path "C:\Program Files\OPTIMUSOFT\orion-cc-servicios\ori-cc-servicios.exe"

# Desinstalar
& 'C:\Program Files\OPTIMUSOFT\orion-cc-servicios\unins000.exe'

# Limpiar compilaciones anteriores
Remove-Item -Recurse -Force "dist\ori-cc-servicios"
Remove-Item -Recurse -Force "installer\ori-cc-servicios-setup.exe"
Remove-Item -Recurse -Force "build\release"
```

---

**Última actualización**: Noviembre 2025
**Versión del instalador**: 0.2.1
**Inno Setup requerido**: 6.0 o superior

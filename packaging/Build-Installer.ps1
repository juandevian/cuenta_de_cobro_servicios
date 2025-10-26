# ============================================================================
# Build-Installer.ps1
# ============================================================================
# Script profesional de compilación del instalador Inno Setup
# Orión CC Servicios
# 
# Uso:
#   .\Build-Installer.ps1 -BuildMode "Full"          # Compilación completa
#   .\Build-Installer.ps1 -BuildMode "Validate"      # Solo validar
#   .\Build-Installer.ps1 -BuildMode "Clean"         # Limpiar y reconstruir
# 
# Requisitos:
#   - PowerShell 5.0+
#   - Inno Setup 6.0+ instalado
#   - Ejecutar como administrador (recomendado)
# ============================================================================

param(
    [ValidateSet("Full", "Validate", "Clean", "QuickBuild")]
    [string]$BuildMode = "Full",
    
    [switch]$SkipValidation,
    [switch]$Verbose
)

# ============================================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================================

$ErrorActionPreference = "Stop"
$WarningPreference = "Continue"

# Rutas importantes
$projectRoot = (Get-Item $PSScriptRoot).Parent.FullName
$packagingDir = Join-Path $projectRoot "packaging"
$installerScript = Join-Path $packagingDir "installer.iss"
$installerOutput = Join-Path $projectRoot "installer"
$distDir = Join-Path $projectRoot "dist"

# Inno Setup
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6"
$isccExe = Join-Path $innoSetupPath "iscc.exe"
$spanishFile = Join-Path $innoSetupPath "Languages\Spanish.isl"

# Archivos requeridos
$requiredFiles = @(
    (Join-Path $projectRoot "config.example.json"),
    (Join-Path $projectRoot "docs\setup_mysql_user.sql"),
    (Join-Path $distDir "ori-cc-servicios\ori-cc-servicios.exe"),
    (Join-Path $distDir "set_password.exe"),
    $installerScript
)

# ============================================================================
# FUNCIONES UTILITARIAS
# ============================================================================

function Write-Header {
    param([string]$Message)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "=" * 70 -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

# ============================================================================
# VALIDACIÓN DEL ENTORNO
# ============================================================================

function Test-InnoSetupInstallation {
    Write-Header "Validando Instalación de Inno Setup"
    
    # Verificar ruta de Inno Setup
    if (-not (Test-Path $innoSetupPath)) {
        Write-Error "Inno Setup 6 no encontrado en: $innoSetupPath"
        Write-Info "Descargar desde: https://www.innosetup.com"
        return $false
    }
    Write-Success "Inno Setup 6 encontrado"
    
    # Verificar iscc.exe
    if (-not (Test-Path $isccExe)) {
        Write-Error "Compilador iscc.exe no encontrado"
        return $false
    }
    Write-Success "Compilador iscc.exe encontrado"
    
    # Verificar Spanish.isl
    if (-not (Test-Path $spanishFile)) {
        Write-Error "Archivo de idioma Spanish.isl no encontrado"
        Write-Warning "Reinstalar Inno Setup e incluir paquete de idiomas"
        return $false
    }
    Write-Success "Spanish.isl disponible"
    
    return $true
}

function Test-RequiredFiles {
    Write-Header "Validando Archivos Requeridos"
    
    $allValid = $true
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Success (Split-Path $file -Leaf)
        } else {
            Write-Error "FALTA: $(Split-Path $file -Leaf)"
            Write-Info "  Ruta esperada: $file"
            $allValid = $false
        }
    }
    
    return $allValid
}

function Test-ProgramDataDirectory {
    Write-Header "Validando Directorio Base ProgramData"
    
    $baseDir = "C:\ProgramData\OPTIMUSOFT"
    
    if (Test-Path $baseDir) {
        Write-Success "Directorio base existe: $baseDir"
        
        # Verificar permisos
        try {
            $acl = Get-Acl $baseDir
            Write-Success "Permisos verificados"
            return $true
        } catch {
            Write-Error "No se pueden leer permisos: $_"
            return $false
        }
    } else {
        Write-Warning "Directorio base NO existe: $baseDir"
        Write-Info "Se creará automáticamente durante la instalación"
        Write-Warning "Debe existir ANTES de ejecutar el instalador final"
        return $false
    }
}

function Test-VersionConsistency {
    Write-Header "Validando Consistencia de Versiones"
    
    $versionExpected = "0.1.0"
    $allValid = $true
    
    # Verificar en setup.py
    try {
        $setupContent = Get-Content (Join-Path $projectRoot "setup.py") -Raw
        if ($setupContent -match 'version\s*=\s*["\']([^"\']+)["\']') {
            $setupVersion = $matches[1]
            if ($setupVersion -eq $versionExpected) {
                Write-Success "setup.py: $setupVersion"
            } else {
                Write-Warning "setup.py: $setupVersion (esperado: $versionExpected)"
                $allValid = $false
            }
        }
    } catch {
        Write-Warning "No se pudo verificar versión en setup.py"
    }
    
    # Verificar en installer.iss
    try {
        $issContent = Get-Content $installerScript -Raw
        if ($issContent -match '#define MyAppVersion "([^"]+)"') {
            $issVersion = $matches[1]
            if ($issVersion -eq $versionExpected) {
                Write-Success "installer.iss: $issVersion"
            } else {
                Write-Warning "installer.iss: $issVersion (esperado: $versionExpected)"
                $allValid = $false
            }
        }
    } catch {
        Write-Warning "No se pudo verificar versión en installer.iss"
    }
    
    return $allValid
}

function Test-FileIntegrity {
    Write-Header "Validando Integridad de Archivos"
    
    # Validar config.example.json
    $configFile = Join-Path $projectRoot "config.example.json"
    try {
        $config = Get-Content $configFile | ConvertFrom-Json
        Write-Success "config.example.json es JSON válido"
        Write-Info "  Campos: host, port, username, database"
    } catch {
        Write-Error "config.example.json es JSON inválido: $_"
        return $false
    }
    
    # Validar que installer.iss es válido Pascal/Inno
    $issContent = Get-Content $installerScript -Raw
    
    $requiredSections = @("[Setup]", "[Files]", "[Code]", "[Languages]")
    foreach ($section in $requiredSections) {
        if ($issContent -like "*$section*") {
            Write-Success "Sección $section encontrada"
        } else {
            Write-Error "Sección $section NO encontrada"
            return $false
        }
    }
    
    return $true
}

# ============================================================================
# PROCESOS DE COMPILACIÓN
# ============================================================================

function Invoke-Cleanup {
    Write-Header "Limpiando Archivos Anteriores"
    
    # Limpiar directorio de salida
    if (Test-Path $installerOutput) {
        Write-Info "Eliminando directorio: $installerOutput"
        Remove-Item -Path $installerOutput -Recurse -Force
        Write-Success "Directorio limpiado"
    }
    
    # Crear directorio de salida
    New-Item -ItemType Directory -Path $installerOutput -Force | Out-Null
    Write-Success "Directorio de salida creado"
}

function Invoke-InstallerCompilation {
    Write-Header "Compilando Instalador Inno Setup"
    
    Write-Info "Script: $installerScript"
    Write-Info "Salida: $installerOutput"
    
    try {
        # Compilar
        & $isccExe $installerScript
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Compilación completada"
            
            # Verificar archivo generado
            $setupExe = Join-Path $installerOutput "ori-cc-servicios-setup.exe"
            if (Test-Path $setupExe) {
                $fileSize = (Get-Item $setupExe).Length / 1MB
                Write-Success "Instalador generado: ori-cc-servicios-setup.exe"
                Write-Info "  Tamaño: $([Math]::Round($fileSize, 2)) MB"
                
                # Verificar tamaño razonable
                if ($fileSize -gt 20 -and $fileSize -lt 150) {
                    Write-Success "Tamaño dentro de límites esperados"
                } else {
                    Write-Warning "Tamaño podría indicar problema con compresión"
                }
                
                return $true
            } else {
                Write-Error "Archivo de instalador no encontrado"
                return $false
            }
        } else {
            Write-Error "Compilación fallida (código: $LASTEXITCODE)"
            return $false
        }
    } catch {
        Write-Error "Error durante compilación: $_"
        return $false
    }
}

# ============================================================================
# MODOS DE CONSTRUCCIÓN
# ============================================================================

function Start-FullBuild {
    Write-Header "COMPILACIÓN COMPLETA"
    
    # Paso 1: Validar entorno
    if (-not (Test-InnoSetupInstallation)) {
        Write-Error "Entorno de Inno Setup inválido"
        return $false
    }
    
    # Paso 2: Validar archivos
    if (-not (Test-RequiredFiles)) {
        Write-Error "Archivos requeridos incompletos"
        return $false
    }
    
    # Paso 3: Validar integridad
    if (-not (Test-FileIntegrity)) {
        Write-Error "Integridad de archivos comprometida"
        return $false
    }
    
    # Paso 4: Validar directorio base
    Test-ProgramDataDirectory | Out-Null
    
    # Paso 5: Validar versiones
    if (-not (Test-VersionConsistency)) {
        Write-Warning "Inconsistencia de versiones detectada"
    }
    
    # Paso 6: Limpiar
    Invoke-Cleanup
    
    # Paso 7: Compilar
    if (-not (Invoke-InstallerCompilation)) {
        Write-Error "Compilación del instalador fallida"
        return $false
    }
    
    Write-Header "COMPILACIÓN EXITOSA"
    Write-Success "Instalador listo en: $installerOutput\ori-cc-servicios-setup.exe"
    Write-Info "Siguiente paso: Ejecutar como administrador en máquina destino"
    
    return $true
}

function Start-ValidationOnly {
    Write-Header "VALIDACIÓN SOLAMENTE"
    
    # Ejecutar todas las validaciones
    $validations = @(
        (Test-InnoSetupInstallation),
        (Test-RequiredFiles),
        (Test-FileIntegrity),
        (Test-ProgramDataDirectory),
        (Test-VersionConsistency)
    )
    
    $allValid = $true
    foreach ($result in $validations) {
        if (-not $result) {
            $allValid = $false
        }
    }
    
    Write-Header "RESULTADO DE VALIDACIÓN"
    if ($allValid) {
        Write-Success "Todas las validaciones pasaron"
        return $true
    } else {
        Write-Error "Algunas validaciones fallaron"
        return $false
    }
}

function Start-CleanBuild {
    Write-Header "LIMPIEZA Y RECONSTRUCCIÓN"
    
    Write-Warning "Esto eliminará compilaciones anteriores"
    
    # Limpiar distribuciones
    if (Test-Path $distDir) {
        Write-Info "Limpiando: $distDir"
        Remove-Item -Path $distDir -Recurse -Force
        Write-Success "Directorio dist limpiado"
    }
    
    # Limpiar instalador
    if (Test-Path $installerOutput) {
        Write-Info "Limpiando: $installerOutput"
        Remove-Item -Path $installerOutput -Recurse -Force
        Write-Success "Directorio installer limpiado"
    }
    
    Write-Info "Ahora debe:"
    Write-Info "1. Compilar ejecutables: pyinstaller packaging/ori_cc_servicios.spec"
    Write-Info "2. Ejecutar nuevamente: Build-Installer.ps1 -BuildMode Full"
}

function Start-QuickBuild {
    Write-Header "COMPILACIÓN RÁPIDA"
    Write-Info "Omitiendo validaciones detalladas..."
    
    if (-not (Test-Path $isccExe)) {
        Write-Error "iscc.exe no encontrado"
        return $false
    }
    
    Invoke-Cleanup
    return (Invoke-InstallerCompilation)
}

# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================

function Main {
    Write-Host "`n"
    Write-Host "╔════════════════════════════════════════════════════════════════════╗"
    Write-Host "║          Build-Installer.ps1 - Orión CC Servicios                ║"
    Write-Host "║                        v0.1.0                                     ║"
    Write-Host "╚════════════════════════════════════════════════════════════════════╝"
    
    Write-Info "Modo: $BuildMode"
    Write-Info "Directorio: $projectRoot"
    Write-Info "Perfil: $([Security.Principal.WindowsIdentity]::GetCurrent().Name)"
    
    # Verificar permisos de administrador
    $isAdmin = [Security.Principal.WindowsIdentity]::GetCurrent() | 
        ForEach-Object { (New-Object Security.Principal.WindowsPrincipal $_).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) }
    
    if (-not $isAdmin) {
        Write-Warning "Este script funciona mejor ejecutado como administrador"
    }
    
    # Ejecutar según modo
    $result = switch ($BuildMode) {
        "Full" { Start-FullBuild }
        "Validate" { Start-ValidationOnly }
        "Clean" { Start-CleanBuild; return $true }
        "QuickBuild" { Start-QuickBuild }
        default { Write-Error "Modo desconocido: $BuildMode"; return $false }
    }
    
    Write-Host "`n"
    
    # Retornar código de salida
    if ($result) {
        exit 0
    } else {
        exit 1
    }
}

# Ejecutar main
Main

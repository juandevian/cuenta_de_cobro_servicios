# Script para desarrollo en PowerShell
param (
    [switch]$install,
    [switch]$run,
    [switch]$test
)

# Activar entorno virtual si existe, si no, crearlo
if (-not (Test-Path .venv)) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activar entorno virtual
. .venv/Scripts/Activate.ps1

if ($install) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install --upgrade pip
    pip install -e .
}

if ($test) {
    Write-Host "Ejecutando tests..." -ForegroundColor Yellow
    pytest
}

if ($run) {
    Write-Host "Ejecutando aplicación..." -ForegroundColor Yellow
    # Cargar variables de entorno de desarrollo
    Get-Content .env.development | ForEach-Object {
        if (-not [string]::IsNullOrWhiteSpace($_) -and -not $_.StartsWith("#")) {
            $key, $value = $_.Split('=', 2)
            $value = $value.Replace('${PWD}', $PWD)
            [System.Environment]::SetEnvironmentVariable($key, $value)
        }
    }
    python -m src.main
}

# Si no se especifica ningún parámetro, mostrar ayuda
if (-not ($install -or $run -or $test)) {
    Write-Host "Uso:" -ForegroundColor Yellow
    Write-Host "  .\dev.ps1 -install  # Instalar dependencias" -ForegroundColor Cyan
    Write-Host "  .\dev.ps1 -run      # Ejecutar aplicación" -ForegroundColor Cyan
    Write-Host "  .\dev.ps1 -test     # Ejecutar tests" -ForegroundColor Cyan
}
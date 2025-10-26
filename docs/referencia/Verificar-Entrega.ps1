#!/usr/bin/env powershell
# ============================================================================
# Verificacion de Entrega - Instalador Inno Setup
# ============================================================================
# Script para validar que la estructura post-reorganizacion es correcta

Write-Host ""
Write-Host "======================================================================"
Write-Host "      VERIFICACION DE ENTREGA - INSTALADOR INNO SETUP               "
Write-Host "                  Oriòn CC Servicios v1.0.0                          "
Write-Host "                 Estado: POST-REORGANIZACION                         "
Write-Host "======================================================================"
Write-Host ""

$projectRoot = "c:\Users\juanv\dev\work\ori_cc_servicios"
$packagingDir = Join-Path $projectRoot "packaging"
$docsDir = Join-Path $projectRoot "docs"
$docsGuidesDir = Join-Path $docsDir "guias"
$docsInstaladorDir = Join-Path $docsDir "instalador"
$docsReferenciaDir = Join-Path $docsDir "referencia"

# Colores
$green = @{ ForegroundColor = "Green" }
$red = @{ ForegroundColor = "Red" }
$yellow = @{ ForegroundColor = "Yellow" }
$cyan = @{ ForegroundColor = "Cyan" }

# ============================================================================
# VERIFICAR ESTRUCTURA PRINCIPAL EN RAIZ
# ============================================================================

Write-Host "[1/4] ARCHIVOS CLAVE EN RAIZ DEL PROYECTO" @cyan
Write-Host "======================================================================" @cyan

$rootKeyFiles = @("README.md", "PLAN_REORGANIZACION.md", "CHANGELOG.md")

foreach ($file in $rootKeyFiles) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        $size = (Get-Item $fullPath).Length
        Write-Host "OK  $file ($('{0:N0}' -f $size) bytes)" @green
    } else {
        Write-Host "FALTA: $file" @red
    }
}

Write-Host ""

# ============================================================================
# VERIFICAR DOCUMENTACION EN docs/
# ============================================================================

Write-Host "[2/4] DOCUMENTACION EN docs/" @cyan
Write-Host "======================================================================" @cyan

$docsFiles = @(
    @{ Path = "docs"; File = "README.md"; Type = "INDICE MAESTRO" },
    @{ Path = "docs/guias"; File = "COMENZAR.md"; Type = "TUTORIAL" },
    @{ Path = "docs/guias"; File = "TROUBLESHOOTING.md"; Type = "PROBLEMAS" },
    @{ Path = "docs/guias"; File = "TESTING.md"; Type = "VALIDACION" },
    @{ Path = "docs/instalador"; File = "REFERENCIA.md"; Type = "QUICK REF" },
    @{ Path = "docs/instalador"; File = "ARQUITECTURA.md"; Type = "DISENO" },
    @{ Path = "docs/referencia"; File = "INDICE.md"; Type = "MAPA COMPLETO" },
    @{ Path = "docs/referencia"; File = "ENTREGA.md"; Type = "CHECKLIST" },
    @{ Path = "docs/referencia"; File = "RESUMEN_FINAL.md"; Type = "EJECUTIVO" }
)

foreach ($item in $docsFiles) {
    $fullPath = Join-Path -Path (Join-Path -Path $projectRoot -ChildPath $item.Path) -ChildPath $item.File
    if (Test-Path $fullPath) {
        $lines = (Get-Content $fullPath | Measure-Object -Line).Lines
        Write-Host "OK  $($item.Path)/$($item.File) ($lines lineas)" @green
    } else {
        Write-Host "FALTA: $($item.Path)/$($item.File)" @red
    }
}

Write-Host ""

# ============================================================================
# VERIFICAR HERRAMIENTAS DE BUILD
# ============================================================================

Write-Host "[3/4] HERRAMIENTAS DE BUILD EN packaging/" @cyan
Write-Host "======================================================================" @cyan

$buildFiles = @(
    @{ File = "installer.iss"; Type = "CODIGO INNO SETUP" },
    @{ File = "Build-Installer.ps1"; Type = "SCRIPT BUILD" },
    @{ File = "INSTALADOR_ARQUITECTURA.md"; Type = "DOC TECNICA" },
    @{ File = "GUIA_COMPILACION.md"; Type = "DOC PASO A PASO" },
    @{ File = "EJEMPLOS_COMPILACION.md"; Type = "EJEMPLOS" }
)

foreach ($item in $buildFiles) {
    $fullPath = Join-Path $packagingDir $item.File
    if (Test-Path $fullPath) {
        $size = (Get-Item $fullPath).Length
        $lines = (Get-Content $fullPath | Measure-Object -Line).Lines
        Write-Host "OK  $($item.File) ($lines lineas)" @green
    } else {
        Write-Host "FALTA: $($item.File)" @red
    }
}

Write-Host ""

# ============================================================================
# CHECKLIST FINAL
# ============================================================================

Write-Host "[4/4] CHECKLIST DE ENTREGA" @cyan
Write-Host "======================================================================" @cyan

$checklist = @(
    @{ Item = "docs/README.md"; Path = (Join-Path $docsDir "README.md") },
    @{ Item = "docs/guias/COMENZAR.md"; Path = (Join-Path $docsGuidesDir "COMENZAR.md") },
    @{ Item = "docs/guias/TROUBLESHOOTING.md"; Path = (Join-Path $docsGuidesDir "TROUBLESHOOTING.md") },
    @{ Item = "docs/guias/TESTING.md"; Path = (Join-Path $docsGuidesDir "TESTING.md") },
    @{ Item = "docs/instalador/REFERENCIA.md"; Path = (Join-Path $docsInstaladorDir "REFERENCIA.md") },
    @{ Item = "docs/instalador/ARQUITECTURA.md"; Path = (Join-Path $docsInstaladorDir "ARQUITECTURA.md") },
    @{ Item = "docs/referencia/INDICE.md"; Path = (Join-Path $docsReferenciaDir "INDICE.md") },
    @{ Item = "docs/referencia/ENTREGA.md"; Path = (Join-Path $docsReferenciaDir "ENTREGA.md") },
    @{ Item = "docs/referencia/RESUMEN_FINAL.md"; Path = (Join-Path $docsReferenciaDir "RESUMEN_FINAL.md") },
    @{ Item = "packaging/installer.iss"; Path = (Join-Path $packagingDir "installer.iss") },
    @{ Item = "packaging/Build-Installer.ps1"; Path = (Join-Path $packagingDir "Build-Installer.ps1") },
    @{ Item = "packaging/INSTALADOR_ARQUITECTURA.md"; Path = (Join-Path $packagingDir "INSTALADOR_ARQUITECTURA.md") },
    @{ Item = "packaging/GUIA_COMPILACION.md"; Path = (Join-Path $packagingDir "GUIA_COMPILACION.md") },
    @{ Item = "packaging/EJEMPLOS_COMPILACION.md"; Path = (Join-Path $packagingDir "EJEMPLOS_COMPILACION.md") }
)

$allPassed = $true
foreach ($item in $checklist) {
    if (Test-Path $item.Path) {
        Write-Host "OK  $($item.Item)" @green
    } else {
        Write-Host "FALTA: $($item.Item)" @red
        $allPassed = $false
    }
}

Write-Host ""

# ============================================================================
# RESULTADO FINAL
# ============================================================================

Write-Host "======================================================================" @cyan

if ($allPassed) {
    Write-Host ""
    Write-Host "======================================================================" @green
    Write-Host "                                                                      " @green
    Write-Host "     OK - ENTREGA COMPLETADA Y VERIFICADA                           " @green
    Write-Host "                                                                      " @green
    Write-Host "     CODIGO + DOCUMENTACION + AUTOMATIZACION = LISTO PARA USO        " @green
    Write-Host "                                                                      " @green
    Write-Host "======================================================================" @green
    Write-Host ""
    Write-Host "PROXIMOS PASOS:" @cyan
    Write-Host "  1. Leer: docs/README.md"
    Write-Host "  2. Luego: docs/guias/COMENZAR.md (tutorial 30 min)"
    Write-Host "  3. Build: cd packaging && .\Build-Installer.ps1 -BuildMode Full"
    Write-Host ""
} else {
    Write-Host "ERROR - FALTAN ARCHIVOS" @red
    Write-Host "Revisar lista arriba para identificar archivos faltantes"
    Write-Host ""
}

Write-Host "ESTRUCTURA COMPLETA:" @cyan
Write-Host "  docs/README.md ....................... Punto de entrada"
Write-Host "  docs/guias/COMENZAR.md .............. Tutorial 30 min"
Write-Host "  docs/guias/TROUBLESHOOTING.md ...... Problemas comunes"
Write-Host "  docs/guias/TESTING.md ............... Validacion"
Write-Host "  docs/instalador/REFERENCIA.md ...... Guia rapida"
Write-Host "  docs/instalador/ARQUITECTURA.md ... Diseno tecnico"
Write-Host "  docs/referencia/INDICE.md ......... Mapa completo"
Write-Host "  docs/referencia/ENTREGA.md ....... Checklist"
Write-Host "  docs/referencia/RESUMEN_FINAL.md . Ejecutivo"
Write-Host ""

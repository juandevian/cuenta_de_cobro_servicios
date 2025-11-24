Param(
    [string]$ReleaseVersion = "0.2.0",
    [string]$HashFile = "RELEASE-0.2.0-SHA256.txt"
)

Write-Host "Verificando hashes release v$ReleaseVersion..." -ForegroundColor Cyan

if (-not (Test-Path $HashFile)) {
    Write-Error "Archivo de hashes no encontrado: $HashFile"
    exit 2
}

$lines = Get-Content $HashFile | Where-Object { $_ -and ($_ -notmatch '^#') }

$errores = @()
foreach ($line in $lines) {
    $parts = $line -split '\s+'
    if ($parts.Count -lt 2) { continue }
    $expectedHash = $parts[0].Trim()
    $relPath = $parts[1].Trim()
    $fullPath = Join-Path (Get-Location) $relPath

    if (-not (Test-Path $fullPath)) {
        $errores += "FALTA ARCHIVO: $relPath"
        continue
    }

    $computed = (Get-FileHash -Algorithm SHA256 $fullPath).Hash.ToUpper()
    if ($computed -ne $expectedHash) {
        $errores += "HASH MISMATCH: $relPath`n  Esperado: $expectedHash`n  Obtenido: $computed"
    } else {
        Write-Host "OK  $relPath" -ForegroundColor Green
    }
}

if ($errores.Count -gt 0) {
    Write-Host "\nResumen de inconsistencias:" -ForegroundColor Yellow
    $errores | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    exit 1
}

Write-Host "\nTodos los hashes coinciden para release v$ReleaseVersion." -ForegroundColor Green
exit 0

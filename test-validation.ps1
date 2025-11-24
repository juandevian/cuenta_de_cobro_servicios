Write-Host '======================================' -ForegroundColor Cyan
Write-Host ' TEST: Validacion de Cambios de Ruta' -ForegroundColor Cyan
Write-Host '======================================' -ForegroundColor Cyan
Write-Host ''

Write-Host '[1/3] Verificando installer.iss...' -ForegroundColor Yellow
$iss = Get-Content .\packaging\installer.iss -Raw
if ($iss -match 'OPTIMUSOFT') {
    Write-Host '  OK: Ruta OPTIMUSOFT encontrada' -ForegroundColor Green
}
if ($iss -match 'ori-cc-servicios') {
    Write-Host '  OK: Carpeta ori-cc-servicios (sin acento)' -ForegroundColor Green
}

Write-Host ''
Write-Host '[2/3] Verificando Build-Installer.ps1...' -ForegroundColor Yellow
$build = Get-Content .\packaging\Build-Installer.ps1 -Raw
if ($build -match 'Test-InstallationDirectory') {
    Write-Host '  OK: Funcion renombrada correctamente' -ForegroundColor Green
}
if ($build -match 'Program Files\\OPTIMUSOFT') {
    Write-Host '  OK: Ruta actualizada a Program Files' -ForegroundColor Green
}

Write-Host ''
Write-Host '[3/3] Ejecutando validacion del instalador...' -ForegroundColor Yellow
Write-Host '--------------------------------------' -ForegroundColor DarkGray
.\packaging\Build-Installer.ps1 -BuildMode Validate
Write-Host '--------------------------------------' -ForegroundColor DarkGray
Write-Host ''
Write-Host 'Siguiente paso: .\packaging\Build-Installer.ps1 -BuildMode Full' -ForegroundColor Yellow

# 🔧 Solución de Problemas - Troubleshooting

## Problemas Comunes

### Spanish.isl no encontrado

**Síntoma**: Error compilando: "Spanish.isl no found"

**Causa**: Inno Setup instalado sin paquete de idiomas

**Solución**:
```powershell
# 1. Verificar ruta
$innoPath = "C:\Program Files (x86)\Inno Setup 6"
$spanishFile = "$innoPath\Languages\Spanish.isl"

Test-Path $spanishFile  # Debe retornar True

# 2. Si no existe:
#    - Descargar desde: https://www.innosetup.com
#    - Ejecutar: Instalador de Inno Setup
#    - Seleccionar: Languages (marcar Spanish)
#    - Reinstalar

# 3. Verificar después de instalar
Test-Path $spanishFile  # Debe retornar True
```

---

### C:\ProgramData\OPTIMUSOFT no existe

**Síntoma**: Error durante instalación: "Directorio requerido no encontrado"

**Causa**: Directorio base no creado. No tiene instalado Orión Plus.

**Solución**:
```powershell
# 1. ANTES de ejecutar el instalador:
New-Item -ItemType Directory -Path "C:\ProgramData\OPTIMUSOFT" -Force

# 2. Verificar que se creó:
Test-Path "C:\ProgramData\OPTIMUSOFT"  # Debe retornar True

# 3. Luego ejecutar instalador:
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs
```

---

### Permiso Denegado

**Síntoma**: "Access denied" durante compilación o instalación

**Causa**: No ejecutado como administrador

**Solución**:
```powershell
# Opción 1: Ejecutar PowerShell como admin
# Click derecho en PowerShell → "Ejecutar como administrador"

# Opción 2: Desde línea de comandos
Start-Process powershell -Verb RunAs

# Opción 3: Script
# Click derecho en Build-Installer.ps1 → "Ejecutar como administrador"
```

---

### Archivos Faltantes

**Síntoma**: "FALTA: ori-cc-servicios.exe"

**Causa**: Ejecutables no compilados con PyInstaller

**Solución**:
```powershell
# 1. Compilar ejecutables
pyinstaller packaging/ori_cc_servicios.spec --clean

# 2. Verificar que se crearon
Test-Path "dist\ori-cc-servicios\ori-cc-servicios.exe"  # True?
Test-Path "dist\set_password.exe"                        # True?

# 3. Si falta alguno, recompilar:
pyinstaller packaging/set_password.spec --clean
```

---

### config.example.json es JSON inválido

**Síntoma**: Error de validación en JSON

**Causa**: Sintaxis JSON incorrecta

**Solución**:
```powershell
# 1. Verificar sintaxis
$config = Get-Content "config.example.json" | ConvertFrom-Json

# 2. Si hay error, revisar archivo:
notepad config.example.json

# 3. Ejemplo correcto:
@{
    host = "localhost"
    port = 3306
    username = "mi_usuario"
    database = "panorama_net"
} | ConvertTo-Json | Out-File "config.example.json"
```

---

### Tamaño de Instalador Sospechoso

**Síntoma**: Instalador < 20 MB o > 150 MB

**Causa**: Compresión LZMA no activa o archivos innecesarios

**Solución**:
```powershell
# 1. Verificar tamaño
$size = (Get-Item "installer\ori-cc-servicios-setup.exe").Length / 1MB
Write-Host "Tamaño: $size MB"

# 2. Si < 20 MB:
#    - Compilar ejecutables (PyInstaller)
#    - Verificar que incluyen dependencias

# 3. Si > 150 MB:
#    - Verificar installer.iss (compresión LZMA)
#    - Revisar qué archivos se incluyen
```

---

### No se puede escribir INSTRUCCIONES_CONFIGURACION.txt

**Síntoma**: Advertencia durante instalación

**Causa**: Permisos insuficientes o espacio en disco

**Solución**:
```powershell
# 1. Verificar permisos en directorio
$appDir = "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"
$acl = Get-Acl $appDir
$acl | Format-List

# 2. Verificar espacio en disco
$drive = Get-Item C:\
$freeSpace = $drive.AvailableFreeSpace / 1GB
Write-Host "Espacio libre: $freeSpace GB"

# 3. Si faltan permisos:
#    - Ejecutar como administrador
#    - O cambiar permisos del directorio
```

---

### El compilador iscc.exe no se encuentra

**Síntoma**: "iscc.exe no encontrado"

**Causa**: Inno Setup no instalado

**Solución**:
```powershell
# 1. Verificar instalación
$isccPath = "C:\Program Files (x86)\Inno Setup 6\iscc.exe"
Test-Path $isccPath  # ¿Retorna True?

# 2. Si no existe:
#    - Descargar desde: https://www.innosetup.com
#    - Ejecutar instalador
#    - Marcar: Compiler
#    - Instalar

# 3. Después, actualizar variable si es necesario:
$env:Path += ";C:\Program Files (x86)\Inno Setup 6"
```

---

### Compilación sale prematuramente

**Síntoma**: Script termina sin completar

**Causa**: Error no capturado o permisos insuficientes

**Solución**:
```powershell
# 1. Ejecutar con modo verbose
.\Build-Installer.ps1 -BuildMode Full -Verbose

# 2. Capturar errores explícitamente
try {
    .\Build-Installer.ps1 -BuildMode Full
    if ($LASTEXITCODE -ne 0) {
        throw "Build falló con código: $LASTEXITCODE"
    }
} catch {
    Write-Host "Error: $_"
    exit 1
}

# 3. Ejecutar modo de validación primero:
.\Build-Installer.ps1 -BuildMode Validate
```

---

### Las rutas tienen caracteres especiales

**Síntoma**: Errores con rutas en español o caracteres especiales

**Causa**: Inno Setup sensible a caracteres no-ASCII

**Solución**:
```powershell
# 1. Mover proyecto a ruta sin caracteres especiales:
# ❌ C:\Users\Javier\Mis Documentos\proyecto
# ✅ C:\Users\javier\dev\proyecto

# 2. O usar rutas cortas (8.3 format):
cmd /c for %A in ("C:\Users\Javier\Mis Documentos") do @echo %~sA
```

---

### config.json se sobrescribe en actualización

**Síntoma**: Configuración perdida después de actualizar

**Causa**: Flag `onlyifdoesntexist` no está configurado

**Solución**:
```powershell
# Verificar en installer.iss:
# Source: "..\config.example.json"; DestDir: "{app}"; \
#     DestName: "config.json"; \
#     Flags: onlyifdoesntexist uninsneveruninstall;  ← Estos flags

# Si falta, agregar a installer.iss
```

---

### Notepad no abre después de instalar

**Síntoma**: INSTRUCCIONES_CONFIGURACION.txt no se abre

**Causa**: Notepad.exe no en PATH o archivo no creado

**Solución**:
```powershell
# 1. Verificar que el archivo existe
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\INSTRUCCIONES_CONFIGURACION.txt"

# 2. Abrir manualmente
notepad "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\INSTRUCCIONES_CONFIGURACION.txt"

# 3. Si no existe, reinstalar:
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs
```

---

## 🔍 Debug: Activar Modo Verbose

```powershell
# Para obtener más información
$VerbosePreference = "Continue"
.\Build-Installer.ps1 -BuildMode Full -Verbose

# Ver logs detallados
.\Build-Installer.ps1 -BuildMode Validate
```

---

## 📞 Si Nada Funciona

1. **Ejecutar validación completa**:
   ```powershell
   .\Build-Installer.ps1 -BuildMode Validate
   ```

2. **Limpiar y reconstruir**:
   ```powershell
   .\Build-Installer.ps1 -BuildMode Clean
   pyinstaller packaging/ori_cc_servicios.spec --clean
   .\Build-Installer.ps1 -BuildMode Full
   ```

3. **Consultar otros documentos**:
   - [`TESTING.md`](./TESTING.md)
   - [`../instalador/REFERENCIA.md`](../instalador/REFERENCIA.md)
   - [`../referencia/INDICE.md`](../referencia/INDICE.md)

---

## 👤 Problemas Comunes - Usuario Final

### Error: "Columnas faltantes"

**Síntoma**: "Columnas faltantes: id_carpeta, id_servicio..."

**Causa**: El archivo Excel no tiene la estructura requerida

**Solución**:
1. Usar la plantilla oficial (botón "Crear Plantilla de Importación")
2. Verificar que todas las columnas requeridas estén presentes
3. No modificar los nombres de las columnas

### Error: "id_carpeta debe ser un entero entre 1 y 99"

**Síntoma**: Error de validación en columna id_carpeta

**Causa**: Valor fuera del rango permitido (1-99)

**Solución**:
- Verificar que id_carpeta sea un número entero
- Confirmar que el valor esté entre 1 y 99
- Revisar que no haya espacios o caracteres especiales

### Error: "id_predio e id_tercero_cliente no pueden tener valores al mismo tiempo"

**Síntoma**: Error de exclusividad mutua

**Causa**: Ambas columnas tienen valores en la misma fila

**Solución**:
- Cada fila debe tener SOLO UNO de los dos identificadores
- Usar `id_predio` para predios (texto) o `id_tercero_cliente` para clientes (número)
- Dejar vacío el campo no utilizado

### Error: "periodo_inicio_cobro debe ser una cadena de exactamente 6 dígitos"

**Síntoma**: Error de formato en periodo

**Causa**: Formato incorrecto (debe ser AAAAMM)

**Solución**:
- Formato: AAAAMM (ejemplo: 202411 para Noviembre 2024)
- Año: entre año actual-1 y 2040
- Mes: entre 01 y 12

### Error: "valor_unitario debe ser un número entre 0 y 999999"

**Síntoma**: Error de rango en valor unitario

**Causa**: Valor fuera del rango permitido

**Solución**:
- Valor debe estar entre 0 y 999999
- Puede incluir decimales
- No puede ser negativo

### Error: "lectura_actual debe ser mayor o igual a lectura_anterior"

**Síntoma**: Error en lecturas del medidor

**Causa**: Lectura actual menor que la anterior

**Solución**:
- Verificar que lectura_actual ≥ lectura_anterior
- Ambas lecturas deben ser números no negativos
- Consumos no pueden exceder 999999

### Advertencia: "Consumo muy alto, revisar datos"

**Síntoma**: Advertencia de consumo alto (>10000)

**Causa**: Consumo calculado muy alto

**Solución**:
- Revisar las lecturas del medidor
- Verificar que los valores sean correctos
- Confirmar que no hay errores de tipeo

### Error: "id_carpeta debe ser igual en todas las filas"

**Síntoma**: Error de consistencia

**Causa**: Valores diferentes de id_carpeta en el archivo

**Solución**:
- Todos los registros deben pertenecer a la misma carpeta
- Verificar que id_carpeta sea igual en todas las filas
- Lo mismo aplica para id_servicio y periodo_inicio_cobro

### Error: "No se encontraron registros válidos para importar"

**Síntoma**: Importación procesa 0 registros

**Causa**: Todos los registros tienen errores de validación

**Solución**:
- Revisar el log de errores detallado
- Corregir todos los errores de validación
- Usar "Vista Previa" para verificar antes de importar

---

## 📝 Reportar Problema

Si el problema persiste, recopilar:
1. Salida de `.\Build-Installer.ps1 -BuildMode Validate`
2. `$PSVersionTable` (versión de PowerShell)
3. `[System.Environment]::OSVersion.Version` (versión de Windows)
4. Ruta completa del proyecto

---

**Versión**: 0.2.1 | **Última actualización**: Nov 2025

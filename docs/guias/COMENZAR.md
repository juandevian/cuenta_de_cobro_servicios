# 🚀 Primeros Pasos - Comenzar con el Instalador

## ¿Nuevo en el proyecto? Comienza aquí

Esta guía te llevará desde cero hasta tener el instalador compilado en menos de 30 minutos.

---

## ✅ Paso 1: Verificar Requisitos (5 minutos)

### Windows
```powershell
# Verificar versión
[System.Environment]::OSVersion.Version
# Debe ser Windows 7 o superior
```

### Inno Setup 6
```powershell
# Verificar instalación
Test-Path "C:\Program Files (x86)\Inno Setup 6\iscc.exe"

# Si NO existe:
# 1. Descargar desde: https://www.innosetup.com
# 2. Ejecutar instalador
# 3. Seleccionar: Compiler + Languages (Spanish)
```

### Python 3.13+
```powershell
# Verificar
python --version
# O
py --version

# Si NO existe: descargar desde https://www.python.org
```

### PyInstaller
```powershell
# Verificar
pip list | Select-String PyInstaller

# Si NO existe:
pip install PyInstaller
```

---

## ✅ Paso 2: Preparar el Entorno (5 minutos)

### 1. Clonar o actualizar el proyecto
```powershell
git clone https://github.com/juandevian/cuenta_de_cobro_servicios.git
cd ori_cc_servicios
```

### 2. Crear/Activar entorno virtual
```powershell
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# O si ya existe:
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 4. Verificar estructura
```powershell
# Desde raíz del proyecto
ls packaging/
ls dist/ -ErrorAction SilentlyContinue
ls config.example.json
ls docs/setup_mysql_user.sql
```

---

## ✅ Paso 3: Compilar Ejecutables (10 minutos)

### Ejecutable Principal
```powershell
# Desde raíz del proyecto
pyinstaller packaging/ori_cc_servicios.spec --clean

# Resultado: dist/ori-cc-servicios/ori-cc-servicios.exe
```

### Herramienta de Contraseña
```powershell
# Desde raíz del proyecto
pyinstaller packaging/set_password.spec --clean

# Resultado: dist/set_password.exe
```

### Verificar que compilaron
```powershell
Test-Path "dist\ori-cc-servicios\ori-cc-servicios.exe"  # Must be True
Test-Path "dist\set_password.exe"                        # Must be True
```

---

## ✅ Paso 4: Compilar Instalador (5 minutos)

### Opción A: Script Automático (RECOMENDADO)
```powershell
# Desde packaging/
cd packaging

# Validar antes de compilar
.\Build-Installer.ps1 -BuildMode Validate

# Compilar
.\Build-Installer.ps1 -BuildMode Full
```

### Opción B: Manual
```powershell
cd packaging
"C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss
```

### Resultado
```
✅ installer\ori-cc-servicios-setup.exe (~45 MB)
```

---

## ✅ Paso 5: Verificar Instalación (3 minutos)

```powershell
# Desde raíz del proyecto

# Verificar que el archivo existe
Test-Path "installer\ori-cc-servicios-setup.exe"

# Verificar tamaño (debe ser ~45-50 MB)
$file = Get-Item "installer\ori-cc-servicios-setup.exe"
Write-Host "Tamaño: $($file.Length / 1MB) MB"

# Verificar que es reciente
Write-Host "Creado: $($file.CreationTime)"
```

---

## ✅ Paso 6: Testing Básico (2 minutos)

```powershell
# 1. Crear directorio base (si no existe)
New-Item "C:\ProgramData\OPTIMUSOFT" -Force

# 2. Ejecutar instalador como admin
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs

# 3. Seguir el wizard de instalación
# 4. Verificar que se creó:
Test-Path "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\ori-cc-servicios.exe"
```

---

## 🎯 ¿Problemas?

Si algo no funciona, consulta:
- [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) - Problemas comunes
- [`TESTING.md`](./TESTING.md) - Testing más avanzado
- [`../instalador/REFERENCIA.md`](../instalador/REFERENCIA.md) - Referencia rápida

---

## 📚 Próxima Lectura

Una vez completados estos pasos:

1. **Para entender cómo funciona**: [`../instalador/ARQUITECTURA.md`](../instalador/ARQUITECTURA.md)
2. **Para la guía completa del instalador**: [`../instalador/GUIA_INSTALADOR.md`](./GUÍA_USUARIO_INSTALADOR.md)
3. **Para referencia rápida**: [`../instalador/REFERENCIA.md`](../instalador/REFERENCIA.md)


---

## ⏱️ Resumen de Tiempo

```
Verificar requisitos:     5 minutos
Preparar entorno:         5 minutos
Compilar ejecutables:    10 minutos
Compilar instalador:      5 minutos
Verificar:                3 minutos
Testing:                  2 minutos
─────────────────────────────────
TOTAL:                   30 minutos ✅
```

---

## 🎉 ¡Listo!

Tu instalador está compilado y listo para:
- ✅ Distribuir a usuarios finales
- ✅ Testing en máquina limpia
- ✅ CI/CD integration
- ✅ Deployment automatizado

---

## 📞 Ayuda

**¿Dónde empiezo si tengo problemas?**

1. Consulta [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)
2. Revisa [`../instalador/REFERENCIA.md`](../instalador/REFERENCIA.md)
3. Lee [`../referencia/INDICE.md`](../referencia/INDICE.md)

---

**Versión**: 0.1.0 | **Fecha**: Oct 2025 | **Duración**: ~30 minutos

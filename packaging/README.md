# Compilación de Ejecutables - Orión CC Servicios

Esta carpeta contiene los archivos de especificación (`.spec`) para compilar los ejecutables de la aplicación usando PyInstaller.

## 📦 Archivos de Especificación

### `ori_cc_servicios.spec`
Compila la aplicación principal (GUI de importación de facturas).

**Salida**: `dist/ori-cc-servicios/` (carpeta con ejecutable y dependencias)

### `set_password.spec`
Compila la herramienta de configuración de contraseñas (standalone).

**Salida**: `dist/set_password.exe` (ejecutable único)

---

## 🚀 Compilar los Ejecutables

### Pre-requisitos

Asegúrate de tener el entorno virtual activado y las dependencias instaladas:

```powershell
# Activar entorno virtual (si no está activo)
.\.venv\Scripts\Activate.ps1

# Instalar/actualizar dependencias
pip install -r requirements.txt
```

### Compilar Aplicación Principal

Desde la **raíz del proyecto**:

```powershell
# Usando Python del entorno virtual
C:/Users/juanv/dev/work/ori_cc_servicios/.venv/Scripts/python.exe -m PyInstaller packaging/ori_cc_servicios.spec --clean
```

O si el venv está activado:

```powershell
pyinstaller packaging/ori_cc_servicios.spec --clean
```

**Resultado**: `dist/ori-cc-servicios/ori-cc-servicios.exe`

### Compilar Herramienta de Contraseña

Desde la **raíz del proyecto**:

```powershell
# Usando Python del entorno virtual
C:/Users/juanv/dev/work/ori_cc_servicios/.venv/Scripts/python.exe -m PyInstaller packaging/set_password.spec --clean
```

O si el venv está activado:

```powershell
pyinstaller packaging/set_password.spec --clean
```

**Resultado**: `dist/set_password.exe`

### Compilar Ambos (Recomendado)

```powershell
# Compilar aplicación principal
pyinstaller packaging/ori_cc_servicios.spec --clean

# Compilar herramienta de contraseña
pyinstaller packaging/set_password.spec --clean
```

---

## 📁 Estructura de Salida

Después de compilar, la carpeta `dist/` contendrá:

```
dist/
├── ori-cc-servicios/           # Aplicación principal (carpeta)
│   ├── ori-cc-servicios.exe
│   ├── assets/
│   │   └── database_schema.sql
│   └── ... (DLLs y dependencias)
└── set_password.exe            # Herramienta standalone (archivo único)
```

---

## 🔧 Notas Importantes

### Carpetas Generadas

- **`build/`**: Archivos temporales de compilación (se puede eliminar)
- **`dist/`**: Ejecutables finales (distribuir estos)

Ambas carpetas están en `.gitignore` y se regeneran cada compilación.

### Paths Relativos

Los archivos `.spec` usan paths relativos desde la raíz del proyecto:
- `../src/main.py` → código fuente de la app
- `../src/tools/set_password_tool.py` → código fuente de la herramienta
- `../assets/database_schema.sql` → recurso incluido

**IMPORTANTE**: Siempre ejecuta PyInstaller desde la **raíz del proyecto**, no desde esta carpeta.

### Compilación Limpia

El flag `--clean` elimina cache y recompila todo. Úsalo siempre para evitar inconsistencias.

---

## 🔍 Verificación Rápida

Después de compilar, prueba los ejecutables:

```powershell
# Probar herramienta de contraseña
.\dist\set_password.exe

# Probar aplicación principal
.\dist\ori-cc-servicios\ori-cc-servicios.exe
```

---

## 📦 Compilar Instalador

Una vez compilados los ejecutables, genera el instalador con Inno Setup:

```powershell
iscc installer.iss
```

El instalador se generará en: `installer/ori-cc-servicios-setup.exe`

---

## 🛠️ Solución de Problemas

### Error: "No such file or directory"
- Verifica que estés ejecutando desde la **raíz del proyecto**
- Los paths en `.spec` son relativos a la raíz

### Error: "ModuleNotFoundError"
- Instala dependencias: `pip install -r requirements.txt`
- Verifica que el venv esté activado

### Ejecutable no funciona
- Compila con `--clean` para limpiar cache
- Verifica que todas las dependencias estén en `hiddenimports`
- Revisa logs en `build/*/warn-*.txt`

### Permisos Denegados al compilar
- Cierra los ejecutables si están corriendo
- Ejecuta: `taskkill /IM ori-cc-servicios.exe /F; taskkill /IM set_password.exe /F`

---

## 📚 Referencias

- [Documentación de PyInstaller](https://pyinstaller.org/en/stable/)
- [Guía de Despliegue](../docs/GUIA_DESPLIEGUE.md)
- [Checklist de Validación](../docs/CHECKLIST_VALIDACION.md)

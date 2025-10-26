# Referencia Rápida - Instalador Inno Setup

## 🚀 Comando Principal

```powershell
# Compilación completa (RECOMENDADO)
cd packaging
.\Build-Installer.ps1 -BuildMode Full
```

**Resultado**: `installer\ori-cc-servicios-setup.exe` (45-50 MB)

---

## 📋 Checklist Pre-Compilación

```
[ ] Python ejecutables compilados:
    pyinstaller packaging/ori_cc_servicios.spec --clean
    pyinstaller packaging/set_password.spec --clean

[ ] Archivos requeridos existen:
    dist/ori-cc-servicios/ori-cc-servicios.exe
    dist/set_password.exe
    config.example.json
    docs/setup_mysql_user.sql

[ ] Versiones consistentes:
    setup.py → version="0.1.0"
    installer.iss → #define MyAppVersion "0.1.0"
    CHANGELOG.md → Actualizado
```

---

## 🎯 3 Pasos de Compilación

### Paso 1: Validar
```powershell
cd packaging
.\Build-Installer.ps1 -BuildMode Validate
```

### Paso 2: Compilar
```powershell
cd packaging
.\Build-Installer.ps1 -BuildMode Full
```

### Paso 3: Testing
```powershell
# Crear directorio base (si no existe)
New-Item "C:\ProgramData\OPTIMUSOFT" -Force

# Ejecutar instalador como admin
Start-Process "installer\ori-cc-servicios-setup.exe" -Verb RunAs
```

---

## 📊 Modos de Compilación

```powershell
# Modo Full - Recomendado para producción
.\Build-Installer.ps1 -BuildMode Full
# → Todas validaciones + compila

# Modo Validate - Pre-flight check
.\Build-Installer.ps1 -BuildMode Validate
# → Solo validaciones, sin compilar

# Modo QuickBuild - Desarrollo rápido
.\Build-Installer.ps1 -BuildMode QuickBuild
# → Omite validaciones, compila rápido

# Modo Clean - Reconstrucción completa
.\Build-Installer.ps1 -BuildMode Clean
# → Limpia dist/ e installer/
```

---

## 🔑 Características Clave

### ✅ Seguridad
- Valida directorio base antes de instalar
- Requiere permisos administrativos
- Protege credenciales (Credential Manager)
- Preserva configuración en actualizaciones

### ✅ Automatización
- Genera instrucciones automáticamente
- Abre Notepad con instrucciones
- 5 validaciones exhaustivas
- 4 modos de compilación

### ✅ Arquitectura SOLID
- Single Responsibility: 3 clases, cada una con propósito único
- Open/Closed: Extensible sin modificar código
- Liskov Substitution: Abstracciones intercambiables
- Interface Segregation: Interfaces específicas
- Dependency Inversion: Inyección de dependencias

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| **Spanish.isl no encontrado** | Reinstalar Inno Setup con idiomas |
| **C:\ProgramData\OPTIMUSOFT no existe** | `New-Item "C:\ProgramData\OPTIMUSOFT" -Force` |
| **Permiso denegado** | Ejecutar como administrador |
| **Archivos faltantes** | Compilar ejecutables primero |
| **JSON inválido** | Validar `config.example.json` |

---

## 🔍 Validaciones Incluidas

El script ejecuta:

```
✓ Inno Setup 6 instalado
✓ Spanish.isl disponible  
✓ Archivos requeridos presentes
✓ JSON válido
✓ Versiones consistentes
✓ Integridad de archivos
✓ Directorio base existe
✓ Compilación exitosa
✓ Tamaño razonable
```

---

## 📦 Resultado Final

```
installer/ori-cc-servicios-setup.exe
├─ Tamaño: 45-50 MB (compresión LZMA)
├─ Formato: Inno Setup 6
├─ Lenguaje: Español
└─ Requisitos: Admin, Windows 7+
```

---

## 💡 Tips

```powershell
# Verificar que todo está listo
.\Build-Installer.ps1 -BuildMode Validate

# Compilar sin esperar confirmación
.\Build-Installer.ps1 -BuildMode QuickBuild

# Ejecutar como admin automáticamente
Start-Process powershell -Verb RunAs
.\Build-Installer.ps1 -BuildMode Full
```

---

## 📖 Documentación Relacionada

- [`ARQUITECTURA.md`](./ARQUITECTURA.md) - Explicación técnica SOLID
- [`COMPILACION.md`](./COMPILACION.md) - Guía completa paso a paso
- [`EJEMPLOS.md`](./EJEMPLOS.md) - Casos de uso avanzados
- [`../guias/TROUBLESHOOTING.md`](../guias/TROUBLESHOOTING.md) - Problemas comunes
- [`../guias/TESTING.md`](../guias/TESTING.md) - Testing y validación

---

## 🎯 Próximos Pasos

1. **Compilar**:
   ```powershell
   cd packaging
   .\Build-Installer.ps1 -BuildMode Full
   ```

2. **Validar**:
   ```powershell
   Test-Path "installer\ori-cc-servicios-setup.exe"
   ```

3. **Distribuir**:
   ```
   Copiar: installer\ori-cc-servicios-setup.exe
   ```

---

**Versión**: 0.1.0 | **Fecha**: Oct 2025 | **Estado**: ✅ Completado

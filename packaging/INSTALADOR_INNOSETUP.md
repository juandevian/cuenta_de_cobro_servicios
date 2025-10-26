# Instalador Inno Setup - Guía Completa

## 📦 Descripción General

Esta guía cubre todo lo relacionado con la **creación del instalador** usando Inno Setup 6 para empaquetar la aplicación Orión CC Servicios de forma profesional.

El instalador se genera en dos fases:
1. **Compilación de ejecutables** (PyInstaller) → Ver `README.md` en esta carpeta
2. **Empaquetamiento** (Inno Setup) → Ver esta guía

---

## 🎯 Instalador de Producción

### Estructura de Archivos

```
packaging/
├── installer.iss                      # ← NUEVO: Script Inno Setup (SOLID)
├── Build-Installer.ps1                # ← NUEVO: Script de compilación
├── INSTALADOR_ARQUITECTURA.md         # ← NUEVO: Arquitectura técnica
├── GUIA_COMPILACION.md                # ← NUEVO: Guía paso a paso
├── README.md                          # ← EXISTENTE: PyInstaller specs
├── ori_cc_servicios.spec              # PyInstaller - App principal
└── set_password.spec                  # PyInstaller - Tool contraseñas
```

---

## ✨ Características Implementadas

### Principios SOLID Aplicados

El código `installer.iss` implementa:

- **Single Responsibility**: Cada clase tiene una única responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Liskov Substitution**: Abstracciones intercambiables
- **Interface Segregation**: Interfaces bien definidas
- **Dependency Inversion**: Inyección de dependencias

### Clases Profesionales

```pascal
// Validar prerequisitos del sistema
TPrerequisiteValidator

// Generar instrucciones post-instalación
TInstructionContentGenerator

// Ejecutar tareas post-instalación
TPostInstallationFileHandler
```

### Características de Seguridad

✅ **Protección de datos sensibles**:
- Contraseñas NUNCA en archivos plano
- Uso de Windows Credential Manager
- Separación binarios (protegidos) vs configuración (editable)

✅ **Validaciones obligatorias**:
- Verificar directorio base antes de instalar
- Requerir permisos administrativos
- Validar consistencia de versiones

✅ **Actualizaciones seguras**:
- `config.json` se preserva (nunca se sobrescribe)
- Binarios se actualizan completamente
- Configuración anterior se mantiene intacta

---

## 🚀 Proceso de Compilación

### Fase 1: Compilar Ejecutables (PyInstaller)

Ver `README.md` en esta carpeta:

```powershell
# Compilar app principal
pyinstaller packaging/ori_cc_servicios.spec --clean

# Compilar herramienta de contraseña
pyinstaller packaging/set_password.spec --clean

# Resultado:
# dist/ori-cc-servicios/ori-cc-servicios.exe
# dist/set_password.exe
```

### Fase 2: Compilar Instalador (Inno Setup)

**Opción A: Script automático (recomendado)**

```powershell
# Compilación completa con validaciones
.\Build-Installer.ps1 -BuildMode Full

# Solo validar (sin compilar)
.\Build-Installer.ps1 -BuildMode Validate

# Compilación rápida (sin validaciones)
.\Build-Installer.ps1 -BuildMode QuickBuild
```

**Opción B: Compilación manual**

```powershell
# Desde carpeta packaging/
cd packaging
"C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss

# Resultado: ..\installer\ori-cc-servicios-setup.exe
```

---

## 📋 Validaciones Automáticas

El script `Build-Installer.ps1` valida:

```
✓ Inno Setup 6 instalado correctamente
✓ Spanish.isl disponible
✓ config.example.json es JSON válido
✓ Ejecutables compilados existen
✓ installer.iss es script válido
✓ Versiones consistentes (0.1.0)
✓ Directorio base C:\ProgramData\OPTIMUSOFT
✓ Archivo instalador generado correctamente
✓ Tamaño del instalador (compresión activa)
```

---

## 🏗️ Arquitectura Interna

### Flujo de Instalación

```
Usuario ejecuta setup
        ↓
InitializeSetup()
├─ TPrerequisiteValidator.ValidateAll()
└─ Verifica C:\ProgramData\OPTIMUSOFT
        ↓
    ¿Existe?
    /     \
  NO      SÍ
   │       │
   │       ↓
   │   Copia archivos
   │       ↓
   │   CurStepChanged(ssPostInstall)
   │   ├─ Genera instrucciones
   │   ├─ Guarda en archivo
   │   ├─ Muestra resumen
   │   └─ Abre en Notepad
   │       │
   └───┬───┘
       ↓
   [FIN]
```

### Generador de Contenido (Template Method)

```pascal
Generate()
├─ GenerateHeader()
├─ GenerateStep1Header() + GenerateStep1Content()
├─ GenerateStep2Header() + GenerateStep2Content()
├─ GenerateStep3Header() + GenerateStep3Content()
├─ GenerateImportantFilesSection()
└─ GenerateFooter()
```

**Ventajas**:
- Cada sección es independiente y reutilizable
- Fácil modificar contenido específico
- Formato consistente garantizado
- Principio DRY (Don't Repeat Yourself)

---

## 📚 Documentación Técnica

### Documento 1: `INSTALADOR_ARQUITECTURA.md`
- Explicación detallada de arquitectura
- Patrones de diseño (Strategy, DI, Template Method, Factory)
- Guía de extensibilidad futura
- Mejores prácticas implementadas

### Documento 2: `GUIA_COMPILACION.md`
- Pre-requisitos y configuración
- Checklist pre-compilación
- Compilación paso a paso
- Testing en máquina limpia
- Solución de problemas comunes

---

## 🔧 Requisitos

### Máquina de Compilación
- Windows 7/10/11
- PowerShell 5.0+
- **Inno Setup 6.0+** (con Spanish.isl)
- Python 3.9+ con PyInstaller
- Permisos de administrador

### Máquina Destino
- Windows 7/10/11 (32 o 64-bit)
- Directorio `C:\ProgramData\OPTIMUSOFT` (debe crearse)
- Permisos de administrador
- .NET Framework
- MySQL Server (local o remoto)

---

## 📦 Resultado Final

### Instalador Generado

```
installer/ori-cc-servicios-setup.exe
├─ Tamaño: ~30-100 MB (compresión LZMA)
├─ Formato: Ejecutable Inno Setup
├─ Lenguaje: Español
└─ Requiere: Permisos admin, Windows 7+
```

### Estructura Post-Instalación

```
C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\
├── ori-cc-servicios.exe                  (ejecutable)
├── set_password.exe                      (herramienta)
├── config.json                           (configuración)
├── INSTRUCCIONES_CONFIGURACION.txt       (guía)
├── docs/setup_mysql_user.sql             (referencia)
└── [dependencias PyInstaller]
```

---

## ✅ Checklist de Validación

### Pre-Compilación
```
[ ] Versión 0.1.0 en setup.py
[ ] Versión 0.1.0 en installer.iss
[ ] config.example.json existe
[ ] setup_mysql_user.sql existe
[ ] Ejecutables compilados existen
```

### Compilación
```
[ ] Build-Installer.ps1 ejecuta sin errores
[ ] installer\ori-cc-servicios-setup.exe generado
[ ] Tamaño razonable (30-100 MB)
[ ] Compresión LZMA activa
```

### Testing Post-Instalación
```
[ ] Instalación en máquina limpia funciona
[ ] C:\ProgramData\OPTIMUSOFT se valida
[ ] config.json se crea desde plantilla
[ ] INSTRUCCIONES_CONFIGURACION.txt se genera
[ ] Notepad abre automáticamente
[ ] Permisos correctos en directorio
[ ] Actualización preserva config.json
[ ] Desinstalación funciona correctamente
```

---

## 🔐 Seguridad Implementada

### Protección de Credenciales
- ❌ Contraseñas NO en archivos texto
- ✅ Windows Credential Manager obligatorio
- ✅ Configuración (no sensible) separada de credenciales

### Permisos de Directorios
```
C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\
├─ Administradores: Control Total
├─ Sistema: Control Total
└─ Usuarios: Lectura + Ejecución (sin escritura)
```

### Validaciones Obligatorias
- Directorio base debe existir
- Permisos de administrador requeridos
- Estructura de archivos verificada
- Consistencia de versiones validada

---

## 🎓 Principios SOLID en Práctica

### Single Responsibility
```pascal
// Cada clase tiene UNA responsabilidad
TPrerequisiteValidator      → Solo validar
TInstructionContentGenerator → Solo generar contenido
TPostInstallationFileHandler → Solo ejecutar tareas
```

### Open/Closed
```pascal
// Se puede extender sin modificar
function ValidateAll: Boolean;
begin
  if not BaseDirExists then... // Validación actual
  // Aquí se pueden agregar más validaciones
end;
```

### Dependency Inversion
```pascal
// Dependencias inyectadas (no hardcodeadas)
FileHandler := TPostInstallationFileHandler.Create(ExpandConstant('{app}'));
Generator := TInstructionContentGenerator.Create(AppPath, ExeName);
```

---

## 📖 Lectura Recomendada

1. **INSTALADOR_ARQUITECTURA.md** - Comprensión técnica profunda
2. **GUIA_COMPILACION.md** - Instrucciones prácticas paso a paso
3. **Build-Installer.ps1** - Estudio del script de automatización
4. **installer.iss** - Análisis del código Inno Setup

---

## 🆘 Solución de Problemas

### Problema: "Spanish.isl no encontrado"
```powershell
# Ubicación esperada:
# C:\Program Files (x86)\Inno Setup 6\Languages\Spanish.isl

# Solución: Reinstalar Inno Setup e incluir idiomas
```

### Problema: "C:\ProgramData\OPTIMUSOFT no existe"
```powershell
# Crear directorio (como administrador)
New-Item -ItemType Directory "C:\ProgramData\OPTIMUSOFT" -Force
```

### Problema: "Permiso denegado"
```powershell
# Ejecutar como administrador
Start-Process powershell -Verb RunAs
.\Build-Installer.ps1 -BuildMode Full
```

---

## 🚀 Próximos Pasos

1. **Compilar ejecutables**:
   ```powershell
   pyinstaller packaging/ori_cc_servicios.spec --clean
   ```

2. **Compilar instalador**:
   ```powershell
   .\Build-Installer.ps1 -BuildMode Full
   ```

3. **Testing**:
   ```powershell
   .\Build-Installer.ps1 -BuildMode Validate
   ```

4. **Distribuir**:
   ```
   Copiar installer\ori-cc-servicios-setup.exe
   ```

---

## 📞 Soporte

Para problemas o preguntas:
1. Consultar `GUIA_COMPILACION.md` (sección Solución de Problemas)
2. Contactar a OptimuSoft SAS
3. Revisar logs del compilador Inno Setup

---

**Versión**: 0.1.0  
**Actualizado**: Octubre 2025  
**Autor**: OptimuSoft SAS

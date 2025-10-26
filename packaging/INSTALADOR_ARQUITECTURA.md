# Arquitectura del Instalador Inno Setup - Orión CC Servicios

## Descripción General

El instalador `installer.iss` implementa una arquitectura moderna basada en **principios SOLID** y **patrones de diseño profesionales** para la instalación segura y confiable de la aplicación Orión CC Servicios.

## Principios SOLID Implementados

### 1. **S - Single Responsibility Principle**

Cada clase y función tiene una única responsabilidad bien definida:

- **`TPrerequisiteValidator`**: Solo valida prerequisitos del sistema
- **`TInstructionContentGenerator`**: Solo genera contenido de instrucciones
- **`TPostInstallationFileHandler`**: Solo ejecuta tareas post-instalación
- **`InitializeSetup`**: Solo orquesta validaciones iniciales
- **`CurStepChanged`**: Solo orquesta tareas post-instalación

**Beneficio**: Código fácil de entender, mantener y testear.

### 2. **O - Open/Closed Principle**

El código es:
- **Abierto para extensión**: Nuevas validaciones pueden agregarse sin modificar `TPrerequisiteValidator`
- **Cerrado para modificación**: Los métodos públicos tienen interfaces estables

**Ejemplo**:
```pascal
function TPrerequisiteValidator.ValidateAll: Boolean;
begin
  // Estructura permite agregar más validaciones sin romper el contrato
  if not BaseDirExists then
  begin
    // ...validación actual
  end;
  // Aquí se podrían agregar más validaciones
end;
```

### 3. **L - Liskov Substitution Principle**

Las abstracciones (tipos clase) son intercambiables:

```pascal
// El generador de contenido puede ser reemplazado por otra implementación
ContentGenerator := TInstructionContentGenerator.Create(FAppPath, MyAppExeName);
InstructionsContent := ContentGenerator.Generate;
```

### 4. **I - Interface Segregation Principle**

Interfaces específicas y bien definidas:

```pascal
// Cada clase tiene métodos públicos específicos
TPrerequisiteValidator.ValidateAll;              // Responsabilidad única
TInstructionContentGenerator.Generate;           // Responsabilidad única
TPostInstallationFileHandler.ExecutePostInstallationTasks;  // Responsabilidad única
```

### 5. **D - Dependency Inversion Principle**

Las dependencias se inyectan a través de constructores:

```pascal
// En lugar de codificar rutas, se pasan como parámetros
FileHandler := TPostInstallationFileHandler.Create(ExpandConstant('{app}'));
ContentGenerator := TInstructionContentGenerator.Create(FAppPath, MyAppExeName);
```

## Estructura de Clases

### `TPrerequisiteValidator`

**Responsabilidad**: Validar condiciones previas a la instalación

```
┌─ TPrerequisiteValidator
├─ Constructor(RequiredBaseDir: String)
├─ Métodos Privados:
│  ├─ BaseDirExists(): Boolean
│  └─ ShowBaseDirNotFoundError(): void
└─ Métodos Públicos:
   └─ ValidateAll(): Boolean
```

**Flujo**:
1. Verifica si `C:\ProgramData\OPTIMUSOFT` existe
2. Si no existe, muestra error y retorna `False`
3. Si existe, retorna `True` y continúa instalación

### `TInstructionContentGenerator`

**Responsabilidad**: Generar contenido formateado de instrucciones

```
┌─ TInstructionContentGenerator
├─ Constructor(AppPath: String; ExecutableName: String)
├─ Métodos Privados (Generadores de secciones):
│  ├─ GenerateLineBreak(): String
│  ├─ GenerateHeader(): String
│  ├─ GenerateStep1Header/Content(): String
│  ├─ GenerateStep2Header/Content(): String
│  ├─ GenerateStep3Header/Content(): String
│  ├─ GenerateImportantFilesSection(): String
│  └─ GenerateFooter(): String
└─ Métodos Públicos:
   └─ Generate(): String (orquesta generación completa)
```

**Ventajas del diseño por secciones**:
- Cada sección es independiente y reutilizable
- Fácil de modificar contenido específico
- Mantiene formato consistente (CRLF, anchura, etc.)
- Sigue principio DRY (Don't Repeat Yourself)

### `TPostInstallationFileHandler`

**Responsabilidad**: Ejecutar tareas post-instalación

```
┌─ TPostInstallationFileHandler
├─ Constructor(AppPath: String)
├─ Métodos Privados:
│  ├─ GetInstructionsFilePath(): String
│  ├─ SaveInstructionsFile(Content: String): void
│  ├─ ShowPostInstallationSummary(): void
│  └─ OpenInstructionsFile(): void
└─ Métodos Públicos:
   └─ ExecutePostInstallationTasks(): void (orquesta todas las tareas)
```

**Flujo de ejecución**:
1. Genera contenido de instrucciones
2. Guarda en `INSTRUCCIONES_CONFIGURACION.txt`
3. Muestra resumen al usuario
4. Abre archivo en Notepad

## Flujo de Instalación

```
┌─────────────────────────┐
│  Usuario ejecuta setup  │
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ InitializeSetup()                │
│ ├─ TPrerequisiteValidator        │
│ └─ Valida C:\ProgramData\OPTIMUSOFT
└────────────┬─────────────────────┘
             │
        ¿Válido?
         /     \
       NO       SÍ
        │        │
        ▼        ▼
    [ERROR]  [INSTALACIÓN]
        │        │
        ▼        ▼
   Cancela   Copia archivos
        │        │
        │        ▼
        │   ┌──────────────────────────────┐
        │   │ CurStepChanged(ssPostInstall)│
        │   ├─ TInstructionContentGenerator
        │   ├─ TPostInstallationFileHandler
        │   └─ Genera instrucciones
        │        │
        │        ▼
        │   Abre en Notepad
        │        │
        └────┬───┘
             │
             ▼
        [FIN INSTALACIÓN]
```

## Patrones de Diseño Utilizados

### 1. **Strategy Pattern**
Las diferentes estrategias de generación de contenido pueden ser reemplazadas:
```pascal
ContentGenerator := TInstructionContentGenerator.Create(...);
InstructionsContent := ContentGenerator.Generate;
```

### 2. **Dependency Injection**
```pascal
// Las dependencias se inyectan en constructores
Validator := TPrerequisiteValidator.Create(REQUIRED_BASE_DIR);
FileHandler := TPostInstallationFileHandler.Create(ExpandConstant('{app}'));
```

### 3. **Template Method**
```pascal
// El método Generate() orquesta la generación de todas las secciones
function TInstructionContentGenerator.Generate: String;
begin
  Result := GenerateHeader +
            GenerateStep1Header + GenerateStep1Content +
            GenerateStep2Header + GenerateStep2Content +
            GenerateStep3Header + GenerateStep3Content +
            GenerateImportantFilesSection +
            GenerateFooter;
end;
```

### 4. **Factory Pattern (implícito)**
Las clases se instancian con parámetros específicos que definen su comportamiento.

## Manejo de Errores y Validación

### Validaciones Pre-Instalación
- ✅ Verificar existencia de directorio base `C:\ProgramData\OPTIMUSOFT`
- ✅ Mostrar mensaje de error claro si no existe
- ✅ Cancelar instalación automáticamente

### Errores Post-Instalación
- ✅ Manejo gracioso si no puede guardarse archivo de instrucciones
- ✅ Mensajes informativos no bloqueantes
- ✅ Continúa ejecución aunque falle alguna tarea

## Configuración de Seguridad

### Permisos de Directorio
```
C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\
├─ Acceso Total: Administradores y Sistema
├─ Lectura/Ejecución: Usuarios regulares
└─ Escritura: Solo binarios (protegidos)
```

### Gestión de Credenciales
- ❌ NUNCA se guardan contraseñas en archivos de texto
- ✅ Se requiere ejecutar `set_password.exe` por separado
- ✅ Las credenciales se almacenan en Windows Credential Manager

### Configuración (config.json)
- ✅ Solo contiene datos no sensibles (host, puerto, usuario, BD)
- ✅ Se copia una sola vez (preserva configuraciones previas)
- ✅ Se marca como `uninsneveruninstall` (nunca se elimina)

## Compilación y Distribución

### Requisitos
- Inno Setup 6.0 o superior
- Spanish.isl disponible en compilador de Inno Setup

### Compilación
```powershell
# Desde la carpeta packaging/
iscc installer.iss

# Resultado: installer\ori-cc-servicios-setup.exe
```

### Pre-requisitos en máquina destino
- Windows 7/10/11 (32 o 64-bit)
- Directorio `C:\ProgramData\OPTIMUSOFT` debe existir
- Acceso de administrador
- .NET Framework (dependencia del ejecutable PyInstaller)

## Características del Instalador

### ✅ Implementadas
- Validación de prerequisitos antes de instalar
- Generación automática de instrucciones post-instalación
- Separación clara entre binarios y configuración
- Generación automática de INSTRUCCIONES_CONFIGURACION.txt
- Apertura automática de instrucciones en Notepad
- Preservación de config.json en actualizaciones
- Permisos de seguridad apropiados

### ❌ Deliberadamente NO Implementadas
- Accesos directos en menú inicio (se ejecuta desde VB.NET)
- Ejecución automática de la aplicación
- Ejecución automática de scripts SQL (seguridad)
- Validación de conectividad a BD (responsabilidad del usuario)
- Cambio de directorio de instalación (ubicación fija)

## Extensibilidad Futura

El código está diseñado para permitir:

1. **Nuevas validaciones**:
   ```pascal
   // Agregar en ValidateAll()
   if not ValidateNetworkConnectivity then...
   ```

2. **Nuevas tareas post-instalación**:
   ```pascal
   // Agregar en ExecutePostInstallationTasks()
   CreateRequiredDirectories;
   ConfigureRegistry;
   ```

3. **Generadores de contenido alternativos**:
   ```pascal
   // Implementar otro generador con otra interfaz
   class TAlternativeInstructionGenerator...
   ```

## Mejores Prácticas Aplicadas

| Práctica | Implementación |
|----------|---|
| **Documentación en código** | Comentarios explicativos en cada sección |
| **Nombres descriptivos** | Métodos y variables autoexplicativas |
| **Constantes centralizadas** | Definición de constantes al inicio |
| **Manejo de recursos** | Try-finally para liberar objetos |
| **Validación de entrada** | Validaciones antes de operaciones críticas |
| **Separación de responsabilidades** | Clases con propósitos únicos y claros |
| **Código reutilizable** | Métodos privados componibles |
| **Mensajes al usuario** | Claros, informativos y en español |

## Conclusión

El instalador implementa arquitectura profesional siguiendo principios SOLID, facilitando:

- ✅ **Mantenibilidad**: Código organizado y bien estructurado
- ✅ **Extensibilidad**: Fácil agregar nuevas funcionalidades
- ✅ **Testabilidad**: Componentes independientes
- ✅ **Robustez**: Validaciones adecuadas y manejo de errores
- ✅ **Seguridad**: Protección de datos sensibles
- ✅ **Usabilidad**: Experiencia clara y guiada para el usuario

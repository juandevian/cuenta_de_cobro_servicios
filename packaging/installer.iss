; ============================================================================
; Instalador Inno Setup - Orión CC Servicios
; ============================================================================
; OBJETIVO: Instalar la aplicación con validaciones de seguridad y
;          configuración post-instalación sin intervención del usuario
; ============================================================================
; Requerimientos:
;   - Inno Setup 6.0 o superior
;   - Compilar desde packaging/:  iscc installer.iss
;   - Idioma español disponible
; ============================================================================

#define MyAppName "Orion CC Servicios"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "OptimuSoft SAS"
#define MyAppExeName "ori-cc-servicios.exe"
#define MyAppSetupName "ori-cc-servicios-setup.exe"
#define MyAppGUID "{{A5B8C9D0-1234-5678-90AB-CDEF12345678}}"
#define MyAppBaseDir "C:\ProgramData\OPTIMUSOFT"
#define MyAppFolderName "ori-cc-servicios"
#define MyAppInstallDir MyAppBaseDir + "\" + MyAppFolderName

; ============================================================================
; CONFIGURACIÓN PRINCIPAL DEL INSTALADOR
; ============================================================================
[Setup]
AppId={#MyAppGUID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://optimusoft.com
AppSupportURL=https://optimusoft.com/support
AppUpdatesURL=https://optimusoft.com/updates
DefaultDirName={#MyAppInstallDir}
DisableDirPage=yes
DefaultGroupName={#MyAppFolderName}
DisableProgramGroupPage=yes
DisableFinishedPage=no
OutputDir=..\installer
; Evitar doble extensión .exe.exe: usar base sin extensión
OutputBaseFilename=ori-cc-servicios-setup
Compression=lzma/max
SolidCompression=yes
PrivilegesRequired=admin
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoOriginalFileName={#MyAppSetupName}
ShowLanguageDialog=no
LanguageDetectionMethod=none
WizardStyle=modern
SetupIconFile=..\assets\installer_icon.ico
Uninstallable=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

; ============================================================================
; IDIOMA Y LOCALIZACIÓN
; ============================================================================
[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

; ============================================================================
; DIRECTORIOS
; ============================================================================
; La carpeta {app} se expande a {#MyAppInstallDir}
;   Estructura final: C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\

; ============================================================================
; SECCIÓN [Files] - ARCHIVOS A INSTALAR
; ============================================================================
[Files]
; 3.1 Ejecutable principal y dependencias (compiladas con PyInstaller)
Source: "..\dist\{#MyAppFolderName}\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs; \
    Components: executables

; 3.2 Herramienta de configuración de contraseña
Source: "..\dist\set_password.exe"; DestDir: "{app}"; \
    Flags: ignoreversion; \
    Components: executables

; 3.3 Archivo de configuración (plantilla - nunca se sobrescribe)
Source: "..\config.example.json"; DestDir: "{app}"; \
    DestName: "config.json"; \
    Flags: ignoreversion onlyifdoesntexist uninsneveruninstall; \
    Components: configuration

; 3.4 Scripts de base de datos (documentación de referencia)
Source: "..\docs\setup_mysql_user.sql"; DestDir: "{app}\docs"; \
    Flags: ignoreversion; \
    Components: documentation

; ============================================================================
; COMPONENTES SELECCIONABLES
; ============================================================================
[Components]
Name: "executables"; Description: "Ejecutables de la aplicacion"; \
    Types: compact full custom; Flags: fixed
Name: "configuration"; Description: "Archivo de configuracion"; \
    Types: compact full custom; Flags: fixed
Name: "documentation"; Description: "Documentacion y scripts SQL"; \
    Types: full custom

; ============================================================================
; PERMISOS DE DIRECTORIO
; ============================================================================
[Dirs]
Name: "{app}"; Permissions: admins-full system-full; \
    Flags: uninsalwaysuninstall

Name: "{app}\docs"; Permissions: admins-full system-full; \
    Flags: uninsalwaysuninstall

; ============================================================================
; SECCIÓN [Run] - EJECUTABLES DESPUÉS DE LA INSTALACIÓN
; ============================================================================
; Deliberadamente vacío - La aplicación NO se ejecuta automáticamente
; La invocación ocurre únicamente desde aplicaciones VB.NET
; El usuario debe completar la configuración ANTES del primer uso
;
; Razones de esta decisión:
; 1. La contraseña de BD no está registrada aún
; 2. El archivo config.json podría necesitar edición manual
; 3. La conexión a BD no ha sido validada
; 4. Es responsabilidad del usuario completar la configuración inicial
;
[Run]

; ============================================================================
; SECCIÓN [UninstallDelete] - ARCHIVOS A BORRAR EN DESINSTALACIÓN
; ============================================================================
[UninstallDelete]
; Las credenciales en Credential Manager se dejan intactas
; (son responsabilidad del usuario de eliminarlas manualmente)
; Los archivos de datos generados se dejan intactos

; ============================================================================
; CÓDIGO PASCAL - INICIALIZACIÓN Y VALIDACIÓN
; ============================================================================
[Code]

// ========================================================================
// Constantes de configuración
// ========================================================================
const
  REQUIRED_BASE_DIR = 'C:\ProgramData\OPTIMUSOFT';
  CRLF = #13#10;
  INSTRUCTIONS_FILENAME = 'INSTRUCCIONES_CONFIGURACION.txt';
  CONFIG_FILENAME = 'config.json';
  EXECUTABLE_NAME = '{#MyAppExeName}';

// ========================================================================
// UTILIDADES Y POST-INSTALACIÓN (simplificado)
// ========================================================================

function ValidatePrerequisites(RequiredBaseDir: string): Boolean;
begin
  Result := DirExists(RequiredBaseDir);
  if not Result then
  begin
    MsgBox('Error: No se encuentra el directorio requerido.' + CRLF +
           'Ruta: ' + RequiredBaseDir + CRLF + CRLF +
           'El sistema no tiene los recursos necesarios para generar la instalacion.' + CRLF +
           'Por favor, contacte al administrador del sistema.',
           mbError, MB_OK);
  end;
end;

function GenerateInstructions(AppPath, ExecutableName: string): string;
begin
  Result :=
    '===============================================================' + CRLF +
    '  ORION CC SERVICIOS - INSTRUCCIONES DE CONFIGURACION' + CRLF +
    '===============================================================' + CRLF + CRLF +
    'La instalacion se completo correctamente.' + CRLF +
    'Para que la aplicacion funcione, debe completar estos pasos:' + CRLF + CRLF +

    '---------------------------------------------------------------' + CRLF +
    'PASO 1: Configurar usuario de base de datos (DBA)' + CRLF +
    '---------------------------------------------------------------' + CRLF + CRLF +
    '1. Abra MySQL con un usuario administrador (root)' + CRLF +
    '2. Ejecute el script SQL ubicado en:' + CRLF +
    '   ' + AppPath + '\docs\setup_mysql_user.sql' + CRLF + CRLF +
    '   Este script crea un usuario con permisos minimos.' + CRLF +
    '   IMPORTANTE: Edite el script antes de ejecutarlo para:' + CRLF +
    '   - Cambiar TU_PASSWORD_SEGURA_AQUI por una contrasena real' + CRLF +
    '   - Ajustar localhost si MySQL esta en otro servidor' + CRLF + CRLF +

    '---------------------------------------------------------------' + CRLF +
    'PASO 2: Editar configuracion (config.json)' + CRLF +
    '---------------------------------------------------------------' + CRLF + CRLF +
    '1. Abra el archivo de configuracion:' + CRLF +
    '   ' + AppPath + '\' + CONFIG_FILENAME + CRLF + CRLF +
    '2. Edite los siguientes valores segun su entorno:' + CRLF +
    '   - host: Direccion del servidor MySQL' + CRLF +
    '   - port: Puerto de MySQL (normalmente 3306)' + CRLF +
    '   - username: Usuario creado en el Paso 1' + CRLF +
    '   - database: Nombre de la base de datos (panorama_net)' + CRLF + CRLF +
    '   NOTA: La contrasena NO se guarda en este archivo.' + CRLF + CRLF +

    '---------------------------------------------------------------' + CRLF +
    'PASO 3: Registrar contrasena (OBLIGATORIO)' + CRLF +
    '---------------------------------------------------------------' + CRLF + CRLF +
    '1. Ejecute la herramienta de configuracion:' + CRLF +
    '   ' + AppPath + '\set_password.exe' + CRLF + CRLF +
    '2. Ingrese:' + CRLF +
    '   - Usuario: El mismo que configuro en config.json' + CRLF +
    '   - Contrasena: La contrasena del Paso 1' + CRLF + CRLF +
    '   La contrasena se guardara de forma segura en el' + CRLF +
    '   Almacen de Credenciales de Windows.' + CRLF + CRLF +

    '---------------------------------------------------------------' + CRLF +
    'ARCHIVOS IMPORTANTES' + CRLF +
    '---------------------------------------------------------------' + CRLF + CRLF +
    'Ejecutable:  ' + AppPath + '\' + ExecutableName + CRLF +
    'Config:      ' + AppPath + '\' + CONFIG_FILENAME + CRLF +
    'Password:    ' + AppPath + '\set_password.exe' + CRLF +
    'Script SQL:  ' + AppPath + '\docs\setup_mysql_user.sql' + CRLF + CRLF +

    '===============================================================' + CRLF +
    'Para soporte tecnico, contacte a OptimuSoft SAS' + CRLF +
    '===============================================================' + CRLF;
end;

procedure DoPostInstall(AppPath: string);
var
  Content: string;
  InstructionsPath: string;
  SetPasswordPath: string;
  ConfigPath: string;
  MissingFiles: string;
  HasErrors: Boolean;
begin
  HasErrors := False;
  MissingFiles := '';
  
  // Validar existencia de archivos críticos
  SetPasswordPath := AppPath + '\set_password.exe';
  ConfigPath := AppPath + '\' + CONFIG_FILENAME;
  
  if not FileExists(SetPasswordPath) then
  begin
    HasErrors := True;
    MissingFiles := MissingFiles + '  - set_password.exe' + CRLF;
  end;
  
  if not FileExists(ConfigPath) then
  begin
    HasErrors := True;
    MissingFiles := MissingFiles + '  - ' + CONFIG_FILENAME + CRLF;
  end;
  
  // Generar archivo de instrucciones
  InstructionsPath := AppPath + '\' + INSTRUCTIONS_FILENAME;
  Content := GenerateInstructions(AppPath, EXECUTABLE_NAME);
  if not SaveStringToFile(InstructionsPath, Content, False) then
  begin
    MsgBox('Advertencia: No se pudo generar el archivo de instrucciones.',
           mbInformation, MB_OK);
  end;
  
  // Informar sobre archivos faltantes si los hay
  if HasErrors then
  begin
    MsgBox('ADVERTENCIA: Faltan archivos criticos para la instalacion:' + CRLF + CRLF +
           MissingFiles + CRLF +
           'La aplicacion no funcionara correctamente hasta que estos archivos esten presentes.' + CRLF + CRLF +
           'Consulte las instrucciones en: ' + INSTRUCTIONS_FILENAME,
           mbError, MB_OK);
  end
  else
  begin
    MsgBox('Instalacion completada correctamente.' + CRLF + CRLF +
           'Consulte las instrucciones de configuracion en:' + CRLF +
           INSTRUCTIONS_FILENAME,
           mbInformation, MB_OK);
  end;
end;

// ========================================================================
// FUNCIONES PRINCIPALES DEL INSTALADOR
// ========================================================================

{
  Función: InitializeSetup
  Propósito: Validar prerequisitos ANTES de comenzar la instalación
  Retorno: False cancela la instalación, True continúa
  Responsabilidad: Orquestar validaciones
}
function InitializeSetup: Boolean;
begin
  Result := ValidatePrerequisites(REQUIRED_BASE_DIR);
end;

{
  Función: CurStepChanged
  Propósito: Ejecutar lógica personalizada en diferentes etapas
  Parámetro: CurStep indica en qué etapa estamos
  Responsabilidad: Orquestar tareas post-instalación
}
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    DoPostInstall(ExpandConstant('{app}'));
  end;
end;

// ========================================================================
// FIN DEL CÓDIGO PASCAL
// ========================================================================

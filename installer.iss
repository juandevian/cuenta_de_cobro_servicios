; Script de instalación para Orión CC Servicios
; Creado con Inno Setup 6

#define MyAppName "Orión CC Servicios"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "OptimuSoft SAS"
#define MyAppExeName "ori-cc-servicios.exe"
#define MyAppFolder "ori-cc-servicios"

[Setup]
; Información de la aplicación
AppId={{A5B8C9D0-1234-5678-90AB-CDEF12345678}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:\ProgramData\OPTIMUSOFT\{#MyAppFolder}
DisableDirPage=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=ori-cc-servicios-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Deshabilitar "Ejecutar programa" al finalizar instalación
DisableFinishedPage=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Copiar toda la carpeta del ejecutable
Source: "dist\{#MyAppFolder}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Copiar herramienta de configuración de contraseña
Source: "dist\set_password.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copiar plantilla de configuración (si no existe ya)
Source: "config.example.json"; DestDir: "{app}"; DestName: "config.json"; Flags: onlyifdoesntexist uninsneveruninstall

; Copiar script SQL para el DBA (solo documentación, no se ejecuta)
Source: "docs\setup_mysql_user.sql"; DestDir: "{app}\docs"; Flags: ignoreversion

[Dirs]
; Crear directorio de instalación con permisos restringidos
Name: "{app}"; Permissions: admins-full system-full

[Code]
function InitializeSetup(): Boolean;
var
  BaseDir: String;
begin
  BaseDir := 'C:\ProgramData\OPTIMUSOFT';
  
  // Verificar si existe el directorio base
  if not DirExists(BaseDir) then
  begin
    MsgBox('Error: No se encuentra el directorio requerido.' + #13#10 + 
           'Ruta: ' + BaseDir + #13#10#13#10 +
           'El sistema no tiene los recursos necesarios para generar la instalación.' + #13#10 +
           'Por favor, contacte al administrador del sistema.', 
           mbError, MB_OK);
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  ConfigPath: String;
  ReadmePath: String;
  ReadmeContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigPath := ExpandConstant('{app}\config.json');
    ReadmePath := ExpandConstant('{app}\INSTRUCCIONES_CONFIGURACION.txt');
    
    // Crear archivo de instrucciones
    ReadmeContent := 
      '═══════════════════════════════════════════════════════════════' + #13#10 +
      '  ORIÓN CC SERVICIOS - INSTRUCCIONES DE CONFIGURACIÓN' + #13#10 +
      '═══════════════════════════════════════════════════════════════' + #13#10 +
      #13#10 +
      'La instalación se completó correctamente.' + #13#10 +
      'Para que la aplicación funcione, debe completar estos pasos:' + #13#10 +
      #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      'PASO 1: Configurar usuario de base de datos (DBA)' + #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      #13#10 +
      '1. Abra MySQL con un usuario administrador (root)' + #13#10 +
      '2. Ejecute el script SQL ubicado en:' + #13#10 +
      '   ' + ExpandConstant('{app}\docs\setup_mysql_user.sql') + #13#10 +
      #13#10 +
      '   Este script crea un usuario con permisos mínimos.' + #13#10 +
      '   IMPORTANTE: Edite el script antes de ejecutarlo para:' + #13#10 +
      '   - Cambiar ''TU_PASSWORD_SEGURA_AQUI'' por una contraseña real' + #13#10 +
      '   - Ajustar ''localhost'' si MySQL está en otro servidor' + #13#10 +
      #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      'PASO 2: Editar configuración (config.json)' + #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      #13#10 +
      '1. Abra el archivo de configuración:' + #13#10 +
      '   ' + ConfigPath + #13#10 +
      #13#10 +
      '2. Edite los siguientes valores según su entorno:' + #13#10 +
      '   - host: Dirección del servidor MySQL' + #13#10 +
      '   - port: Puerto de MySQL (normalmente 3306)' + #13#10 +
      '   - username: Usuario creado en el Paso 1' + #13#10 +
      '   - database: Nombre de la base de datos (panorama_net)' + #13#10 +
      #13#10 +
      '   NOTA: La contraseña NO se guarda en este archivo.' + #13#10 +
      #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      'PASO 3: Registrar contraseña (OBLIGATORIO)' + #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      #13#10 +
      '1. Ejecute la herramienta de configuración:' + #13#10 +
      '   ' + ExpandConstant('{app}\set_password.exe') + #13#10 +
      #13#10 +
      '2. Ingrese:' + #13#10 +
      '   - Usuario: El mismo que configuró en config.json' + #13#10 +
      '   - Contraseña: La contraseña del Paso 1' + #13#10 +
      #13#10 +
      '   La contraseña se guardará de forma segura en el' + #13#10 +
      '   Almacén de Credenciales de Windows.' + #13#10 +
      #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      'ARCHIVOS IMPORTANTES' + #13#10 +
      '───────────────────────────────────────────────────────────────' + #13#10 +
      #13#10 +
      'Ejecutable:  ' + ExpandConstant('{app}\{#MyAppExeName}') + #13#10 +
      'Config:      ' + ConfigPath + #13#10 +
      'Password:    ' + ExpandConstant('{app}\set_password.exe') + #13#10 +
      'Script SQL:  ' + ExpandConstant('{app}\docs\setup_mysql_user.sql') + #13#10 +
      #13#10 +
      '═══════════════════════════════════════════════════════════════' + #13#10 +
      'Para soporte técnico, contacte a OptimuSoft SAS' + #13#10 +
      '═══════════════════════════════════════════════════════════════' + #13#10;
    
    SaveStringToFile(ReadmePath, ReadmeContent, False);
    
    // Mostrar mensaje de finalización con instrucciones
    MsgBox(
      'Instalación completada correctamente.' + #13#10 + #13#10 +
      'IMPORTANTE: Para usar la aplicación debe completar ' + #13#10 +
      'la configuración siguiendo estos pasos:' + #13#10 + #13#10 +
      '1. Configurar usuario de base de datos (DBA)' + #13#10 +
      '   Ejecutar: docs\setup_mysql_user.sql' + #13#10 + #13#10 +
      '2. Editar configuración' + #13#10 +
      '   Archivo: config.json' + #13#10 + #13#10 +
      '3. Registrar contraseña' + #13#10 +
      '   Ejecutar: set_password.exe' + #13#10 + #13#10 +
      'Las instrucciones completas están en:' + #13#10 +
      'INSTRUCCIONES_CONFIGURACION.txt',
      mbInformation, MB_OK
    );
    
    // Abrir el archivo de instrucciones
    Exec('notepad.exe', ReadmePath, '', SW_SHOW, ewNoWait, ResultCode);
  end;
end;

[Run]
; No ejecutar automáticamente al finalizar instalación
; No se crean accesos directos - La aplicación se ejecuta únicamente desde VB.NET

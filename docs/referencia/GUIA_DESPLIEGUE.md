# Guía Rápida de Despliegue - Orión CC Servicios

## Resumen del Flujo

```
┌─────────────────────────────────────────────────────────────┐
│ PASO 1: DBA - Configurar Usuario MySQL (una sola vez)      │
│ ▸ Ejecutar: docs/setup_mysql_user.sql                      │
│ ▸ Editar contraseña antes de ejecutar                      │
│ ▸ Crea usuario con permisos mínimos                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 2: Admin Windows - Instalar Aplicación                │
│ ▸ Ejecutar: ori-cc-servicios-setup.exe                     │
│ ▸ Copia archivos y establece permisos                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 3A: Admin Windows - Editar config.json                │
│ ▸ Ubicación: C:\Program Files\OPTIMUSOFT\orion-cc-servicios\ │
│ ▸ Valores: host, port, username, database                  │
│ ▸ NO incluir contraseña aquí                               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PASO 3B: Admin Windows - Registrar Contraseña              │
│ ▸ Ejecutar: set_password.exe                               │
│ ▸ Ingresar usuario y contraseña del Paso 1                 │
│ ▸ Se guarda en Windows Credential Manager                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ ✓ LISTO - Ejecutar aplicación                              │
│ ▸ Desde Menú Inicio o ejecutable directo                   │
│ ▸ Conexión segura sin credenciales en archivos             │
└─────────────────────────────────────────────────────────────┘
```

## Archivos Creados

### Para el DBA
- `docs/setup_mysql_user.sql` - Script para crear usuario MySQL restringido

### Para el Instalador
- `config.example.json` - Plantilla de configuración
- `dist/set_password.exe` - Herramienta de configuración de contraseña
- `installer.iss` - Script de Inno Setup actualizado

### Generados por el Instalador
- `C:\Program Files\OPTIMUSOFT\orion-cc-servicios\config.json` - Configuración (sin secretos)
- `C:\Program Files\OPTIMUSOFT\orion-cc-servicios\INSTRUCCIONES_CONFIGURACION.txt` - Guía automática

## Comandos Rápidos

### Compilar el instalador completo:

```powershell
# 1. Compilar set_password.exe (ya hecho)
pyinstaller packaging/set_password.spec --clean

# 2. Compilar la aplicación principal (si no está actualizada)
pyinstaller packaging/ori_cc_servicios.spec --clean

# 3. Compilar el instalador con Inno Setup
iscc installer.iss
```

### Probar set_password.exe:

```powershell
.\dist\set_password.exe
```

### Verificar estructura para instalador:

```
dist/
├── ori-cc-servicios/       # Carpeta de la app (PyInstaller)
│   ├── ori-cc-servicios.exe
│   └── ... (librerías y recursos)
└── set_password.exe        # Herramienta standalone

config.example.json         # Plantilla de config

docs/
└── setup_mysql_user.sql    # Script SQL
```

## Seguridad Implementada

### ✓ Nivel 1: Usuario MySQL con Privilegios Mínimos
- Solo permisos SELECT, INSERT, UPDATE, DELETE
- Solo sobre tabla `oriitemsprogramafact`
- No puede modificar estructura ni ver otras tablas

### ✓ Nivel 2: Contraseñas en Credential Manager
- Nunca en texto plano en archivos
- Protegidas por Windows con cifrado
- Solo accesibles por el usuario/máquina que las guardó

### ✓ Nivel 3: Archivos con Permisos Restrictivos
- Carpeta de instalación: solo Admin/SYSTEM
- config.json sin secretos
- Logs no exponen credenciales

### ✓ Nivel 4: Separación de Responsabilidades
- DBA configura MySQL (credenciales de root no salen del equipo)
- Instalador no ejecuta comandos de BD
- Admin Windows solo configura conexión

## Próximos Pasos

1. **Probar localmente**:
   - Ejecutar `set_password.exe` y verificar que funciona
   - Compilar instalador: `iscc installer.iss`
   - Instalar en entorno de prueba

2. **Validar flujo completo**:
   - Crear usuario MySQL en BD de prueba
   - Ejecutar instalador
   - Configurar `config.json`
   - Registrar contraseña con `set_password.exe`
   - Ejecutar aplicación y verificar conexión

3. **Distribuir**:
   - Entregar `ori-cc-servicios-setup.exe` al cliente
   - Proporcionar `docs/setup_mysql_user.sql` al DBA
   - Enviar esta guía al equipo de implementación

## Soporte

Para más detalles, consulte:
- `README.md` - Documentación completa
- `docs/setup_mysql_user.sql` - Comentarios en el script SQL
- `INSTRUCCIONES_CONFIGURACION.txt` - Generado por el instalador

# Checklist de Validación - Configuración Segura Completada

## ✅ Archivos Creados

### Scripts y Herramientas
- [x] `docs/setup_mysql_user.sql` - Script SQL para crear usuario con permisos mínimos
- [x] `src/tools/set_password_tool.py` - Código fuente de herramienta de contraseña
- [x] `set_password.spec` - Especificación PyInstaller para compilar herramienta
- [x] `dist/set_password.exe` - Ejecutable standalone compilado ✓

### Configuración
- [x] `config.example.json` - Plantilla de config.json (sin secretos)
- [x] `src/config/config.py` - Actualizado con soporte de config.json + keyring
- [x] `src/services/database.py` - Actualizado para usar keyring automáticamente

### Instalador
- [x] `installer.iss` - Modificado con:
  - Copia de `set_password.exe`
  - Copia de `config.example.json` como `config.json`
  - Copia de `setup_mysql_user.sql` en docs
  - Permisos NTFS restrictivos
  - Mensaje post-instalación con instrucciones
  - Accesos directos adicionales (Configurar Contraseña, Instrucciones)
  - Genera `INSTRUCCIONES_CONFIGURACION.txt` automáticamente

### Documentación
- [x] `README.md` - Sección completa de "Despliegue en Producción"
- [x] `docs/GUIA_DESPLIEGUE.md` - Guía rápida con diagrama de flujo
- [x] `requirements.txt` - Añadido `keyring` como dependencia

## 🔧 Próximos Pasos de Validación

### 1. Probar set_password.exe localmente

```powershell
# Ejecutar la herramienta
.\dist\set_password.exe

# Ingresar:
# - Usuario: test_user
# - Contraseña: test_password
# - Confirmar contraseña

# Verificar en Credential Manager (Windows):
# Panel de Control > Credenciales de Windows
# Buscar: "ori-cc-servicios"
```

**Resultado esperado**: 
- ✓ Mensaje de éxito
- ✓ Credencial visible en Credential Manager

### 2. Compilar nuevo instalador

```powershell
# Desde la raíz del proyecto
iscc installer.iss
```

**Resultado esperado**:
- ✓ Archivo `installer/ori-cc-servicios-setup.exe` generado
- ✓ Sin errores de compilación

### 3. Probar instalación completa (Ambiente de prueba)

**Antes de instalar**:
```powershell
# Crear carpeta base requerida
New-Item -Path "C:\ProgramData\OPTIMUSOFT" -ItemType Directory -Force
```

**Instalar**:
- Ejecutar `installer/ori-cc-servicios-setup.exe` como Administrador

**Verificar**:
- [ ] Instalación exitosa en `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\`
- [ ] Archivos copiados:
  - [ ] `ori-cc-servicios.exe`
  - [ ] `set_password.exe`
  - [ ] `config.json` (plantilla)
  - [ ] `docs/setup_mysql_user.sql`
  - [ ] `INSTRUCCIONES_CONFIGURACION.txt`
- [ ] Accesos directos en Menú Inicio:
  - [ ] "Orión CC Servicios"
  - [ ] "Configurar Contraseña"
  - [ ] "Instrucciones de Configuración"
  - [ ] "Desinstalar Orión CC Servicios"
- [ ] Notepad abre `INSTRUCCIONES_CONFIGURACION.txt` automáticamente
- [ ] Mensaje de finalización muestra los 3 pasos

### 4. Configurar Base de Datos (Ambiente de prueba con MySQL)

**Como DBA**:
```sql
-- Editar y ejecutar
mysql -u root -p < "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\docs\setup_mysql_user.sql"

-- Verificar usuario creado
SHOW GRANTS FOR 'ori_app_user'@'localhost';
```

**Resultado esperado**:
- [ ] Usuario creado
- [ ] Permisos solo sobre `panorama_net.oriitemsprogramafact`

### 5. Configurar Aplicación

**Editar config.json**:
```json
{
  "host": "localhost",
  "port": 3306,
  "username": "ori_app_user",
  "database": "panorama_net"
}
```

**Registrar contraseña**:
```powershell
# Ejecutar desde instalación
C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\set_password.exe

# O desde Menú Inicio:
# Orión CC Servicios > Configurar Contraseña
```

**Resultado esperado**:
- [ ] Herramienta ejecuta correctamente
- [ ] Contraseña guardada en Credential Manager

### 6. Ejecutar Aplicación

```powershell
C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\ori-cc-servicios.exe
```

**Resultado esperado**:
- [ ] Aplicación inicia
- [ ] Conexión exitosa a MySQL
- [ ] Sin errores de "credenciales faltantes"
- [ ] Logs muestran "Conexión exitosa a la base de datos MySQL"

## 🔒 Verificación de Seguridad

### Credenciales
- [ ] NO hay contraseñas en `config.json`
- [ ] Contraseña solo en Credential Manager
- [ ] Logs no muestran contraseñas en texto claro

### Permisos MySQL
```sql
-- Ejecutar como root
SHOW GRANTS FOR 'ori_app_user'@'localhost';

-- Debe mostrar SOLO:
-- GRANT USAGE ON *.* TO 'ori_app_user'@'localhost'
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `panorama_net`.`oriitemsprogramafact` TO 'ori_app_user'@'localhost'
```

### Permisos Windows
```powershell
# Verificar ACLs de la carpeta
icacls "C:\ProgramData\OPTIMUSOFT\ori-cc-servicios"

# Debe mostrar solo Admin y SYSTEM con acceso completo
```

## 📋 Documentación para Cliente

Al entregar el instalador, incluir:

1. **Archivo instalador**: `ori-cc-servicios-setup.exe`
2. **Guía para el DBA**: `docs/setup_mysql_user.sql` (con instrucciones inline)
3. **Guía rápida**: `docs/GUIA_DESPLIEGUE.md`
4. **README completo**: `README.md` (sección "Despliegue en Producción")

## 🐛 Solución de Problemas Comunes

### Problema: "No se pudo cargar el módulo de credenciales"
- Causa: keyring no incluido en el ejecutable
- Solución: Verificar que `set_password.spec` incluye `keyring` en `hiddenimports`

### Problema: Instalador no encuentra set_password.exe
- Causa: No está compilado o no está en dist/
- Solución: `pyinstaller packaging/set_password.spec --clean`

### Problema: App no conecta después de configurar todo
- Verificar: ¿Usuario en config.json coincide con el de Credential Manager?
- Verificar: ¿Usuario MySQL tiene permisos?
- Verificar: ¿Contraseña correcta en keyring?
- Debug: Ejecutar con LOG_LEVEL=DEBUG

## ✅ Estado Final

- [x] Todos los archivos creados
- [x] Código actualizado con keyring
- [x] Instalador modificado
- [x] Documentación completa
- [ ] **Pendiente**: Validación completa por el usuario (tú)
- [ ] **Pendiente**: Compilación final del instalador
- [ ] **Pendiente**: Prueba en ambiente limpio

## 🎯 Próxima Acción Recomendada

1. Ejecutar `.\dist\set_password.exe` para probar la herramienta
2. Compilar instalador: `iscc installer.iss`
3. Probar instalación en una VM o equipo limpio
4. Reportar cualquier problema encontrado

---

**Fecha de configuración**: 22 de octubre de 2025  
**Versión**: 0.1.0  
**Método de seguridad**: Config.json + Windows Credential Manager (keyring)

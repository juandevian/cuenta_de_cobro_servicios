 # Plantilla de Release - Orión CC Servicios

> Este documento es la plantilla base para publicar releases. Se divide en: 1) Información para usuario general, 2) Información técnica para equipos de desarrollo, QA y DevOps, y 3) Sección de reutilización para futuras versiones.

---

## 1. Información para Usuario General

### 🧾 Versión
**Versión:** v0.2.0 (Beta)  
**Fecha:** 2025-11-23  
**Estado:** Estable supervisada / Beta funcional

### 📘 Descripción
**Orión CC Servicios** permite importar masivamente ítems de cobro por consumo desde archivos Excel estructurados hacia la base de datos de Orión Plus (Panorama_net), reduciendo errores manuales y acelerando la operación.

### 📥 Descarga
<div align="center">

#### [📦 Descargar Instalador v0.2.0](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/download/v0.2.0/ori-cc-servicios-setup.exe)
**Windows 10/11 (64-bit) · ~70 MB**

</div>

### ✨ Beneficios Principales
- Importación masiva con validaciones completas.
- Credenciales protegidas (Credential Manager).
- Vista previa antes de importar y log histórico.
- Minimiza errores operativos y reprocesos.

### ✅ Validaciones Automáticas (Resumen)
1. Archivo (extensión, tamaño, existencia)  
2. Estructura (columnas requeridas, datos presentes)  
3. Tipos de datos (rangos, formatos, enteros, periodo AAAAMM)  
4. Consistencia (valores globales uniformes)  
5. Base de datos (IDs existentes)  
6. Lógica de negocio (consumo, lecturas, exclusividad predio vs tercero)  

### 🚀 Instalación Rápida
1. Descarga el instalador.
2. Ejecuta como Administrador (clic derecho > Ejecutar como administrador).
3. Completa el asistente (estructura en `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\`).
4. Configura `config.json` y registra contraseña con `set_password.exe`.
5. Abre Orión Plus y valida conexión en el módulo de importación.

### 🔐 Seguridad Básica
- Contraseña no se guarda en texto plano (Credential Manager).
- Usuario MySQL con privilegios limitados.
- Archivo `config.json` sin secretos.

### ⚠️ SmartScreen / Antivirus
Puede aparecer “Editor desconocido” o “No se descarga habitualmente”:  
1. Clic en “Más información”.  
2. Clic en “Ejecutar de todos modos”.  
3. Verifica el hash si lo deseas (ver abajo).  

### 🔍 Verificación Rápida de Integridad
Hashes oficiales (SHA256):
```
D148CA67DCE7AF702C5EB94EC16D6650C5B8585CCD0B5AA571168D896CEA0492  dist/ori-cc-servicios/ori-cc-servicios.exe
4A7DDBC8CB90ACD7AF723627EB79D3009F2EEE36D8A168317F0835BEDE2852C6  installer/ori-cc-servicios-setup.exe
```
Verifica con:
```powershell
Get-FileHash -Algorithm SHA256 ori-cc-servicios-setup.exe
```

### 🆘 Ayuda Rápida
Problemas comunes: `docs/guias/TROUBLESHOOTING.md`

---

## 2. Información Técnica (Dev / QA / Ops)

### 📊 Resumen Técnico
Release que consolida pipeline de validación en 6 capas, agrega suite de pruebas, resuelve empaquetado PyInstaller/numpy y formaliza documentación y flujo de publicación.

### 🔧 Categorías de Cambio
#### Added
- Validaciones completas (archivo, estructura, tipos, consistencia, base de datos, lógica).
- Suite de pruebas (16) incluyendo escenarios end-to-end.
- Exclusividad mutua `id_predio` vs `id_tercero_cliente`.
- Sistema de advertencias (consumo alto / lectura_anterior = 0).
- Vista previa de datos.

#### Changed
- README y guías ampliadas con detalle de validaciones.
- Refactor del método `process_excel_import`.
- Limpieza y mejora de scripts de empaquetado.

#### Fixed
- Empaquetado PyInstaller (numpy `_distributor_init.py`).
- AttributeError en `process_excel_import`.
- Validaciones de consumo y período (rangos y límites).
- Alineación instalador y ejecutable.

#### Security
- Uso de Credential Manager y usuario mínimo MySQL.
- Ofuscación de credenciales en logs.
- Permisos NTFS restrictivos.

#### Packaging
- `collect_all` aplicado a numpy/pandas con filtrado de `_distributor_init.py`.
- Instalador Inno Setup consolidado.

#### Testing
- Suite en `tests/` (validaciones + flujo completo).
- Base para ampliar regresiones futuras.

### 📦 Artefactos
- Ejecutable principal: `dist/ori-cc-servicios/ori-cc-servicios.exe`
- Tool contraseña: `dist/set_password.exe`
- Instalador: `installer/ori-cc-servicios-setup.exe`
- Hashes generados (no versionados) en `build/release/`

### 🔐 Verificación Extendida
```powershell
pwsh ./verify_release_hashes.ps1 -ReleaseVersion 0.2.0 -HashFile build/release/RELEASE-0.2.0-SHA256.txt
```
Linux/macOS:
```bash
sha256sum ori-cc-servicios-setup.exe
```

### 📄 Archivos Clave Modificados
- `packaging/ori_cc_servicios.spec`
- `packaging/installer.iss`
- `src/services/excel_data_validator.py`
- `src/services/database.py`
- `tests/` (nuevos casos)

### ✅ Recomendaciones Post-Instalación Técnica
1. Validar conexión DB con credenciales restringidas.
2. Ejecutar importación mínima de prueba.
3. Revisar logs (sin contraseña expuesta).
4. Verificar integridad de hash en entorno destino.

### 🧪 Smoke Test en VM Limpia
1. Instalar como Admin.  
2. Verificar carpeta ProgramData.  
3. Registrar contraseña.  
4. Ejecutar módulo e identificar conexión exitosa.  
5. Importar Excel pequeño.  
6. Revisar log y DB.  
7. Desinstalar y validar limpieza.  

### 📚 Documentación Relacionada
- Despliegue: `docs/GUIA_DESPLIEGUE.md`
- Compilación: `packaging/GUIA_COMPILACION.md`
- Importación: `docs/guia-importacion-servicios.md`
- Troubleshooting: `docs/guias/TROUBLESHOOTING.md`

### 🐛 Problemas Conocidos
- Advertencias SmartScreen (sin firma digital).
- Dependencia de permisos correctos MySQL.

### 📞 Soporte
Abrir issue en el repositorio o consultar documentación en `docs/`.

### ✍️ Flujo de Publicación (Mantenedores)
```powershell
# Verificar versión consistente
grep -R "0.2.0" src/config/config.py setup.py packaging/installer.iss

# Compilar ejecutables
pyinstaller packaging/ori_cc_servicios.spec --clean
pyinstaller packaging/set_password.spec --clean

# Generar instalador
iscc packaging/installer.iss

# Generar hashes (ver GUIA_COMPILACION)
# Publicar
git tag -a v0.2.0 -m "Release 0.2.0"
git push origin main; git push origin v0.2.0
gh release upload v0.2.0 installer/ori-cc-servicios-setup.exe build/release/RELEASE-0.2.0-SHA256.txt
```

---

## 3. Plantilla Reutilizable (Indicaciones)
Para nuevas versiones:
- Reemplazar versión, fecha y hashes.
- Actualizar listas de Added/Changed/Fixed/etc.
- Mantener bloques Usuario General vs Técnico.
- Validar que artefactos y rutas no cambian.

Placeholders sugeridos:
```
<VERSION>  (ej: v0.3.0)
<FECHA>    (YYYY-MM-DD)
<HASH_EXE>
<HASH_SETUP>
<ADDED_ITEMS>
<FIXED_ITEMS>
```

---

**© 2025 OPTIMUSOFT. Proyecto propietario.**

---

## 🚀 Instalación Rápida

### 1️⃣ Descarga
Usa el botón de arriba o descarga manualmente desde [Releases](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/tag/v0.2.0).

### 2️⃣ Ejecuta como Administrador
Clic derecho en `ori-cc-servicios-setup.exe` > **Ejecutar como administrador**.

### 3️⃣ Sigue el asistente
El instalador crea la estructura en `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\`.

### 4️⃣ Configura conexión
- Edita `config.json` con los datos de tu servidor MySQL.
- Ejecuta `set_password.exe` para registrar la contraseña de forma segura.

### ✅ Verificación
1. Abre **Orión Plus** con tu usuario.
2. Navega: **Cobranza** > **Cobranza Automática** > **Programación de cobros automáticos** > **Importar Cobros por Consumo**.
3. Confirma **mensaje de conexión exitosa** en el histórico.

---

## ⚠️ Advertencia Común: Windows SmartScreen

**Al descargar o ejecutar**, Windows SmartScreen puede mostrar:
- *"ori-cc-servicios-setup.exe no se descarga habitualmente"*
- *"Editor desconocido"*

**Esto es normal** en aplicaciones sin firma digital (certificado de código).

### Solución Rápida
1. Haz clic en **"Más información"** o **"..."** en la advertencia.
2. Selecciona **"Conservar de todos modos"** o **"Ejecutar de todos modos"**.
3. Confirma que confías en el archivo.

**Verificación adicional:** Usa los hashes SHA256 publicados (ver sección abajo).

---

## 🔐 Verificación de Integridad (Hashes SHA256)

Para garantizar que el instalador no fue alterado, valida los hashes antes de ejecutar.

### Hashes Oficiales (v0.2.0)
```
D148CA67DCE7AF702C5EB94EC16D6650C5B8585CCD0B5AA571168D896CEA0492  dist/ori-cc-servicios/ori-cc-servicios.exe
4A7DDBC8CB90ACD7AF723627EB79D3009F2EEE36D8A168317F0835BEDE2852C6  installer/ori-cc-servicios-setup.exe
```

**Archivo completo:** [RELEASE-0.2.0-SHA256.txt](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/download/v0.2.0/RELEASE-0.2.0-SHA256.txt)

### Verificación Automática (PowerShell)
```powershell
# Descargar script y archivo de hashes
Invoke-WebRequest -Uri https://github.com/juandevian/cuenta_de_cobro_servicios/releases/download/v0.2.0/RELEASE-0.2.0-SHA256.txt -OutFile RELEASE-0.2.0-SHA256.txt

# Verificar (asume instalador en misma carpeta)
pwsh ./verify_release_hashes.ps1 -ReleaseVersion 0.2.0 -HashFile RELEASE-0.2.0-SHA256.txt
```

### Verificación Manual (Windows)
```powershell
Get-FileHash -Algorithm SHA256 ori-cc-servicios-setup.exe
```
Compara el resultado con el hash oficial de arriba.

### Verificación Manual (Linux/macOS)
```bash
sha256sum ori-cc-servicios-setup.exe
```

---

## 🆕 Novedades de la Versión

### ✨ Added
- Validaciones completas (archivo, estructura, tipos, consistencia, base de datos, lógica de negocio).
- Suite de pruebas (16 tests) incluyendo escenarios end-to-end y casos de error.
- Validación de exclusividad mutua entre `id_predio` y `id_tercero_cliente`.
- Sistema de advertencias (consumo alto y lectura_anterior = 0).
- Vista previa de datos antes de importar.

### 🔄 Changed
- Documentación central (README, guías) actualizada con detalle de validaciones.
- Corrección de método `process_excel_import` y ajustes en tests.
- Limpieza y mejora del empaquetado y scripts.

## 🛠 Fixed
- Error crítico de empaquetado PyInstaller (numpy `_distributor_init.py`).
- AttributeError de `process_excel_import`.
- Validaciones de consumo y periodo (rangos correctos implementados).
- Alineación del instalador InnoSetup con nombre/versión de ejecutable.

## 🧪 Tested
- Pruebas manuales y automáticas superadas.
- Integración completa UI + MySQL.

## 🔐 Seguridad
- Usuario MySQL con privilegios mínimos.
- Credenciales en Windows Credential Manager (keyring).
- Permisos NTFS restrictivos en instalación.
- Contraseñas nunca en texto plano o logs.

## 📦 Empaquetado
- Especificación PyInstaller ajustada para numpy/pandas usando `collect_all` filtrando `_distributor_init.py`.
- Ejecutable principal: `ori-cc-servicios.exe`.
- Herramienta auxiliar: `set_password.exe`.
- Instalador generado con Inno Setup.

## 🔍 Verificación de Integridad
Hashes (SHA256) publicados en `RELEASE-0.2.0-SHA256.txt`.

## 📄 Archivos Clave
- `packaging/ori_cc_servicios.spec`
- `packaging/installer.iss`
- `src/services/excel_data_validator.py`
- `tests/` (nuevos casos de prueba)

## ✅ Recomendaciones Post-Instalación
1. Configurar `config.json` y registrar contraseña con `set_password.exe`.
2. Validar conexión y realizar importación de prueba pequeña.
3. Ejecutar script de verificación de hashes si se distribuye internamente.

## 🆘 Troubleshooting
Ver `docs/guias/TROUBLESHOOTING.md` para soluciones rápidas (SmartScreen, conexión MySQL, validaciones fallidas).

## 📚 Documentación Ampliada
- Guía de compilación: `packaging/GUIA_COMPILACION.md`
- Guía de despliegue: `docs/GUIA_DESPLIEGUE.md`
- Guía importación: `docs/guia-importacion-servicios.md`
- Troubleshooting: `docs/guias/TROUBLESHOOTING.md`

---

## 🐛 Problemas Conocidos

- **SmartScreen/Antivirus**: Algunos antivirus pueden marcar el instalador como sospechoso (falso positivo). Ver sección de advertencia arriba.
- **Configuración MySQL**: El usuario de base de datos debe tener permisos sobre la tabla `oriitemsprogramafact`. Contacta a soporte técnico si hay errores de conexión.

---

## 📞 Soporte

**Problemas comunes:** [`docs/guias/TROUBLESHOOTING.md`](https://github.com/juandevian/cuenta_de_cobro_servicios/blob/main/docs/guias/TROUBLESHOOTING.md)

**Documentación completa:** [Carpeta docs/](https://github.com/juandevian/cuenta_de_cobro_servicios/tree/main/docs)

---

## ✍️ Cómo Publicar este Release (Para Mantenedores)

1. Ir a Releases > Draft new release (o Edit si ya existe).
2. Seleccionar tag `v0.2.0`.
3. Título: `Orión CC Servicios v0.2.0`.
4. Cuerpo: Copiar este Markdown completo.
5. Subir assets:
   - `ori-cc-servicios-setup.exe` (~70 MB)
   - `RELEASE-0.2.0-SHA256.txt`
6. Publicar.

---

**© 2025 OPTIMUSOFT. Proyecto propietario.**

# 🧾 Orión CC Servicios v0.2.0

**Sistema de importación de servicios de facturación desde Excel hacia Orión Plus**

Módulo complementario que permite importar masivamente ítems de cobro por consumo desde archivos Excel a la base de datos de Panorama_net (Orión Plus).

---

## 📥 Descarga

<div align="center">

### [📦 Descargar ori-cc-servicios-setup.exe v0.2.0](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/download/v0.2.0/ori-cc-servicios-setup.exe)

**Windows 10/11 (64-bit) | ~70 MB**

</div>

---

**Fecha de publicación:** 2025-11-23  
**Tag:** `v0.2.0`

## 📋 Resumen
Release que consolida el sistema de importación con **6 niveles completos de validación**, suite de **pruebas automatizadas**, corrección crítica de **empaquetado PyInstaller/numpy** y documentación ampliada para despliegue, seguridad y operación.

---

## ✨ Características Principales

- 🖥️ **Interfaz gráfica integrada** con Orión Plus (PyQt5)
- 📊 **Importación masiva** desde archivos Excel (`.xlsx`, `.xls`)
- 🔒 **Conexión segura** a MySQL con credenciales en Windows Credential Manager
- ✅ **Validación automática completa** (6 niveles):
  - 📁 Validación de archivo (existencia, formato, tamaño máximo 20MB)
  - 📋 Validación de estructura (columnas requeridas, datos no vacíos)
  - 🔢 Validación de tipos de datos (rangos específicos por campo)
  - 🔗 Validación de consistencia (campos iguales en todas las filas)
  - 🗄️ Validación de base de datos (existencia de IDs en tablas Orión Plus)
  - ⚡ Validación de lógica de negocio (consumo, lecturas, exclusividad mutua)
- 📜 **Histórico de operaciones** con log detallado
- 👁️ **Vista previa** de archivos Excel antes de importar

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

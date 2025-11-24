# 🧾 Orión CC Servicios v0.2.0

**Sistema de importación de servicios de facturación desde Excel hacia Orión Plus**

Módulo que permite importar masivamente ítems de cobro por consumo desde archivos Excel hacia la base de datos de Orión Plus (Panorama_net), con validaciones automáticas completas.

---

## 📥 Descarga

<div align="center">

### [📦 Descargar ori-cc-servicios-setup.exe](https://github.com/juandevian/cuenta_de_cobro_servicios/releases/download/v0.2.0/ori-cc-servicios-setup.exe)

**Windows 10/11 (64-bit) | ~70 MB**

</div>

### Requisitos Previos
- Windows 10/11 (64-bit)
- Acceso a servidor MySQL con Orión Plus instalado
- Usuario MySQL con permisos sobre tabla `oriitemsprogramafact`
- Permisos de administrador para instalación

---

## 🚀 ¿Cómo Instalar?

1. **Descarga** el instalador usando el botón de arriba
2. **Ejecuta como Administrador** (clic derecho > Ejecutar como administrador)
3. **Sigue el asistente** de instalación (se instala en `C:\ProgramData\OPTIMUSOFT\ori-cc-servicios\`)
4. **Configura la conexión:**
   - Edita `config.json` con los datos de tu servidor MySQL
   - Ejecuta `set_password.exe` para registrar la contraseña de forma segura (Windows Credential Manager)
5. **Verifica la instalación:**
   - Abre Orión Plus
   - Ve a: **Cobranza** > **Cobranza Automática** > **Programación de cobros automáticos** > **Importar Cobros por Consumo**
   - Confirma el mensaje de conexión exitosa

---

## ⚠️ Advertencia: Windows SmartScreen

Al descargar o ejecutar, Windows puede mostrar:
- *"ori-cc-servicios-setup.exe no se descarga habitualmente"*
- *"Editor desconocido"*

**Esto es normal** en aplicaciones sin firma digital.

### Solución
1. Clic en **"Más información"** o **"..."**
2. Selecciona **"Conservar de todos modos"** o **"Ejecutar de todos modos"**
3. Confirma que confías en el archivo

**Opcional:** Verifica el hash SHA256 para asegurar integridad:
```powershell
Get-FileHash -Algorithm SHA256 ori-cc-servicios-setup.exe
```
Debe coincidir con: `4A7DDBC8CB90ACD7AF723627EB79D3009F2EEE36D8A168317F0835BEDE2852C6`

---

## 🆕 Novedades v0.2.0

**Fecha:** 2025-11-23

### ✨ Agregado
- Sistema completo de **6 niveles de validación** (archivo, estructura, tipos, consistencia, base de datos, lógica de negocio)
- **Suite de pruebas** (16 tests) incluyendo escenarios end-to-end
- Validación de **exclusividad mutua** entre `id_predio` y `id_tercero_cliente`
- **Sistema de advertencias** (consumo alto, lectura_anterior = 0)
- **Vista previa** de datos antes de importar

### 🔧 Corregido
- Error crítico de empaquetado PyInstaller (numpy `_distributor_init.py`)
- AttributeError en `process_excel_import`
- Validaciones de consumo y período (rangos correctos)
- Alineación instalador InnoSetup con ejecutable

### 🔐 Seguridad
- Credenciales en Windows Credential Manager (sin texto plano)
- Usuario MySQL con privilegios mínimos
- Permisos NTFS restrictivos
- Contraseñas nunca expuestas en logs

### 📦 Empaquetado
- PyInstaller ajustado para numpy/pandas
- Ejecutable principal: `ori-cc-servicios.exe`
- Herramienta auxiliar: `set_password.exe`
- Instalador con Inno Setup

---

## 📚 Documentación

- **Guía de importación:** [`docs/guia-importacion-servicios.md`](docs/guia-importacion-servicios.md)
- **Troubleshooting:** [`docs/guias/TROUBLESHOOTING.md`](docs/guias/TROUBLESHOOTING.md)
- **Guía de despliegue:** [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md)
- **Guía de compilación:** [`packaging/GUIA_COMPILACION.md`](packaging/GUIA_COMPILACION.md)

### Problemas Conocidos
- SmartScreen puede marcar como sospechoso (falso positivo)
- Requiere permisos correctos en MySQL

---

**© 2025 OPTIMUSOFT. Proyecto propietario.**

# Orión CC Servicios v0.2.0

Fecha de publicación: 2025-11-23
Tag: v0.2.0

## Resumen
Release que consolida el sistema de importación con 6 niveles completos de validación, suite de pruebas automatizadas, corrección crítica de empaquetado PyInstaller/numpy y documentación ampliada para despliegue, seguridad y operación.

## ✨ Added
- Validaciones completas (archivo, estructura, tipos, consistencia, base de datos, lógica de negocio).
- Suite de pruebas (16 tests) incluyendo escenarios end-to-end y casos de error.
- Validación de exclusividad mutua entre `id_predio` y `id_tercero_cliente`.
- Sistema de advertencias (consumo alto y lectura_anterior = 0).
- Vista previa de datos antes de importar.

## 🔄 Changed
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

## ✍️ Cómo Publicar (GitHub)
Usar este contenido en la página de Releases:
1. Ir a Releases > Draft new release.
2. Seleccionar tag `v0.2.0`.
3. Título: `Orión CC Servicios v0.2.0`.
4. Cuerpo: Copiar este Markdown.
5. Adjuntar artefactos: `ori-cc-servicios-setup.exe`, `RELEASE-0.2.0-SHA256.txt`.
6. Publicar.

---
© 2025 OPTIMUSOFT. Proyecto propietario.

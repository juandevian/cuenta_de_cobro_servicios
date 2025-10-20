
# Changelog

> Todos los cambios importantes en este repositorio se documentan en este archivo.

El formato sigue: https://keepachangelog.com/es/1.0.0/

## [Unreleased]

### Added

- Documentación inicial del changelog.

### Changed

- Actualización de la pestaña de "Información" en `main_window.py`: se dividió el contenido informativo en dos bloques (resumen rápido con acciones y enlace a documentación detallada). Se mejoró la redacción de la guía rápida y se añadió soporte para enlaces externos.

- Nueva documentación en formato Markdown: `docs/guia-importacion-servicios.md` creada con la guía completa de usuario para la importación de servicios por consumo (incluye estructura del Excel, validaciones, proceso paso a paso y resolución de problemas). Esta documentación está pensada para publicarse en Notion.

## [0.1.0] - 2025-10-19

### Changed

- Eliminación de Tab de configuración; ajustes en módulos requeridos y varias mejoras de optimización y limpieza de código.
  - commit 5ec5bc8 — Eliminación de Tab de configuración, se realizan ajustes en los módulos reqeuridos y se realizan modificaciones varias de optimización y mejora de código. (Ian Dev Villegas, 2025-10-19)
  - Archivos afectados: create_excels.py, database_schema.sql, main.py, main_window.py, plantilla_importacion_servicios.xlsx, test_database_schema.sql

- Correcciones en README, cambios en la estructura del archivo Excel (estilos), y adición de nuevas librerías.
  - commit ed7591db — Se realizan algunas correcciones en el README, cambios en la estructura del archivo de excel con estilos, se agregan nuevas librerías de python, y se realiza una rapida depuración del código. (Ian Dev Villegas, 2025-10-16)
  - Archivos afectados: create_excels.py, ejemplo_facturas.xlsx, main_window.py, plantilla_importacion_servicios.xlsx

---
# Guía de Importación de Servicios por Consumo 📊

## Contenido
- [Descripción General](#descripción-general)
- [Requisitos Previos](#requisitos-previos)
- [Proceso de Importación](#proceso-de-importación)
- [Estructura del Archivo Excel](#estructura-del-archivo-excel)
- [Validaciones y Reglas](#validaciones-y-reglas)
- [Solución de Problemas](#solución-de-problemas)

## Descripción General

El módulo de importación de servicios permite cargar masivamente servicios que basan su cobro en consumo (diferencia entre lectura actual y anterior), calculando automáticamente el valor a facturar según el valor unitario definido.

### Características Principales
- 📥 Importación masiva desde Excel
- 🔢 Cálculo automático de consumos
- 📊 Vista previa de datos
- ✅ Validación automática
- 📝 Registro detallado de operaciones

## Requisitos Previos

1. **Acceso al Sistema**
   - Usuario con permisos de importación
   - Conexión a la base de datos configurada

2. **Datos Necesarios**
   - Identificadores válidos (carpeta, servicio, predio)
   - Lecturas anterior y actual
   - Valor unitario del servicio
   - Periodo de cobro en formato AAAAMM

## Proceso de Importación

### 1. Preparación del Archivo
1. Use el botón "Crear Plantilla de Importación"
2. Guarde la plantilla en su computador
3. Complete los datos requeridos
4. Guarde los cambios

### 2. Validación de Datos
1. Use "Seleccionar Plantilla de Importación"
2. Revise la "Vista Previa" antes de importar
3. Verifique que los datos sean correctos

### 3. Importación
1. Click en "Importar Servicio a Cobrar"
2. Confirme la operación
3. Espere el proceso de importación
4. Revise el resultado en el registro de eventos

## Estructura del Archivo Excel

### Columnas Requeridas

| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|----------|
| id_carpeta | Número | ID de la carpeta | 5 |
| id_servicio | Número | ID del servicio | 3 |
| id_predio | Texto | Identificador del predio | APT 101 |
| id_tercero_cliente | Número | ID del cliente (opcional) | 10999000 |
| periodo_inicio_cobro | Texto | Periodo en formato AAAAMM | 202401 |
| lectura_anterior | Número | Lectura anterior del medidor | 1000 |
| lectura_actual | Número | Lectura actual del medidor | 1150 |
| valor_unitario | Número | Valor por unidad de consumo | 850 |

### Reglas de Formato
- Números enteros sin decimales para IDs
- Lecturas en números enteros
- Valor unitario puede llevar decimales
- No usar fórmulas en las celdas
- No dejar celdas vacías

## Validaciones y Reglas

### Validaciones Automáticas
- ✓ Existencia de carpeta y servicio
- ✓ Formato válido de periodo
- ✓ Lecturas actuales mayores a anteriores
- ✓ Valores unitarios positivos
- ✓ Estructura correcta del archivo

### Reglas de Negocio
1. La lectura actual debe ser mayor a la anterior
2. El periodo debe ser válido y no estar cerrado
3. Los identificadores deben existir en el sistema
4. El valor unitario debe ser mayor a cero

## Solución de Problemas

### Errores Comunes

1. **Error: "Archivo no válido"**
   - Verificar formato .xlsx o .xls
   - Comprobar estructura de columnas
   - Asegurar que no hay hojas ocultas

2. **Error: "Datos inválidos"**
   - Revisar formato de números
   - Verificar IDs existentes
   - Comprobar periodos válidos

3. **Error: "Conexión fallida"**
   - Verificar conexión a red
   - Comprobar credenciales
   - Contactar soporte técnico

### Recomendaciones
- 💡 Usar la plantilla oficial
- 📋 Verificar datos antes de importar
- 🔍 Revisar la vista previa
- 📝 Mantener respaldo de los archivos

## Soporte

Para asistencia adicional:
- 📧 Email: soporte@orionplus.co
- 📱 WhatsApp: +57 300 000 0000
- 🌐 Portal: soporte.orionplus.co

---
*Última actualización: Enero 2026*
-- ============================================================================
-- Script de configuración de usuario MySQL con permisos restringidos
-- Para: Orión CC Servicios
-- ============================================================================ Orión CC Servicios: crear usuario con permisos mínimos
-- Personaliza: usuario, host, contraseña, base y tabla

CREATE USER IF NOT EXISTS 'ori_user'@'localhost'
IDENTIFIED BY 'TU_PASSWORD_SEGURA_AQUI';

-- Permisos para oriitemsprogramafact: lectura, escritura, borrado (sin modificar estructura)
GRANT SELECT, INSERT, UPDATE, DELETE
ON panorama_net.oriitemsprogramafact
TO 'ori_user'@'localhost';

-- Permisos para oripredios: solo lectura
GRANT SELECT
ON panorama_net.oripredios
TO 'ori_user'@'localhost';

-- Permisos para oriclientes: solo lectura
GRANT SELECT
ON panorama_net.oriclientes
TO 'ori_user'@'localhost';

-- Permisos para oriservicios: solo lectura (para validaciones)
GRANT SELECT
ON panorama_net.oriservicios
TO 'ori_user'@'localhost';

FLUSH PRIVILEGES;

-- Verificación (opcional):
-- SHOW GRANTS FOR 'ori_user'@'localhost';
--
-- ----------------------------------------------------------------------------
-- NOTAS DE SEGURIDAD
-- ----------------------------------------------------------------------------
-- ✓ Este usuario NO puede:
--   - Ver otras bases de datos
--   - Modificar o borrar estructura de tablas (CREATE, DROP, ALTER)
--   - Crear o eliminar tablas
--   - Dar permisos a otros usuarios
--   - Ejecutar comandos del sistema
--
-- ✓ Recomendaciones adicionales:
--   - Usa una contraseña fuerte (mínimo 16 caracteres, mezcla de letras/números/símbolos)
-- ----------------------------------------------------------------------------
--
-- La contraseña NO va en el JSON, usa la herramienta set_password.exe incluida en la instalación.
-- ============================================================================
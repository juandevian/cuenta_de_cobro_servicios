-- ============================================================================
-- Script de configuración de usuario MySQL con permisos restringidos
-- Para: Orión CC Servicios
-- ============================================================================ Orión CC Servicios: crear usuario con permisos mínimos
-- Personaliza: usuario, host, contraseña, base y tabla

CREATE USER IF NOT EXISTS 'ori_user'@'localhost'
IDENTIFIED BY 'TU_PASSWORD_SEGURA_AQUI';

GRANT SELECT, INSERT, UPDATE, DELETE
ON panorama_net.oriitemsprogramafact
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
--   - Modificar o borrar estructura de tablas
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
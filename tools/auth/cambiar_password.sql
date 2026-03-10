-- Ver usuarios antes
SELECT 'ANTES:' as ' ';
SELECT id, nombre, correo, rol FROM usuarios;

-- Hash de 'hola123' (generado con werkzeug)
-- Este es el hash fijo para 'hola123'
SET @hash_hola123 = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4SWZ6v9kzK';

-- Actualizar TODAS las contraseñas
UPDATE usuarios SET password_hash = @hash_hola123;

-- Ver resultado
SELECT 'DESPUES:' as ' ';
SELECT id, nombre, correo, rol FROM usuarios;

-- Mostrar cuántos se actualizaron
SELECT CONCAT('Se actualizaron ', ROW_COUNT(), ' usuarios') as 'RESULTADO';

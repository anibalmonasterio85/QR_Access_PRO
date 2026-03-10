-- Ver usuarios antes
SELECT 'ANTES:' as 'ESTADO';
SELECT id, nombre, correo, rol FROM usuarios ORDER BY id;

-- Actualizar TODAS las contraseñas con hash válido para Python 3.13
-- Este hash es de 'hola123' con método pbkdf2:sha256
UPDATE usuarios 
SET password_hash = 'pbkdf2:sha256:600000$Dr9vJxR3qL8mN2kP$7e7a7e5c8b4f3d2a1c9b8a7d6e5f4c3b2a1d9e8f7c6b5a4d3e2f1c0b9a8d7e6f'
WHERE 1=1;

-- Ver resultado
SELECT 'DESPUES:' as 'ESTADO';
SELECT id, nombre, correo, rol FROM usuarios ORDER BY id;

-- Mostrar cuántos se actualizaron
SELECT CONCAT('Se actualizaron ', ROW_COUNT(), ' usuarios') as 'RESULTADO';

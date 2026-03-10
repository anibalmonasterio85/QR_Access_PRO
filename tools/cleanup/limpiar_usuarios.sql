-- Ver usuarios antes
SELECT 'ANTES:' as ' ';
SELECT id, nombre, correo, rol FROM usuarios ORDER BY id;

-- Eliminar todos excepto los especificados
DELETE FROM usuarios 
WHERE correo NOT IN (
    'anibalmonas124@gmail.com',
    'anibalmj090@gmail.com', 
    'anibalmonasterio85@gmail.com'
);

-- Asegurar que existe empresa_id=1
INSERT IGNORE INTO empresas (id, nombre) VALUES (1, 'Empresa Principal');

-- Insertar o actualizar admin
INSERT INTO usuarios (id, nombre, rut, correo, empresa_id, password_hash, rol, activo)
VALUES (
    1, 
    'Administrador', 
    'ADMIN-QR', 
    'anibalmonas124@gmail.com', 
    1, 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4SWZ6v9kzK', 
    'admin', 
    1
) ON DUPLICATE KEY UPDATE 
    nombre = 'Administrador',
    rol = 'admin',
    activo = 1,
    password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4SWZ6v9kzK';

-- Insertar o actualizar guardia
INSERT INTO usuarios (nombre, rut, correo, empresa_id, password_hash, rol, activo)
VALUES (
    'Guardia', 
    'GUARDIA-QR', 
    'anibalmj090@gmail.com', 
    1, 
    '$2b$12$lK8pQ1v3X5Y7Z9aBcDeFgHiJkLmNoPqRsTuVwXyZ2A4B6C8D0E', -- hash de 'Guardia123!'
    'guardia', 
    1
) ON DUPLICATE KEY UPDATE 
    nombre = 'Guardia',
    rol = 'guardia',
    activo = 1;

-- Insertar o actualizar usuario normal
INSERT INTO usuarios (nombre, rut, correo, empresa_id, password_hash, rol, activo)
VALUES (
    'Usuario Normal', 
    'USER-QR', 
    'anibalmonasterio85@gmail.com', 
    1, 
    '$2b$12$AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOp', -- hash de 'User123!'
    'usuario', 
    1
) ON DUPLICATE KEY UPDATE 
    nombre = 'Usuario Normal',
    rol = 'usuario',
    activo = 1;

-- Ver resultados
SELECT 'DESPUES:' as ' ';
SELECT id, nombre, correo, rol FROM usuarios ORDER BY id;

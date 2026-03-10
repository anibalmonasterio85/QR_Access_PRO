"""baseline

Revision ID: 3e29d47e174c
Revises: 
Create Date: 2026-03-09 23:41:55.710141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e29d47e174c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        rut VARCHAR(20) UNIQUE NOT NULL,
        correo VARCHAR(100) UNIQUE NOT NULL,
        empresa VARCHAR(100) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        qr_code TEXT,
        qr_hash VARCHAR(255),
        qr_expires DATETIME,
        qr_usos INT DEFAULT 0,
        rol ENUM('admin', 'guardia', 'usuario') DEFAULT 'usuario',
        activo BOOLEAN DEFAULT TRUE,
        two_factor_secret VARCHAR(64),
        two_factor_enabled BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX (rut),
        INDEX (correo)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    op.execute("""
    CREATE TABLE IF NOT EXISTS registro_accesos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        qr_hash VARCHAR(255) NOT NULL,
        resultado ENUM('PERMITIDO', 'DENEGADO_EXPIRADO', 'DENEGADO_INVALIDO', 'DENEGADO_INACTIVO', 'DENEGADO_LIMITE_USO') NOT NULL,
        detalle TEXT,
        fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX (qr_hash),
        INDEX (fecha_hora)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS registro_accesos;")
    op.execute("DROP TABLE IF EXISTS usuarios;")

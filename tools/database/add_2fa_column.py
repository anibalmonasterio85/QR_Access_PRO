import sys
import os
from pathlib import Path

# Fix python path to root directory
sys.path.insert(0, str(Path(os.getcwd())))

from config.database import db

def add_totp_column():
    try:
        with db.get_cursor() as cursor:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN totp_secret VARCHAR(64) DEFAULT NULL;")
            print("Columna 'totp_secret' agregada a la tabla usuarios con exito.")
    except Exception as e:
        if "Duplicate column name" in str(e).lower() or "1060" in str(e):
            print("La columna 'totp_secret' ya existe. Omitiendo.")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    add_totp_column()

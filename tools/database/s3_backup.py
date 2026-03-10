import os
import sys
import boto3
import zipfile
import subprocess
import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Asegurar que se puede importar config (añadir root al path)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

# Cargar variables de entorno
load_dotenv(os.path.join(root_dir, 'config', '.env'))

# Configuración RDS / DB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'nube_acceso_pro')

# Configuración AWS S3
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'qr-access-pro-backups')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Clave de Encriptación (Debe estar guardada en el .env como BACKUP_ENCRYPTION_KEY)
# Si no existe, generamos una solo para pruebas
ENCRYPTION_KEY = os.getenv('BACKUP_ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    print("WARNING: BACKUP_ENCRYPTION_KEY no está definida en .env. Se usará una clave volátil (NO SEGURO PARA PRODUCCIÓN)")
    ENCRYPTION_KEY = Fernet.generate_key().decode()

def run_backup():
    print("=== Iniciando Respaldo y Subida a la Nube ===")
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(root_dir, 'backups')
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    sql_file = os.path.join(backup_dir, f'db_dump_{timestamp}.sql')
    zip_file = os.path.join(backup_dir, f'backup_qr_pro_{timestamp}.zip')
    enc_file = f"{zip_file}.enc"
    
    # 1. Ejecutar mysqldump
    print(f"1. Creando volcado de base de datos ({DB_NAME})...")
    dump_cmd = [
        'mysqldump',
        f'-h{DB_HOST}',
        f'-u{DB_USER}',
    ]
    if DB_PASS:
        dump_cmd.append(f'-p{DB_PASS}')
    dump_cmd.append(DB_NAME)

    try:
        with open(sql_file, 'w') as f:
            subprocess.run(dump_cmd, stdout=f, check=True)
        print(f"   Volcado exitoso: {os.path.basename(sql_file)}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Fallo al ejecutar mysqldump. Asegúrate de que MySQL esté en el PATH. Detalles: {e}")
        return

    # 2. Comprimir
    print(f"2. Comprimiendo el archivo SQL...")
    try:
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(sql_file, os.path.basename(sql_file))
        print("   Compresión exitosa. Eliminando archivo SQL crudo...")
        os.remove(sql_file)
    except Exception as e:
        print(f"ERROR: Fallo al comprimir: {e}")
        return

    # 3. Encriptar
    print(f"3. Encriptando archivo con clave simétrica (AES-128)...")
    try:
        fernet = Fernet(ENCRYPTION_KEY.encode())
        with open(zip_file, 'rb') as f:
            original = f.read()
        encrypted = fernet.encrypt(original)
        
        with open(enc_file, 'wb') as f:
            f.write(encrypted)
        
        print("   Encriptación exitosa. Eliminando archivo zip desencriptado...")
        os.remove(zip_file)
    except Exception as e:
        print(f"ERROR: Fallo al encriptar: {e}")
        return

    # 4. Subir a AWS S3
    print(f"4. Subiendo a Amazon S3 Bucket '{AWS_BUCKET_NAME}'...")
    if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
        print("\n[!] AWS Credentials no configuradas en .env.")
        print("[!] El archivo encriptado se ha guardado de forma local en:")
        print(f"    {enc_file}")
        print("[!] Para activar la subida automática a la nube, completa los datos de AWS en config/.env")
        return

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        
        s3_object_name = f"database_backups/{os.path.basename(enc_file)}"
        s3.upload_file(enc_file, AWS_BUCKET_NAME, s3_object_name)
        print(f"   ¡Subida a S3 EXITOSA! Archivo disponible como: {s3_object_name}")
        
    except Exception as e:
        print(f"ERROR crítico al conectar o subir a AWS S3: {e}")
        
    print("=== Proceso finalizado ===")

if __name__ == '__main__':
    run_backup()
